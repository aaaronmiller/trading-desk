---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Aaron Miller (DRAFT — for human review and ratification)
model: Muse Spark
tags: [strata, intent, human-authored, draft]
---

# Trading Desk Intent v1.0 — DRAFT

> Status: drafted by the system from the approved plan for Aaron to review,
> amend, and ratify. Nothing downstream is built until this is ratified.

## 1. Goal
Operate an autonomous multi-agent trading desk that researches opportunities,
validates strategies without risking capital, and only trades real capital
after paper results clear a human-set bar.

## 2. Intent level
Consumer intent (the desk as an operating capability) and engineering intent
(the build-out of that capability in phases). Both are carried here.

## 3. Constraints
- Paper trading first: no real capital is risked until paper results clear a
  human-ratified validation bar. This gate is non-negotiable.
- A human governs all high-risk actions: position sizing beyond limits,
  enabling live execution, and exceeding spend budgets each require explicit
  human approval.
- Every agent operates under a spend ceiling; breaching it pauses the agent
  automatically.
- The desk runs unattended around the clock on a single rented virtual
  server; it must survive restarts without losing its decision history.
- Evaluation must be honest: historical evaluations may only use information
  available at the decision date. Using future information, even implicitly,
  invalidates an evaluation.
- The operator is a US person; venue availability follows from that.

## 4. Scale and quality expectations
- One human operator acting as the board; five to eight specialist agents.
- Agents wake on schedules measured in minutes, not seconds; decisions take
  seconds to minutes of model inference. Fill-speed latency is not a design
  driver — reliability and auditability are.
- Recovery: after a server restart, the desk resumes its schedule with no
  lost decisions and no duplicated orders.
- Decision history is durable and replayable: any past decision can be
  reconstructed with its inputs, reasoning, and outcome.

## 5. Success conditions
- Paper trading runs continuously and its results are recorded per decision.
- Historical evaluations reproduce without lookahead bias (verified by
  construction, not by trust).
- A human can review any decision's full trail — inputs, debate, sizing,
  outcome — and understand why it happened.
- Live trading, when enabled, stays within risk limits with zero unapproved
  exceptions.

## 6. Failure conditions
- A market-data feed is unreachable: the affected analysis degrades
  gracefully, marks its inputs as unavailable (never as empty), and the
  desk continues with reduced scope rather than guessing.
- An agent exceeds its spend ceiling: the agent pauses; the human is
  notified; nothing else stops.
- A venue rejects or fails an order: the failure is recorded with the
  venue's reason, the position is left flat, and the human is notified.
- Model provider outage: scheduled work skips cleanly and resumes on the
  next cycle; no partial decisions are recorded as complete.
- Drawdown beyond the human-set limit: new positions halt until the human
  reviews.

## 7. Personas
- **Aaron, operator and board.** Builder by trade; runs the desk, sets risk
  limits and budgets, approves live trading and high-risk actions, reviews
  the audit trail. Technically sophisticated; wants leverage, not babysitting.

## 8. Scope boundaries
| In scope | Out of scope | Rationale |
|----------|-------------|-----------|
| Stocks, crypto, forex, and prediction markets as venue classes | High-frequency trading | Decisions take minutes; fill speed is not the edge |
| Paper trading with per-decision records | Live trading before the validation bar is ratified and cleared | Capital preservation is the point of the gate |
| Historical evaluation with point-in-time discipline | Portfolio simulation as an evaluation tool | Turning ratings into fills needs an execution model; inventing one inside evaluation corrupts it |
| Specialist roles: market analysts, debate researchers, trader, risk reviewers, portfolio approver | Financial advice to third parties | Personal operation only |
| Budgets, approvals, and a replayable decision log | Fully autonomous operation with no human gates | Real money requires human accountability |

## 9. Prior art
| Solution | Strength | Weakness | Gap this fills |
|----------|----------|----------|----------------|
| Multi-agent trading research framework (open source, ~110k stars) | Role structure mirroring real firms; curated analyst prompts; point-in-time backtest discipline; monthly releases | Orchestration fused to a graph framework; no spend governance; no audit trail; simulated execution only | This project extracts its domain content (prompts, tools, evaluation discipline) and re-houses it in a thinner harness |
| Agent organization platform (open source, MIT, ~97k stars) | Org charts, heartbeat scheduling, per-agent budgets with hard stops, approval workflows, replayable audit log | Ships no trading logic; its trading-desk template is community-built, not vetted | This project supplies the trading domain content the platform lacks, and uses its governance layer for the live-money problem |
| Lab-vs-firm analysis (this conversation) | Established the division: research framework as the lab, orchestration platform as the firm | Analysis only, no implementation | This project is the implementation of that division |

Patterns adopted: specialist analyst roles with structured debate; adversarial
review before execution; point-in-time evaluation discipline; heartbeat-driven
autonomous operation; spend ceilings with automatic pause; human approval gates
for high-risk actions; immutable decision log.
Patterns deliberately avoided: monolithic single-agent trading; framework-fused
orchestration that cannot be re-prompted without code changes; evaluation that
invents fills; live execution without a paper validation gate.

## 10. Assumptions and dependencies
- Model providers remain available as metered services; the desk assumes
  inference cost, not free inference.
- Market-data vendors and trading venues expose programmatic access the desk
  can consume; feed outages are expected and handled per section 6.
- Paper trading precedes live trading by weeks, not days.

## 11. Open intent questions
- [NEEDS CLARIFICATION] What quantitative bar clears the paper-to-live gate
  (e.g. minimum paper return, risk-adjusted threshold, maximum drawdown,
  over what evaluation window)?
- [NEEDS CLARIFICATION] What starting capital per venue class when live
  trading begins (drives position sizing and risk limits)?
- [NEEDS CLARIFICATION] Which specific venues and accounts will be used
  (affects data entitlements, connectivity, and settlement)?
