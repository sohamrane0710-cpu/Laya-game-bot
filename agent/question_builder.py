
def build_questions(state):
    criteria = {
        "forward": "Move forward to explore when no enemy needs attention.",
        "turn_left": "Turn left to search for or align with an enemy.",
        "turn_right": "Turn right to search for or align with an enemy.",
        "attack": "Fire when an enemy is approximately centered.",
        "forward_attack": "Move forward while firing when advancing is useful.",
        "left_attack": "Turn left while firing to align with an enemy on the left.",
        "right_attack": "Turn right while firing to align with an enemy on the right.",
        "wait": "Remain still only when there is a specific tactical reason.",
    }

    enemies = state.get("visible_enemies", [])
    if enemies:
        enemy_summary = "; ".join(
            f"{enemy.get('name', 'enemy')}: "
            f"horizontal offset "
            f"{enemy.get('horizontal_offset_from_center', 0):.0f}px"
            for enemy in enemies[:2]
        )
        situation = (
            f"Visible enemy detected: {enemy_summary}. "
            "Prioritize engaging or aligning with a visible enemy. "
            "Do not choose wait merely because the player is safe."
        )
    else:
        situation = (
            "No visible enemy is currently detected. "
            "Prefer exploration over repeated waiting."
        )

    health = state.get("health")
    ammo = state.get("ammo")

    instructions = (
        "Choose one valid DOOM action for the next short interval. "
        f"{situation} "
        f"Health={health}; ammo={ammo}. "
        "Use only the supplied observation; do not invent enemies "
        "or environmental details. Choose wait only when justified."
    )

    return {
        "action": {
            "type": "choice",
            "instructions": instructions,
            "criteria": criteria,
        }
    }
