---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-derived)
model: Muse Spark
tags: [strata, context, system-derived]
---

# Trading Desk Context v1.0 (derived)

## 1. Derivation summary
Derived from intent sections 3 (paper-first gate, human governance, spend
ceilings, 24/7 unattended operation, honest evaluation) and 4 (single
operator, minute-scale heartbeats, restart recovery, replayable history), plus
section 9 prior art (extract domain content from the research framework;
adopt the orchestration platform's management layer). The ledger is empty —
this is a kickoff, so there is no empirical memory and several decisions below
are architect intuition stated as such (see section 3 citations).

## 2. Architecture overview

```
                    +-------------------+
                    |   Human (board)   |  approvals, budgets, live-trading gate
                    +--------+----------+
                             | governance requests / audit
                    +--------v----------+
                    |  Orchestrator     |  org chart, heartbeats, budgets,
                    |  (management      |  approvals, audit log, multi-org
                    |   layer)          |  isolation per venue book
                    +--------+----------+
                             | delegate / collect
        +--------------------+--------------------+
        |                    |                    |
 +------v------+   +--------v--------+   +-------v-------+
 | Analyst     |   | Debate + Trader |   | Risk +        |
 | agents      |   | agents          |   | Portfolio     |
 | (per role,  |   | (bull/bear,     |   | agents        |
 |  per venue) |   |  trader)        |   | (limits,      |
 +------+------+   +--------+--------+   |  approval)    |
        |                    |           +-------+-------+
        v                    v                   |
 +-----------------------------------------------------+
 | Tool layer: market-data adapters, order gateways     |
 | (one adapter per venue class; date-clamped reads)    |
 +-----------------------------------------------------+
        |
 +------v----------------------------------------------+
 | Durable store: decision log, approvals, spend ledger |
 +-----------------------------------------------------+
```

## 3. Decisions

**CTX-001: Thin harness agents, not a fused framework, for trading roles**
- Derived from: intent section 9 (adopt extracted domain content; avoid
  framework-fused orchestration) and section 3 (honest evaluation must be
  enforceable in the tool layer, not buried in framework code).
- Memory: no empirical memory — intuition-based. Rationale: the extracted
  content is prompts + tool schemas + debate protocol; a harness (model +
  tools + loop + guardrails) carries it with less ceremony and is
  re-promptable without code changes.
- Options considered: (a) run the research framework stock; (b) port its
  graph layer 1:1; (c) harness rebuild. Chose (c) for the live path, with
  (a) retained as the reference lab per the phased plan.
- Trade-offs accepted: reimplementation cost; loss of upstream maintenance.

**CTX-002: Management layer owns scheduling, budgets, approvals, audit**
- Derived from: intent section 3 (human governance, spend ceilings), section
  4 (replayable history), and section 6 (drawdown halts are enforced here).
- Memory: no empirical memory — intuition-based, following the prior-art
  analysis that governance is the missing piece for live money.
- Options considered: (a) cron + scripts; (b) management layer. Chose (b):
  heartbeat scheduling, budget hard-stops, approval workflows, and the
  immutable activity log are first-class there; (a) would reimplement them.
- Trade-offs accepted: operational dependency on the management layer.

**CTX-003: Single durable store for decisions, approvals, spend**
- Derived from: intent section 3 (survive restarts without losing history)
  and section 4 (replayable history).
- Memory: no empirical memory — intuition-based.
- Options considered: flat files vs. relational store. Chose relational
  store: the audit/replay queries (per-decision trail, per-agent spend) are
  relational in shape.
- Trade-offs accepted: a database to operate and back up.

**CTX-004: Date-clamped tool layer enforcing point-in-time discipline**
- Derived from: intent section 3 (honest evaluation) and SPEC-005/006/007.
- Memory: no empirical memory — but the rule set is extracted verbatim from
  prior art (sources/tradingagents/backtest-methodology.md), so this is
  adoption, not invention.
- The tool layer — not the agents — clamps every dated read to the decision
  date, excludes undated items from historical windows, and labels coverage
  gaps as unavailable.
- Trade-offs accepted: every new venue adapter must implement the clamping
  contract; it is a tax on each integration.

**CTX-005: Simulated execution venue as the default order sink**
- Derived from: intent section 3 (paper-first gate) and SPEC-009/010.
- The order path terminates at a simulated venue unless a human has enabled
  live execution AND a portfolio approval exists per order. The live path is
  additive later, not a flag flip.
- Trade-offs accepted: live integration is deliberately not built in phase 1.

**CTX-006: Per-venue-class adapters with per-class risk limits**
- Derived from: intent section 8 (four venue classes) and SPEC-019.
- One adapter per class behind a common interface; risk limits configured
  per class. New classes add an adapter, never a rewrite.
- Trade-offs accepted: interface design must precede the second adapter.

## 4. Data model
- **decisions**: id, cycle id, instrument, venue class, decision date,
  analyst reports (4, with authors + timestamps), debate record, trader
  proposal, risk review, portfolio approval (nullable), order record,
  fill record (simulated or live), realized return (nullable until settled),
  benchmark-relative return (nullable until settled).
- **approvals**: id, action type, requester, decider, decision,
  timestamp, rationale.
- **spend_ledger**: agent id, period, recorded spend, ceiling, pause state.
- **heartbeats**: agent id, scheduled at, ran at, outcome, work product refs.
- Access patterns: append-only writes for decisions/approvals/spend; reads
  are per-decision replay and per-agent aggregates. Migration strategy:
  schema versioned with additive-only changes during paper phase.

## 5. Component specifications
- **Analyst agents** (4 roles × venue classes): produce timestamped reports
  via the tool layer; no trading authority.
- **Debate researchers** (bull/bear): consume analyst reports; produce
  mutually-referential arguments.
- **Trader**: consumes debate + plan; produces sized proposals with entry,
  stop, and rationale. No execution authority.
- **Risk reviewers**: produce downside scenarios and limit checks per
  proposal.
- **Portfolio approver**: the only path to order preparation; records
  approval per proposal.
- **Order gateway**: routes to simulated venue by default; live routing
  requires the human-enabled flag AND a portfolio approval (SPEC-010/011).
- **Tool layer**: date-clamped market-data adapters; order submission
  adapters; coverage-gap labeling.

## 6. Hosting and deployment
Derived from intent section 3 (single rented virtual server, unattended
24/7, restart recovery). One virtual server hosts the management layer, the
harness workers, the tool layer, and the durable store. Deployment is containerized
per service with the decision store on a persistent volume and scheduled
backups. On the deployment constraint changing, this section is regenerated
and the delta appended to the ledger.

## 7. Security
- Secrets (model provider keys, venue credentials) live in the server
  environment, never in the repo or logs; scoped per organization.
- The management layer's approval workflow is the authorization boundary
  for high-risk actions; there is no secondary path to live execution.
- Supply chain: pinned dependencies, no auto-update on the trading path;
  the extracted prompts are versioned in-repo.
- Threat model: credential exfiltration via a compromised agent is the
  primary risk — mitigated by scoped secrets, spend ceilings, and the audit
  log; a rogue agent cannot exceed its budget or bypass approvals.

## 8. Build phases
- Phase 1 — run the research framework stock on paper; establish the
  baseline and learn which roles carry signal. Validates SPEC-005..008
  (evaluation integrity) against the reference.
- Phase 2 — extract domain content into harness agents (plays: extract).
  Validates SPEC-001..004 (pipeline) in the harness.
- Phase 3 — historical evaluation on the harness with the date-clamp
  contract. Validates SPEC-005..008.
- Phase 4 — paper trading on the harness with budgets, approvals, audit.
  Validates SPEC-009..018.
- Phase 5 — multi-venue adapters (one class at a time). Validates
  SPEC-019/020.
- Phase 6 — live-trading readiness review against the human-ratified gate;
  no code change enables live trading without it.

## 9. Project structure
```
trading-desk/
  sources/            curated extractions (reference only, never built from)
    tradingagents/    role prompts, tool inventory, dataflow inventory,
                      backtest methodology, SOURCING.md
    paperclip/        orchestration model summary, SOURCING.md,
                      trading-firm-template/
  strata/trading-desk/  intent, spec, context, plays, ledger, substrate
  strata/evals/       eval manifest (outside the build tree)
  harness/            (phase 2+) role agents, tool layer, order gateway
  README.md
```
Organizing principle: reference material (`sources/`) is read-only input;
authored artifacts (`strata/`) own the contract; implementation (`harness/`)
is derived and never the source of truth.

## 10. Spec traceability
Every spec clause is supported by at least one decision above:
| Clause | Supporting decision(s) |
|--------|------------------------|
| SPEC-001 | CTX-001 (role agents carry the pipeline order) |
| SPEC-002 | CTX-001 (debate protocol is extracted domain content) |
| SPEC-003 | CTX-001 (risk reviewers are first-class roles) |
| SPEC-004 | CTX-005 (portfolio approval gates order preparation) |
| SPEC-005 | CTX-004 (date-clamped tool layer) |
| SPEC-006 | CTX-004 (undated-item exclusion rule) |
| SPEC-007 | CTX-004 (coverage-gap labeling rule) |
| SPEC-008 | CTX-003 (durable decision log settles with outcomes) |
| SPEC-009 | CTX-005 (simulated venue is the default sink) |
| SPEC-010 | CTX-005 (live path is additive; lockout by construction) |
| SPEC-011 | CTX-005 (per-order approval required even when live) |
| SPEC-012 | CTX-002 (budget hard-stops in the management layer) |
| SPEC-013 | CTX-002 (approval workflows for high-risk actions) |
| SPEC-014 | CTX-002 (durable activity log records approvals) |
| SPEC-015 | CTX-006 (per-class risk limits) |
| SPEC-016 | CTX-002 (management layer monitors drawdown; halts) |
| SPEC-017 | CTX-003 (durable store survives restarts) |
| SPEC-018 | CTX-003 (replay queries over the decision log) |
| SPEC-019 | CTX-006 (per-venue-class adapters) |
| SPEC-020 | CTX-006 (adapters isolate venue failures) |
| SPEC-021 | CTX-005 (live path is additive; enablement is a change event), CTX-002 (approval workflow records the decision) |
