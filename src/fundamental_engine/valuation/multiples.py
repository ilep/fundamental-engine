from fundamental_engine.models import Confidence, MetricResult


def calculate_earnings_multiple_value(
    normalized_earnings: MetricResult | float,
    *,
    multiple: float,
    net_debt: float = 0.0,
    earnings_are_after_interest: bool = True,
) -> MetricResult:
    earnings = normalized_earnings.value if isinstance(normalized_earnings, MetricResult) else float(normalized_earnings)
    if multiple <= 0:
        raise ValueError("multiple must be positive")
    value = earnings * multiple
    if not earnings_are_after_interest:
        value -= net_debt
    return MetricResult(
        metric="earnings_multiple_equity_value",
        value=value,
        formula="normalized earnings * multiple" + ("" if earnings_are_after_interest else " - net debt"),
        inputs={"normalized_earnings": earnings, "multiple": multiple, "net_debt": net_debt},
        assumptions=[f"earnings_are_after_interest={earnings_are_after_interest}"],
        confidence=Confidence.MEDIUM,
    )

