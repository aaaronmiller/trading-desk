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

## [013] [audit-improve cycle 2] [decision]
- What: Re-audit of cycle-1 artifacts. Removed a leftover hedge in
  role-bindings.md (market analyst tool tuple now stated plainly after
  verification against upstream TOOLS); confirmed venue-interfaces.md's
  docs/open-questions.md reference matches the renamed file; confirmed no
  live-trading code paths or secrets in any new file.
- Why: cycle-1 artifacts must hold up under fresh eyes before more is built
  on them.
- Effect: harness/agents/role-bindings.md.
- Outcome: done.

## [014] [audit-improve cycle 2] [decision]
- What: Implemented the cheapest keyless evals: `harness/tool-layer/
  date_clamp.py` (pure-stdlib `as_of`, `clamp_window`, `in_window`,
  `coverage_gaps`, `feed_status`) plus `test_date_clamp.py` — 10 fixture
  checks mapping to EVAL-005 (no future-dated items), EVAL-006 (undated
  items), EVAL-007 (coverage gaps labeled unavailable). All 10 pass with no
  API keys, no network, no trading paths.
- Why: the point-in-time discipline is the project's core integrity claim;
  its cheapest testable surface is pure date logic, runnable now, long
  before any vendor integration.
- Effect: first executable harness code; paper/research-only.
- Outcome: 10/10 tests green.

