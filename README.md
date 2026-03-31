# Winback Marketing Agents

An interview-ready machine learning project that mirrors the type of problem User Centric companies are solving: who is likely to lapse, who is worth winning back, what action should be recommended, and whether the intervention is incrementally profitable.

The project is intentionally framed as a marketing and lifecycle decision system, not just a churn model.

## Business Problem

Many retention and winback programs are still managed with broad audience rules and shallow success metrics. Teams often:

- contact all inactive customers the same way
- overuse offers to drive short-term response
- measure opens, clicks, or gross conversions instead of incremental value

That creates a predictable set of business problems:

- high-value and low-value customers get treated the same
- promo spend gets wasted on users with weak return potential
- teams cannot clearly separate response from true lift
- lifecycle decisions become hard to explain to Finance and leadership

This project demonstrates a more disciplined alternative: combine churn risk, customer value, next best action, and holdout-style evaluation in one lightweight decision system.

## Agent Design

The repo uses a lightweight agent pattern:

- `RiskAgent`: predicts churn / lapse risk
- `ValueAgent`: estimates 90-day customer value
- `PolicyAgent`: recommends the next best action
- `EvaluationAgent`: simulates holdout measurement and expected profit

## What This Project Does

- Generates a synthetic remittance-like lifecycle dataset out of the box
- Trains a `RiskAgent` to predict lapse / churn risk
- Trains a `ValueAgent` to estimate 90-day future value
- Uses a `PolicyAgent` to recommend a next best action:
  - `suppress`
  - `trust_message`
  - `timing_nudge`
  - `limited_offer`
- Uses an `EvaluationAgent` to simulate holdout measurement and estimate:
  - reactivation rate
  - incremental transactions
  - incremental revenue
  - incentive cost
  - net contribution

## Why It Is Relevant

This project is designed to sound and behave like a small-scale version of a winback growth engine:

- separate churn risk from customer value
- avoid sending offers to everyone
- choose different actions for different lifecycle states
- measure expected impact with a holdout-style framework
- create a closed loop between model outputs and lifecycle execution

## Business Outcomes

This type of system is designed to support outcomes like:

- increasing reactivation of high-value customers
- improving lifecycle relevance by matching actions to customer context
- reducing unnecessary incentive spend
- prioritizing trust or timing messages when offers are not justified
- giving CRM and lifecycle teams a more structured targeting framework
- creating a more defensible retention story for Finance and leadership

## Where This Could Be Used

This project is most relevant for businesses with repeat customer behavior and meaningful retention economics, including:

- remittances and cross-border payments
- digital wallets and fintech
- subscription or membership products
- e-commerce retention and reactivation
- marketplaces with repeat transactions
- CRM and lifecycle marketing teams building winback programs

## Why A Business Team Would Care

The point is not just to predict churn. The point is to make better decisions.

This kind of framework helps answer questions like:

- Which customers are truly worth winning back?
- Who should receive a trust-based message instead of a discount?
- When should a team suppress contact to avoid wasted spend or fatigue?
- Which actions are likely to improve reactivation and net contribution?
- How should a team structure measurement so they can estimate incremental impact?

## Repo Structure

```text
winback-marketing-agents/
├── README.md
├── requirements.txt
├── data/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── scripts/
│   └── run_demo.py
└── src/
    └── winback_marketing_agents/
        ├── __init__.py
        ├── agents.py
        ├── data.py
        └── pipeline.py
```

## Quick Start

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
OMP_NUM_THREADS=1 python scripts/run_demo.py
```

The script will:

- generate synthetic lifecycle data
- train the models
- score customers
- assign next best actions
- simulate a holdout evaluation
- write outputs to `outputs/`

Generated files:

- `outputs/scored_customers.csv`
- `outputs/action_summary.csv`
- `outputs/metrics.csv`
- `outputs/BUSINESS_CASE.md`
- `outputs/DEMO_SUMMARY.md`
- `outputs/charts/action_mix.png`
- `outputs/charts/risk_value_matrix.png`
- `outputs/charts/holdout_lift.png`

Recommended files to open first:

- [outputs/BUSINESS_CASE.md](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/outputs/BUSINESS_CASE.md)
- [outputs/DEMO_SUMMARY.md](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/outputs/DEMO_SUMMARY.md)
- [PROJECT_BRIEF.md](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/PROJECT_BRIEF.md)

## Example Use Case

This synthetic environment simulates a money-transfer style business where customers have:

- different sending frequency
- different average transaction amounts
- different sensitivity to offers
- trust and urgency needs
- different risk of churning after inactivity

The project deliberately focuses on marketing questions like:

- Should we send a promo or not?
- Which customers should be suppressed?
- Which customers need a trust-focused message instead of an offer?
- How do we evaluate whether the intervention is incrementally profitable?

## Example Stakeholders

This type of system could be useful to:

- **Lifecycle marketing teams** defining winback and retention campaigns
- **CRM teams** designing trigger logic and targeting rules
- **Growth teams** connecting customer behavior to action strategy
- **Analytics teams** evaluating incrementality and promo efficiency
- **Finance partners** assessing lifecycle ROI and offer economics
- **ML teams** operationalizing predictive signals in a business workflow

## Demo Outputs

The end-to-end demo now produces:

- scored customer-level output
- action-level business summary
- topline holdout metrics
- chart assets for GitHub or presentations
- a business case memo
- a short demo summary

## Key Files

- [scripts/run_demo.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/scripts/run_demo.py)
- [src/winback_marketing_agents/data.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/src/winback_marketing_agents/data.py)
- [src/winback_marketing_agents/agents.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/src/winback_marketing_agents/agents.py)
- [src/winback_marketing_agents/pipeline.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/src/winback_marketing_agents/pipeline.py)
- [src/winback_marketing_agents/visualization.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/src/winback_marketing_agents/visualization.py)
- [src/winback_marketing_agents/reporting.py](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/src/winback_marketing_agents/reporting.py)
- [PROJECT_BRIEF.md](/Users/Lana/Downloads/MS%20Connects%202/winback-marketing-agents/PROJECT_BRIEF.md)

## Why this project

I can describe it like this:

> I built a lightweight winback decision engine that separates churn risk from customer value, recommends a next best action, and estimates incremental business impact through a holdout-style framework. The goal was not just to predict churn, but to create something closer to a lifecycle marketing operating system.



