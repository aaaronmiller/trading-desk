# Ledger — trading-desk

> Append-only. Never edited, never reordered, never pruned.

## [001] [kickoff] [decision]
- What: Project kicked off from the approved plan: extract durable domain
  content from the TradingAgents research framework and re-house it as
  harness-based agents under Paperclip-style orchestration.
- Why: intent section 9 (prior-art analysis: lab-vs-firm division).
- Effect: repo aaaronmiller/trading-desk created; sources/ curated;
  strata tree authored.
- Outcome: pending human ratification of intent/spec.

## [002] [kickoff] [decision]
- What: Harness-over-framework chosen for the live path; the research
  framework retained as the reference lab, not ported 1:1.
- Why: intent section 9 (avoid framework-fused orchestration); the durable
  value is prompts, tools, and evaluation discipline.
- Effect: context.md CTX-001; sources/ deliberately excludes graph wiring,
  CLI, checkpointing.
- Outcome: pending.

## [003] [kickoff] [decision]
- What: Paper-first-then-live is a non-negotiable gate; live execution is
  not built in phase 1, only the simulated order sink.
- Why: intent section 3.
- Effect: SPEC-009/010/011; context.md CTX-005; paper-run play halt
  conditions.
- Outcome: pending.

## [004] [kickoff] [decision]
- What: Venue classes fixed at stocks, crypto, forex, prediction markets;
  per-class adapters behind a common interface with per-class risk limits.
- Why: intent section 8.
- Effect: SPEC-019/020; context.md CTX-006.
- Outcome: pending.

## [005] [kickoff] [decision]
- What: Management layer (org chart, heartbeats, budgets, approvals, audit)
  adopted for scheduling, cost control, and governance rather than
  reimplemented.
- Why: intent section 3 (human governance, spend ceilings) and section 4
  (replayable history); prior-art gap analysis.
- Effect: context.md CTX-002; SPEC-012/013/014.
- Outcome: pending.

## [006] [kickoff] [decision]
- What: Three open questions recorded as [NEEDS CLARIFICATION] in intent
  (paper-to-live quantitative bar; starting capital per venue; specific
  venues/accounts) instead of stalling the kickoff.
- Why: confidence gate scored ~83%; these dimensions are genuinely below
  threshold and materially change scope.
- Effect: intent.md section 11.
- Outcome: awaiting Aaron's answers.

## [007] [kickoff] [decision]
- What: Living Documents `ld` unavailable in this environment; strata
  artifacts live in the repo tree at strata/trading-desk/ with no permanent
  dossier home yet.
- Why: `ld` resolves to the GNU linker here; fallback per the skill.
- Effect: noted in delivery summary; revive protocol reads
  strata/trading-desk/ledger/standing.md + ledger tail.
- Outcome: pending a future dossier home.

## [008] [depth-verification] [decision]
- What: Independent depth-verification review of the strata tree found 3
  blocking and 8 should-fix issues; all were fixed before push.
- Blocking fixes: added SPEC-021 (paper-to-live gate: ratified bar, cleared
  results, human approval as a change event); scoped SPEC-011 to phase 6+;
  qualified SPEC-019 with US-person venue availability.
- Should-fix: settlement horizon and drawdown metric defined as
  human-configured; analyst dimensions generalized per venue class;
  SPEC-002 requires quoting an opposing claim; backtest resume cadence;
  deploy precondition is ratified AND cleared; commit play exempts
  system-owned artifacts; CTX-002 cites intent section 6; dropped the
  untraced local-machine line from context section 6.
- Effect: spec has 21 clauses; eval manifest has 21 evals; validator re-run.
- Outcome: passed.
