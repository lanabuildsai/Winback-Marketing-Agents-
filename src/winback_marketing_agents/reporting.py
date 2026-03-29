from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_business_case(
    metrics: dict[str, float],
    action_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_table = action_summary.reset_index().to_markdown(index=False)

    content = f"""# Business Case

## Executive Summary

This project simulates a lifecycle marketing winback engine for a remittance-like business. Instead of treating all inactive customers the same, it combines churn risk, expected value, next best action, and holdout-style evaluation to support more disciplined re-engagement decisions.

## Problem

Traditional retention programs often over-message customers, overuse incentives, and evaluate success on response instead of incremental business impact. That makes it difficult to understand:

- which customers are truly worth winning back
- when a trust or timing message is better than an offer
- whether the program is actually generating profitable reactivation

## Proposed Approach

The system uses four lightweight components:

1. `RiskAgent` to estimate lapse risk
2. `ValueAgent` to estimate expected future value
3. `PolicyAgent` to recommend the next best action
4. `EvaluationAgent` to simulate holdout-style business measurement

## Outcome Highlights

- Risk model AUC: **{metrics["risk_model_auc"]:.4f}**
- Value model MAE: **{metrics["value_model_mae"]:.2f}**
- Treatment reactivation rate: **{metrics["treatment_reactivation_rate"]:.2%}**
- Control reactivation rate: **{metrics["control_reactivation_rate"]:.2%}**
- Incremental reactivation lift: **{metrics["incremental_reactivation_lift"]:.2%}**
- Treatment average net contribution: **${metrics["treatment_avg_net_contribution"]:.2f}**
- Total expected net contribution: **${metrics["total_expected_net_contribution"]:.2f}**

## Recommended Action Summary

{summary_table}

## How A Business Team Could Use This

- Prioritize high-value winback targets instead of contacting everyone
- Reduce unnecessary promo spend
- Route customers toward trust, timing, or offer strategies based on context
- Give Finance and lifecycle leadership a clearer view of expected net contribution
- Create a starting point for more advanced uplift or next-best-action systems

## Where This Fits

This approach is especially relevant for:

- remittances and money movement
- digital wallets and fintech
- subscription or membership retention
- e-commerce reactivation
- CRM and lifecycle marketing experimentation

## Next Steps

- Replace the synthetic dataset with a real marketing or churn dataset
- Add segment-specific business rules by corridor or customer type
- Expand from policy rules to uplift modeling
- Add a lightweight dashboard or app for non-technical stakeholders
"""
    (output_dir / "BUSINESS_CASE.md").write_text(content)


def write_demo_summary(
    metrics: dict[str, float],
    output_dir: Path,
) -> None:
    content = f"""# Demo Summary

## What the Demo Shows

The demo runs a complete winback decision workflow:

1. generate lifecycle data
2. score churn risk
3. estimate customer value
4. recommend a next best action
5. simulate a holdout evaluation
6. produce business-facing outputs

## Key Results

- Risk model AUC: `{metrics["risk_model_auc"]:.4f}`
- Value model MAE: `{metrics["value_model_mae"]:.2f}`
- Treatment reactivation rate: `{metrics["treatment_reactivation_rate"]:.2%}`
- Control reactivation rate: `{metrics["control_reactivation_rate"]:.2%}`
- Incremental reactivation lift: `{metrics["incremental_reactivation_lift"]:.2%}`
- Total expected net contribution: `${metrics["total_expected_net_contribution"]:.2f}`

## Output Files

- `outputs/scored_customers.csv`
- `outputs/action_summary.csv`
- `outputs/metrics.csv`
- `outputs/charts/action_mix.png`
- `outputs/charts/risk_value_matrix.png`
- `outputs/charts/holdout_lift.png`
- `outputs/BUSINESS_CASE.md`
"""
    (output_dir / "DEMO_SUMMARY.md").write_text(content)
