from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


@dataclass
class SystemConfig:
    orchestrator_llm: Dict[str, Any]
    embedding: Dict[str, Any]
    rag: Dict[str, Any]
    logging: Dict[str, Any]


@dataclass
class TargetConfig:
    base_url: str
    endpoint: str
    request_key: str
    response_key: str
    model: str
    api_key_env: str | None = None


def load_yaml(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_system_config(path: str) -> SystemConfig:
    load_dotenv()
    payload = load_yaml(path)
    return SystemConfig(
        orchestrator_llm=payload["orchestrator_llm"],
        embedding=payload["embedding"],
        rag=payload["rag"],
        logging=payload["logging"],
    )


def load_target_config(path: str) -> TargetConfig:
    load_dotenv()
    payload = load_yaml(path)
    return TargetConfig(**payload)
