from __future__ import annotations

from fundamental_engine.metrics._helpers import ensure_non_financial, same_company_and_currency, value
from fundamental_engine.models import Confidence, FinancialPeriod, MetricResult


def _ending_capital(
    period: FinancialPeriod,
    *,
    goodwill_policy: str,
    cash_policy: str,
    include_finance_leases: bool,
) -> tuple[float, dict[str, float], list[str]]:
    equity = value(period.total_equity, "total_equity")
    debt = value(period.total_debt, "total_debt")
    leases = period.finance_lease_liabilities.value if period.finance_lease_liabilities else 0.0
    goodwill = period.goodwill.value if period.goodwill else 0.0
    warnings: list[str] = []

    if cash_policy == "all_cash":
        cash_deduction = value(period.cash_and_equivalents, "cash_and_equivalents")
    elif cash_policy == "reported_excess_cash_only":
        cash_deduction = period.excess_cash.value if period.excess_cash else 0.0
        if period.excess_cash is None:
            warnings.append("No explicit excess-cash figure; no cash was deducted")
    elif cash_policy == "none":
        cash_deduction = 0.0
    else:
        raise ValueError(f"Unsupported cash_policy: {cash_policy}")

    if goodwill_policy == "include":
        goodwill_adjustment = 0.0
    elif goodwill_policy == "exclude":
        goodwill_adjustment = -goodwill
    else:
        raise ValueError(f"Unsupported goodwill_policy: {goodwill_policy}")

    lease_adjustment = leases if include_finance_leases else 0.0
    invested = equity + debt + lease_adjustment - cash_deduction + goodwill_adjustment
    inputs = {
        "equity": equity,
        "debt": debt,
        "finance_leases": lease_adjustment,
        "cash_deduction": cash_deduction,
        "goodwill_adjustment": goodwill_adjustment,
    }
    return invested, inputs, warnings


def calculate_invested_capital(
    current: FinancialPeriod,
    previous: FinancialPeriod | None = None,
    *,
    capital_policy: str = "average_financing_approach",
    goodwill_policy: str = "include",
    cash_policy: str = "reported_excess_cash_only",
    include_finance_leases: bool = True,
) -> MetricResult:
    ensure_non_financial(current)
    current_value, inputs, warnings = _ending_capital(
        current,
        goodwill_policy=goodwill_policy,
        cash_policy=cash_policy,
        include_finance_leases=include_finance_leases,
    )

    if capital_policy == "ending_financing_approach":
        result = current_value
        formula = "ending equity + debt + leases - cash - excluded goodwill"
    elif capital_policy == "average_financing_approach":
        if previous is None:
            raise ValueError("Average invested capital requires a previous period")
        ensure_non_financial(previous)
        same_company_and_currency(current, previous)
        previous_value, previous_inputs, previous_warnings = _ending_capital(
            previous,
            goodwill_policy=goodwill_policy,
            cash_policy=cash_policy,
            include_finance_leases=include_finance_leases,
        )
        result = (current_value + previous_value) / 2
        inputs.update({f"previous_{key}": val for key, val in previous_inputs.items()})
        inputs["current_ending_invested_capital"] = current_value
        inputs["previous_ending_invested_capital"] = previous_value
        warnings.extend(previous_warnings)
        formula = "(current ending invested capital + previous ending invested capital) / 2"
    else:
        raise ValueError(f"Unsupported capital_policy: {capital_policy}")

    if result <= 0:
        warnings.append("Invested capital is non-positive; ROIC may not be economically meaningful")

    return MetricResult(
        metric="invested_capital",
        value=result,
        formula=formula,
        inputs=inputs,
        assumptions=[
            f"capital_policy={capital_policy}",
            f"goodwill_policy={goodwill_policy}",
            f"cash_policy={cash_policy}",
            f"include_finance_leases={include_finance_leases}",
        ],
        warnings=warnings,
        confidence=Confidence.MEDIUM if warnings else Confidence.HIGH,
    )

