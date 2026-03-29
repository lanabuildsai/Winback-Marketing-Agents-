from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


NUMERIC_COLUMNS = [
    "tenure_months",
    "txn_count_90d",
    "txn_count_365d",
    "avg_txn_amount",
    "days_since_last_txn",
    "days_since_last_marketing_touch",
    "prior_campaign_contacts_90d",
    "prior_offer_redemptions_365d",
    "app_sessions_30d",
    "support_tickets_90d",
    "promo_sensitivity",
    "trust_score",
    "price_sensitivity",
    "family_support_sender",
    "education_sender",
    "emergency_sender",
]

CATEGORICAL_COLUMNS = ["corridor", "customer_type"]


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def _encode_frame(
    frame: pd.DataFrame,
    numeric_means: pd.Series | None = None,
    numeric_stds: pd.Series | None = None,
    feature_columns: list[str] | None = None,
) -> tuple[np.ndarray, pd.Series, pd.Series, list[str]]:
    numeric = frame[NUMERIC_COLUMNS].copy()

    if numeric_means is None:
        numeric_means = numeric.mean()
    numeric = numeric.fillna(numeric_means)

    if numeric_stds is None:
        numeric_stds = numeric.std().replace(0, 1.0)
    numeric = (numeric - numeric_means) / numeric_stds.replace(0, 1.0)

    categorical = pd.get_dummies(frame[CATEGORICAL_COLUMNS], dummy_na=False, dtype=float)
    encoded = pd.concat([numeric, categorical], axis=1)

    if feature_columns is None:
        feature_columns = encoded.columns.tolist()
    else:
        encoded = encoded.reindex(columns=feature_columns, fill_value=0.0)

    matrix = encoded.to_numpy(dtype=float)
    intercept = np.ones((len(encoded), 1), dtype=float)
    matrix = np.hstack([intercept, matrix])
    return matrix, numeric_means, numeric_stds, feature_columns


def _roc_auc_score(y_true: np.ndarray, y_score: np.ndarray) -> float:
    order = np.argsort(y_score)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(y_score) + 1)
    positives = y_true == 1
    n_pos = positives.sum()
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    rank_sum = ranks[positives].sum()
    return float((rank_sum - (n_pos * (n_pos + 1) / 2)) / (n_pos * n_neg))


@dataclass
class RiskAgent:
    learning_rate: float = 0.08
    epochs: int = 500
    l2: float = 0.001
    weights: np.ndarray | None = None
    numeric_means: pd.Series | None = None
    numeric_stds: pd.Series | None = None
    feature_columns: list[str] = field(default_factory=list)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "RiskAgent":
        matrix, self.numeric_means, self.numeric_stds, self.feature_columns = _encode_frame(X)
        target = y.to_numpy(dtype=float)
        self.weights = np.zeros(matrix.shape[1], dtype=float)

        for _ in range(self.epochs):
            predictions = _sigmoid(matrix @ self.weights)
            gradient = (matrix.T @ (predictions - target)) / len(target)
            gradient[1:] += self.l2 * self.weights[1:]
            self.weights -= self.learning_rate * gradient

        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if self.weights is None or self.numeric_means is None or self.numeric_stds is None:
            raise ValueError("RiskAgent must be fit before scoring.")
        matrix, _, _, _ = _encode_frame(
            X,
            numeric_means=self.numeric_means,
            numeric_stds=self.numeric_stds,
            feature_columns=self.feature_columns,
        )
        return _sigmoid(matrix @ self.weights)

    def score_auc(self, X: pd.DataFrame, y: pd.Series) -> float:
        return _roc_auc_score(y.to_numpy(dtype=int), self.predict_proba(X))


@dataclass
class ValueAgent:
    ridge_penalty: float = 1.0
    weights: np.ndarray | None = None
    numeric_means: pd.Series | None = None
    numeric_stds: pd.Series | None = None
    feature_columns: list[str] = field(default_factory=list)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "ValueAgent":
        matrix, self.numeric_means, self.numeric_stds, self.feature_columns = _encode_frame(X)
        target = y.to_numpy(dtype=float)
        identity = np.eye(matrix.shape[1], dtype=float)
        identity[0, 0] = 0.0
        self.weights = np.linalg.solve(
            matrix.T @ matrix + self.ridge_penalty * identity,
            matrix.T @ target,
        )
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if self.weights is None or self.numeric_means is None or self.numeric_stds is None:
            raise ValueError("ValueAgent must be fit before scoring.")
        matrix, _, _, _ = _encode_frame(
            X,
            numeric_means=self.numeric_means,
            numeric_stds=self.numeric_stds,
            feature_columns=self.feature_columns,
        )
        return np.maximum(matrix @ self.weights, 0.0)

    def score_mae(self, X: pd.DataFrame, y: pd.Series) -> float:
        prediction = self.predict(X)
        return float(np.mean(np.abs(prediction - y.to_numpy(dtype=float))))


