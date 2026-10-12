
import json
from datetime import datetime, timezone
from pathlib import Path


class AgentLogger:
    def __init__(self, log_path="logs/episodes.jsonl"):
        self.path = Path(log_path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def record(self, event):
        entry = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            **event,
        }

        with self.path.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(entry, ensure_ascii=False)
                + "\n"
            )

    def info(self, message, **fields):
        self.record({
            "event": "info",
            "message": message,
            **fields,
        })

    def warning(self, message, **fields):
        self.record({
            "event": "warning",
            "message": message,
            **fields,
        })

    def error(self, message, **fields):
        self.record({
            "event": "error",
            "message": message,
            **fields,
        })
