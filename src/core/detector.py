from __future__ import annotations

from typing import List

from pydantic import BaseModel


class DetectorInput(BaseModel):
    prompt: str
    response: str


class DetectorOutput(BaseModel):
    verdict: str
    scores: List[float]
