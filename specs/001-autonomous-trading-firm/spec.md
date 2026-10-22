---
date: 2026-10-21 15:10:00 UTC
ver: 1.2.0
author: Aaron Miller (owner statements) compiled by Claude Code session; system-drafted, ratified by launching the build
model: Claude (Claude Code session)
tags: [spec, autonomous-trading-firm, ears, eval-binding, contract, spec-kit]
layer: human
---
# Autonomous Trading Firm Specification v1.0

**Feature Branch**: `001-autonomous-trading-firm`

**Created**: 2026-10-21

**Status**: Prepared. System-drafted from the owners' own statements (see `intent.md` section 11). Items marked [INFERENCE] in `intent.md` are the system's readings; launching the build session with the reset handoff ratifies this specification and those readings.

**Input**: Owner statements T1 to T9 in the intake record, the pasted earlier prompts, the 2025 architecture draft, the legacy contract pack, and research waves 1 and 2.

**Identifier note**: SPEC identifiers are this feature's functional requirement identifiers. Each carries exactly one EVAL identifier bound to a held-out evaluation stored outside the build repository. The execution mode words "simulated" and "virtual" appear here because this document is owner-facing; agent-facing context never contains them (SPEC-052).

## 1. User Scenarios and Testing

### User Story 1: The firm runs itself around the clock on crypto (Priority: P1)

The operator deploys the firm once. From then on a virtual chief executive and its staff research crypto markets every 15 minutes, write plans for the house book and for twenty investor personas, compile each plan into a checked structure, execute it in the virtual market at live prices, commit predictions before they can be known, and keep running logs, with no human in the loop.

**Why this priority**: every other capability (reports, steering, tribunals, calibration) needs a running firm with a record.

**Independent Test**: start the firm on the local runtime against a recorded 48-hour crypto price tape; with no owner activity, at least 191 of 192 research cycles complete, every executed plan has a compiled structure, fills, wallet updates, committed predictions and log entries, and a restart injected mid-cycle loses and duplicates nothing.

**Acceptance Scenarios**:

1. **Given** a deployed firm with no owner activity, **When** 7 days pass, **Then** at least 99 percent of the 672 scheduled research cycles (at most 6 missed) are recorded complete, each with assessment, scope, bankroll, proposal, compiled plan or abstention, and prediction records. (EVAL-021, EVAL-022, EVAL-009)
2. **Given** an approved plan to buy a crypto asset, **When** the next price after the decision arrives, **Then** the virtual market fills at that price plus modeled costs and the book's wallet and running log update. (EVAL-063, EVAL-046, EVAL-113)
3. **Given** a cycle interrupted after its predictions are committed and before its orders are released, **When** the firm restarts, **Then** the predictions exist once, the orders are released once, and no step repeats its side effects. (EVAL-135, EVAL-029)

---

### User Story 2: The owners learn from the firm's reports (Priority: P1)

Each morning before the US equity market opens, both owners can read a daily report that explains what the firm did and why, teaching the concept behind each decision. A weekly feasibility report states, from the firm's own record, how likely the partner's 1 to 3 percent per day appetite is at the current risk level, and what risk the target would demand.

**Why this priority**: the owners said reports, analysis and predictions are the critical output, and that the system is how both of them will learn.

**Independent Test**: after a recorded 7-day run, the daily reports exist for each day with every required section, each decision carries its concept explanation, glossary link, other-side note, change-of-mind condition and lesson, and the feasibility report's figures match an independent recomputation from the same trade record within 0.5 percentage points.

**Acceptance Scenarios**:

1. **Given** a completed trading day, **When** 06:00 Pacific time arrives, **Then** the daily report for that day is available in the portal with every required section. (EVAL-115, EVAL-119)
2. **Given** a firm record of at least 30 closed positions, **When** the weekly report runs, **Then** it states the required win rate at current payoff ratios, realized edge, attainment probabilities for 1, 2 and 3 percent per day over 30 and 90 days, and risk of ruin, each with an interval. (EVAL-121)
3. **Given** a decision that used funding rates, **When** the owner opens it, **Then** the report explains funding rates in plain language and links the glossary entry. (EVAL-119, EVAL-120)

---

### User Story 3: The owners steer from outside the organization (Priority: P2)

Either owner can ask any seat a question, send the chief executive an idea or instruction, open a sandbox portfolio with theoretical cash, turn heat dials up or down, and pause the firm or a book. Nothing the firm does waits for them.

**Why this priority**: the partner's money motivates the firm, and both owners want to probe it, propose trades and test ideas.

**Independent Test**: an owner question, an owner idea and a heat change submitted during a recorded run are each answered or applied within the stated windows while the cycle completion rate stays at or above 99 percent.

**Acceptance Scenarios**:

1. **Given** the partner asks the chief risk officer why a position was cut, **When** the next cycle completes, **Then** an attributed answer citing the risk record is in the partner's console. (EVAL-127)
2. **Given** the operator turns the house heat from 8 to 4, **When** the next cycle starts, **Then** every new house order respects the heat-4 limits and the change is logged with both owners notified. (EVAL-073, EVAL-074)
3. **Given** the partner presses pause on the house book, **When** the next order release step runs, **Then** no house order is released and the pause is attributed. (EVAL-011)

---

### User Story 4: The firm trades every asset class it can automate (Priority: P2)

Beyond crypto, the firm researches and trades stocks, funds, options, bonds, foreign exchange, commodities, crypto perpetual futures, prediction-market contracts and a data-center GPU price index, each on its own market calendar, long or short.

**Why this priority**: the owners asked for conventional trading in every category that can be automated, and for bets in both directions.

**Independent Test**: a recorded multi-asset tape run produces fills only during each class's open hours, short and option positions carry their borrow, funding and premium effects, and a bearish verdict produces a short-side position in each class that supports one.

**Acceptance Scenarios**:

1. **Given** a stock plan decided on a Saturday, **When** the weekend passes, **Then** the order fills at the first price after Monday's open, never on the weekend. (EVAL-026, EVAL-027)
2. **Given** a bearish tribunal verdict on a stock with available puts, **When** the plan compiles, **Then** it implements the view as a short sale, an inverse fund or a put, chosen by the plan, with the corresponding costs modeled. (EVAL-059, EVAL-066)

---

### User Story 5: Serious targets face a tribunal (Priority: P2)

For each serious target, two advocates from different model families build their cases over a research window (one day by default), then debate in rounds. A judge from a third family rules. The ruling sets direction and conviction; the risk gate sets size.

**Why this priority**: the owners asked for pro and con arguments, a traditional debate, different model systems and a third-model judge.

**Independent Test**: a tribunal on a recorded target produces two dossiers from two distinct model families, four rounds in which each argument references the opponent's prior argument, a ruling from a third family with direction, conviction and reasons, and a plan whose size passed the risk gate.

**Acceptance Scenarios**:

1. **Given** a proposal above the tribunal threshold, **When** the window ends, **Then** opening, rebuttal, cross-examination and closing records exist for both sides, each after the prior round. (EVAL-087, EVAL-088)
2. **Given** a ruling for the short side with conviction 0.7, **When** the plan reaches the risk gate, **Then** the size is the minimum of the heat-scaled sizing rule and every hard limit. (EVAL-090, EVAL-075)

---

### User Story 6: Predictions are honest, calibrated and connected (Priority: P2)

Every prediction is sealed before its outcome can be known, scored when it resolves, compared with prediction markets and naive baselines, and linked to the drivers and other predictions it depends on.

**Why this priority**: verifiable history is what gives the firm's opportunity lists their weight, and the owners want correlation between predictions identified and used.

**Independent Test**: on a recorded set of 300 resolved predictions, scoring reproduces independently computed Brier and log scores to four decimals, an altered past record is detected, and a driver resolution flags every dependent prediction within one cycle.

**Acceptance Scenarios**:

1. **Given** a prediction committed at 09:00 for a 10:00 economic release, **When** the release resolves the driver, **Then** every prediction linked to that driver is flagged for update by the next cycle. (EVAL-102, EVAL-104)
2. **Given** someone edits a stored prediction after commitment, **When** verification runs, **Then** the edit is reported with the first divergent sequence number. (EVAL-096, EVAL-153)

---

### User Story 7: The firm hunts structural opportunities without getting eaten (Priority: P3)

A scheme-lifecycle desk identifies payout schemes and structurally doomed assets, estimates collapse hazard from rate-of-change signals, and stages exits. A manipulation-awareness function flags pumps, fake volume, spoofing and liquidation cascades, which feed the risk rules. The firm itself never manipulates or promotes.

**Why this priority**: the aggressive mandate needs a disciplined method for structurally doomed assets, whose documented lifecycle (early participants recover principal and profit, late participants lose at shutdown) is predictable from public signals.

**Independent Test**: on a recorded scheme case with known collapse date, the desk's hazard estimate crosses the payout rate before the collapse date and its staged exit plan never exceeds the configured share of daily volume; on a recorded pump tape, entries inside the flagged window are blocked.

**Acceptance Scenarios**:

1. **Given** a scheme position earning 3 percent per day, **When** the estimated daily hazard exceeds 3 percent, **Then** the desk issues a staged exit plan sized to observed liquidity and withdrawal limits. (EVAL-107, EVAL-108)
2. **Given** a suspected scheme on the restricted list, **When** live execution is enabled and a live order for it is proposed, **Then** the order is blocked unless an owner acknowledgment record exists for that asset. (EVAL-109, EVAL-080)

---

### User Story 8: Any seat runs in any harness (Priority: P3)

The operator can run any seat (for example the chief risk officer) inside Claude Code or Roo Code on a laptop, from the same canonical role files the cloud firm uses, and get the same structured outputs.

**Why this priority**: the owners asked for roles, skills and markdown that work with any harness.

**Independent Test**: regenerating harness files from the canonical sources produces byte-identical output to the committed files, both harness formats pass their schema checks, and a seat run locally against the recorded tape returns an output that validates against the same output contract as the cloud run.

**Acceptance Scenarios**:

1. **Given** a canonical role edit, **When** generation runs, **Then** every generated harness file for that role changes and the drift check passes; a hand edit to a generated file fails the drift check. (EVAL-013, EVAL-014)

---