@dataclass
class PolicyAgent:
    high_value_threshold: float

    def recommend(self, scored: pd.DataFrame) -> pd.Series:
        high_value = scored["predicted_future_value_90d"] >= self.high_value_threshold
        high_risk = scored["predicted_churn_risk"] >= 0.50
        medium_risk = scored["predicted_churn_risk"].between(0.30, 0.50, inclusive="left")
        promo_sensitive = scored["promo_sensitivity"] >= 0.58
        high_trust = scored["trust_score"] >= 0.60
        stale = scored["days_since_last_txn"] >= 45
        fatigued = scored["prior_campaign_contacts_90d"] >= 5

        actions = np.select(
            [
                fatigued & ~high_value,
                (high_risk | medium_risk) & high_value & promo_sensitive & stale,
                high_risk & high_value & ~promo_sensitive,
                medium_risk & stale & high_trust,
                medium_risk | stale,
            ],
            [
                "suppress",
                "limited_offer",
                "trust_message",
                "trust_message",
                "timing_nudge",
            ],
            default="suppress",
        )
        return pd.Series(actions, index=scored.index, name="recommended_action")


@dataclass
class EvaluationAgent:
    action_costs: dict[str, float]
    holdout_rate: float = 0.10
    seed: int = 42

    def evaluate(self, scored: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
        rng = np.random.default_rng(self.seed)
        evaluation = scored.copy()
        evaluation["holdout"] = rng.random(len(evaluation)) < self.holdout_rate
        evaluation["applied_action"] = np.where(
            evaluation["holdout"],
            "suppress",
            evaluation["recommended_action"],
        )

        probability_lookup = {
            "suppress": "response_prob_suppress",
            "trust_message": "response_prob_trust_message",
            "timing_nudge": "response_prob_timing_nudge",
            "limited_offer": "response_prob_limited_offer",
        }
        probability_columns = evaluation["applied_action"].map(probability_lookup)
        evaluation["response_probability"] = [
            evaluation.at[idx, column_name]
            for idx, column_name in zip(evaluation.index, probability_columns)
        ]
        evaluation["reactivated"] = (
            rng.random(len(evaluation)) < evaluation["response_probability"]
        ).astype(int)
        evaluation["incremental_transactions"] = np.where(
            evaluation["reactivated"] == 1,
            np.maximum(1, np.round(evaluation["predicted_future_value_90d"] / 250)).astype(int),
            0,
        )
        evaluation["gross_value"] = np.where(
            evaluation["reactivated"] == 1,
            evaluation["predicted_future_value_90d"] * 0.35,
            0.0,
        )
        evaluation["action_cost"] = evaluation["applied_action"].map(self.action_costs)
        evaluation["net_contribution"] = evaluation["gross_value"] - evaluation["action_cost"]

        treatment = evaluation[~evaluation["holdout"]]
        control = evaluation[evaluation["holdout"]]

        metrics = {
            "risk_model_auc": round(float(scored["risk_model_auc"].iloc[0]), 4),
            "value_model_mae": round(float(scored["value_model_mae"].iloc[0]), 2),
            "treatment_reactivation_rate": round(float(treatment["reactivated"].mean()), 4),
            "control_reactivation_rate": round(float(control["reactivated"].mean()), 4),
            "incremental_reactivation_lift": round(
                float(treatment["reactivated"].mean() - control["reactivated"].mean()), 4
            ),
            "treatment_avg_net_contribution": round(float(treatment["net_contribution"].mean()), 2),
            "control_avg_net_contribution": round(float(control["net_contribution"].mean()), 2),
            "total_expected_net_contribution": round(float(evaluation["net_contribution"].sum()), 2),
        }
        return evaluation, metrics
