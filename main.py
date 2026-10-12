from agent.experience_store import ExperienceStore

from time import perf_counter

from laya import Router

from config import (
    GAME_VISIBLE,
    EPISODE_TIMEOUT,
    ACTION_FRAMES,
    MAX_STEPS_PER_EPISODE,
    LOG_PATH,
    MAX_CONSECUTIVE_ERRORS,
)

from adapters.doom.game_client import DoomGameClient
from adapters.doom.state_adapter import DoomStateAdapter
from adapters.doom.decision_adapter import DoomDecisionAdapter

from agent.question_builder import build_questions

from safety.validator import ActionValidator
from safety.error_handler import ErrorHandler

from monitoring.logger import AgentLogger


def main():
    logger = AgentLogger(LOG_PATH)

    error_handler = ErrorHandler(
        logger,
        MAX_CONSECUTIVE_ERRORS,
    )

    # Initialize Laya once, outside the game loop.
    router = Router()

    game = None

    try:
        game = DoomGameClient(
            visible=GAME_VISIBLE,
            episode_timeout=EPISODE_TIMEOUT,
            action_frames=ACTION_FRAMES,
        )

        state_adapter = DoomStateAdapter()
        decision_adapter = DoomDecisionAdapter()

        validator = ActionValidator(
            decision_adapter.allowed_actions
        )

        experience_store = ExperienceStore(LOG_PATH)

        raw_state = game.reset()

        if raw_state is None:
            raise RuntimeError(
                "Game did not provide an initial state"
            )

        logger.info("Episode started", episode=1)

        for step in range(MAX_STEPS_PER_EPISODE):
            if game.is_terminal():
                logger.info(
                    "Game episode ended",
                    episode=1,
                    step=step,
                )
                break

            raw_state = game.observe()

            if raw_state is None:
                logger.warning(
                    "No game state available",
                    episode=1,
                    step=step,
                )
                break

            # 1. Normalize the actual game state.
            state = state_adapter.transform(raw_state)
            state["relevant_experiences"] = (
            experience_store.retrieve(state, limit=3)
)

            # 2. Ask Laya to select an action.
            started = perf_counter()

            try:
                result = router.predict(
                    state,
                    build_questions(state),
                )

                inference_seconds = (
                    perf_counter() - started
                )

            except Exception as exc:
                should_continue = error_handler.recover(
                    exc,
                    context={
                        "episode": 1,
                        "step": step,
                        "operation": "inference",
                    },
                )

                if not should_continue:
                    break

                # No game action was sent. We can safely
                # retry inference on the next iteration.
                continue

            answers = result.get("answers", {})
            action_answer = answers.get("action", {})
            proposed_action = action_answer.get("choice")

            # 3. Validate Laya's result.
            valid, reason = validator.validate(
                proposed_action
            )

            if not valid:
                logger.warning(
                    "Action rejected",
                    episode=1,
                    step=step,
                    proposed_action=proposed_action,
                    reason=reason,
                )

                # Safe fallback: do not execute the invalid
                # action. Advance the game with no buttons.
                executed_action = "wait"
            else:
                executed_action = (
                    decision_adapter.transform(
                        proposed_action
                    )
                )

            # 4. Execute the action.
            try:
                reward = game.execute(executed_action)

            except Exception as exc:
                # Do not blindly repeat an action whose
                # execution status may be uncertain.
                error_handler.recover(
                    exc,
                    context={
                        "episode": 1,
                        "step": step,
                        "operation": "execution",
                        "action": executed_action,
                    },
                )
                break

            # 5. Read the state after the action.
            next_raw_state = game.observe()

            if next_raw_state is None:
                next_state = None
            else:
                next_state = state_adapter.transform(
                    next_raw_state
                )

            # 6. Record the transition.
            logger.record({
                "event": "transition",
                "episode": 1,
                "step": step,
                "state": state,
                "proposed_action": proposed_action,
                "action_valid": valid,
                "validation_reason": reason,
                "executed_action": executed_action,
                "reward": float(reward),
                "next_state": next_state,
                "terminal": game.is_terminal(),
                "inference_seconds": inference_seconds,
                "model": result.get("routing", {}).get(
                    "model"
                ),
            })

            print(
                f"Step {step:03d} | "
                f"health={state['health']:.0f} | "
                f"ammo={state['ammo']:.0f} | "
                f"proposed={proposed_action!r} | "
                f"executed={executed_action} | "
                f"reward={reward:.2f} | "
                f"inference={inference_seconds:.3f}s"
            )

            error_handler.report_success()

            if game.is_terminal():
                break

        print(
            "Total episode reward:",
            game.get_total_reward(),
        )

        logger.info(
            "Episode finished",
            episode=1,
            total_reward=float(game.get_total_reward()),
        )

    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

        logger.warning(
            "Agent interrupted",
            episode=1,
        )

    except Exception as exc:
        logger.error(
            "Agent terminated unexpectedly",
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        raise

    finally:
        if game is not None:
            game.close()


if __name__ == "__main__":
    main()
