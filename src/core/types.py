from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TagMixin(BaseModel):
    agentic_tags: List[str] = Field(default_factory=list)
    llm_tags: List[str] = Field(default_factory=list)
    aisi_tags: List[str] = Field(default_factory=list)
    cia_tags: Dict[str, List[str]] = Field(default_factory=dict)


class RunLog(TagMixin):
    run_id: str
    step: str
    llm_role: str
    prompt: str
    response: Optional[str] = None
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_type: Optional[str] = None
    http_status: Optional[int] = None
    exception: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Hypothesis(TagMixin):
    hypothesis_id: str
    statement: str
    confidence: float = 0.0


class Finding(TagMixin):
    finding_id: str
    hypothesis_id: Optional[str] = None
    description: str
    severity: str = "medium"
    evidence: List[str] = Field(default_factory=list)


class JudgeResult(TagMixin):
    hypothesis_id: str
    verdict: str
    rationale: str
    score: float


class RagChunkMetadata(BaseModel):
    doc_id: str
    page: int
    chunk_id: str
    source_type: str
    section: Optional[str] = None
    heading: Optional[str] = None
    rule_id: Optional[str] = None
    rule_type: Optional[str] = None


class RagResult(BaseModel):
    doc_id: str
    page: int
    quote: str
    metadata: RagChunkMetadata
