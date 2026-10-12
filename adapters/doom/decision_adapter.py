
class DoomDecisionAdapter:
    """
    Converts normalized action labels to game-client actions.
    """

    def __init__(self):
        self.allowed_actions = {
            "forward",
            "turn_left",
            "turn_right",
            "attack",
            "forward_attack",
            "left_attack",
            "right_attack",
            "wait",
        }

    def transform(self, action):
        """
        Validate an action returned by the decision model
        and pass it to the game client.
        """
        if not isinstance(action, str):
            raise ValueError(
                f"Action must be a string, got: {type(action).__name__}"
            )

        if action not in self.allowed_actions:
            raise ValueError(
                f"Action is not supported: {action}"
            )

        return action
