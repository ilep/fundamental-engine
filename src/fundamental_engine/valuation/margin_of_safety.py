from fundamental_engine.models import Confidence, MetricResult


def calculate_margin_of_safety(
    intrinsic_value: MetricResult | float,
    market_price: float,
) -> MetricResult:
    fair_value = intrinsic_value.value if isinstance(intrinsic_value, MetricResult) else float(intrinsic_value)
    if fair_value <= 0:
        raise ValueError("intrinsic_value must be positive")
    if market_price < 0:
        raise ValueError("market_price must not be negative")
    return MetricResult(
        metric="margin_of_safety",
        value=(fair_value - market_price) / fair_value,
        formula="(intrinsic value - market price) / intrinsic value",
        inputs={"intrinsic_value": fair_value, "market_price": market_price},
        confidence=Confidence.HIGH,
    )

