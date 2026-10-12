import vizdoom as vzd

game = vzd.DoomGame()

game.set_doom_scenario_path(
    vzd.scenarios_path + "/basic.wad"
)

game.set_available_buttons([
    vzd.Button.MOVE_LEFT,
    vzd.Button.MOVE_RIGHT,
    vzd.Button.ATTACK,
])

game.set_available_game_variables([
    vzd.GameVariable.HEALTH,
    vzd.GameVariable.AMMO2,
])

game.set_window_visible(True)
game.set_episode_timeout(300)

game.init()

try:
    game.new_episode()

    for step in range(30):
        if game.is_episode_finished():
            break

        state = game.get_state()

        print(
            "Step:", step,
            "Health:", state.game_variables[0],
            "Ammo:", state.game_variables[1],
        )

        # Temporary test action, not an AI decision.
        reward = game.make_action(
            [False, False, True],
            4,
        )

        print("Reward:", reward)

    print("Episode reward:", game.get_total_reward())

finally:
    game.close()