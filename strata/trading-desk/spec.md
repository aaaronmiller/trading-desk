---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Aaron Miller (DRAFT — for human review and ratification)
model: Muse Spark
tags: [strata, spec, human-authored, draft, eval-binding]
---

# Trading Desk Specification v1.0 — DRAFT

> Status: drafted by the system for Aaron to review, amend, and ratify.

## 1. Contract clauses

### 1.1 Decision pipeline

**SPEC-001** [EVAL-001] WHEN a scheduled analysis cycle begins for an
instrument, THE system SHALL produce independent analyst reports covering the
instrument's venue class's defined coverage dimensions (for equities:
fundamentals, market technicals, news, sentiment) before any debate or
trading decision occurs.
- Eval: a completed cycle's record contains one analyst report per defined
  dimension for the instrument's class, with distinct authors and timestamps
  preceding the debate record. Fail if any dimension's report is missing or
  postdates the debate.
- Traces to: intent section 9 (specialist analyst roles).

**SPEC-002** [EVAL-002] WHEN analyst reports are complete, THE system SHALL
conduct a structured adversarial review in which a bullish case and a bearish
case are argued against each other before the trader acts.
- Eval: the cycle record contains a bull argument and a bear argument that
  each quote or restate at least one of the other's claims before rebutting.
  Fail if the trader's decision precedes both arguments.
- Traces to: intent section 9 (structured debate).

**SPEC-003** [EVAL-003] WHEN the debate concludes, THE system SHALL require an
independent risk review of the proposed trade before any order is prepared.
- Eval: the cycle record contains a risk review naming at least one downside
  scenario, recorded before order preparation. Fail if absent.
- Traces to: intent section 9 (adversarial review).

**SPEC-004** [EVAL-004] THE system SHALL NOT prepare or submit any order
unless a portfolio-level approval is recorded for that specific proposal.
- Eval: every prepared order links to a matching approval record. Fail if any
  order lacks one.
- Traces to: intent section 3 (human governance), section 8 (portfolio
  approver in scope).

### 1.2 Evaluation integrity

**SPEC-005** [EVAL-005] WHEN a historical evaluation runs for a decision date,
THE system SHALL exclude all market data, news, social content, and company
information dated after that decision date.
- Eval: run the evaluation for a past date against a fixture containing one
  future-dated item per feed; the decision record must contain none of the
  future items. Fail if any leaks through.
- Traces to: intent section 3 (honest evaluation), section 5.

**SPEC-006** [EVAL-006] WHEN a historical evaluation encounters an item with
no date, THE system SHALL exclude it unless the evaluation window reaches the
present day.
- Eval: fixture with an undated item and a window ending last week; the
  decision record must not reference the item. Fail if referenced.
- Traces to: intent section 3 (honest evaluation).

**SPEC-007** [EVAL-007] WHEN a data feed cannot cover the requested window,
THE system SHALL record the gap as unavailable rather than as an empty result.
- Eval: fixture with a feed whose coverage starts after the window start; the
  record must mark the feed unavailable for that window. Fail if recorded as
  "no data found".
- Traces to: intent section 6 (degrade gracefully, mark unavailable).

**SPEC-008** [EVAL-008] THE system SHALL settle every recorded decision with
its realized outcome and its return relative to a benchmark, after the fact.
The settlement horizon is a human-configured duration.
- Eval: a decision record older than the configured settlement horizon
  carries realized and benchmark-relative returns. Fail if unsettled past
  the horizon.
- Traces to: intent section 5 (per-decision records).

### 1.3 Paper trading

**SPEC-009** [EVAL-009] WHEN live execution is not enabled, THE system SHALL
route every approved order to a simulated venue and record the simulated fill.
- Eval: with live execution disabled, submit ten approved orders; all ten
  records show simulated fills and zero venue submissions. Fail otherwise.
- Traces to: intent section 3 (paper first), section 8.

**SPEC-010** [EVAL-010] THE system SHALL NOT submit a real order while live
execution is disabled, under any input.
- Eval: adversarial run attempting to force live submission with live
  execution disabled (direct instruction, malformed approval, replayed
  approval). Zero real submissions. Fail on any.
