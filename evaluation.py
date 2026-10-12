
import random

from adapters.doom.game_client import DoomGameClient


def run_random_baseline(episodes=5):
    actions = [
        "strafe_left",
        "strafe_right",
        "attack",
        "left_attack",
        "right_attack",
        "wait",
    ]

    results = []

    for episode in range(episodes):
        game = DoomGameClient(
            visible=False,
            episode_timeout=300,
            action_frames=4,
        )

        try:
            game.reset()
            steps = 0

            while (
                not game.is_terminal()
                and steps < 100
            ):
                action = random.choice(actions)
                game.execute(action)
                steps += 1

            results.append({
                "episode": episode + 1,
                "steps": steps,
                "total_reward": game.get_total_reward(),
            })

        finally:
            game.close()

    for result in results:
        print(result)

    mean_reward = sum(
        result["total_reward"] for result in results
    ) / len(results)

    print("Mean reward:", mean_reward)


if __name__ == "__main__":
    run_random_baseline()
