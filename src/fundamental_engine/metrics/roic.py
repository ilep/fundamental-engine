from __future__ import annotations

from fundamental_engine.models import Confidence, MetricResult


def calculate_roic(nopat: MetricResult | float, invested_capital: MetricResult | float) -> MetricResult:
    nopat_value = nopat.value if isinstance(nopat, MetricResult) else float(nopat)
    capital_value = (
        invested_capital.value if isinstance(invested_capital, MetricResult) else float(invested_capital)
    )
    if capital_value == 0:
        raise ValueError("Invested capital must not be zero")
    warnings = []
    if capital_value < 0:
        warnings.append("ROIC on negative invested capital is not economically comparable")
    return MetricResult(
        metric="roic",
        value=nopat_value / capital_value,
        formula="NOPAT / invested capital",
        inputs={"nopat": nopat_value, "invested_capital": capital_value},
        warnings=warnings,
        confidence=Confidence.LOW if warnings else Confidence.HIGH,
    )


def calculate_incremental_roic(
    current_nopat: MetricResult | float,
    previous_nopat: MetricResult | float,
    current_ending_capital: MetricResult | float,
    previous_ending_capital: MetricResult | float,
) -> MetricResult:
    cn = current_nopat.value if isinstance(current_nopat, MetricResult) else float(current_nopat)
    pn = previous_nopat.value if isinstance(previous_nopat, MetricResult) else float(previous_nopat)
    cc = (
        current_ending_capital.value
        if isinstance(current_ending_capital, MetricResult)
        else float(current_ending_capital)
    )
    pc = (
        previous_ending_capital.value
        if isinstance(previous_ending_capital, MetricResult)
        else float(previous_ending_capital)
    )
    delta_capital = cc - pc
    if delta_capital == 0:
        raise ValueError("Change in invested capital must not be zero")
    warnings = []
    if delta_capital < 0:
        warnings.append("Capital contracted; incremental ROIC needs contextual interpretation")
    return MetricResult(
        metric="incremental_roic",
        value=(cn - pn) / delta_capital,
        formula="change in NOPAT / change in ending invested capital",
        inputs={
            "current_nopat": cn,
            "previous_nopat": pn,
            "current_ending_capital": cc,
            "previous_ending_capital": pc,
        },
        warnings=warnings,
        confidence=Confidence.MEDIUM if warnings else Confidence.HIGH,
    )

