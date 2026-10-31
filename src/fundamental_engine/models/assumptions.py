from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceCapexPolicy(str, Enum):
    TOTAL_CAPEX = "total_capex"
    DEPRECIATION_PROXY = "depreciation_proxy"
    EXPLICIT = "explicit"
    SCENARIO_RANGE = "scenario_range"


class Scenario(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    normalized_nopat: float
    cost_of_capital: float = Field(gt=0)
    growth_rate: float = 0.0
    net_non_operating_assets: float = 0.0
    net_debt: float = 0.0
    shares_outstanding: float | None = Field(default=None, gt=0)

