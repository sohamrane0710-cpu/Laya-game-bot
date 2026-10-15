
class DoomStateAdapter:
    """
    Converts ViZDoom's raw state into a stable agent schema.
    """

    def transform(self, raw_state):
        if raw_state is None:
            raise ValueError(
                "Cannot normalize a missing game state"
            )

        variables = raw_state.game_variables

        health = None
        ammo = None

        if variables is not None and len(variables) >= 2:
            health = float(variables[0])
            ammo = float(variables[1])

        visible_enemies = []

        for label in (raw_state.labels or []):
            name = getattr(label, "object_name", None)
            category = getattr(label, "object_category", None)

            if category != "Monster":
                continue

            x = float(label.x)
            y = float(label.y)
            width = float(label.width)
            height = float(label.height)

            center_x = x + width / 2
            center_y = y + height / 2

            visible_enemies.append({
                "name": name,
                "screen_x": x,
                "screen_y": y,
                "width": width,
                "height": height,
                "center_x": center_x,
                "center_y": center_y,
                "horizontal_offset_from_center": (
                    center_x - 320
                ),
            })

        return {
            "game": "doom",
            "step": int(raw_state.number),
            "health": health,
            "ammo": ammo,
            "visible_enemies": visible_enemies,
            "enemy_visible": len(visible_enemies) > 0,
            "observation_source": "structured_game_variables_and_visible_labels",
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