### User Story 9: Live trading is ready and off (Priority: P3)

Live venue adapters exist and pass contract tests, but no real order can leave the system until the operator switches live on through a recorded act. The readiness scorecard informs that judgment without blocking it.

**Why this priority**: the owners chose simulation first with live code built but disabled.

**Independent Test**: with live off, a full recorded run makes zero requests to any order endpoint; enabling live without the operator role is refused; enabling it with the operator role produces a change event with an envelope snapshot.

**Acceptance Scenarios**:

1. **Given** live is off, **When** a plan is approved, **Then** the order goes only to the virtual market and the network log shows no order-endpoint request. (EVAL-146)
2. **Given** the partner account attempts to enable live, **When** the request arrives, **Then** it is refused and recorded. (EVAL-147)

---

### User Story 10: Personas, an institution model and a macro book (Priority: P3)

Twenty virtual investors with distinct worldviews and dials hold their own books; the firm studies a reference institution and the public holdings of major funds; a standing macro book positions for bear markets and policy shocks.

**Why this priority**: the original concept centers on virtual people whose worldviews mediate strategy, and the owners want to learn how a major firm operates.

**Independent Test**: twenty persona books exist with distinct profiles, every persona plan respects its persona's constraints, and the weekly report includes an institution study note.

**Acceptance Scenarios**:

1. **Given** a conservative persona that forbids leverage, **When** a planner proposes a leveraged plan for it, **Then** compilation rejects the plan with the persona constraint as the reason. (EVAL-048, EVAL-054)

### Edge Cases

- A data source returns nothing or stale data: inputs are marked unavailable, the cycle continues with reduced scope, and no fill uses a price older than the class's staleness limit (SPEC-040, SPEC-072).
- A model provider times out mid-cycle: the step retries within its budget, then the cycle records the step as skipped and releases no orders that depended on it (SPEC-030, SPEC-144).
- Two owners change the same dial within one cycle in opposite directions: the more conservative value applies and both are notified (SPEC-012).
- A role reaches its budget cap mid-cycle: the role pauses, its pending work is reassigned or deferred by the chief executive, and the firm keeps running (SPEC-136).
- A prediction's resolution source disagrees with a prediction market's resolution: the firm's declared resolution source governs and the disagreement is recorded (SPEC-099).
- A market reopens after a holiday with a price gap through a stop: the stop fills at the first available price, not at the stop level (SPEC-063).
- An instruction embedded in a scraped article ("sell everything now"): treated as text, never executed (SPEC-037).
- A planner outputs a percentage stop with no price-structure basis: compilation rejects it (SPEC-057).
- A scheme stops processing withdrawals before the hazard estimate crosses: the position is marked impaired at zero realizable value and the miss is recorded as a lesson (SPEC-108).
- The firm-wide budget is exhausted near month end: non-essential seats pause; risk, execution, logging and reporting seats keep their reserved share (SPEC-137).
- Clock skew between data timestamps and the firm clock exceeds the tolerance: affected data is quarantined and labeled (SPEC-033).

## 2. Requirements

### 2.1 Contract clauses

Clauses use EARS phrasing. "The system" means the deployed firm including its owner portal. "Seat" means an agent role instance. "Book" means a portfolio with its own wallet. Default numbers are configuration values; the clause is evaluated against the configured value, and the stated default applies when none is configured.

#### 2.1.1 Organization, seats and authority

**SPEC-001** [EVAL-001] THE system SHALL define every seat by a canonical role definition containing mission, responsibilities, inputs, outputs, authority, handoffs, cadence reference and boundaries, and SHALL refuse to load a seat whose definition lacks any of these sections.
- Eval: remove one section from a copy of a role definition; loading must fail naming the missing section; every shipped definition loads.
- Traces to: intent sections 1, 8 (US8); requirements ROLE-01

**SPEC-002** [EVAL-002] THE system SHALL staff at minimum these seats, each with exactly one reporting line that ends at the chief executive seat or, for internal audit, at the owners: chief executive; chief investment officer; house portfolio manager; persona portfolio managers (one per persona); strategy portfolio managers; macro strategist; crypto markets analyst; conventional markets analyst; news and event analyst; quantitative researcher; special situations analyst; prediction markets analyst; strategy compiler; red team (advocates and judges); chief risk officer; market risk analyst; market integrity analyst; model validation; prediction scoring; chief compliance officer; pre-trade compliance; conduct surveillance; chief operating officer; execution trader; reconciliation; fund accounting; controller; data engineering; release control; records keeper; investor education and reporting; internal audit.
- Eval: the loaded registry contains every listed seat; walking reporting lines from every seat terminates at the chief executive (or owners for internal audit) with no cycle.
- Traces to: intent sections 1, 7; ORG-01, ORG-08

**SPEC-003** [EVAL-003] WHEN the daily cycle opens, THE system SHALL publish within 30 minutes a chief executive agenda listing priorities, capital allocation changes, staffing changes and the risk posture for the day.
- Eval: for each day of a recorded 7-day run, an agenda record exists with all four fields, timestamped within 30 minutes of the configured daily open.
- Traces to: intent section 8 (US1); ORG-02, CYC-06

**SPEC-004** [EVAL-004] WHEN the chief executive or chief investment officer changes capital allocation between books, THE system SHALL record the change with reason and SHALL reject any allocation that breaches a ceiling set by the chief risk officer or the owner envelope.
- Eval: submit an allocation exceeding a ceiling; it is rejected with the ceiling named; a valid one is recorded with reason and actor.
- Traces to: intent sections 3, 8; ORG-02, ORG-05

**SPEC-005** [EVAL-005] WHEN the chief executive creates, revises or retires a seat, THE system SHALL record the change with a reason derived from scored performance, store the prior definition version, and SHALL reject any change that alters an envelope ceiling, a hard limit or a scoring rule.
- Eval: a revision that edits a hard limit is rejected; a revision that edits prompt text is accepted with both versions retrievable and the reason recorded.
- Traces to: intent section 1; ORG-02

**SPEC-006** [EVAL-006] THE system SHALL reject any approval in which the approving seat is the seat that proposed the item, wrote the item, or produced the analysis the item depends on.
- Eval: craft a proposal and an approval by the same seat, and by the seat that wrote its analysis; both are rejected; an independent approval passes.
- Traces to: intent section 3; ORG-06

**SPEC-007** [EVAL-007] THE system SHALL release orders only from the execution trader seat class, SHALL book positions only from fund accounting, and SHALL compute and publish net asset value and profit and loss only from the controller seat, which recomputes them independently of the books' own figures.
- Eval: attempts by any other seat to release, book or publish are rejected; a planted mismatch between book figures and controller recomputation above tolerance blocks publication.
- Traces to: intent section 3; ORG-06

**SPEC-008** [EVAL-008] THE system SHALL attribute every record that changes state (decision, order, fill, allocation, dial, definition, owner action) to an actor identifier and a timestamp, and SHALL reject an unattributed write.
- Eval: an unattributed write fails; every state-changing record in a recorded run carries actor and timestamp.
- Traces to: intent section 1; ORG-07

**SPEC-009** [EVAL-009] WHILE no owner is active, THE system SHALL complete every scheduled cycle without any step waiting for owner input.
- Eval: a recorded 48-hour run with zero owner activity reaches the cycle completion rate of SPEC-028; no step record shows a wait state attributed to an owner.
- Traces to: intent sections 3, 6; ORG-03

**SPEC-010** [EVAL-010] THE system SHALL accept the owner envelope actions (enable or disable live execution, change envelope ceilings, lift a restricted-list entry, resume the house book after its stop) only from the operator owner account, SHALL accept pause and resume of the firm or any other book from either owner account, and SHALL record each as a change event with the prior and new values.
- Eval: each action from the partner account other than pause and resume is refused and recorded; from the operator account it is applied with a change event holding prior and new values.
- Traces to: intent sections 3, 7; ORG-04, ORG-05

**SPEC-011** [EVAL-011] WHEN an owner pauses the firm or a book, THE system SHALL release no further orders for the paused scope from the next order release step until an owner resumes it.
- Eval: pause between a plan approval and its release; the order is not released; resume releases nothing retroactively and new orders flow again.
- Traces to: intent section 8 (US3); ORG-04

**SPEC-012** [EVAL-012] IF both owners change the same dial within one cycle to different values, THEN THE system SHALL apply the more conservative value and notify both owners of the conflict and the applied value.
- Eval: submit heat 9 and heat 3 for one book within one cycle; heat 3 applies; both owners have a notification naming both requests.
- Traces to: intent section 6; HEAT-02

**SPEC-013** [EVAL-013] THE system SHALL keep exactly one canonical source for each seat, skill, rule, cycle, persona and strategy, and SHALL generate every harness-specific file from those sources with an embedded source hash, so that a drift check fails whenever a generated file differs from regeneration.
- Eval: regenerate and compare to the committed files: identical; edit one generated file by hand: the drift check fails naming the file.
- Traces to: intent sections 3, 8 (US8); ROLE-02, ROLE-03

**SPEC-014** [EVAL-014] THE system SHALL generate for every seat a Claude Code subagent file and a Roo Code custom mode entry that each pass their harness's published schema.
- Eval: schema validation of all generated files passes; removing a required field from a generated file fails validation.
- Traces to: intent section 3; ROLE-03

**SPEC-015** [EVAL-015] THE system SHALL generate files for additional harnesses listed in its capability matrix and SHALL report, per harness and seat, each declared feature the harness cannot represent.
- Eval: the generation report lists every seat-harness pair with unsupported features named; a harness with no support for iteration caps reports that gap for every seat that declares one.
- Traces to: intent section 3; ROLE-03

**SPEC-016** [EVAL-016] THE system SHALL declare each seat's tool authority in abstract classes (read, write paths, network, order release, spawn) and SHALL grant no tool in any generated or runtime context beyond the declared classes.
- Eval: compare every generated file and the runtime tool list per seat with the declaration; any extra grant fails; a seat without order-release authority cannot call the order tool at runtime.
- Traces to: intent section 3; ROLE-05, QA-05