- Traces to: intent section 3 (paper-first gate).

**SPEC-011** [EVAL-011] WHEN a live execution path exists (phase 6+) and live
execution has been enabled by a recorded human decision, THE system SHALL
still require per-order portfolio approval before submission.
- Eval: with live execution enabled, an order lacking portfolio approval is
  blocked and logged. Fail if submitted.
- Traces to: intent section 3 (human governance).

### 1.4 Budgets and governance

**SPEC-012** [EVAL-012] WHEN an agent's recorded spend reaches its configured
ceiling, THE system SHALL pause that agent and block new work until a human
resumes it.
- Eval: drive a test agent to its ceiling; subsequent scheduled work is
  blocked and a pause record exists. Fail if work continues.
- Traces to: intent section 3 (spend ceiling), section 6.

**SPEC-013** [EVAL-013] WHEN an action is classified high-risk (enabling live
execution, exceeding position limits, raising a budget), THE system SHALL
require explicit human approval before proceeding.
- Eval: attempt each high-risk action without approval; all are blocked and
  logged as pending approval. Fail if any proceeds.
- Traces to: intent section 3 (human governance).

**SPEC-014** [EVAL-014] WHEN a human approves or rejects a pending action,
THE system SHALL record the decision, the decider, and the timestamp.
- Eval: approve one pending action and reject another; both records carry
  decider identity and timestamp. Fail if either is missing.
- Traces to: intent section 4 (replayable history).

### 1.5 Risk limits

**SPEC-015** [EVAL-015] WHEN a proposed position would exceed the configured
per-position size limit, THE system SHALL block the order and require human
review.
- Eval: propose an oversized position; the order is blocked with a review
  request recorded. Fail if submitted.
- Traces to: intent section 6 (drawdown/limits), section 3.

**SPEC-016** [EVAL-016] WHEN realized drawdown exceeds the configured maximum,
THE system SHALL halt new positions until a human reviews and re-enables
trading. Drawdown is the peak-to-trough decline in portfolio equity on a
mark-to-market basis, measured at the configured level (portfolio-wide or per
venue class) over the configured window.
- Eval: simulate drawdown past the limit; subsequent new-position proposals
  are halted. Fail if any proceeds.
- Traces to: intent section 6 (drawdown beyond limit halts).

**SPEC-021** [EVAL-021] THE system SHALL NOT enable live execution unless
(a) the paper-to-live validation bar has been human-ratified, (b) paper
results clear the bar, including the minimum paper-trading duration and
decision count, and (c) an explicit human approval is recorded. Enabling live
execution is a recorded change event, not a flag flip.
- Eval: attempt enablement with each of (a), (b), (c) missing in turn; all
  three attempts are blocked and logged. Fail if any proceeds.
- Traces to: intent sections 3 (non-negotiable gate), 5 (zero unapproved
  exceptions), 10 (paper precedes live by weeks, not days).

### 1.6 Audit and replay

**SPEC-017** [EVAL-017] THE system SHALL record every decision with its
inputs, the agents involved, the reasoning trail, and the outcome, in a
durable store that survives restarts.
- Eval: restart the system mid-cycle; all prior decision records are intact
  and complete. Fail on any loss.
- Traces to: intent section 4 (durable, replayable), section 3.

**SPEC-018** [EVAL-018] WHEN a human requests the history of a decision, THE
system SHALL reproduce the inputs, debate, sizing, approvals, and outcome in
chronological order.
- Eval: request history for a settled decision; the replay contains all five
  elements in order. Fail if any element is missing.
- Traces to: intent section 5 (reviewable trail).

### 1.7 Multi-venue operation

**SPEC-019** [EVAL-019] THE system SHALL support instrument classes across
stocks, crypto, forex, and prediction markets, with per-class data adapters
and per-class risk limits — subject to venue availability for a US person; a
class with no accessible venue is marked unavailable, not failed. (Venue
selection is an open question; see intent section 11.)
- Eval: configure one instrument per class with an accessible venue; each
  produces a completed paper cycle respecting its class risk limit. Fail if
  any accessible class cannot complete.
- Traces to: intent section 8 (venue classes in scope).

