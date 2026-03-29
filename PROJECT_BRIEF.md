# Project Brief

## Title

**Winback Marketing Agents**

## Short Description

A lightweight lifecycle marketing decision engine that predicts lapse risk, estimates customer value, recommends next best action, and evaluates expected winback impact through a holdout-style framework.

## Business Context

Most retention programs do not fail because teams lack campaigns. They fail because teams lack decision structure.

Common problems:

- all inactive customers are treated the same
- incentives are used too broadly
- response is confused with incremental value
- lifecycle strategy is hard to connect to profit

This project is designed to show what a more disciplined winback system can look like.

## What The System Does

The project combines four simple components:

- **RiskAgent**
  - predicts lapse / churn risk
- **ValueAgent**
  - estimates expected 90-day customer value
- **PolicyAgent**
  - recommends the best action for each customer
- **EvaluationAgent**
  - simulates holdout-style measurement to estimate business impact

## Recommended Actions

The policy layer currently assigns:

- `suppress`
- `trust_message`
- `timing_nudge`
- `limited_offer`

This is intentional. A useful lifecycle system should not default to “send an offer to everyone.”

## Why It Matters

This type of decision engine helps a business:

- target high-value reactivation opportunities more effectively
- reduce wasted spend on low-propensity or low-value customers
- test actions in a more structured way
- connect lifecycle strategy to revenue and net contribution
- create a bridge between ML prediction and marketing execution

## Example Use Cases

- remittance and money transfer products
- fintech and digital wallets
- CRM and lifecycle marketing teams
- subscription retention teams
- e-commerce reactivation
- growth teams building next-best-action systems

## Portfolio Value

This is a strong portfolio project because it demonstrates:

- business framing
- lifecycle strategy thinking
- lightweight ML implementation
- next-best-action policy design
- incrementality-oriented evaluation

## Suggested GitHub Repo Description

Agent-style lifecycle marketing project that predicts churn risk, estimates customer value, recommends next best action, and evaluates expected winback impact through a holdout-style framework.

## Suggested Resume / Portfolio Blurb

Built a GitHub project simulating a winback decision engine for lifecycle marketing, combining churn risk, customer value, action policy, and holdout-style business evaluation to support more profitable re-engagement decisions.