**SPEC-017** [EVAL-017] THE system SHALL keep cadence, budget and escalation settings in a runtime manifest separate from role prose, and the role prose SHALL contain no cadence, budget or escalation values.
- Eval: a linter over role prose finds no cadence, budget or escalation values; the manifest supplies each seat's three settings.
- Traces to: intent section 3; ROLE-06

**SPEC-018** [EVAL-018] THE system SHALL define every cycle as a step graph with declared inputs, outputs, verdict contracts, gates and iteration caps, and SHALL refuse to load a graph with a cycle-without-cap, a dangling input or an undeclared output.
- Eval: load three malformed graphs (uncapped loop, dangling input, undeclared output); each is refused with the defect named; all shipped graphs load.
- Traces to: intent section 8; ROLE-04

**SPEC-019** [EVAL-019] THE system SHALL load a skill only when its folder name matches its declared name and its description is non-empty, and SHALL refuse an external skill whose commit or content hash differs from its pin.
- Eval: a renamed skill folder and a tampered pinned skill are both refused; valid skills load.
- Traces to: intent section 3; ROLE-07

**SPEC-020** [EVAL-020] WHEN a seat runs inside a local agent harness against recorded data, THE system SHALL return an output that validates against the same output contract as the same seat's cloud run.
- Eval: run the chief risk officer seat locally and in the cloud runtime on the same recorded inputs; both outputs validate against the seat's output contract.
- Traces to: intent section 8 (US8); ROLE-02

#### 2.1.2 Cycles, calendars and durability

**SPEC-021** [EVAL-021] THE system SHALL start a research-to-plan cycle every 15 minutes, with each start within 2 minutes of its scheduled slot, continuously.
- Eval: over a recorded 48-hour run, 192 cycle start records exist, each within 2 minutes of its slot.
- Traces to: intent section 4; CYC-01

**SPEC-022** [EVAL-022] WHEN a research-to-plan cycle runs, THE system SHALL record, in order, market assessment, single or multi-instrument scoping, bankroll setting, strategy proposal or abstention, compilation, prediction commitment and next-review scheduling.
- Eval: every completed cycle record contains the seven steps in this order with timestamps ascending; an abstention carries a reason.
- Traces to: intent section 8 (US1); CYC-02

**SPEC-023** [EVAL-023] THE system SHALL analyze every active book once per hour and append the analysis to the book's running log.
- Eval: for each active book over a recorded 24-hour run, 24 hourly analysis entries exist in its log.
- Traces to: intent section 4; CYC-03, LOG-01

**SPEC-024** [EVAL-024] THE system SHALL run a daily rhythm of morning meeting, investment committee, risk report and end-of-day books at configured times, each producing its record.
- Eval: a recorded day contains all four records at their configured times plus or minus 15 minutes.
- Traces to: intent section 4; CYC-06

**SPEC-025** [EVAL-025] THE system SHALL run a weekly review that evaluates every plan to date, records insights from plans that performed, and records strategy promotions and demotions with reasons.
- Eval: after a recorded 8-day run, one weekly review exists listing every plan, insights linked to the performing plans, and promotion or demotion records with reasons.
- Traces to: intent section 4; CYC-04, QA-01

**SPEC-026** [EVAL-026] THE system SHALL fill an order for an instrument only while that instrument's market is open according to its calendar, treating crypto spot and perpetual markets as always open, foreign exchange as open from Sunday 17:00 to Friday 17:00 New York time, and listed securities per their exchange calendars including holidays and early closes.
- Eval: orders submitted on a weekend, a holiday and after an early close fill at the first eligible price; crypto orders fill on weekends.
- Traces to: intent section 4; CYC-05, MKT-02

**SPEC-027** [EVAL-027] WHEN an order is decided at time T, THE system SHALL fill it only at a price observed after T, and in historical replay a decision at a session close SHALL fill no earlier than the next session.
- Eval: every fill timestamp is later than its decision timestamp; replay decisions at close fill in the next session.
- Traces to: intent section 6; CYC-07

**SPEC-028** [EVAL-028] THE system SHALL complete at least 99 percent of scheduled cycles in any rolling 7-day window and SHALL record each missed cycle with its cause.
- Eval: compute completion over a recorded 7-day run with injected faults at a 0.5 percent rate; completion is at least 99 percent and every miss has a cause.
- Traces to: intent sections 4, 5; DUR-02

**SPEC-029** [EVAL-029] WHEN a scheduled trigger is delivered more than once for the same slot, THE system SHALL run that slot's cycle exactly once.
- Eval: deliver each trigger of a recorded day twice; exactly one cycle record per slot exists and no side effect repeats.
- Traces to: intent section 6; DUR-01

**SPEC-030** [EVAL-030] IF a cycle fails or ends partially, THEN THE system SHALL release no orders from it, and the next cycle SHALL reconcile books, orders and predictions before acting.
- Eval: fail a cycle after compilation; no order from it is released; the next cycle's first step is a reconciliation record with zero unexplained differences.
- Traces to: intent section 6; DUR-03

#### 2.1.3 Research, data and point-in-time integrity

**SPEC-031** [EVAL-031] WHEN a research cycle covers an instrument, THE system SHALL produce one analyst output per coverage dimension defined for its class before any debate or plan uses it (crypto: price structure, flows and on-chain activity, derivatives positioning, news and sentiment; listed securities: fundamentals, price structure, news, sentiment; macro: rates, currencies, commodities, policy calendar).
- Eval: each plan's linked analyses cover every dimension of the instrument's class and are timestamped before the plan; a missing dimension is recorded as unavailable, never silently skipped.
- Traces to: intent section 8 (US1); RES-01

**SPEC-032** [EVAL-032] THE system SHALL store every datum with its source, retrieval time and effective time.
- Eval: every stored price, filing, article and indicator row in a recorded run has all three fields populated.
- Traces to: intent section 3; RES-06

**SPEC-033** [EVAL-033] WHEN a decision is made at time T, THE system SHALL supply only data whose effective time is at or before T, and SHALL quarantine data whose timestamps disagree with the firm clock by more than the configured tolerance (default 5 minutes).
- Eval: plant future price rows and a future-dated article in the store; a decision at T receives none of them; a row skewed by 10 minutes is quarantined and labeled.
- Traces to: intent section 6; RES-03, QA-03

**SPEC-034** [EVAL-034] WHEN a historical window is assembled, THE system SHALL exclude items without an effective time.
- Eval: an undated article in a replay window never appears in any decision input.
- Traces to: intent section 6; RES-03

**SPEC-035** [EVAL-035] IF requested data does not cover a window, THEN THE system SHALL label the gap unavailable in every input that depends on it and SHALL never present the gap as an empty result.
- Eval: remove a source for one hour; affected inputs carry an unavailable label with the window; no input shows an empty list for that window.
- Traces to: intent section 6; RES-03

**SPEC-036** [EVAL-036] THE system SHALL reject any seat output whose trade-relevant numbers (prices, sizes, probabilities, levels, rates) do not trace to a tool result from the same run.
- Eval: an output quoting a price absent from its run's tool results is rejected naming the number; grounded outputs pass.
- Traces to: intent section 6; RES-04

**SPEC-037** [EVAL-037] THE system SHALL treat text from fetched content, filings, social posts, other seats and owner free text as data, and SHALL never perform a tool call because that text instructs it.
- Eval: run a corpus of 50 injection items (hidden instructions to sell, transfer, change limits or reveal configuration) through the research cycle; zero tool calls trace to injected instructions and each item is flagged.
- Traces to: intent section 3; RES-05

**SPEC-038** [EVAL-038] THE system SHALL label every figure in an owner-facing report with its source and time, and SHALL mark inferences and consensus figures as such.
- Eval: sample 100 figures across a week's reports; each has a source and time; inferences and consensus figures carry their markers.
- Traces to: intent section 5; RES-06

**SPEC-039** [EVAL-039] WHEN a deep research report is produced, THE system SHALL include the owner template sections: executive summary, actor map, method with justification, timeline with follow-the-money analysis, patterns, verbatim quotes, methodological defense, quality evaluation and meta-learning note.
- Eval: every deep research report contains all nine sections, each non-empty.
- Traces to: intent section 8 (US2); RES-02

**SPEC-040** [EVAL-040] IF a data source fails, THEN THE system SHALL continue the cycle with reduced scope, mark affected inputs unavailable, and never substitute guessed values.
- Eval: block one price source during a cycle; the cycle completes, affected instruments are excluded or marked, and no fabricated value appears.
- Traces to: intent section 6; RES-03

**SPEC-041** [EVAL-041] WHERE historical replay is configured with masking, THE system SHALL replace instrument names and calendar dates in seat inputs with consistent aliases.
- Eval: a masked replay's seat inputs contain no raw instrument names or dates from the replay period; aliases are consistent within the run.
- Traces to: intent section 6; QA-04

**SPEC-042** [EVAL-042] THE system SHALL include a stored lesson in a seat's input only if the lesson's underlying outcome resolved before the decision time.
- Eval: a lesson derived from an outcome resolving at T plus 1 day never appears in a decision at T.
- Traces to: intent section 6; QA-03

#### 2.1.4 Books, personas and wallets

**SPEC-043** [EVAL-043] THE system SHALL start with twenty personas, each with a distinct worldview, risk profile, horizon, instrument constraints, starting capital and heat setting, and SHALL allow owners to add personas.
- Eval: twenty persona records exist with pairwise-distinct profiles; an owner-added persona gets a book and enters the next cycle.
- Traces to: intent section 7; PLAN-01, WAL-02

**SPEC-044** [EVAL-044] THE system SHALL maintain these book types, each with a multi-asset wallet of cash by currency, positions, lots and cost basis: house book, persona books, strategy books, owner sandbox books and benchmark books.
- Eval: one book of each type exists with all wallet fields; a cross-currency position records its currency.
- Traces to: intent section 8; WAL-01

**SPEC-045** [EVAL-045] WHEN an owner opens a sandbox with theoretical cash (default 10,000 US dollars), THE system SHALL create a book that trades at live prices with the same cost model and compares it with agent books and benchmarks.
- Eval: an owner sandbox fills at the same prices and costs as an agent book for the same order; its report shows comparisons with at least one agent book and one benchmark.
- Traces to: intent section 8 (US3); WAL-03