**SPEC-020** [EVAL-020] WHEN a trading venue is unreachable, THE system SHALL
mark affected work as blocked-by-venue, leave positions flat, and continue
other venues' work.
- Eval: simulate venue outage mid-cycle; no order is attempted at that venue
  and other venues complete. Fail on any attempted order or cascade halt.
- Traces to: intent section 6 (venue failure branch).

## 2. Acceptance scenarios

**Scenario A — full paper cycle.** Given a configured instrument and a
scheduled cycle, when the cycle runs with live execution disabled, then four
analyst reports, a bull/bear debate, a risk review, a trader proposal, a
portfolio approval, and a simulated fill are all recorded in order
(EVAL-001, EVAL-002, EVAL-003, EVAL-004, EVAL-009).

**Scenario B — honest historical evaluation.** Given a past decision date and
feeds containing future-dated and undated items, when the evaluation runs,
then no future-dated item and no undated item appears in the decision record,
and uncovered windows are marked unavailable (EVAL-005, EVAL-006, EVAL-007).

**Scenario C — budget breach.** Given an agent at its spend ceiling, when its
next heartbeat fires, then its work is blocked, a pause is recorded, and the
human is notified (EVAL-012).

**Scenario D — live gate.** Given live execution disabled, when any path
attempts a real order, then zero real orders are submitted (EVAL-010). Given
live execution human-enabled, when an order lacks portfolio approval, then it
is blocked (EVAL-011).

**Scenario E — drawdown halt.** Given drawdown past the configured maximum,
when new positions are proposed, then they halt pending human review
(EVAL-016).

**Scenario F — restart recovery.** Given a mid-cycle restart, when the system
resumes, then the schedule continues with no lost decisions and no duplicated
orders (EVAL-017, intent section 4).

## 3. Eval index
| EVAL-ID | Asserts | Bound clause | Stored at |
|---------|---------|--------------|-----------|
| EVAL-001 | One analyst report per defined class dimension, preceding debate | SPEC-001 | strata/evals/evals.md |
| EVAL-002 | Bull/bear arguments quote and rebut each other before the trader decides | SPEC-002 | strata/evals/evals.md |
| EVAL-003 | Risk review precedes order preparation | SPEC-003 | strata/evals/evals.md |
| EVAL-004 | Every order links a portfolio approval | SPEC-004 | strata/evals/evals.md |
| EVAL-005 | No future-dated data in historical runs | SPEC-005 | strata/evals/evals.md |
| EVAL-006 | Undated items excluded from past windows | SPEC-006 | strata/evals/evals.md |
| EVAL-007 | Coverage gaps marked unavailable, not empty | SPEC-007 | strata/evals/evals.md |
| EVAL-008 | Decisions settle with realized returns past the configured horizon | SPEC-008 | strata/evals/evals.md |
| EVAL-009 | Orders route to simulated venue when live off | SPEC-009 | strata/evals/evals.md |
| EVAL-010 | Zero real orders while live disabled | SPEC-010 | strata/evals/evals.md |
| EVAL-011 | Per-order approval still required when live on (phase 6+) | SPEC-011 | strata/evals/evals.md |
| EVAL-012 | Spend ceiling pauses the agent | SPEC-012 | strata/evals/evals.md |
| EVAL-013 | High-risk actions need human approval | SPEC-013 | strata/evals/evals.md |
| EVAL-014 | Approvals record decider and timestamp | SPEC-014 | strata/evals/evals.md |
| EVAL-015 | Oversized positions blocked for review | SPEC-015 | strata/evals/evals.md |
| EVAL-016 | Drawdown past max halts new positions | SPEC-016 | strata/evals/evals.md |
| EVAL-017 | Decision records survive restarts | SPEC-017 | strata/evals/evals.md |
| EVAL-018 | Decision history replays in order | SPEC-018 | strata/evals/evals.md |
| EVAL-019 | Accessible venue classes complete paper cycles | SPEC-019 | strata/evals/evals.md |
| EVAL-020 | Venue outage blocks only that venue | SPEC-020 | strata/evals/evals.md |
| EVAL-021 | Live enablement requires ratified bar, cleared results, human approval | SPEC-021 | strata/evals/evals.md |
