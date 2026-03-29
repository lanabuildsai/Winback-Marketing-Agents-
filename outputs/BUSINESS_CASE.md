# Business Case

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

- Risk model AUC: **0.7475**
- Value model MAE: **286.74**
- Treatment reactivation rate: **18.29%**
- Control reactivation rate: **4.24%**
- Incremental reactivation lift: **14.05%**
- Treatment average net contribution: **$81.75**
- Total expected net contribution: **$137438.36**

## Recommended Action Summary

| recommended_action   |   customers |   avg_risk |   avg_value |   reactivation_rate |   avg_net_contribution |
|:---------------------|------------:|-----------:|------------:|--------------------:|-----------------------:|
| timing_nudge         |         865 |     0.2396 |    1190.27  |              0.2231 |               108.313  |
| suppress             |         707 |     0.2405 |     965.733 |              0.0509 |                24.0623 |
| trust_message        |         203 |     0.3905 |     890.292 |              0.335  |               106.097  |
| limited_offer        |          25 |     0.4148 |    1672.86  |              0.36   |               207.912  |

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
