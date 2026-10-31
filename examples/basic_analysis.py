from datetime import date

from fundamental_engine import (
    FinancialPeriod,
    Provenance,
    SourcedValue,
    calculate_invested_capital,
    calculate_nopat,
    calculate_owner_earnings,
    calculate_roic,
)


def reported(value: float, label: str) -> SourcedValue:
    return SourcedValue(value=value, provenance=Provenance(source_label=label))


previous = FinancialPeriod(
    company_name="Example Corp",
    ticker="EXM",
    fiscal_period_end=date(2024, 12, 31),
    currency="USD",
    total_equity=reported(600, "Total equity"),
    total_debt=reported(250, "Total debt"),
    excess_cash=reported(50, "Excess cash"),
)

current = FinancialPeriod(
    company_name="Example Corp",
    ticker="EXM",
    fiscal_period_end=date(2025, 12, 31),
    currency="USD",
    ebit=reported(180, "EBIT"),
    net_income=reported(125, "Net income"),
    depreciation_and_amortization=reported(35, "D&A"),
    capital_expenditures=reported(-50, "Capital expenditures"),
    total_equity=reported(680, "Total equity"),
    total_debt=reported(220, "Total debt"),
    excess_cash=reported(70, "Excess cash"),
)

nopat = calculate_nopat(current, normalized_tax_rate=0.25)
capital = calculate_invested_capital(current, previous)
roic = calculate_roic(nopat, capital)
owner_earnings = calculate_owner_earnings(current)

print(nopat.model_dump_json(indent=2))
print(capital.model_dump_json(indent=2))
print(roic.model_dump_json(indent=2))
print(owner_earnings.model_dump_json(indent=2))