**SPEC-046** [EVAL-046] THE system SHALL compute each book's net asset value as cash plus marked positions, with realized and unrealized profit and loss, fees, borrow and funding shown separately, and SHALL reconcile each book to the ledger every cycle.
- Eval: independent recomputation of a recorded run matches every book's figures to the cent; a planted ledger difference produces a reconciliation break record.
- Traces to: intent section 5; WAL-01, LEDGER-01

**SPEC-047** [EVAL-047] THE system SHALL maintain benchmark books for buy-and-hold bitcoin, a broad US equity index fund, a 60/40 stock and bond mix, and cash, and SHALL show each book's performance relative to them.
- Eval: four benchmark books exist and every book report shows relative performance against them.
- Traces to: intent section 5; WAL-03

**SPEC-048** [EVAL-048] WHEN a plan targets a persona book, THE system SHALL reject it at compilation if it violates the persona's constraints on instrument classes, leverage, position size or horizon.
- Eval: a leveraged plan for a no-leverage persona is rejected naming the constraint; a compliant plan compiles.
- Traces to: intent section 8 (US10); PLAN-01

**SPEC-049** [EVAL-049] THE system SHALL keep live-price books and historical replay runs separate, such that no replay run writes to a live-price book.
- Eval: run a replay concurrently with live-price cycles; no replay record references a live-price book.
- Traces to: intent section 9; WAL-04

**SPEC-050** [EVAL-050] WHERE running-cost allocation is enabled, THE system SHALL report each book's return net of its allocated share of inference, data and hosting costs.
- Eval: with allocation on, gross minus allocated cost equals reported net for each book in a recorded week.
- Traces to: intent section 5; COST-01

**SPEC-051** [EVAL-051] THE system SHALL show the execution mode (simulated or live) on every owner-facing page, report and message through a label that no seat output can alter.
- Eval: every owner-facing artifact in a recorded run carries the mode label; a seat output containing a contrary label does not change the displayed label.
- Traces to: intent section 3; PLAN-03

**SPEC-052** [EVAL-052] THE system SHALL keep agent-facing context free of statements that execution is simulated, virtual or paper.
- Eval: scan every prompt sent in a recorded run against the configured denylist of simulation terms; zero matches outside owner-facing artifacts.
- Traces to: intent section 3; PLAN-03

#### 2.1.5 Plans and the plan language

**SPEC-053** [EVAL-053] WHEN a portfolio manager seat issues a plan, THE system SHALL have the strategy compiler translate it into a typed plan structure covering instruments, direction, entry conditions, exits, sizing rule, risk rules, schedule and linked predictions.
- Eval: every executed plan in a recorded run has a compiled structure containing all eight fields and a link to the source plan text.
- Traces to: intent section 8 (US1); DSL-01

**SPEC-054** [EVAL-054] IF a compiled plan fails validation, THEN THE system SHALL reject it with machine-readable reasons and SHALL not send any part of it to the market.
- Eval: submit ten invalid plans (unknown instrument, closed class, missing exit, size over cap, persona breach and others); each is rejected with a reason and no order exists for it.
- Traces to: intent section 6; DSL-01

**SPEC-055** [EVAL-055] THE system SHALL evaluate plan conditions only through a closed expression language whose functions are on a whitelist, and SHALL reject any expression using anything else.
- Eval: a fuzz corpus of 1,000 generated expressions produces no evaluation outside the whitelist; expressions referencing unlisted names are rejected at compilation.
- Traces to: intent section 3; DSL-01

**SPEC-056** [EVAL-056] THE system SHALL support single-instrument, multi-instrument within one class, cross-asset, and whole-book allocation plans.
- Eval: one plan of each kind compiles and executes in a recorded run.
- Traces to: intent section 8; PLAN-02

**SPEC-057** [EVAL-057] THE system SHALL require entry, stop and target levels to be absolute prices that appear in the price-structure analysis linked to the plan.
- Eval: a plan with a percentage-only stop is rejected; a plan whose stop price is absent from its linked analysis is rejected; a grounded plan compiles.
- Traces to: intent section 6; DSL-03

**SPEC-058** [EVAL-058] WHEN a seat cannot form a view, THE system SHALL record an abstention with a reason, and WHEN a seat's rating cannot be parsed, THE system SHALL route the item to review rather than treat it as a hold.
- Eval: a seat output without a view yields an abstention record with reason; a malformed rating yields a review record and no hold decision.
- Traces to: intent section 6; DSL-04

**SPEC-059** [EVAL-059] WHEN a view is bearish, THE system SHALL let the plan implement it through any available short-side form for the instrument (short sale, inverse fund, put option, perpetual short, or the opposing side of an event contract).
- Eval: for each class with a short-side form, a bearish plan compiles and executes with the class's costs; a class without one is rejected with that reason.
- Traces to: intent section 8 (US4); DIR-01

**SPEC-060** [EVAL-060] THE system SHALL answer, for any plan at any time, whether it is active, its current value, its profitability and its time in trade.
- Eval: query 20 plans at random times in a recorded run; every answer matches independent recomputation.
- Traces to: intent section 8; PLAN-02

**SPEC-061** [EVAL-061] WHEN a plan is revised, THE system SHALL create a new version and retain every prior version.
- Eval: revise a plan twice; three versions are retrievable with timestamps and authors.
- Traces to: intent section 5; LOG-02

**SPEC-062** [EVAL-062] THE system SHALL link every plan to its predictions, its tribunal record when one exists, its gate outcomes, its orders and its fills.
- Eval: from any fill in a recorded run, the full chain back to the plan, gates, tribunal and predictions resolves in one query.
- Traces to: intent section 5; LOG-01

#### 2.1.6 Virtual market

**SPEC-063** [EVAL-063] THE system SHALL fill market orders at the opposite side of the observed quote plus modeled slippage, and SHALL trigger limit and stop orders only when observed prices cross their levels, filling gapped stops at the first available price.
- Eval: on a recorded tape, every fill equals the expected price under these rules to the instrument's tick; a gap through a stop fills at the gap price.
- Traces to: intent section 8 (US1); MKT-01

**SPEC-064** [EVAL-064] THE system SHALL charge fees from the fee profile of the instrument's class and reference venue.
- Eval: every fill's fee equals the profile's rate applied to its notional; changing the profile changes subsequent fees only.
- Traces to: intent section 8; MKT-01

