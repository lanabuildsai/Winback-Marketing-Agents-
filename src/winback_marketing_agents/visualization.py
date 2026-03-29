from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


COLORS = {
    "trust_message": "#1f6feb",
    "timing_nudge": "#2da44e",
    "limited_offer": "#d97706",
    "suppress": "#6e7781",
}


def create_charts(evaluation: pd.DataFrame, metrics: dict[str, float], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _plot_action_mix(evaluation, output_dir / "action_mix.png")
    _plot_value_vs_risk(evaluation, output_dir / "risk_value_matrix.png")
    _plot_holdout_comparison(metrics, output_dir / "holdout_lift.png")


def _plot_action_mix(evaluation: pd.DataFrame, path: Path) -> None:
    summary = (
        evaluation.groupby("recommended_action")
        .size()
        .sort_values(ascending=False)
    )
    colors = [COLORS.get(action, "#999999") for action in summary.index]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(summary.index, summary.values, color=colors)
    ax.set_title("Recommended Action Mix")
    ax.set_ylabel("Customers")
    ax.set_xlabel("Action")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 8, f"{int(height)}", ha="center")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_value_vs_risk(evaluation: pd.DataFrame, path: Path) -> None:
    sampled = evaluation.sample(min(1200, len(evaluation)), random_state=42)
    colors = sampled["recommended_action"].map(COLORS).fillna("#999999")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        sampled["predicted_churn_risk"],
        sampled["predicted_future_value_90d"],
        c=colors,
        alpha=0.6,
        s=20,
    )
    ax.set_title("Risk vs. Value by Recommended Action")
    ax.set_xlabel("Predicted Churn Risk")
    ax.set_ylabel("Predicted 90-Day Value")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_holdout_comparison(metrics: dict[str, float], path: Path) -> None:
    labels = ["Control", "Treatment"]
    values = [
        metrics["control_reactivation_rate"],
        metrics["treatment_reactivation_rate"],
    ]
    colors = ["#6e7781", "#1f6feb"]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Reactivation Rate: Holdout vs Treatment")
    ax.set_ylabel("Rate")
    ax.set_ylim(0, max(values) * 1.3)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.005, f"{value:.1%}", ha="center")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
