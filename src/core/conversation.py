from __future__ import annotations

from typing import Iterable, Tuple


def format_conversation_history(messages: Iterable[Tuple[str, str]]) -> str:
    lines = []
    for role, content in messages:
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
