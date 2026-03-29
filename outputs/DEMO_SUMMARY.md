# Demo Summary

## What the Demo Shows

The demo runs a complete winback decision workflow:

1. generate lifecycle data
2. score churn risk
3. estimate customer value
4. recommend a next best action
5. simulate a holdout evaluation
6. produce business-facing outputs

## Key Results

- Risk model AUC: `0.7475`
- Value model MAE: `286.74`
- Treatment reactivation rate: `18.29%`
- Control reactivation rate: `4.24%`
- Incremental reactivation lift: `14.05%`
- Total expected net contribution: `$137438.36`

## Output Files

- `outputs/scored_customers.csv`
- `outputs/action_summary.csv`
- `outputs/metrics.csv`
- `outputs/charts/action_mix.png`
- `outputs/charts/risk_value_matrix.png`
- `outputs/charts/holdout_lift.png`
- `outputs/BUSINESS_CASE.md`
