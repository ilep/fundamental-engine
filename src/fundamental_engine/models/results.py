from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from fundamental_engine.models.provenance import Confidence


class MetricResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    metric: str
    value: float
    formula: str
    inputs: dict[str, float | str]
    assumptions: list[str] = []
    warnings: list[str] = []
    confidence: Confidence = Confidence.MEDIUM


class RangeResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    metric: str
    low: float
    base: float
    high: float
    formula: str
    assumptions: list[str] = []
    warnings: list[str] = []
    confidence: Confidence = Confidence.LOW


class ScenarioResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    enterprise_value: float
    equity_value: float
    per_share_value: float | None = None
    assumptions: list[str] = []

