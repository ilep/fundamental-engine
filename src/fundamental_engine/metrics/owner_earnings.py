from __future__ import annotations

from fundamental_engine.metrics._helpers import value
from fundamental_engine.models import (
    Confidence,
    FinancialPeriod,
    MaintenanceCapexPolicy,
    MetricResult,
    RangeResult,
)


def _base_cash_earnings(period: FinancialPeriod) -> tuple[float, dict[str, float]]:
    net_income = value(period.net_income, "net_income")
    da = value(period.depreciation_and_amortization, "depreciation_and_amortization")
    sbc = period.stock_based_compensation.value if period.stock_based_compensation else 0.0
    working_capital = (
        period.change_in_working_capital.value if period.change_in_working_capital else 0.0
    )
    exceptional = (
        period.exceptional_operating_items.value if period.exceptional_operating_items else 0.0
    )
    base = net_income + da + sbc - working_capital - exceptional
    return base, {
        "net_income": net_income,
        "depreciation_and_amortization": da,
        "stock_based_compensation": sbc,
        "change_in_working_capital": working_capital,
        "exceptional_operating_items": exceptional,
    }


def calculate_owner_earnings(
    period: FinancialPeriod,
    *,
    maintenance_capex_policy: MaintenanceCapexPolicy | str = MaintenanceCapexPolicy.SCENARIO_RANGE,
    explicit_maintenance_capex: float | None = None,
    low_maintenance_ratio: float = 0.5,
    base_maintenance_ratio: float = 0.75,
    high_maintenance_ratio: float = 1.0,
) -> MetricResult | RangeResult:
    policy = MaintenanceCapexPolicy(maintenance_capex_policy)
    base_cash, inputs = _base_cash_earnings(period)
    total_capex = abs(value(period.capital_expenditures, "capital_expenditures"))

    if policy == MaintenanceCapexPolicy.TOTAL_CAPEX:
        maintenance = total_capex
        assumption = "maintenance capex equals total capex"
    elif policy == MaintenanceCapexPolicy.DEPRECIATION_PROXY:
        maintenance = value(period.depreciation_and_amortization, "depreciation_and_amortization")
        assumption = "maintenance capex equals D&A"
    elif policy == MaintenanceCapexPolicy.EXPLICIT:
        if explicit_maintenance_capex is None or explicit_maintenance_capex < 0:
            raise ValueError("explicit_maintenance_capex must be a non-negative number")
        maintenance = explicit_maintenance_capex
        assumption = "maintenance capex supplied explicitly"
    else:
        ratios = (low_maintenance_ratio, base_maintenance_ratio, high_maintenance_ratio)
        if not all(0 <= ratio <= 1 for ratio in ratios):
            raise ValueError("Maintenance-capex ratios must be between 0 and 1")
        if not low_maintenance_ratio <= base_maintenance_ratio <= high_maintenance_ratio:
            raise ValueError("Maintenance-capex ratios must be ordered low <= base <= high")
        # Higher maintenance capex produces lower owner earnings.
        return RangeResult(
            metric="owner_earnings",
            low=base_cash - total_capex * high_maintenance_ratio,
            base=base_cash - total_capex * base_maintenance_ratio,
            high=base_cash - total_capex * low_maintenance_ratio,
            formula="net income + D&A + SBC - required working capital - exceptional items - maintenance capex",
            assumptions=[
                f"maintenance capex scenarios={ratios} of total capex",
                "SBC is added back as non-cash; review dilution separately",
            ],
            warnings=["Maintenance capex is estimated rather than directly observed"],
            confidence=Confidence.LOW,
        )

    inputs["maintenance_capex"] = maintenance
    warnings = ["SBC add-back should be reviewed together with dilution"] if inputs["stock_based_compensation"] else []
    return MetricResult(
        metric="owner_earnings",
        value=base_cash - maintenance,
        formula="net income + D&A + SBC - required working capital - exceptional items - maintenance capex",
        inputs=inputs,
        assumptions=[assumption],
        warnings=warnings,
        confidence=Confidence.MEDIUM,
    )

