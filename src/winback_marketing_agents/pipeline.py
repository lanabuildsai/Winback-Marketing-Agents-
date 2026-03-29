from __future__ import annotations

from pathlib import Path

import pandas as pd

from .agents import EvaluationAgent, PolicyAgent, RiskAgent, ValueAgent
from .data import ACTION_COSTS, generate_synthetic_winback_dataset
from .reporting import write_business_case, write_demo_summary
from .visualization import create_charts


def _train_test_split(
    X: pd.DataFrame,
    y_risk: pd.Series,
    y_value: pd.Series,
    test_size: float = 0.30,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
    shuffled = X.copy()
    shuffled["_risk"] = y_risk
    shuffled["_value"] = y_value
    shuffled = shuffled.sample(frac=1.0, random_state=seed)

    split_index = int(len(shuffled) * (1 - test_size))
    train = shuffled.iloc[:split_index].copy()
    test = shuffled.iloc[split_index:].copy()

    X_train = train.drop(columns=["_risk", "_value"])
    X_test = test.drop(columns=["_risk", "_value"])
    y_risk_train = train["_risk"]
    y_risk_test = test["_risk"]
    y_value_train = train["_value"]
    y_value_test = test["_value"]
    return X_train, X_test, y_risk_train, y_risk_test, y_value_train, y_value_test


def run_demo_pipeline(output_dir: Path) -> dict[str, float]:
    output_dir.mkdir(parents=True, exist_ok=True)
    charts_dir = output_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    bundle = generate_synthetic_winback_dataset()
    dataset = bundle.features.merge(bundle.labels, on="customer_id", how="inner")

    feature_columns = bundle.features.columns.drop("customer_id").tolist()
    X = dataset[feature_columns]
    y_risk = dataset["churned_next_90d"]
    y_value = dataset["future_value_90d"]

    X_train, X_test, y_risk_train, y_risk_test, y_value_train, y_value_test = _train_test_split(
        X,
        y_risk,
        y_value,
        test_size=0.30,
        seed=42,
    )

    risk_agent = RiskAgent().fit(X_train, y_risk_train)
    value_agent = ValueAgent().fit(X_train, y_value_train)

    risk_auc = risk_agent.score_auc(X_test, y_risk_test)
    value_mae = value_agent.score_mae(X_test, y_value_test)

    scored = X_test.copy()
    scored["predicted_churn_risk"] = risk_agent.predict_proba(X_test)
    scored["predicted_future_value_90d"] = value_agent.predict(X_test)
    scored["risk_model_auc"] = risk_auc
    scored["value_model_mae"] = value_mae

    policy_agent = PolicyAgent(high_value_threshold=float(scored["predicted_future_value_90d"].quantile(0.65)))
    scored["recommended_action"] = policy_agent.recommend(scored)

    full_test = scored.reset_index(drop=True).copy()
    label_columns = [
        "response_prob_trust_message",
        "response_prob_timing_nudge",
        "response_prob_limited_offer",
        "response_prob_suppress",
        "true_best_action",
    ]
    full_test = pd.concat(
        [
            full_test,
            dataset.loc[X_test.index, label_columns].reset_index(drop=True),
        ],
        axis=1,
    )

    evaluator = EvaluationAgent(action_costs=ACTION_COSTS)
    evaluation, metrics = evaluator.evaluate(full_test)

    action_summary = (
        evaluation.groupby("recommended_action")
        .agg(
            customers=("recommended_action", "size"),
            avg_risk=("predicted_churn_risk", "mean"),
            avg_value=("predicted_future_value_90d", "mean"),
            reactivation_rate=("reactivated", "mean"),
            avg_net_contribution=("net_contribution", "mean"),
        )
        .sort_values("customers", ascending=False)
        .round(4)
    )

    evaluation.to_csv(output_dir / "scored_customers.csv", index=False)
    action_summary.to_csv(output_dir / "action_summary.csv")
    pd.DataFrame([metrics]).to_csv(output_dir / "metrics.csv", index=False)
    create_charts(evaluation, metrics, charts_dir)
    write_business_case(metrics, action_summary, output_dir)
    write_demo_summary(metrics, output_dir)

    return metrics
