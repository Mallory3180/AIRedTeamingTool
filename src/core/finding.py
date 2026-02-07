from __future__ import annotations

from typing import Iterable


def should_promote_finding(mutations: Iterable[str]) -> bool:
    unique = {mutation.strip() for mutation in mutations if mutation.strip()}
    return len(unique) >= 2
