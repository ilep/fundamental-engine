from __future__ import annotations

from fundamental_engine.models import Confidence, MetricResult


def calculate_epv(
    normalized_nopat: MetricResult | float,
    *,
    cost_of_capital: float,
    growth_rate: float = 0.0,
    net_non_operating_assets: float = 0.0,
    net_debt: float = 0.0,
) -> MetricResult:
    nopat = normalized_nopat.value if isinstance(normalized_nopat, MetricResult) else float(normalized_nopat)
    if cost_of_capital <= growth_rate:
        raise ValueError("cost_of_capital must exceed growth_rate")
    if growth_rate != 0:
        warnings = ["Non-zero growth turns strict no-growth EPV into a growing perpetuity"]
    else:
        warnings = []
    enterprise_value = nopat / (cost_of_capital - growth_rate)
    equity_value = enterprise_value + net_non_operating_assets - net_debt
    return MetricResult(
        metric="epv_equity_value",
        value=equity_value,
        formula="NOPAT / (cost of capital - growth) + net non-operating assets - net debt",
        inputs={
            "normalized_nopat": nopat,
            "cost_of_capital": cost_of_capital,
            "growth_rate": growth_rate,
            "net_non_operating_assets": net_non_operating_assets,
            "net_debt": net_debt,
            "enterprise_value": enterprise_value,
        },
        warnings=warnings,
        confidence=Confidence.MEDIUM if warnings else Confidence.HIGH,
    )

