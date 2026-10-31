from __future__ import annotations

from collections.abc import Sequence

from fundamental_engine.models import Confidence, MetricResult


def calculate_dcf(
    cash_flows: Sequence[float],
    *,
    discount_rate: float,
    terminal_growth_rate: float = 0.0,
    net_debt: float = 0.0,
) -> MetricResult:
    if not cash_flows:
        raise ValueError("At least one cash flow is required")
    if discount_rate <= terminal_growth_rate:
        raise ValueError("discount_rate must exceed terminal_growth_rate")
    present_value = sum(cf / (1 + discount_rate) ** year for year, cf in enumerate(cash_flows, 1))
    terminal_value = cash_flows[-1] * (1 + terminal_growth_rate) / (
        discount_rate - terminal_growth_rate
    )
    discounted_terminal = terminal_value / (1 + discount_rate) ** len(cash_flows)
    return MetricResult(
        metric="dcf_equity_value",
        value=present_value + discounted_terminal - net_debt,
        formula="PV(explicit cash flows) + PV(terminal value) - net debt",
        inputs={
            "discount_rate": discount_rate,
            "terminal_growth_rate": terminal_growth_rate,
            "explicit_periods": float(len(cash_flows)),
            "present_value_explicit": present_value,
            "present_value_terminal": discounted_terminal,
            "net_debt": net_debt,
        },
        confidence=Confidence.MEDIUM,
    )

