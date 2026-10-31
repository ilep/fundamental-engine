from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Provenance(BaseModel):
    """Where a financial input came from and how it was produced."""

    model_config = ConfigDict(frozen=True)

    source_document: str = ""
    page_number: int | None = Field(default=None, ge=1)
    source_label: str = ""
    evidence: str = ""
    status: str = "reported"
    confidence: Confidence = Confidence.MEDIUM


class SourcedValue(BaseModel):
    """A numeric value paired with source metadata."""

    model_config = ConfigDict(frozen=True)

    value: float
    provenance: Provenance = Field(default_factory=Provenance)

