from __future__ import annotations

from fundamental_engine.metrics._helpers import value
from fundamental_engine.models import Confidence, FinancialPeriod, MetricResult


def calculate_cfo_fcf(period: FinancialPeriod) -> MetricResult:
    cfo = value(period.cash_from_operations, "cash_from_operations")
    capex = abs(value(period.capital_expenditures, "capital_expenditures"))
    return MetricResult(
        metric="cfo_fcf",
        value=cfo - capex,
        formula="cash from operations - absolute capital expenditures",
        inputs={"cash_from_operations": cfo, "capital_expenditures": capex},
        assumptions=["capital expenditures are normalized to a positive outflow"],
        confidence=Confidence.HIGH,
    )


def calculate_fcff(nopat: MetricResult | float, change_in_invested_capital: float) -> MetricResult:
    nopat_value = nopat.value if isinstance(nopat, MetricResult) else float(nopat)
    return MetricResult(
        metric="fcff",
        value=nopat_value - change_in_invested_capital,
        formula="NOPAT - change in invested capital",
        inputs={"nopat": nopat_value, "change_in_invested_capital": change_in_invested_capital},
        confidence=Confidence.HIGH,
    )

