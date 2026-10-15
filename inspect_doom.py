
import vizdoom as vzd


game = vzd.DoomGame()

game.set_doom_scenario_path(
    vzd.scenarios_path + "/basic.wad"
)
game.set_doom_map("map01")
game.set_screen_resolution(
    vzd.ScreenResolution.RES_640X480
)
game.set_labels_buffer_enabled(True)
game.set_objects_info_enabled(True)
game.set_window_visible(True)

game.init()

try:
    game.new_episode()

    for _ in range(10):
        if game.is_episode_finished():
            break

        state = game.get_state()

        if state is None:
            print("No game state available.")
            break

        print("\n" + "=" * 50)
        print("Step:", state.number)
        print("Game variables:", state.game_variables)

        print("\nVISIBLE LABELS:")
        for label in (state.labels or []):
            print({
                "name": getattr(label, "object_name", None),
                "category": getattr(label, "object_category", None),
                "screen_x": getattr(label, "x", None),
                "screen_y": getattr(label, "y", None),
                "width": getattr(label, "width", None),
                "height": getattr(label, "height", None),
            })

        print("\nOBJECT INFORMATION:")
        for obj in (state.objects or []):
            print({
                "name": getattr(obj, "name", None),
                "category": getattr(obj, "category", None),
                "x": getattr(obj, "position_x", None),
                "y": getattr(obj, "position_y", None),
                "angle": getattr(obj, "angle", None),
            })

        # Advance the game without pressing any buttons.
        game.make_action(
            [False] * game.get_available_buttons_size(),
            4,
        )

finally:
    game.close()
