from datetime import date

from fundamental_engine.adapters import from_ai_fund, from_eod


def metric(value, label):
    return {
        "status": "reported",
        "value_raw": value,
        "numeric_value": value,
        "source_label": label,
        "page_number": 42,
        "verbatim_extract": f"{label}: {value}",
    }


def test_ai_fund_adapter_preserves_provenance():
    period = from_ai_fund(
        {
            "company_name": "Adapter Corp",
            "fiscal_period_end": "2024-12-31",
            "reporting_currency": "USD",
            "income_statement_universal": {
                "revenue": metric(1_000, "Revenue"),
                "operating_income": metric(120, "Operating income"),
            },
            "cash_flow_statement_universal": {
                "cash_from_operations": metric(160, "Operating cash flow"),
                "capital_expenditures": metric(-50, "Capital expenditures"),
            },
        },
        ticker="ADC",
        source_document="annual-report.pdf",
    )
    assert period.revenue.value == 1_000
    assert period.revenue.provenance.page_number == 42
    assert period.operating_income.value == 120
    assert period.cash_from_operations.value == 160
    assert period.capital_expenditures.value == -50


def test_eod_adapter_maps_one_period():
    payload = {
        "General": {"Name": "EOD Corp", "Code": "EOD"},
        "Financials": {
            "Income_Statement": {
                "yearly": {
                    "2024-12-31": {
                        "totalRevenue": "1000",
                        "ebit": "150",
                        "netIncome": "100",
                    }
                }
            },
            "Cash_Flow": {"yearly": {"2024-12-31": {"capitalExpenditures": "-50"}}},
            "Balance_Sheet": {
                "yearly": {
                    "2024-12-31": {
                        "totalStockholderEquity": "500",
                        "shortLongTermDebtTotal": "200",
                        "cash": "80",
                    }
                }
            },
        },
    }
    period = from_eod(payload, fiscal_period_end=date(2024, 12, 31), currency="USD")
    assert period.ebit.value == 150
    assert period.total_debt.value == 200
    assert period.capital_expenditures.value == -50

