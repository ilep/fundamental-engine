from __future__ import annotations

from datetime import date
from typing import Any

from fundamental_engine.models import Confidence, FinancialPeriod, Provenance, SourcedValue


def _number(record: dict[str, Any], key: str, document: str) -> SourcedValue | None:
    raw = record.get(key)
    if raw in (None, "", "None"):
        return None
    try:
        numeric = float(raw)
    except (TypeError, ValueError):
        return None
    return SourcedValue(
        value=numeric,
        provenance=Provenance(
            source_document=document,
            source_label=key,
            status="provider",
            confidence=Confidence.MEDIUM,
        ),
    )


def from_eod(
    fundamentals: dict[str, Any],
    *,
    fiscal_period_end: date,
    currency: str,
    ticker: str = "",
) -> FinancialPeriod:
    """Convert one annual EOD fundamentals period into the canonical model."""

    key = fiscal_period_end.isoformat()
    financials = fundamentals.get("Financials", {})
    income = financials.get("Income_Statement", {}).get("yearly", {}).get(key, {})
    cash_flow = financials.get("Cash_Flow", {}).get("yearly", {}).get(key, {})
    balance = financials.get("Balance_Sheet", {}).get("yearly", {}).get(key, {})
    general = fundamentals.get("General", {})
    document = f"EOD fundamentals {key}"

    debt = _number(balance, "shortLongTermDebtTotal", document) or _number(
        balance, "longTermDebtTotal", document
    )
    return FinancialPeriod(
        company_name=general.get("Name") or ticker or "Unknown",
        ticker=ticker or general.get("Code", ""),
        fiscal_period_end=fiscal_period_end,
        currency=currency,
        revenue=_number(income, "totalRevenue", document),
        ebit=_number(income, "ebit", document),
        operating_income=_number(income, "operatingIncome", document),
        income_tax_expense=_number(income, "incomeTaxExpense", document),
        pretax_income=_number(income, "incomeBeforeTax", document),
        net_income=_number(income, "netIncome", document),
        depreciation_and_amortization=_number(income, "depreciationAndAmortization", document)
        or _number(cash_flow, "depreciation", document),
        cash_from_operations=_number(cash_flow, "totalCashFromOperatingActivities", document),
        capital_expenditures=_number(cash_flow, "capitalExpenditures", document),
        change_in_working_capital=_number(cash_flow, "changeInWorkingCapital", document),
        total_equity=_number(balance, "totalStockholderEquity", document),
        total_debt=debt,
        cash_and_equivalents=_number(balance, "cash", document),
        goodwill=_number(balance, "goodWill", document),
        shares_outstanding=_number(balance, "commonStockSharesOutstanding", document),
    )

