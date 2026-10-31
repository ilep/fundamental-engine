from __future__ import annotations

from fundamental_engine.metrics._helpers import ensure_non_financial, value
from fundamental_engine.models import Confidence, FinancialPeriod, MetricResult


def calculate_nopat(
    period: FinancialPeriod,
    *,
    tax_policy: str = "normalized",
    normalized_tax_rate: float | None = None,
    adjust_exceptional_items: bool = True,
) -> MetricResult:
    """Calculate NOPAT from EBIT/operating income using an explicit tax policy."""

    ensure_non_financial(period)
    operating_profit = period.ebit or period.operating_income
    ebit = value(operating_profit, "ebit or operating_income")
    exceptional = (
        period.exceptional_operating_items.value
        if adjust_exceptional_items and period.exceptional_operating_items
        else 0.0
    )
    normalized_ebit = ebit - exceptional
    warnings: list[str] = []

    if tax_policy == "normalized":
        if normalized_tax_rate is None or not 0 <= normalized_tax_rate <= 1:
            raise ValueError("normalized_tax_rate must be between 0 and 1")
        tax_rate = normalized_tax_rate
        tax_amount = normalized_ebit * tax_rate
    elif tax_policy == "effective":
        pretax = value(period.pretax_income, "pretax_income")
        tax = value(period.income_tax_expense, "income_tax_expense")
        if pretax <= 0:
            raise ValueError("Effective tax policy requires positive pretax income")
        tax_rate = min(max(tax / pretax, 0.0), 1.0)
        tax_amount = normalized_ebit * tax_rate
    elif tax_policy == "cash":
        tax_amount = value(period.cash_taxes, "cash_taxes")
        tax_rate = tax_amount / normalized_ebit if normalized_ebit else 0.0
        warnings.append("Cash taxes can include non-operating and timing effects")
    else:
        raise ValueError(f"Unsupported tax_policy: {tax_policy}")

    return MetricResult(
        metric="nopat",
        value=normalized_ebit - tax_amount,
        formula="normalized EBIT - operating taxes",
        inputs={
            "reported_operating_profit": ebit,
            "exceptional_operating_items": exceptional,
            "tax_rate": tax_rate,
            "operating_taxes": tax_amount,
        },
        assumptions=[f"tax_policy={tax_policy}", f"exceptional_items_adjusted={adjust_exceptional_items}"],
        warnings=warnings,
        confidence=Confidence.MEDIUM if tax_policy == "cash" else Confidence.HIGH,
    )