## [015] [audit-improve cycle 2] [decision]
- What: Researched and wrote `docs/vendor-matrix.md`: cost, rate limits,
  and gotchas for Alpha Vantage, Yahoo/yfinance, FRED, SEC EDGAR, Alpaca
  data, OANDA, Polymarket, Reddit, StockTwits, X, plus execution-venue
  paper paths (Alpaca, OANDA, Kalshi) and practical takeaways. Notable
  captures: Alpaca free data is IEX-only (backtests won't match live SIP);
  legacy alpaca-trade-api defaults to the LIVE host; Reddit research via
  Data API is a policy violation per Reddit's own help centre.
- Why: Aaron needs this before choosing vendors for the backtest/paper
  phases; it also feeds the open venue question (intent section 11).
- Effect: docs/vendor-matrix.md (snapshot dated 2026-10-03, not a contract).
- Outcome: done.

## [016] [audit-improve cycle 2] [decision]
- What: Chose NOT to do this cycle: runnable harness agent definitions
  (actual LLM loops), venue adapter implementations, and the eval-manifest
  runner. All are gated on intent/spec ratification and the scaffold play;
  building them now would bake in unapproved assumptions. The DRAFT
  interface specs and bindings stand in their place.
- Why: the strata contract's own halt conditions say not to build downstream
  of a DRAFT contract.
- Effect: nothing built; recorded as deferred work for post-ratification.
- Outcome: pending Aaron's ratification.

## [017] [0.1] [decision]
- What: Specification preparation (spec-prep 2.4.0, Spec Kit native) for the autonomous trading firm, with the trading-desk repository as build root on branch 001-autonomous-trading-firm. The legacy pack moved to sources/legacy/strata-2026-10-03 as superseded source; this ledger moved with it and continues here.
- Why: owner request T6 ("modify and improve the selected base project ... use the spec-prep skill ... restart session after spec-prep and before implementation").
- Effect: specs/001-autonomous-trading-firm/ holds intent, spec, plan, substrate, ledger; legacy files unchanged in content.
- Outcome: done.

## [018] [1.1] [decision]
- What: Confidence gate scored 86 percent weighted after the owners answered the preparation questions (money mode, success measures, partner mandate, repository). Hosting and cost ceiling were not answered; the default (paid edge plan, 25 dollars per month all in) is recorded as an assumption and as intent question 1.
- Why: confidence-gate rubric; the answers raised problem, success and constraint dimensions above 75 percent; technical constraints stayed near 75 percent because hosting was unanswered.
- Effect: intent.md section 12 carries three NEEDS CLARIFICATION markers with defaults.
- Outcome: pending owner answers; defaults apply if unanswered.

## [019] [1.2] [decision]
- What: Owner message T9 recorded verbatim: aggressive mandate, a payout-scheme lifecycle case study (kept in the private intake record), exit timing from rate-of-change signals, manipulation awareness, a reference institution to study, educational daily reports, heat dials, a cross-family debate tribunal with a third-family judge, both-direction bets and linked predictions.
- Why: new owner intent mid-preparation.
- Effect: requirements v0.2.0 added HEAT, SCHEME, MANIP, TRIB, DIR, GRAPH, EDU, INST and MACRO; spec clauses SPEC-073 to SPEC-112 and SPEC-119 to SPEC-124 trace to it.
- Outcome: done.

## [020] [1.3] [decision]
- What: Resolved the 27 conflicts found in the local intent inventory (R11 section 6) per the table in requirements v0.2.0: no human waits in the trading loop; the operator holds the live switch and ceilings, either owner pauses; leverage allowed with a 3x default ceiling; cloud from day one; the house book stops at 50 percent below its high-water mark and only the operator resumes it; the paper bar is guidance; the sandbox is separate from evaluation; Paperclip is an export target, not the runtime.
- Why: the newest owner statements (T3, T4, T7, T9) and the MOU addendum govern older plans.
- Effect: intent sections 3 and 6; SPEC-010, SPEC-076, SPEC-077, SPEC-133.
- Outcome: done. Dissent preserved: R11 recommended telling agents the capital is virtual; the owner's directive (T6, "the agent is not to know") governs, and honesty is kept by deterministic owner-facing labels (SPEC-051, SPEC-052). What would change the ruling: evidence that concealment degrades audit honesty or seat behavior.

## [021] [2.1] [outcome]
- What: Research waves. Wave 1 (Haiku scouts R01 to R12) covered role packs, markdown skill packs, firm structure, harness formats, LLM trading literature, prediction-market calibration, market data and venues, strategy and persona library, hosting and providers, starred repositories, the local intent corpus and build-versus-adopt. Wave 2 (R13 to R16) covers payout-scheme lifecycle and clawback law, manipulation awareness, institutional practice and education, and debate tribunals with prediction graphs.
- Why: owner request for deep and wide research with low-cost models, arXiv literature, prediction markets and mining existing projects.
- Effect: research.md synthesizes them; intent section 10 holds prior art.
- Outcome: partial verification. The shared web-search budget ran out mid-wave, a usage limit paused all scouts for about four hours, and the environment's egress policy blocked arXiv, most vendor documentation and every market-data host; affected claims are marked "(verify)" in the reports.

## [022] [3.1] [decision]
- What: Architecture derived as a greenfield, runtime-agnostic TypeScript core with a Cloudflare Workers run plane (Cron Triggers, deterministic Workflow instances, one Durable Object per book, D1 record, R2 artifacts), an in-house seat runner, and generated harness workspaces (plan CTX-001 to CTX-021).
- Why: intent constraints 4 to 6 and the cost ceiling. R12 recommended adopting Paperclip as the operating base and forking Vibe-Trading; rejected as the runtime because harness-process heartbeats and an always-on server exceed the ceiling and a Python trading service conflicts with the owners' stack; Paperclip remains an export target and Vibe-Trading, LEAN, Nautilus, ai-hedge-fund and TradingAgents remain concept sources.
- Effect: plan.md.
- Outcome: pending build. Empirical memory: none deployed; research-based.

## [023] [3.2] [decision]
- What: Default model route profile "economy-api" (Muse Spark Contributor for bulk content without identifiers, Jev for typed decisions, DeepSeek V4 Flash for review and the second advocate, a Claude model as third-family judge); the subscription profile is excluded from the always-on loop unless the operator accepts its terms risk in a recorded change. Budget meter throttles to the ceiling.
- Why: owner decision D-15 (Muse allowed for strategy), owner rule CO-13 (no unsettled consumer subscriptions in the always-on loop), R09 cost and terms findings.
- Effect: plan CTX-009, CTX-010; intent question 2.
- Outcome: pending owner answer to intent question 2.

## [024] [4.1] [decision]
- What: Initialized Spec Kit 1.2.3.dev0 with the Claude integration in the build root after confirming on a clean branch that it adds only .specify/ and .claude/skills/speckit-*.
- Why: spec-prep requires native Spec Kit paths.
- Effect: .specify/, .claude/skills/speckit-*.
- Outcome: done.

## [025] [4.2] [decision]
- What: Constitution v1.0.0 with eleven principles (simulation by default; deterministic risk authority; point-in-time integrity; honest measurement; durable idempotent operation; one canonical definition many harnesses; cost discipline; security and untrusted input; evidence-gated delivery; owner sovereignty with humans outside the loop; lawful market conduct).
- Why: owner statements T1 to T9, T7 "simulate; live code off", T6 gates request.
- Effect: .specify/memory/constitution.md.
- Outcome: done; ratified by launching the build.

## [026] [4.3] [decision]
- What: spec.md v1.0 with 162 EARS clauses and intent.md v1.0; held-out evaluations EVAL-001 to EVAL-162 stored outside the build repository in the intake folder's evaluator-only directory, mirrored to the default spec-prep store in this container.
- Why: spec-prep rules 1 and 3.
- Effect: spec.md, intent.md, external evals.
- Outcome: done. Isolation is procedural only: anyone with access to the intake repository can read the evaluations.

## [027] [4.4] [outcome]
- What: The installed spec-prep validator fails to run (two identifiers that are not valid Python). A project copy patched only in those identifiers lives at .specify/gates/spec-prep-validate.py with the upstream hash in its header.
- Why: a check never observed running is not a check.
- Effect: validation uses the patched copy until the skill is fixed upstream.
- Outcome: patched copy parses and runs; intent and spec audit passed.

## [028] [4.5] [outcome]
- What: The build environment's network policy blocks every market-data host and the deployment API; the owner was told which hosts and secrets to add.
- Why: the fresh build session needs them for live smoke tests and deployment.
- Effect: tests run on recorded fixtures; deployment falls back to a dry run with a documented manual step until the settings change.
- Outcome: pending owner environment change.
