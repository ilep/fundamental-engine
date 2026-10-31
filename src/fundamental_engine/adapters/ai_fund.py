from __future__ import annotations

from datetime import date
from typing import Any

from fundamental_engine.models import Confidence, FinancialPeriod, Provenance, SourcedValue


AI_FUND_FIELD_MAP = {
    "revenue": "revenue",
    "operating_income": "operating_income",
    "pretax_income": "pretax_income",
    "income_tax_expense": "income_tax_expense",
    "net_income": "net_income",
    "depreciation_and_amortization": "depreciation_and_amortization",
    "stock_based_compensation": "stock_based_compensation",
    "cash_from_operations": "cash_from_operations",
    "capital_expenditures": "capital_expenditures",
    "change_in_working_capital": "change_in_working_capital",
}


def _metric(metric: dict[str, Any] | None, source_document: str) -> SourcedValue | None:
    if not metric or metric.get("status") != "reported":
        return None
    numeric = metric.get("numeric_value")
    raw = metric.get("value_raw")
    value = numeric if numeric not in (None, "") else raw
    if value is None:
        return None
    page = metric.get("page_number") or None
    return SourcedValue(
        value=float(value),
        provenance=Provenance(
            source_document=source_document,
            page_number=page,
            source_label=metric.get("source_label", ""),
            evidence=metric.get("verbatim_extract", ""),
            status="reported",
            confidence=Confidence.HIGH,
        ),
    )


def from_ai_fund(
    payload: dict[str, Any],
    *,
    company_name: str | None = None,
    fiscal_period_end: date | None = None,
    currency: str | None = None,
    ticker: str = "",
    source_document: str = "",
    balance_sheet: dict[str, Any] | None = None,
) -> FinancialPeriod:
    """Convert ai-fund's universal normalized metric dictionary to a FinancialPeriod."""

    income = payload.get("income_statement_universal", {})
    cash_flow = payload.get("cash_flow_statement_universal", {})
    if income or cash_flow:
        normalized = {**income, **cash_flow}
    else:
        normalized = payload.get("normalized", payload.get("universal_attributes", payload))

    resolved_company = company_name or payload.get("company_name")
    resolved_currency = currency or payload.get("reporting_currency")
    raw_period_end = fiscal_period_end or payload.get("fiscal_period_end")
    if not resolved_company:
        raise ValueError("company_name is required when absent from the ai-fund payload")
    if not resolved_currency:
        raise ValueError("currency is required when absent from the ai-fund payload")
    if not raw_period_end:
        raise ValueError("fiscal_period_end is required when absent from the ai-fund payload")
    resolved_period_end = (
        raw_period_end if isinstance(raw_period_end, date) else date.fromisoformat(raw_period_end)
    )
    values: dict[str, Any] = {}
    for source_name, target_name in AI_FUND_FIELD_MAP.items():
        values[target_name] = _metric(normalized.get(source_name), source_document)
    for name in (
        "total_equity",
        "total_debt",
        "finance_lease_liabilities",
        "cash_and_equivalents",
        "excess_cash",
        "goodwill",
        "shares_outstanding",
    ):
        values[name] = _metric((balance_sheet or {}).get(name), source_document)
    return FinancialPeriod(
        company_name=resolved_company,
        ticker=ticker,
        fiscal_period_end=resolved_period_end,
        currency=resolved_currency,
        **values,
    )

