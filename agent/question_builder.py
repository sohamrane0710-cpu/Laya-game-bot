def build_questions(state):
    actions = [
        "forward",
        "turn_left",
        "turn_right",
        "attack",
        "forward_attack",
        "left_attack",
        "right_attack",
        "wait",
    ]

    criteria = {
        "forward": (
            "Move forward to explore the environment."
        ),
        "turn_left": (
            "Rotate left to change the viewing direction."
        ),
        "turn_right": (
            "Rotate right to change the viewing direction."
        ),
        "attack": (
            "Fire at a potential target when appropriate."
        ),
        "forward_attack": (
            "Move forward while firing."
        ),
        "left_attack": (
            "Rotate left while firing."
        ),
        "right_attack": (
            "Rotate right while firing."
        ),
        "wait": (
            "Take no action for this short interval."
        ),
    }

    instructions = (
        "Choose exactly one valid DOOM action for the next "
        "short action interval. Use the current health, ammo, "
        "available actions, and any observation information "
        "provided. Prefer exploring when no target information "
        "is available, and avoid repeatedly waiting without a "
        "specific reason. Do not claim to see enemies or walls "
        "unless the observation actually provides that information."
    )

    experiences = state.get("relevant_experiences", [])

    if experiences:
        instructions += (
            "\nPast experiences are optional evidence. "
            "Prioritize the current game state and do not "
            "assume a previous action will have the same outcome."
        )

    return {
        "action": {
            "type": "choice",
            "instructions": instructions,
            "criteria": criteria,
        }
    }