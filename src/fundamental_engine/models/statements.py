from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from fundamental_engine.models.provenance import SourcedValue


class FinancialPeriod(BaseModel):
    """Canonical financial data for one fiscal period, in base currency units."""

    model_config = ConfigDict(frozen=True)

    company_name: str
    ticker: str = ""
    fiscal_period_end: date
    currency: str
    period_type: str = "annual"
    is_financial_institution: bool = False

    revenue: SourcedValue | None = None
    ebit: SourcedValue | None = None
    operating_income: SourcedValue | None = None
    income_tax_expense: SourcedValue | None = None
    cash_taxes: SourcedValue | None = None
    pretax_income: SourcedValue | None = None
    net_income: SourcedValue | None = None
    depreciation_and_amortization: SourcedValue | None = None
    stock_based_compensation: SourcedValue | None = None
    cash_from_operations: SourcedValue | None = None
    capital_expenditures: SourcedValue | None = None
    change_in_working_capital: SourcedValue | None = None

    total_equity: SourcedValue | None = None
    total_debt: SourcedValue | None = None
    finance_lease_liabilities: SourcedValue | None = None
    cash_and_equivalents: SourcedValue | None = None
    excess_cash: SourcedValue | None = None
    goodwill: SourcedValue | None = None
    non_operating_assets: SourcedValue | None = None
    non_operating_liabilities: SourcedValue | None = None
    shares_outstanding: SourcedValue | None = None

    exceptional_operating_items: SourcedValue | None = None
    non_operating_items: SourcedValue | None = None

    @model_validator(mode="after")
    def validate_identity(self) -> "FinancialPeriod":
        if not self.company_name.strip():
            raise ValueError("company_name must not be empty")
        if not self.currency.strip():
            raise ValueError("currency must not be empty")
        return self

