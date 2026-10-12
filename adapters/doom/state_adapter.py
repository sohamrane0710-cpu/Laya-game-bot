
class DoomStateAdapter:
    """
    Converts ViZDoom's raw state into a stable agent schema.
    """

    def transform(self, raw_state):
        """
        Extract structured game variables and expose the
        actions supported by the decision adapter.
        """
        if raw_state is None:
            raise ValueError(
                "Cannot normalize a missing game state"
            )

        variables = raw_state.game_variables

        if variables is None or len(variables) < 2:
            raise ValueError(
                "Expected health and ammo variables"
            )

        health = float(variables[0])
        ammo = float(variables[1])

        return {
            "game": "doom",
            "step": int(raw_state.number),
            "health": health,
            "ammo": ammo,
            "observation_source": "structured_game_variables",
            "available_actions": [
                "forward",
                "turn_left",
                "turn_right",
                "attack",
                "forward_attack",
                "left_attack",
                "right_attack",
                "wait",
            ],
        }