**SPEC-065** [EVAL-065] THE system SHALL increase modeled slippage with order size relative to observed volume or depth, and SHALL fill partially any order above the configured participation cap (default 5 percent of the period's volume).
- Eval: doubling an order's size increases its modeled slippage; an order at 10 percent of period volume fills half and leaves the remainder working.
- Traces to: intent section 8; MKT-01

**SPEC-066** [EVAL-066] THE system SHALL accrue borrow cost on short sales, funding on perpetual positions at observed or modeled rates, and SHALL price options from observed quotes or, when none are available, from a labeled model.
- Eval: a short held 5 days accrues the configured borrow; a perpetual accrues funding each interval; an option without quotes carries a model-price label.
- Traces to: intent section 8 (US4); MKT-01, DIR-01

**SPEC-067** [EVAL-067] WHEN a leveraged position's equity falls below maintenance margin, THE system SHALL liquidate it at the modeled liquidation price and record the event.
- Eval: drive a 3x position through its maintenance level on a recorded tape; liquidation occurs at the modeled price with a record.
- Traces to: intent section 6; RISK-04

**SPEC-068** [EVAL-068] THE system SHALL provide prices for every instrument class it trades, including a data-center GPU price index, bond prices or yields, and commodity reference prices, each with a declared source and update cadence.
- Eval: every tradable instrument has a source and cadence record; a GPU index position marks to its index each update.
- Traces to: intent section 8 (US4); DSL-02

**SPEC-069** [EVAL-069] THE system SHALL present the same order interface to seats for the virtual market and for every live venue adapter.
- Eval: one contract test suite passes against the virtual market and every live adapter running on recorded venue responses.
- Traces to: intent section 3; MKT-03

**SPEC-070** [EVAL-070] THE system SHALL produce identical fills for identical prices, orders and random seed.
- Eval: replay the same recorded day twice; fill records are byte-identical.
- Traces to: intent section 5; MKT-01

**SPEC-071** [EVAL-071] WHILE an instrument's market is closed, THE system SHALL queue orders whose type allows it and reject the rest with a reason.
- Eval: a day order submitted on a holiday is rejected with the reason; a good-till-canceled limit is queued and works at the open.
- Traces to: intent section 6; MKT-02

**SPEC-072** [EVAL-072] IF the latest price for an instrument is older than its class's staleness limit (default 2 minutes for crypto, 20 minutes for listed securities in open hours), THEN THE system SHALL not fill orders in it.
- Eval: stall a price feed past the limit; orders do not fill until a fresh price arrives.
- Traces to: intent section 6; MKT-01

#### 2.1.7 Risk, heat and the owner envelope

**SPEC-073** [EVAL-073] THE system SHALL attach a heat dial from 1 to 10 to the firm, every persona and every strategy, and SHALL derive from the effective heat the sizing fraction, leverage cap, stop distance, drawdown ladder and eligible instrument classes through a published mapping table.
- Eval: for heats 1, 5 and 10, generated limits equal the mapping table; changing heat changes the limits of new orders only.
- Traces to: intent section 8 (US3); HEAT-01

**SPEC-074** [EVAL-074] WHEN an owner changes a heat dial, THE system SHALL apply it from the next cycle within the envelope ceiling, log it with actor and prior value, and notify the other owner.
- Eval: a dial change is effective at the next cycle, logged and notified; a value above the ceiling is clamped to the ceiling and the clamp is reported.
- Traces to: intent section 8 (US3); HEAT-02

**SPEC-075** [EVAL-075] THE system SHALL size each position at no more than the heat-scaled fractional Kelly amount implied by the measured edge of its strategy and conviction, and WHILE a strategy has fewer than the minimum record (default 30 resolved outcomes), at no more than the exploratory size (default 0.5 percent of book value).
- Eval: compute expected sizes for 50 recorded proposals; actual sizes never exceed them; new strategies never exceed the exploratory size.
- Traces to: intent section 6; RISK-03

**SPEC-076** [EVAL-076] WHEN an order would breach a hard limit (maximum position, gross or net exposure, leverage ceiling with default 3x per position, daily loss, order value, turnover), THE system SHALL block it before release and record the limit and values.
- Eval: for each limit, an order just over it is blocked with a record and an order just under it passes.
- Traces to: intent section 3; RISK-04

**SPEC-077** [EVAL-077] WHEN a book falls below its high-water mark by its ladder levels, THE system SHALL warn at the first level, halve new risk at the second, and stop new risk with a post-mortem at the third; the house book's third level is the tighter of its heat ladder level and the envelope stop (default 50 percent below its high-water mark), and only the operator owner resumes it.
- Eval: drive a book down through each level on a recorded tape; the three responses occur at their levels; at heat 8 the house book stops at its 35 percent ladder level, and with a heat ladder looser than the envelope it stops at 50 percent; resuming the stopped house book from a seat or the partner account is refused.
- Traces to: intent section 6; RISK-05

**SPEC-078** [EVAL-078] THE system SHALL change envelope ceilings only through the operator owner action of SPEC-010.
- Eval: attempts by any seat to change a ceiling are refused and recorded.
- Traces to: intent section 3; ORG-05

**SPEC-079** [EVAL-079] WHEN open positions sharing a driver would exceed the configured share of book value (default 25 percent), THE system SHALL block further positions on that driver.
- Eval: build positions sharing one driver up to the cap; the next one is blocked naming the driver.
- Traces to: intent section 8 (US6); GRAPH-02

**SPEC-080** [EVAL-080] WHILE live execution is enabled, THE system SHALL block live orders in assets on the restricted list unless an owner acknowledgment record exists for that asset.
- Eval: with live enabled on recorded venue responses, a restricted-asset order is blocked; after an operator acknowledgment record for that asset, it passes; other restricted assets stay blocked.
- Traces to: intent section 3; SCHEME-03

**SPEC-081** [EVAL-081] THE system SHALL execute the risk gate and order release with no model call in their code paths.
- Eval: a static dependency check finds no model client reachable from these paths; runtime traces of a recorded run show zero model calls inside them.
- Traces to: intent section 3; TRIB-05

**SPEC-082** [EVAL-082] WHEN the risk gate vetoes an item, THE system SHALL not release it in the same cycle under any resubmission.
- Eval: resubmit a vetoed item with altered wording in the same cycle; it is not released.
- Traces to: intent section 3; ORG-06

**SPEC-083** [EVAL-083] WHEN a book's loss for the day reaches its daily loss limit, THE system SHALL stop new risk in that book until the next trading day of its primary class.
- Eval: hit the limit mid-day; no new risk until the next day; closing trades are still allowed.
- Traces to: intent section 6; RISK-04

**SPEC-084** [EVAL-084] THE system SHALL cap any position at the configured share of the instrument's average daily volume (default 2 percent) and SHALL plan exits of larger holdings in stages that each stay under the participation cap.
- Eval: a proposal exceeding the volume share is reduced to the cap; an exit plan for a large holding splits into stages each under the cap.
- Traces to: intent section 6; SCHEME-02

#### 2.1.8 Tribunal and gate chain

**SPEC-085** [EVAL-085] THE system SHALL attach a pro case and a con case to every position proposal before it reaches the gate chain.
- Eval: every proposal in a recorded run has both cases with distinct authors.
- Traces to: intent section 8 (US5); TRIB-01

**SPEC-086** [EVAL-086] WHEN a proposal exceeds the tribunal conviction or size threshold (defaults: conviction 0.7, or a position above 2 percent of book value), or an owner requests a tribunal, THE system SHALL open a tribunal before any order for it is released.
- Eval: proposals above threshold and owner-requested ones get tribunal records before any order; below-threshold ones do not.
- Traces to: intent section 8 (US5); TRIB-02

**SPEC-087** [EVAL-087] WHEN a tribunal opens, THE system SHALL assign two advocates from different model families, give each the configured research window (default 24 hours), and store each advocate's evidence dossier with sources.
- Eval: tribunal records show two distinct model families, dossiers created within the window, and every dossier claim linked to a stored source.
- Traces to: intent section 8 (US5); TRIB-02

**SPEC-088** [EVAL-088] THE system SHALL run each debate as opening, rebuttal, cross-examination and closing rounds in which every argument after the openings cites the opponent's immediately preceding argument, and every quoted source text matches the dossier.
- Eval: four round records per side exist in order; each post-opening argument references the prior opposing argument; quote checks against dossiers pass.
- Traces to: intent section 8 (US5); TRIB-02

**SPEC-089** [EVAL-089] THE system SHALL assign a judge from a third model family that rules against the published rubric with direction, conviction and reasons, without counting votes from any other seat.
- Eval: the judge's family differs from both advocates; the ruling has all three fields and rubric scores; no vote tally appears in its inputs.
- Traces to: intent section 8 (US5); TRIB-02

**SPEC-090** [EVAL-090] WHEN a tribunal rules, THE system SHALL take the ruling's direction and conviction as the plan's direction and conviction, with size set only by the risk gate.
- Eval: plans after rulings match the ruled direction; size equals the risk gate's output for the ruled conviction.
- Traces to: intent section 8 (US5); TRIB-03

**SPEC-091** [EVAL-091] THE system SHALL score every judge and advocate on the outcomes of the positions their rulings and cases supported, and SHALL publish the scores in the weekly report.
- Eval: after a recorded run with 20 resolved tribunals, per-judge and per-advocate scores exist and match recomputation from outcomes.
- Traces to: intent section 5; TRIB-04

**SPEC-092** [EVAL-092] THE system SHALL pass every proposal through a confidence gate (default: calibrated probability that the thesis holds of at least 0.55), a review by a seat on a model family different from the proposer's, and the deterministic risk gate, in that order, and SHALL stop the proposal at the first veto.
- Eval: proposals failing each gate stop there with the gate recorded; passing proposals show all three records in order with distinct families for proposer and reviewer.
- Traces to: intent section 3; TRIB-05

**SPEC-093** [EVAL-093] WHEN a committee memo proposes a new strategy or a position above the committee threshold, THE system SHALL require a written pre-mortem and a red-team challenge on record before approval.
- Eval: approving such a memo without either record fails; with both, approval proceeds.
- Traces to: intent section 8; TRIB-01

#### 2.1.9 Predictions, calibration and the prediction graph

**SPEC-094** [EVAL-094] WHEN a prediction is made, THE system SHALL commit it with a content hash, a sequence number, a commit timestamp and the hash of the previous commitment before its horizon opens.
- Eval: every prediction in a recorded run has the four fields; each commit time precedes its horizon; each record's previous-hash equals the prior record's hash.
- Traces to: intent section 5; PRED-01

**SPEC-095** [EVAL-095] THE system SHALL reject a reveal without a matching commitment, exclude late commitments from scoring, and score an unrevealed committed prediction as the worst possible outcome.
- Eval: a reveal without commit is rejected; a commit after horizon open is excluded; an unrevealed prediction receives the worst score.
- Traces to: intent section 5; PRED-01, PRED-04

**SPEC-096** [EVAL-096] WHEN verification runs, THE system SHALL recompute every prediction chain and report the first sequence number whose stored hash does not match.
- Eval: alter one historical record; verification reports exactly its sequence number; an unaltered store verifies clean.
- Traces to: intent section 5; PRED-01

**SPEC-097** [EVAL-097] WHEN predictions resolve, THE system SHALL compute Brier score, clipped log loss, calibration curve, expected calibration error and recalibration slope per seat, horizon and instrument class.
- Eval: on a recorded set of 300 resolved predictions, every metric matches an independent computation to four decimals.
- Traces to: intent section 5; PRED-02

**SPEC-098** [EVAL-098] THE system SHALL report each scored group's skill against the base rate, persistence, a coin flip and, where a matching market exists, the market price at commit time, and SHALL withhold any skill claim below the configured minimum paired sample (default 200).
- Eval: reports show all applicable baselines; a group with 150 paired questions shows its numbers but no skill claim.
- Traces to: intent section 5; PRED-02

**SPEC-099** [EVAL-099] THE system SHALL use a prediction-market price only if its timestamp is at or before the commit time, SHALL accept market resolutions only in final states, SHALL exclude markets already closed at commit time, and SHALL record any disagreement between its declared resolution source and the market's resolution.
- Eval: a market price stamped after commit is refused; a non-final resolution is ignored; a closed market is excluded; a planted disagreement is recorded.
- Traces to: intent section 6; PRED-03

**SPEC-100** [EVAL-100] THE system SHALL report forecast quality separately from trading return in every performance report.
- Eval: every weekly report has distinct forecast and return sections with no blended score.
- Traces to: intent section 5; PRED-02

**SPEC-101** [EVAL-101] WHEN a seat's recalibration slope is below 0.8 on at least 200 resolved predictions, THE system SHALL raise an overconfidence alert and apply the fitted recalibration to that seat's future probabilities until the slope recovers.
- Eval: a seeded overconfident seat triggers the alert at 200 resolved predictions and its next probabilities are recalibrated; a calibrated seat triggers nothing.
- Traces to: intent section 5; PRED-02

**SPEC-102** [EVAL-102] THE system SHALL record for every prediction its drivers (each with a type and, for scheduled events, a time) and its links to other predictions (each with sign, strength and lag).
- Eval: every prediction in a recorded run has at least one driver; every link has sign, strength and lag; scheduled drivers have times.
- Traces to: intent section 8 (US6); GRAPH-01

**SPEC-103** [EVAL-103] THE system SHALL flag incoherent sets of related predictions, including a joint probability above either marginal and same-direction calls on a negatively linked pair.
- Eval: seed both incoherence types; both are flagged; coherent sets are not.
- Traces to: intent section 8 (US6); GRAPH-02

**SPEC-104** [EVAL-104] WHEN a driver resolves, THE system SHALL flag every prediction linked to it, directly or through links, for update by the next cycle.
- Eval: resolve a driver feeding a two-level link chain; all dependents are flagged by the next cycle and none outside the chain are.
- Traces to: intent section 8 (US6); GRAPH-02

**SPEC-105** [EVAL-105] THE system SHALL report weekly the calibration and score of predictions grouped by analytical complexity (driver and link count).
- Eval: the weekly report has a complexity table with at least three buckets and their metrics.
- Traces to: intent section 5; GRAPH-03

#### 2.1.10 Special situations and market integrity

**SPEC-106** [EVAL-106] THE system SHALL score assets on the configured scheme indicators (including payout promises above market rates, recruitment-linked rewards, unverifiable backing, operator history, withdrawal friction and capital diversion to new ventures) and SHALL store each score with its evidence, classifying an asset as a scheme at the configured threshold (default 0.6 on a 0 to 1 scale).
- Eval: on a recorded case set of 10 known schemes and 10 ordinary assets, every scheme scores above every ordinary asset at the configured threshold, and every score cites stored evidence.
- Traces to: intent section 8 (US7); SCHEME-01

**SPEC-107** [EVAL-107] WHEN a scheme-flagged asset is held, THE system SHALL publish a daily collapse-hazard estimate with its inputs, including the trend and rate of change of net inflow proxies.
- Eval: for a held scheme asset in a recorded run, a daily hazard record with inputs exists for each day.
- Traces to: intent section 8 (US7); SCHEME-01

**SPEC-108** [EVAL-108] WHILE a scheme position is held, THE system SHALL keep it only while the expected daily payout exceeds the expected daily loss from collapse hazard (net of expected recovery), clawback exposure on gains already withdrawn, and withdrawal costs, and SHALL exit in stages sized to observed liquidity and withdrawal limits, starting early enough that the planned stages complete before that expected daily loss reaches twice the payout rate.
- Eval: on a recorded scheme case with known collapse date, recovery fraction, clawback probability and withdrawal costs, the exit begins on the first day expected loss exceeds payout, every stage is within liquidity and withdrawal limits, and the planned completion precedes the doubled-loss date.
- Traces to: intent section 8 (US7); SCHEME-02

**SPEC-109** [EVAL-109] THE system SHALL place every asset whose scheme score crosses the threshold on the live restricted list automatically, and SHALL allow simulated positions in it only in books whose heat meets the configured minimum (default 9, the first heat whose eligibility tier includes payout schemes).
- Eval: crossing the threshold adds the asset to the list; a heat-8 book's order for it is rejected in simulation; a heat-9 book's order fills.
- Traces to: intent section 3; SCHEME-03

**SPEC-110** [EVAL-110] THE system SHALL flag pump-and-dump activity, wash-traded volume, spoofing patterns and liquidation cascades from market data, and SHALL block new entries in a flagged instrument for the configured window (default 60 minutes after the last flag).
- Eval: on recorded tapes containing each pattern, flags appear and entries inside the window are blocked; clean tapes raise no flags above the configured false-positive rate.
- Traces to: intent section 8 (US7); MANIP-01

**SPEC-111** [EVAL-111] THE system SHALL refuse order patterns that would trade against the firm's own resting orders, place and cancel large orders to move price, or coordinate orders across books to move price.
- Eval: attempts of each pattern are refused at the order layer with a conduct record.
- Traces to: intent section 3; MANIP-02

**SPEC-112** [EVAL-112] THE system SHALL produce no content addressed to third parties that promotes an asset or invites investment.
- Eval: every outbound message in a recorded run goes only to owner accounts; a seat attempt to draft promotional content for external audiences is refused and recorded.
- Traces to: intent section 3; SCHEME-04

#### 2.1.11 Logs, reports and education

**SPEC-113** [EVAL-113] THE system SHALL keep an append-only running log for every position and every book, and SHALL reject edits to existing entries.
- Eval: every fill and hourly analysis appears in the right logs; an attempted edit of an existing entry is rejected.
- Traces to: intent section 8 (US1); LOG-01

**SPEC-114** [EVAL-114] THE system SHALL annotate each book's log at least daily with an assessment of the day's entries.
- Eval: every active book's log has a daily assessment entry referencing that day's entries.
- Traces to: intent section 5; LOG-02

**SPEC-115** [EVAL-115] THE system SHALL publish the daily report by 06:00 Pacific time with these sections: firm summary, house book, every other book in brief, decisions with reasons, tribunal outcomes, predictions committed and resolved, calibration, risk events, costs, lessons, and the next day's watch list.
- Eval: for each day of a recorded week, the report exists by 06:00 Pacific with every section non-empty or marked "none today".
- Traces to: intent sections 4, 8 (US2); RPT-01

**SPEC-116** [EVAL-116] THE system SHALL publish a weekly report with strategy review, promotions and demotions, tribunal scores, target feasibility, an institution study note and the macro book review.
- Eval: the weekly report of a recorded 8-day run contains all six parts.
- Traces to: intent section 8 (US2); RPT-01, INST-01, MACRO-01

**SPEC-117** [EVAL-117] THE system SHALL publish a monthly statement per book that quotes the ledger chain head.
- Eval: the monthly statement's quoted head equals the ledger head at statement time.
- Traces to: intent section 5; LEDGER-01

**SPEC-118** [EVAL-118] THE system SHALL publish an opportunity list in which each high-conviction opportunity carries a goodness score from 1 to 10, its reasons, its direction and the supporting track record of the strategy and seats behind it.
- Eval: every listed opportunity has the four elements; the track-record figures match the scored record.
- Traces to: intent section 8 (US2); RPT-02

**SPEC-119** [EVAL-119] THE system SHALL attach to every reported decision a plain-language explanation of the concept behind it, a glossary link, a note on who is on the other side of the trade, the condition that would change the firm's mind, and the lesson recorded when it resolves.
- Eval: sample 50 decisions from a recorded week; each carries all five elements (the lesson once resolved).
- Traces to: intent section 8 (US2); EDU-01

**SPEC-120** [EVAL-120] THE system SHALL maintain a glossary that gains an entry the first time a report uses a concept, and SHALL follow a weekly curriculum of lesson topics recorded in the weekly report.
- Eval: every concept linked in a recorded week's reports has a glossary entry created on or before first use; the weekly report names the week's lesson topics.
- Traces to: intent section 8 (US2); EDU-01

**SPEC-121** [EVAL-121] THE system SHALL publish a target-feasibility report weekly and on owner request stating, from the firm's own record: the win rate required for 1, 2 and 3 percent per day at current payoff ratios and trade frequency, realized edge, probability of averaging each target over 30 and 90 days at current sizing, the sizing each target would require, risk of ruin at current and required sizing, and the daily value-at-risk budget equivalent to each target, each with an interval.
- Eval: on a recorded trade record, every figure matches an independent recomputation within 0.5 percentage points and every figure carries an interval.
- Traces to: intent sections 1, 5; RISK-01, RISK-02

**SPEC-122** [EVAL-122] WHEN an owner requests a report on a topic or asset, THE system SHALL deliver it in the deep research format of SPEC-039 with its sources.
- Eval: an owner request produces a report with the nine sections and stored sources.
- Traces to: intent section 8 (US3); RES-02

**SPEC-123** [EVAL-123] THE system SHALL publish a weekly institution study note on the reference institution's practices and on changes in major funds' public holdings filings.
- Eval: each weekly report links a study note that cites at least one filing or primary document.
- Traces to: intent section 8 (US10); INST-01

**SPEC-124** [EVAL-124] THE system SHALL run a standing macro book covering recession and bear-market positioning, policy-shock hedges and contrarian positions, and SHALL review it weekly.
- Eval: the macro book exists with positions tagged to these themes, and the weekly report includes its review.
- Traces to: intent section 8 (US10); MACRO-01

#### 2.1.12 Owner portal and console

**SPEC-125** [EVAL-125] THE system SHALL provide exactly two owner accounts (operator and partner) with password authentication, expiring sessions and lockout after repeated failures.
- Eval: both accounts sign in; a third account cannot be created through the portal; ten failed attempts lock the account for the configured period; an expired session is refused.
- Traces to: intent section 7; PORT-01

**SPEC-126** [EVAL-126] THE system SHALL show owners the books, positions, logs, reports, predictions, tribunal records, seat status and organization chart, sandboxes, heat dials, costs and ledger.
- Eval: each listed view loads for both owner accounts with data from a recorded run.
- Traces to: intent section 8 (US3); PORT-01

**SPEC-127** [EVAL-127] WHEN an owner asks any seat a question, THE system SHALL deliver an attributed answer citing its records by the end of the next cycle without delaying any scheduled step.
- Eval: questions submitted during a recorded run get answers within one cycle; the cycle completion rate is unchanged.
- Traces to: intent section 8 (US3); PORT-03

**SPEC-128** [EVAL-128] WHEN an owner sends the chief executive an idea or instruction, THE system SHALL acknowledge it within one cycle and record its disposition (adopted, adapted or declined) with reasons within one day.
- Eval: an idea submitted in a recorded run has an acknowledgment within one cycle and a disposition with reasons within one day.
- Traces to: intent section 8 (US3); ORG-04

**SPEC-129** [EVAL-129] THE system SHALL let each owner open, fund with theoretical cash, trade, and close sandbox books, and propose sandbox trades for agent review.
- Eval: an owner completes each action; a proposed trade receives a seat review record.
- Traces to: intent section 8 (US3); WAL-03

**SPEC-130** [EVAL-130] THE system SHALL show both owners the current and effective heat of every dial, its ceiling, and its change history.
- Eval: the dial view lists every dial with the four fields matching the records.
- Traces to: intent section 8 (US3); HEAT-02

**SPEC-131** [EVAL-131] THE system SHALL show the live switch only to the operator account, require a typed confirmation phrase, and display the readiness scorecard beside it.
- Eval: the partner view has no live switch; the operator's switch refuses without the exact phrase; the scorecard is visible beside it.
- Traces to: intent section 3; LIVE-01, LIVE-03

**SPEC-132** [EVAL-132] THE system SHALL end every message to the partner with the line 786110, and SHALL not show 786110 on any error, loss or alert screen.
- Eval: all partner messages in a recorded run end with the line; error, loss and alert screens contain no 786110.
- Traces to: intent section 3; PORT-02

**SPEC-133** [EVAL-133] THE system SHALL compute a readiness scorecard of resolved predictions, weeks of record, calibration, net return after costs, maximum drawdown and feasibility, labeled as guidance.
- Eval: the scorecard shows all six items matching recomputation and the guidance label.
- Traces to: intent section 5; LIVE-03

**SPEC-134** [EVAL-134] THE system SHALL send each owner a notification for envelope changes, book stops, budget alerts, live switch changes and pauses.
- Eval: each event type in a recorded run produces notifications to both owners within one cycle.
- Traces to: intent section 6; ORG-04

#### 2.1.13 Durability, cost and operations

**SPEC-135** [EVAL-135] WHEN the system restarts at any boundary (before commit, after commit, after submit, after acknowledgment), THE system SHALL resume with no lost and no duplicated predictions, orders, fills or ledger entries.
- Eval: inject a crash at each boundary in 100 randomized trials; post-recovery counts equal the no-crash reference run in every trial.
- Traces to: intent sections 4, 6; DUR-01

**SPEC-136** [EVAL-136] THE system SHALL meter every model call against the calling seat's budget and the firm budget, alert at 50 and 80 percent, pause the seat at 100 percent, and have the chief executive reassign or defer the seat's work.
- Eval: drive a seat through 50, 80 and 100 percent; alerts fire at each threshold; the seat pauses at 100; a reassignment or deferral record follows within one cycle.
- Traces to: intent section 3; COST-02

**SPEC-137** [EVAL-137] THE system SHALL keep total monthly running cost at or under the firm ceiling (default 25 US dollars) by throttling non-essential seats first, while reserving budget for risk, execution, records and reporting seats.
- Eval: a recorded month with a raised call load stays at or under the ceiling; throttle records name non-essential seats first; reserved seats never pause.
- Traces to: intent sections 3, 4; COST-01

**SPEC-138** [EVAL-138] THE system SHALL keep credentials and account identifiers out of every model prompt, and in live mode SHALL send position data only on routes configured as not used for training.
- Eval: scan every prompt of a recorded run for credential and identifier patterns: zero matches; in live mode on recorded responses, prompts with position data go only to no-training routes.
- Traces to: intent section 3; COST-03, LIVE-02

**SPEC-139** [EVAL-139] THE system SHALL read model routes, model identifiers, endpoints and prices only from configuration.
- Eval: a static scan of the source finds no model identifier literals outside configuration; changing a route in configuration changes the route used by the next call.
- Traces to: intent section 3; COST-01

**SPEC-140** [EVAL-140] THE system SHALL record a heartbeat for every active seat each cycle and open an incident record for the operations seat when a seat misses three consecutive heartbeats.
- Eval: silence one seat for three cycles; an incident record exists; healthy seats produce none.
- Traces to: intent section 6; DUR-02

**SPEC-141** [EVAL-141] THE system SHALL export all records daily to durable storage outside the primary store and SHALL restore a complete firm state from an export.
- Eval: restore from the latest export into an empty environment; record counts and chain heads equal the source.
- Traces to: intent section 4; DUR-01

**SPEC-142** [EVAL-142] THE system SHALL run the whole firm on a local runtime against recorded data through the same contracts as the cloud runtime.
- Eval: the quickstart's local run completes a recorded day and passes the same contract tests as the cloud runtime.
- Traces to: intent section 3; ROLE-02

**SPEC-143** [EVAL-143] THE system SHALL log every model call with seat, route, model identifier served, input and output token counts, cost, latency and outcome.
- Eval: every call record in a recorded run has all eight fields; summed costs equal the billing estimate.
- Traces to: intent section 5; COST-02

**SPEC-144** [EVAL-144] IF a model provider fails or times out, THEN THE system SHALL retry within the step's limits, fall back to the configured alternate route, and otherwise record the step skipped without recording a partial decision as complete.
- Eval: block the primary route; calls fall back; block both; the step is recorded skipped and no dependent decision is marked complete.
- Traces to: intent section 6; DUR-03

#### 2.1.14 Live path, disabled by default

**SPEC-145** [EVAL-145] THE system SHALL include live adapters for the configured venues that pass the shared order contract tests against recorded venue responses.
- Eval: each adapter passes the SPEC-069 suite on recorded responses.
- Traces to: intent section 3; LIVE-01

**SPEC-146** [EVAL-146] WHILE live execution is disabled, THE system SHALL make no network request to any venue order endpoint.
- Eval: a full recorded run with a network spy shows zero order-endpoint requests.
- Traces to: intent section 3; LIVE-01

**SPEC-147** [EVAL-147] WHEN live execution is enabled, THE system SHALL record a change event with actor, time, envelope snapshot and confirmation phrase, and SHALL refuse the change from any non-operator source.
- Eval: enabling from the operator account produces the record; from the partner account or any seat it is refused and recorded.
- Traces to: intent section 3; LIVE-01

**SPEC-148** [EVAL-148] WHEN live mode starts, THE system SHALL refuse credentials whose venue-reported permissions include withdrawal.
- Eval: recorded permission responses with withdrawal rights cause refusal; trade-only permissions pass.
- Traces to: intent section 3; LIVE-02

**SPEC-149** [EVAL-149] WHEN a live venue rejects an order, THE system SHALL record the venue's reason, leave the intended position unopened, and notify both owners.
- Eval: a recorded rejection produces the record, no position, and two notifications.
- Traces to: intent section 6; LIVE-01

**SPEC-150** [EVAL-150] WHILE live execution is enabled, THE system SHALL compare live fills with the virtual market's fills for the same orders and report divergence daily.
- Eval: on recorded live responses, the daily report shows per-order divergence matching recomputation.
- Traces to: intent section 5; LIVE-01

#### 2.1.15 Ledger and audit

**SPEC-151** [EVAL-151] THE system SHALL record money movements as balanced double entries in integer minor units, append-only and hash-sealed, with corrections only as reversing entries.
- Eval: every entry balances; an edit attempt is rejected; a correction appears as a reversal plus a new entry.
- Traces to: intent section 5; LEDGER-01

**SPEC-152** [EVAL-152] WHEN an owner requests a decision's history, THE system SHALL return its inputs, analyses, cases, tribunal, gates, sizing, orders, fills and outcome in one view.
- Eval: for 20 random decisions, the view contains all nine elements matching stored records.
- Traces to: intent section 5; ORG-07

**SPEC-153** [EVAL-153] THE system SHALL verify every hash chain (ledger, predictions, decision log) on demand and daily, reporting the first divergence per chain.
- Eval: alter one record in each chain; each verification reports the right first divergence; unaltered chains verify clean.
- Traces to: intent section 5; LEDGER-01

**SPEC-154** [EVAL-154] THE system SHALL export the audit trail for any date range in a documented open format.
- Eval: export a range; re-import into a fresh verifier; chains verify and counts match.
- Traces to: intent section 5; ORG-07

**SPEC-155** [EVAL-155] THE system SHALL record for every position-affecting action the model identifier served, the seat definition version, the inputs hash and the timestamp.
- Eval: every such action in a recorded run carries the four fields.
- Traces to: intent section 5; ORG-07

#### 2.1.16 Validation and promotion

**SPEC-156** [EVAL-156] THE system SHALL promote a strategy framework to capital only after out-of-sample validation clears the configured thresholds (defaults: win rate above 55 percent, average profit per trade above 0.5 percent, Sharpe ratio above 1.5, maximum drawdown under the heat ladder's second level, at least 10 trades per month), with promotion steps signed by seats other than the framework's author.
- Eval: a framework failing any threshold is not promoted; one passing all is promoted with signatures from non-author seats.
- Traces to: intent section 5; QA-01

**SPEC-157** [EVAL-157] THE system SHALL register every backtest trial, including failures, and SHALL report the probability of backtest overfitting and the trial-adjusted significance for each promoted framework.
- Eval: trial counts in reports equal the registry; promoted frameworks show both statistics.
- Traces to: intent section 5; QA-01

**SPEC-158** [EVAL-158] THE system SHALL re-validate promoted frameworks monthly and demote any that fail.
- Eval: a framework whose next month fails thresholds is demoted with a record.
- Traces to: intent section 5; QA-01

**SPEC-159** [EVAL-159] THE system SHALL test competing frameworks on the same out-of-sample data and record their comparison.
- Eval: a comparison record lists each competing framework's metrics on identical data windows.
- Traces to: intent section 5; QA-01

**SPEC-160** [EVAL-160] THE system SHALL fail its validation suite when a planted future price row or future text reaches a historical decision.
- Eval: plant each leak type; the suite fails naming the leak.
- Traces to: intent section 6; QA-03

**SPEC-161** [EVAL-161] THE system SHALL check automatically that every tool referenced by a seat's prompt or skills is on that seat's whitelist.
- Eval: add a reference to an unlisted tool in a role's prose; the check fails naming the seat and tool.
- Traces to: intent section 3; QA-05

**SPEC-162** [EVAL-162] THE system SHALL weight seat opinions in committee summaries by scored out-of-sample track record and SHALL never let those weights alter a hard limit.
- Eval: committee summaries show weights matching scored records; a heavily weighted seat's opinion never changes a limit outcome.
- Traces to: intent section 8; ORG-08

#### 2.1.17 Refinements from adversarial review and current practice

**SPEC-163** [EVAL-163] IF a regulator order, warning or enforcement release names an asset, its issuer or its operator, THEN THE system SHALL block every live order in that asset with no owner override, and SHALL label simulated positions in it as subject to that order.
- Eval: with live enabled on recorded venue responses, an asset with a recorded regulator order stays blocked even after an operator acknowledgment; simulated positions in it carry the order label.
- Traces to: intent section 3 constraint 9; SCHEME-03

**SPEC-164** [EVAL-164] THE system SHALL compute a quality score for each venue's reported volume and SHALL use quality-adjusted volume in every liquidity, sizing and signal calculation.
- Eval: on a recorded wash-volume tape, adjusted volume falls below reported volume by the venue's estimated fake share, and sizing reads adjusted volume.
- Traces to: intent section 6 failure 10; MANIP-01

**SPEC-165** [EVAL-165] WHEN open interest and funding both exceed their trailing 90th percentiles for an asset, or its spread exceeds the configured multiple of its trailing median (default 3), or its mark price diverges from its index beyond the configured limit (default 100 basis points), or a collateral asset deviates from an independent reference beyond the configured limit (default 100 basis points), THE system SHALL cap gross leverage and block new leveraged entries in the affected asset or collateral until the condition clears.
- Eval: on the recorded cascade tape the gate engages within one minute of the condition and releases after it clears; a planted collateral deviation suspends that collateral.
- Traces to: intent section 6; MANIP-01

**SPEC-166** [EVAL-166] THE system SHALL treat newly launched tokens and unvetted micro-capitalization securities as ineligible for live orders until they pass the configured launch and listing checks, and SHALL block new long entries within the configured window (default 7 days) before a scheduled token unlock above the configured share of circulating supply (default 5 percent).
- Eval: a recorded launch that fails the checks is ineligible for live orders; an entry 3 days before a 10 percent unlock is blocked.
- Traces to: intent section 6; MANIP-01

**SPEC-167** [EVAL-167] WHEN borrow cost and near-the-money call open interest both spike for a stock, or its short interest and days-to-cover exceed configured thresholds (defaults: 20 percent of float and 5 days), THE system SHALL block new short entries in it.
- Eval: a recorded squeeze setup blocks a new short; ordinary conditions allow it.
- Traces to: intent section 6; DIR-01, RISK-04

**SPEC-168** [EVAL-168] THE system SHALL report each strategy's results against buy-and-hold, equal-weight and moving-average crossover baselines, and SHALL run monthly replay ablations without memory, without debate and without the risk team, reporting each difference.
- Eval: the monthly report shows three baselines and three ablation differences per active strategy.
- Traces to: intent section 5; QA-01

**SPEC-169** [EVAL-169] WHEN skill is claimed for any of several personas, seats or strategies tested together, THE system SHALL adjust significance for multiple comparisons and report resampling intervals with each claim.
- Eval: with twenty personas tested together, claims use adjusted significance; a persona significant only before adjustment carries no skill claim.
- Traces to: intent section 5; PRED-02

**SPEC-170** [EVAL-170] WHEN a historical evaluation window starts, THE system SHALL freeze the memory and lessons available to seats at the window start and record which items each decision retrieved.
- Eval: lessons created during the window never appear in that window's decisions; every decision lists its retrieved items.
- Traces to: intent section 6; QA-03, QA-04

**SPEC-171** [EVAL-171] THE system SHALL run each tribunal judgment in both side orders, score a flipped verdict as a tie, give both advocates equal length budgets, and record each judge's flip rate and length sensitivity.
- Eval: a recorded tribunal is judged in both orders; a planted flip scores as a tie; unequal budgets are refused; flip rate and length sensitivity are recorded per judge.
- Traces to: intent section 8 (US5); TRIB-02, TRIB-04

**SPEC-172** [EVAL-172] THE system SHALL keep any added tribunal round, driver class or link type disabled until it improves out-of-sample Brier score over its parent configuration on a time-split holdout.
- Eval: an added round that fails to improve stays disabled; one that improves is enabled with its comparison recorded.
- Traces to: intent section 5; GRAPH-03

**SPEC-173** [EVAL-173] THE system SHALL include in each daily report two retrieval questions on concepts introduced on earlier days, schedule spaced review of glossary entries, and present each new opportunity as an idea note with thesis, valuation sensitivities, bull, base and bear cases, dated catalysts, risks and falsifiers.
- Eval: every daily report has two retrieval questions on concepts first used at least two days earlier; every idea note has all seven parts; glossary entries reappear on the review schedule.
- Traces to: intent section 8 (US2); EDU-01

**SPEC-174** [EVAL-174] THE system SHALL publish the head of every hash chain daily to a location outside the firm's own stores, and verification SHALL compare stored heads with the published ones.
- Eval: a daily anchor exists for each chain; an altered record yields a recomputed head that mismatches the published anchor.
- Traces to: intent section 5; PRED-01, LEDGER-01

### 2.2 Key entities

- **Owner**: one of two human accounts (operator, partner) outside the organization; holds envelope powers per SPEC-010.
- **Seat**: an agent role instance with a canonical definition version, tool authority classes, budget, cadence, reporting line and scored record.
- **Skill, rule, cycle**: canonical reviewable definitions; cycles are step graphs with gates and iteration caps.
- **Persona**: a virtual investor with worldview, risk profile, horizon, constraints, starting capital and heat; owns one persona book.
- **Book**: house, persona, strategy, owner sandbox or benchmark; owns a wallet, running log, heat, ladder and limits.
- **Wallet**: cash by currency, positions, lots, cost basis, realized and unrealized results, fees, borrow and funding.
- **Instrument**: tradable item with class, calendar, price sources, staleness limit, fee profile, short-side forms and liquidity statistics.
- **Market datum**: a price, quote, bar, rate, filing, article or indicator with source, retrieval time and effective time.
- **Analysis**: a seat output for one coverage dimension, linked to its tool results.
- **Plan**: a portfolio manager's intention in prose plus its compiled typed structure, versions, predictions, cases, tribunal and gate outcomes.
- **Proposal, case, tribunal, round, ruling**: the decision trail; rulings carry direction, conviction and rubric scores.
- **Gate outcome**: confidence, review or risk verdict with reasons and the seat or code path that issued it.
- **Order and fill**: the order interface records shared by the virtual market and live adapters.
- **Prediction**: question, outcome definition, probability, horizon, resolution source, commit record, drivers, links, reveal and score.
- **Driver and link**: drivers carry type and time; links carry sign, strength and lag between predictions.
- **Heat dial and envelope**: dial values per scope, the mapping table, ceilings and change history.
- **Restricted list entry and acknowledgment**: asset, reason, score evidence and owner acknowledgment.
- **Ledger entry**: balanced double entry in minor units with seal and previous seal.
- **Report**: daily, weekly, monthly, feasibility, deep research, opportunity list, institution note; with mode label, provenance and educational elements.
- **Glossary entry and curriculum topic**: concept, plain explanation, first use, linked decisions.
- **Budget meter and call record**: per seat and firm, with thresholds and the eight call fields of SPEC-143.
- **Change event**: owner envelope action with prior and new values and actor.
- **Incident**: missed heartbeats, reconciliation breaks, chain divergences and their resolutions.
- **Chain anchor**: a published chain head with its time and external location, compared during verification.

## 3. Success Criteria

### 3.1 Measurable outcomes

- **SC-001**: Over the first 30 days of operation, at least 99 percent of scheduled cycles complete (SPEC-028).
- **SC-002**: After any restart in the fault-injection suite, zero predictions, orders, fills or ledger entries are lost or duplicated (SPEC-135).
- **SC-003**: By day 30, at least 200 predictions are resolved and scored, with calibration and skill against baselines reported (SPEC-097, SPEC-098).
- **SC-004**: Each daily report is available by 06:00 Pacific on at least 29 of the first 30 days (SPEC-115).
- **SC-005**: Every reported decision carries all five educational elements (SPEC-119).
- **SC-006**: The weekly feasibility report's figures match independent recomputation within 0.5 percentage points (SPEC-121).
- **SC-007**: Total monthly running cost stays at or under the configured ceiling (default 25 US dollars) (SPEC-137).
- **SC-008**: Zero requests reach any venue order endpoint while live is disabled (SPEC-146).
- **SC-009**: Every seat compiles to both harness formats with a passing drift check (SPEC-013, SPEC-014).
- **SC-010**: Owner questions are answered within one cycle in at least 95 percent of cases (SPEC-127).
- **SC-011**: The opportunity list's goodness scores are accompanied by a measured hit rate per score band after 30 days (SPEC-118).
- **SC-012**: Every hash chain verifies clean daily (SPEC-153).

## 4. Assumptions

- The owners operate as two US persons; venue and data choices respect what US persons may access.
- Free and keyless data sources are sufficient for the first build; paid data is added only when a strategy shows it needs it and an owner raises the budget.
- Theoretical starting capital: house book 100,000 US dollars, each owner sandbox 10,000 US dollars by default, personas per their profiles; all values are configuration.
- Model routes for bulk work, typed decisions, review and judging come from at least three distinct model families; exact routes are configuration chosen in the plan.
- The 1 to 3 percent per day appetite is a calibration target; the firm reports its measured attainability rather than promising it.
- Reference institution model for organizational structure: a multi-manager platform with central risk, borrowing believability-weighted debate and public-filings study [INFERENCE, see intent section 12].

## 5. Eval index

Every clause binds one held-out evaluation with the same number: SPEC-001 binds EVAL-001 through SPEC-174 binding EVAL-174. Payloads (fixtures, planted faults, expected values) live in the external evaluator store recorded in `reset-handoff.md`; the implementing agent does not open them.

| Range | Capability | Stored at |
|-------|------------|-----------|
| EVAL-001 to EVAL-020 | Organization, seats, authority, portable definitions | external evaluator store |
| EVAL-021 to EVAL-030 | Cycles, calendars, durability | external evaluator store |
| EVAL-031 to EVAL-042 | Research, data, point-in-time integrity | external evaluator store |
| EVAL-043 to EVAL-052 | Books, personas, wallets, mode labels | external evaluator store |
| EVAL-053 to EVAL-062 | Plans and the plan language | external evaluator store |
| EVAL-063 to EVAL-072 | Virtual market | external evaluator store |
| EVAL-073 to EVAL-084 | Risk, heat, envelope | external evaluator store |
| EVAL-085 to EVAL-093 | Tribunal and gate chain | external evaluator store |
| EVAL-094 to EVAL-105 | Predictions, calibration, prediction graph | external evaluator store |
| EVAL-106 to EVAL-112 | Special situations and market integrity | external evaluator store |
| EVAL-113 to EVAL-124 | Logs, reports, education | external evaluator store |
| EVAL-125 to EVAL-134 | Owner portal and console | external evaluator store |
| EVAL-135 to EVAL-144 | Durability, cost, operations | external evaluator store |
| EVAL-145 to EVAL-150 | Live path, disabled by default | external evaluator store |
| EVAL-151 to EVAL-155 | Ledger and audit | external evaluator store |
| EVAL-156 to EVAL-162 | Validation and promotion | external evaluator store |
| EVAL-163 to EVAL-174 | Refinements: regulator orders, venue quality, cascade and depeg, launches and unlocks, squeezes, baselines and ablations, multiplicity, memory freeze, judge order, complexity budget, retrieval practice, external anchors | external evaluator store |
