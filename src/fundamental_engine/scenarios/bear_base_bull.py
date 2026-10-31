from __future__ import annotations

from collections.abc import Sequence

from fundamental_engine.models import Scenario, ScenarioResult


def evaluate_scenarios(scenarios: Sequence[Scenario]) -> list[ScenarioResult]:
    if not scenarios:
        raise ValueError("At least one scenario is required")
    names = [scenario.name.lower() for scenario in scenarios]
    if len(names) != len(set(names)):
        raise ValueError("Scenario names must be unique")

    results: list[ScenarioResult] = []
    for scenario in scenarios:
        if scenario.cost_of_capital <= scenario.growth_rate:
            raise ValueError(f"Cost of capital must exceed growth in scenario {scenario.name}")
        enterprise = scenario.normalized_nopat / (
            scenario.cost_of_capital - scenario.growth_rate
        )
        equity = enterprise + scenario.net_non_operating_assets - scenario.net_debt
        per_share = equity / scenario.shares_outstanding if scenario.shares_outstanding else None
        results.append(
            ScenarioResult(
                name=scenario.name,
                enterprise_value=enterprise,
                equity_value=equity,
                per_share_value=per_share,
                assumptions=[
                    f"normalized_nopat={scenario.normalized_nopat}",
                    f"cost_of_capital={scenario.cost_of_capital}",
                    f"growth_rate={scenario.growth_rate}",
                ],
            )
        )
    return results

