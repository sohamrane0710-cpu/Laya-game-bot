
import vizdoom as vzd


class DoomGameClient:
    """
    Wraps the ViZDoom API behind a small, stable interface.
    """

    def __init__(
        self,
        visible=True,
        episode_timeout=300,
        action_frames=4,
    ):
        self.action_frames = action_frames
        self.closed = False

        self.game = vzd.DoomGame()

        self.game.set_doom_scenario_path(
            vzd.scenarios_path + "/basic.wad"
        )
        self.game.set_doom_map("map01")

        self.game.set_screen_resolution(
            vzd.ScreenResolution.RES_640X480
        )
        self.game.set_screen_format(vzd.ScreenFormat.RGB24)
        self.game.set_window_visible(visible)

        # Debugging: expose labels and object information.
        self.game.set_labels_buffer_enabled(True)
        self.game.set_objects_info_enabled(True)

        # The order here must match the Boolean action lists
        # used in execute().
        self.game.set_available_buttons([
            vzd.Button.MOVE_FORWARD,
            vzd.Button.TURN_LEFT,
            vzd.Button.TURN_RIGHT,
            vzd.Button.ATTACK,
        ])

        self.game.set_available_game_variables([
            vzd.GameVariable.HEALTH,
            vzd.GameVariable.AMMO2,
        ])

        self.game.set_episode_timeout(episode_timeout)
        self.game.init()

    def reset(self):
        """Start a new episode."""
        if self.closed:
            raise RuntimeError("Game client is closed")

        self.game.new_episode()
        return self.observe()

    def observe(self):
        """Return the current ViZDoom state."""
        if self.closed or self.game.is_episode_finished():
            return None

        return self.game.get_state()

    def execute(self, action):
        """Execute one supported action in the game."""

        action_map = {
            "forward": [True, False, False, False],
            "turn_left": [False, True, False, False],
            "turn_right": [False, False, True, False],
            "attack": [False, False, False, True],
            "forward_attack": [True, False, False, True],
            "left_attack": [False, True, False, True],
            "right_attack": [False, False, True, True],
            "wait": [False, False, False, False],
        }

        if self.closed:
            raise RuntimeError("Game client is closed")

        if self.game.is_episode_finished():
            raise RuntimeError("Cannot execute action: episode has ended")

        if action not in action_map:
            raise ValueError(
                f"Unsupported DOOM action: {action}"
            )

        return self.game.make_action(
            action_map[action],
            self.action_frames,
        )

    def is_terminal(self):
        """Check whether the current episode has ended."""
        return (
            self.closed
            or self.game.is_episode_finished()
        )

    def get_total_reward(self):
        """Return the total reward for the current episode."""
        return self.game.get_total_reward()

    def close(self):
        """Release ViZDoom resources."""
        if not self.closed:
            self.game.close()
            self.closed = True
