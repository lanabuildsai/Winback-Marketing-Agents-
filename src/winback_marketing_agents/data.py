from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


ACTION_COSTS = {
    "suppress": 0.0,
    "trust_message": 0.15,
    "timing_nudge": 0.10,
    "limited_offer": 6.00,
}


@dataclass(frozen=True)
class DatasetBundle:
    features: pd.DataFrame
    labels: pd.DataFrame


def generate_synthetic_winback_dataset(
    n_customers: int = 6000,
    seed: int = 42,
) -> DatasetBundle:
    rng = np.random.default_rng(seed)

    customer_id = np.arange(1, n_customers + 1)
    corridor = rng.choice(
        ["LATAM", "South Asia", "Africa", "Eastern Europe", "Middle East"],
        size=n_customers,
        p=[0.22, 0.25, 0.16, 0.18, 0.19],
    )
    customer_type = rng.choice(
        ["family_support", "education", "emergency", "property", "mixed"],
        size=n_customers,
        p=[0.42, 0.18, 0.15, 0.08, 0.17],
    )
    tenure_months = rng.integers(1, 61, size=n_customers)
    txn_count_90d = rng.poisson(lam=2.8, size=n_customers)
    txn_count_365d = np.maximum(txn_count_90d + rng.poisson(lam=7.0, size=n_customers), 1)
    avg_txn_amount = rng.normal(loc=310, scale=120, size=n_customers).clip(25, 1200)
    days_since_last_txn = rng.integers(1, 180, size=n_customers)
    days_since_last_marketing_touch = rng.integers(0, 60, size=n_customers)
    prior_campaign_contacts_90d = rng.integers(0, 7, size=n_customers)
    prior_offer_redemptions_365d = rng.integers(0, 5, size=n_customers)
    app_sessions_30d = rng.poisson(lam=8.0, size=n_customers)
    support_tickets_90d = rng.poisson(lam=0.6, size=n_customers)
    promo_sensitivity = rng.beta(a=2.2, b=3.2, size=n_customers)
    trust_score = rng.beta(a=3.4, b=1.9, size=n_customers)
    price_sensitivity = rng.beta(a=2.5, b=2.5, size=n_customers)
    send_frequency_score = np.clip(txn_count_90d / 6.0, 0, 1)

    family_support = (customer_type == "family_support").astype(int)
    education_sender = (customer_type == "education").astype(int)
    emergency_sender = (customer_type == "emergency").astype(int)

    raw_risk_score = (
        0.85 * (days_since_last_txn / 180.0)
        + 0.35 * (prior_campaign_contacts_90d / 6.0)
        + 0.20 * (support_tickets_90d / 4.0)
        - 0.45 * send_frequency_score
        - 0.30 * trust_score
        - 0.18 * (app_sessions_30d / 20.0)
        - 0.12 * (prior_offer_redemptions_365d / 4.0)
        + 0.10 * emergency_sender
    )

    churn_probability = 1 / (1 + np.exp(-(raw_risk_score - 0.55) * 2.8))
    churned_next_90d = rng.binomial(1, churn_probability)

    base_future_value = (
        avg_txn_amount
        * np.maximum(txn_count_90d, 1)
        * (1.1 + 0.5 * family_support + 0.3 * education_sender)
        * (1 - 0.55 * churned_next_90d)
    )
    future_value_90d = np.maximum(base_future_value + rng.normal(0, 80, size=n_customers), 0)

    response_trust = np.clip(
        0.10
        + 0.38 * trust_score
        + 0.15 * family_support
        - 0.18 * churned_next_90d
        - 0.08 * (days_since_last_marketing_touch < 10).astype(int),
        0.0,
        0.95,
    )
    response_timing = np.clip(
        0.08
        + 0.40 * (((days_since_last_txn >= 20) & (days_since_last_txn <= 75)).astype(int))
        + 0.12 * emergency_sender
        + 0.10 * send_frequency_score
        - 0.10 * (prior_campaign_contacts_90d > 4).astype(int),
        0.0,
        0.95,
    )
    response_offer = np.clip(
        0.06
        + 0.45 * promo_sensitivity
        + 0.15 * price_sensitivity
        + 0.10 * (days_since_last_txn > 45).astype(int)
        - 0.12 * (prior_offer_redemptions_365d > 2).astype(int),
        0.0,
        0.95,
    )

    no_contact_prob = np.clip(0.02 + 0.08 * send_frequency_score - 0.20 * churned_next_90d, 0.0, 0.35)

    best_action = np.select(
        [
            (future_value_90d > np.quantile(future_value_90d, 0.7)) & (response_offer > response_trust) & (promo_sensitivity > 0.55),
            response_trust >= np.maximum(response_timing, response_offer),
            response_timing > response_offer,
        ],
        ["limited_offer", "trust_message", "timing_nudge"],
        default="suppress",
    )

    features = pd.DataFrame(
        {
            "customer_id": customer_id,
            "corridor": corridor,
            "customer_type": customer_type,
            "tenure_months": tenure_months,
            "txn_count_90d": txn_count_90d,
            "txn_count_365d": txn_count_365d,
            "avg_txn_amount": avg_txn_amount.round(2),
            "days_since_last_txn": days_since_last_txn,
            "days_since_last_marketing_touch": days_since_last_marketing_touch,
            "prior_campaign_contacts_90d": prior_campaign_contacts_90d,
            "prior_offer_redemptions_365d": prior_offer_redemptions_365d,
            "app_sessions_30d": app_sessions_30d,
            "support_tickets_90d": support_tickets_90d,
            "promo_sensitivity": promo_sensitivity.round(4),
            "trust_score": trust_score.round(4),
            "price_sensitivity": price_sensitivity.round(4),
            "family_support_sender": family_support,
            "education_sender": education_sender,
            "emergency_sender": emergency_sender,
        }
    )

    labels = pd.DataFrame(
        {
            "customer_id": customer_id,
            "churned_next_90d": churned_next_90d,
            "future_value_90d": future_value_90d.round(2),
            "response_prob_trust_message": response_trust.round(4),
            "response_prob_timing_nudge": response_timing.round(4),
            "response_prob_limited_offer": response_offer.round(4),
            "response_prob_suppress": no_contact_prob.round(4),
            "true_best_action": best_action,
        }
    )

    return DatasetBundle(features=features, labels=labels)
