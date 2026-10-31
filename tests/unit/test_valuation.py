import pytest

from fundamental_engine.models import Scenario
from fundamental_engine.scenarios import evaluate_scenarios
from fundamental_engine.valuation import (
    calculate_dcf,
    calculate_earnings_multiple_value,
    calculate_epv,
    calculate_margin_of_safety,
)


def test_strict_epv():
    result = calculate_epv(90, cost_of_capital=0.09, net_debt=100)
    assert result.value == pytest.approx(900)


def test_dcf():
    result = calculate_dcf([100, 105, 110], discount_rate=0.10, terminal_growth_rate=0.02)
    assert result.value > 1_000


def test_multiple_value_and_margin_of_safety():
    fair = calculate_earnings_multiple_value(100, multiple=12)
    margin = calculate_margin_of_safety(fair, 900)
    assert margin.value == pytest.approx(0.25)


def test_scenarios():
    results = evaluate_scenarios(
        [
            Scenario(name="bear", normalized_nopat=70, cost_of_capital=0.11, shares_outstanding=100),
            Scenario(name="base", normalized_nopat=90, cost_of_capital=0.09, shares_outstanding=100),
            Scenario(name="bull", normalized_nopat=110, cost_of_capital=0.08, shares_outstanding=100),
        ]
    )
    assert [result.name for result in results] == ["bear", "base", "bull"]
    assert results[0].per_share_value < results[1].per_share_value < results[2].per_share_value


def test_growth_must_be_below_discount_rate():
    with pytest.raises(ValueError):
        calculate_epv(100, cost_of_capital=0.08, growth_rate=0.08)

