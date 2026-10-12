
import vizdoom as vzd


def main():
    game = vzd.DoomGame()

    game.set_doom_scenario_path(
        vzd.scenarios_path + "/basic.wad"
    )
    game.set_doom_map("map01")

    game.set_available_buttons([
        vzd.Button.MOVE_LEFT,
        vzd.Button.MOVE_RIGHT,
        vzd.Button.ATTACK,
    ])

    game.set_available_game_variables([
        vzd.GameVariable.HEALTH,
        vzd.GameVariable.AMMO2,
    ])

    # Enable additional observation information for inspection.
    game.set_labels_buffer_enabled(True)
    game.set_objects_info_enabled(True)

    game.set_window_visible(True)
    game.set_episode_timeout(200)
    game.init()

    try:
        game.new_episode()

        state = game.get_state()

        if state is None:
            print("No observation available.")
            return

        print("State number:", state.number)
        print("Game variables:", state.game_variables)
        print("Available buttons:", [
            button.name
            for button in game.get_available_buttons()
        ])

        print("Screen buffer:",
              None if state.screen_buffer is None
              else state.screen_buffer.shape)

        print("Labels:", state.labels)
        print("Objects:", state.objects)

    finally:
        game.close()


if __name__ == "__main__":
    main()
