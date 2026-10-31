import pytest

from fundamental_engine.metrics import (
    calculate_cfo_fcf,
    calculate_fcff,
    calculate_incremental_roic,
    calculate_invested_capital,
    calculate_nopat,
    calculate_owner_earnings,
    calculate_roic,
)
from fundamental_engine.models import MaintenanceCapexPolicy, RangeResult


def test_nopat_normalizes_exceptional_items(current_period):
    result = calculate_nopat(current_period, normalized_tax_rate=0.25)
    assert result.value == pytest.approx(135.0)
    assert result.inputs["exceptional_operating_items"] == 20


def test_nopat_effective_tax(current_period):
    result = calculate_nopat(current_period, tax_policy="effective")
    assert result.value == pytest.approx(135.0)


def test_average_invested_capital(current_period, previous_period):
    result = calculate_invested_capital(current_period, previous_period)
    # Current 600 + 200 + 25 - 60 = 765; previous 500 + 250 + 20 - 50 = 720.
    assert result.value == pytest.approx(742.5)


def test_excluding_goodwill(current_period, previous_period):
    result = calculate_invested_capital(
        current_period, previous_period, goodwill_policy="exclude"
    )
    assert result.value == pytest.approx((655 + 620) / 2)


def test_roic(current_period, previous_period):
    nopat = calculate_nopat(current_period, normalized_tax_rate=0.25)
    capital = calculate_invested_capital(current_period, previous_period)
    assert calculate_roic(nopat, capital).value == pytest.approx(135 / 742.5)


def test_incremental_roic():
    result = calculate_incremental_roic(150, 120, 800, 700)
    assert result.value == pytest.approx(0.30)


def test_cash_flow_metrics(current_period):
    assert calculate_cfo_fcf(current_period).value == 130
    assert calculate_fcff(135, 50).value == 85


def test_owner_earnings_range(current_period):
    result = calculate_owner_earnings(current_period)
    assert isinstance(result, RangeResult)
    # Base cash earnings = 140 + 40 + 10 - 15 - 20 = 155.
    assert result.low == 75
    assert result.base == 95
    assert result.high == 115


def test_owner_earnings_explicit(current_period):
    result = calculate_owner_earnings(
        current_period,
        maintenance_capex_policy=MaintenanceCapexPolicy.EXPLICIT,
        explicit_maintenance_capex=55,
    )
    assert result.value == 100


def test_average_capital_requires_previous(current_period):
    with pytest.raises(ValueError, match="previous period"):
        calculate_invested_capital(current_period)

