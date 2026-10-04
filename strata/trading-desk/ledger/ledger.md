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

## [009] [audit-improve cycle 1] [decision]
- What: Audit pass re-verified all source SHAs via GitHub API (TA
  1394a3f72aa4393e1a98f51b382434c4b4c2d972, paperclip
  2a8a99e4a5f69aa803b3f10b982f583e75a87042, trading-firm template
  f05237347dadb56f73598f6f10760ea0f7ab0a54 — all resolve) and spot-checked
  extraction fidelity against upstream source.
- Why: strata contract integrity; extraction fidelity is the foundation of
  the extract play.
- Effect: found 5 factual/fidelity defects; all fixed in this cycle.
- Outcome: documented below.

## [010] [audit-improve cycle 1] [decision]
- What: Fixed extraction fidelity defect: the v2 extractor stamped the
  shared collaboration preamble (including "You have access to the following
  tools") on all 12 roles, but upstream only the analysts use it — and the
  sentiment analyst uses a shortened variant with no tool-range wording
  (upstream #1130: tool wording invites hallucinated tool calls). A v3
  extractor now pulls each role's preamble from its own source; the 8
  preamble-less roles (researchers, risk debators, trader, managers) carry a
  "not used" note. Re-ran over source verified to match the pinned SHA.
- Why: a harness copied from the v2 files would give tool-less agents a
  false tool affordance — a prompt-injection-grade defect for the extract
  play.
- Effect: `sources/tradingagents/extract_roles.py` (v3, committed for
  provenance); 11 of 12 agent files corrected; SOURCING.md documents the
  per-role preamble rule.
- Outcome: extraction verified faithful against upstream files.

## [011] [audit-improve cycle 1] [decision]
- What: Fixed remaining audit defects: completed two truncated tool entries
  in tools.md (get_macro_indicators, get_prediction_markets) from upstream
  docstrings; rewrote dataflows.md with accurate per-module vendor
  descriptions (fixes the truncated alpha_vantage entry) and captured the
  social-feed archival limitation for backtests; corrected Paperclip star
  count 38k -> ~97k (verified 96,764 via GitHub API) in intent.md section 9;
  corrected sources file count 22 -> 23 in README and standing.md; recorded
  the TA license as Apache-2.0 (verified).
- Why: factual accuracy of the curated sources.
- Effect: sources/tradingagents/{tools.md,dataflows.md,SOURCING.md},
  intent.md, README.md, standing.md.
- Outcome: done.

## [012] [audit-improve cycle 1] [decision]
- What: Drafted the first harness-layer artifacts (all marked DRAFT, pending
  ratification + scaffold play): `harness/agents/role-bindings.md`
  (placeholder-to-harness bindings for all 12 roles, pipeline order per
  SPEC-001..004), `harness/agents/debate-protocol.md` (opponent-opening
  marker, report-or-absent, trader price grounding, structured-output
  fallback, multilingual labeled lines), and
  `harness/tool-layer/venue-interfaces.md` (clamp contract, common adapter
  interface, per-class venues: Alpaca stocks/crypto paper, OANDA v20
  practice, Kalshi demo; Polymarket read-only for US persons).
- Why: the extract play's first input; keeps the harness prompt-authoring
  work on the corrected sources.
- Effect: new `harness/` tree (drafts only — no executable trading code, no
  secrets).
- Outcome: drafts complete; validator re-passed.
