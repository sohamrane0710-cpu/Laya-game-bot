
class ActionValidator:
    def __init__(self, allowed_actions):
        self.allowed_actions = set(allowed_actions)

    def validate(self, action):
        if not isinstance(action, str):
            return False, "Action must be a string"

        if action not in self.allowed_actions:
            return False, f"Unsupported action: {action}"

        return True, None
