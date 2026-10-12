
from adapters.doom.game_client import DoomGameClient


def main():
    game = DoomGameClient(visible=True)

    try:
        state = game.reset()

        assert state is not None
        assert len(state.game_variables) == 2

        print("Initial variables:", state.game_variables)

        reward = game.execute("wait")
        print("Wait reward:", reward)

        state = game.observe()
        print(
            "Next state:",
            None if state is None else state.game_variables,
        )

    finally:
        game.close()


if __name__ == "__main__":
    main()
