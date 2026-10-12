from adapters.doom.game_client import DoomGameClient

game = DoomGameClient(
    visible=True,
    episode_timeout=300,
    action_frames=4,
)

try:
    state = game.reset()

    print("Initial state:", state.game_variables)

    for action in [
        "forward",
        "turn_left",
        "forward",
        "turn_right",
        "forward_attack",
        "wait",
    ]:
        if game.is_terminal():
            print("Episode ended.")
            break

        reward = game.execute(action)

        print(
            f"Action: {action:15s} "
            f"Reward: {reward:.2f}"
        )

    print("Total reward:", game.get_total_reward())

finally:
    game.close()