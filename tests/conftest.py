from datetime import date

import pytest

from fundamental_engine.models import FinancialPeriod, Provenance, SourcedValue


def sv(value: float, label: str = "reported") -> SourcedValue:
    return SourcedValue(value=value, provenance=Provenance(source_label=label))


@pytest.fixture
def previous_period() -> FinancialPeriod:
    return FinancialPeriod(
        company_name="Test Corp",
        ticker="TST",
        fiscal_period_end=date(2023, 12, 31),
        currency="USD",
        ebit=sv(120),
        total_equity=sv(500),
        total_debt=sv(250),
        finance_lease_liabilities=sv(20),
        excess_cash=sv(50),
        goodwill=sv(100),
    )


@pytest.fixture
def current_period() -> FinancialPeriod:
    return FinancialPeriod(
        company_name="Test Corp",
        ticker="TST",
        fiscal_period_end=date(2024, 12, 31),
        currency="USD",
        revenue=sv(1_500),
        ebit=sv(200),
        pretax_income=sv(180),
        income_tax_expense=sv(45),
        cash_taxes=sv(38),
        net_income=sv(140),
        depreciation_and_amortization=sv(40),
        stock_based_compensation=sv(10),
        cash_from_operations=sv(210),
        capital_expenditures=sv(-80),
        change_in_working_capital=sv(15),
        total_equity=sv(600),
        total_debt=sv(200),
        finance_lease_liabilities=sv(25),
        cash_and_equivalents=sv(120),
        excess_cash=sv(60),
        goodwill=sv(110),
        shares_outstanding=sv(100),
        exceptional_operating_items=sv(20),
    )

