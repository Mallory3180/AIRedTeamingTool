from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

from .types import RunLog


class RunLogger:
    def __init__(self, run_id: str, logs_root: str) -> None:
        self.run_id = run_id
        self.logs_dir = Path(logs_root) / f"run_{run_id}"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.logs_dir / "runs.jsonl"

    def append(self, log: RunLog) -> None:
        payload = json.dumps(log.model_dump(), default=str, ensure_ascii=False)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(payload + "\n")

    def append_many(self, logs: Iterable[RunLog]) -> None:
        for entry in logs:
            self.append(entry)


def mask_secret(value: str | None) -> str | None:
    if not value:
        return value
    if len(value) <= 4:
        return "****"
    return value[:2] + "****" + value[-2:]


def env_or_none(key: str | None) -> str | None:
    if not key:
        return None
    return os.getenv(key)
