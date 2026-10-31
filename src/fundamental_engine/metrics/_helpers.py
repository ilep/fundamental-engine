from __future__ import annotations

from fundamental_engine.models import FinancialPeriod, SourcedValue


def value(item: SourcedValue | None, name: str) -> float:
    if item is None:
        raise ValueError(f"Missing required financial input: {name}")
    return item.value


def ensure_non_financial(period: FinancialPeriod) -> None:
    if period.is_financial_institution:
        raise ValueError(
            "The default industrial-company methodology is not valid for financial institutions"
        )


def same_company_and_currency(current: FinancialPeriod, previous: FinancialPeriod) -> None:
    if current.company_name != previous.company_name:
        raise ValueError("Periods must belong to the same company")
    if current.currency != previous.currency:
        raise ValueError("Periods must use the same currency")

