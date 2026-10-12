
import json
from pathlib import Path


class ExperienceStore:
    def __init__(self, log_path="logs/episodes.jsonl"):
        self.path = Path(log_path)

    def retrieve(self, state, limit=3):
        """
        Return a few previous transitions with similar
        health and ammunition values.
        """
        if not self.path.exists():
            return []

        current_health = state["health"]
        current_ammo = state["ammo"]

        candidates = []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if record.get("event") != "transition":
                    continue

                previous_state = record.get("state")
                if not isinstance(previous_state, dict):
                    continue

                if "health" not in previous_state:
                    continue

                if "ammo" not in previous_state:
                    continue

                # Simple distance between state features.
                health_difference = abs(
                    current_health - previous_state["health"]
                ) / 100.0

                ammo_difference = abs(
                    current_ammo - previous_state["ammo"]
                ) / 100.0

                distance = (
                    health_difference + ammo_difference
                )

                candidates.append((
                    distance,
                    {
                        "previous_state": previous_state,
                        "action": record.get("executed_action"),
                        "reward": record.get("reward"),
                        "next_state": record.get("next_state"),
                    },
                ))

        candidates.sort(key=lambda item: item[0])

        return [
            experience
            for _, experience in candidates[:limit]
        ]
