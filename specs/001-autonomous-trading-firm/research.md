---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [research, decisions, prior-art, verification, derived]
layer: derived
---
# Research: Autonomous Trading Firm

Phase 0 output. Sixteen research reports (R01 to R16) live in the private intake repository (`new-assignments/autonomous-trading-firm/sources/research/`); each cites sources with access dates and marks unconfirmed claims "(verify)". This file records the decisions they support, the alternatives rejected and what the build must verify live. Owner-intent material stays in the intake; nothing here names the partner.

## Research conditions

- Scouts ran on a low-cost model family as the owners asked. The shared web-search budget ran out mid-wave, a usage limit paused all scouts twice, and the environment's egress policy blocked arXiv, most vendor documentation and every market-data host. Facts that rest on search excerpts carry "(verify)" in the reports. The build's first live smoke test (task T190) converts each needed "(verify)" into a recorded observation or a ledger correction.
- No cloned third-party code was run. Licenses were read from repository files.

## Decisions

### D1. Greenfield core with borrowed concepts (R01, R02, R12)
- Decision: build a runtime-agnostic TypeScript core and our own seat runner; borrow concepts, never code, from TradingAgents (role prompts, reflection loop), ai-hedge-fund (deterministic blend, validator, hash-chained ledger), Vibe-Trading (team presets, multi-asset coverage), FinRobot (code overrides verdicts), HyperGrok and tradermonty (single order-writing role, workflow manifests with gates), alliela and AI Market Maker (code gates).
- Rationale: R12 found no project above 18 of 26 capability points and four capabilities nobody has (personas with risk profiles, a typed plan language, a calibrated prediction registry, budgeted routing). Its hybrid recommendation (Paperclip as operating base plus a Vibe-Trading fork) fails the cost ceiling and the owners' stack (see D2).
- Alternatives rejected: fork TradingAgents (graph-framework plumbing; LLM portfolio manager without a code gate); fork ai-hedge-fund (no costs in fills, no live path, no runtime); adopt Paperclip as runtime (harness-process heartbeats and an always-on server).
- Kept: an Agent Companies export so the firm can run under Paperclip if the owners ever want it.

### D2. Run plane on Workers Paid with Workflows, Durable Objects, D1 and R2 (R09)
- Decision: Cron Triggers create Workflow instances with deterministic identifiers; duplicate creations are skipped; each external effect is its own step; one Durable Object per book serializes orders.
- Rationale: estimated platform usage fits inside included allowances; the plan's floor cost is about 5 dollars; Durable Object alarms give at-least-once wakeups with retries (R09, verify limits).
- Alternatives rejected: small virtual server (maintenance, single point of failure), Inngest (about 138 dollars per month at this volume), Vercel (Hobby plan non-commercial; Pro breaks the ceiling), Pi Durable as the cycle engine (experimental; possible later adapter on Durable Objects).

### D3. Model routes and cost (R09, vantage plan, owner decisions)
- Decision: route profile "economy-api" by default; at least three model families; subscription and prompt-training routes handled as in plan CTX-009; budget meter throttles to the ceiling.
- Rationale: R09 estimates 34 to 44 dollars per month of model spend at steady state on bulk API routes (verify), above the 25-dollar default ceiling, so throttling or a raised ceiling is required; R09 cautions against unattended loops on consumer subscriptions and against sending proprietary text to prompt-training tiers. The owners chose the prompt-training tier for strategy work (decision D-15) and set the rule against unsettled subscriptions (CO-13); the design honors both.
- Verify at build: every route's endpoint, model identifier, price, rate limit and structured-output support.

### D4. Market data and venues (R07)
- Decision: keyless public sources first, labeled by feed quality; Alpaca's free key for US equities, funds and options; Yahoo and similar sources research-only; perpetual data read-only from venues US persons cannot trade; live adapters for Coinbase Advanced, Alpaca and Kalshi only.
- Rationale: R07 found Alpaca the only free source combining paper trading, IEX data, a calendar and corporate actions; Yahoo is personal-use; Stooq reports key gating in 2026; perpetual venues with public data restrict US persons; Kalshi hostnames conflict between its SDK and documentation (verify).
- Fees and models: square-root market impact; participation caps; perpetual funding accrual per venue interval (default 0.01 percent per 8 hours when history is missing); Section 31 and FINRA fees on sales only (rates verify).
- Calendars: XNYS closures for 2026 agree across two libraries; CME Globex 17:00 to 16:00 Central; spot FX Sunday 17:00 to Friday 17:00 New York.

### D5. Point-in-time and evaluation discipline (R05, R11)
- Decision: three timestamps per datum; next-price execution; undated items excluded; masking of names and dates in replays; lessons gated by resolution time; leak suite with planted future rows and text; monthly ablations (no memory, no debate, no risk team); baselines buy-and-hold, equal-weight and moving-average crossover; Holm adjustment across personas; resampling intervals on skill claims.
- Rationale: R05 found standard models lose most of their apparent alpha under look-ahead audits while point-in-time models do not (Look-Ahead-Bench, verify); FINSABER-2 defaults (next-open execution, 5 basis points slippage, 2.5 percent liquidity cap); reported multi-agent Sharpe ratios come from short, cost-free windows; the risk-manager role is the most attackable by poisoning, which is why no model sits in the risk path. R11 found the legacy clamp date-only and its leak test blind to future price rows.

### D6. Prediction calibration against markets (R06, R16)
- Decision: score Brier, clipped log loss, calibration, expected calibration error and recalibration slope; skill against market price at commit time; minimum 200 paired questions before skill claims (R06 arithmetic suggests 800 to 1,800 for a 0.02 Brier edge); resolve only final states; aggregate seats with trimmed means by default and logit pooling only after out-of-sample validation.
- Rationale: Halawi et al. 2024 beat the crowd only on a subset; ForecastBench shows superforecasters ahead; PolyBench reports models losing money while overconfident (verify identifiers).

### D7. Organization and decision culture (R03, R15)
- Decision: multi-manager structure with central risk, chief investment officer allocation, persona and strategy portfolio managers as pods, red team as challenger, second-line risk and compliance, operations split so no seat proposes, approves, executes, books and reconciles the same action; believability weights from scored records; pre-mortems and red-team challenges on committee memos; internal audit reporting to owners.
- Rationale: R03 and R15 both recommend the pod platform (independent allocations, mechanical cuts, reallocation) and Bridgewater-style believability weighting; pod drawdown figures (trim near 5 percent, removal near 7.5 percent) are press-reported and conflict, so the firm's ladders come from the heat table, not copied figures.
- Teaching design (R15): concept cards, counterparty notes, falsification triggers, lessons log, glossary with spaced review and two retrieval questions per daily report (Dunlosky et al. 2013 rate practice testing and spaced practice highest); idea notes follow a sell-side initiation shape (thesis, valuation sensitivities, bull, base and bear cases, dated catalysts, risks, falsifiers); the 1 to 3 percent per day appetite is also shown as its equivalent daily value-at-risk budget.

### D8. Strategy and persona library (R08)
- Decision: 28 personas (20 active at launch) and about 40 strategy templates as canonical files; heat curve from R08 for heats 1 to 7, extended to the envelope for 8 to 10; 1/N benchmark in every persona report; hierarchical risk parity as default allocator under short histories; volatility overlay on risk sleeves; behavioral biases as persona parameters, not analyst outputs.
- Rationale: DeMiguel et al. 2009 (no optimizer reliably beats 1/N out of sample); loss-aversion prior near 2.0; overconfidence the best-supported bias; halving-cycle and on-chain valuation signals treated as low-confidence priors.

### D9. Tribunal protocol (R16)
- Decision: blind first briefs, staged visibility, frozen and hashed evidence bundles shared with the judge, exact-match quote checks, judges run in both side orders with flips scored as ties, equal length budgets with verbosity tracking, at least three families, judge and advocate track records, and a complexity budget that keeps any added round or graph feature off until it beats its parent on a time-split holdout.
- Rationale: debate often fails to beat simple voting (Choi, Zhu and Li 2025; Smit et al. 2024); it helps judges who lack the source text (Khan et al. 2024; Kenton et al. 2024); position, verbosity and self-preference biases are documented; error correlation persists across families.

### D10. Prediction graph (R16)
- Decision: predictions, drivers, scheduled events, links (sign, strength with interval, lag) and logical relations; coherence checks (complements, Frechet bounds, partitions, horizon monotonicity) on every write; cascades in topological order with one joint propagation over shared ancestors; exposure limits per driver and driver cluster.
- Rationale: coherence correlates with accuracy (Paleka et al. 2025); related-contract arbitrage is documented on prediction markets (verify); added complexity does not reliably help (Green and Armstrong 2015, verify).

### D11. Special situations: payout schemes (R13, owner brief)
- Decision: scheme scoring with time-stamped evidence; hazard estimates with intervals; exit rule extended for recovery, clawback exposure and withdrawal costs: hold while (1 - R) h + h lambda (G / B) is below r - rho - c'/(1 - c); staged exits under participation and impact budgets; regulator orders naming an entity hard-block live trading with no override; scheme-classified assets otherwise restricted for live capital with an operator acknowledgment that records legal and clawback exposure; simulation permitted for learning.
- Rationale: R13 documents an emergency cease-and-desist order and an administrative hearing against the scheme in the owner's case study (verify), net-winner clawback precedent (Donell v. Kowell, 2008; Madoff trustee suits), and that written knowledge of a scheme undermines good-faith defenses. R13 recommended a full block, including simulation; the owners' directive to simulate such positions governs simulation, and the dissent is recorded in the ledger.

### D12. Market integrity (R14)
- Decision: venue quality scores and quality-adjusted volume; pump flags (return, volume and no-catalyst test) with entry blocks and exposure trims; spoof-aware book features; sweep confirmation before entries on wicks; cascade gate on open interest, funding, spreads and mark-index divergence; collateral depeg gate; launch eligibility default ineligible for live; two-source confirmation for flow signals; unlock and short-squeeze gates; record liquidation and derivatives data live from day one because history is not reliably available.
- Rationale: wash-trading estimates vary by more than an order of magnitude by venue; the 10 October 2025 liquidation event (about 19 billion dollars reported, verify) and its depegs show cascade and collateral risk.

### D13. Harness formats (R04, R02)
- Decision: canonical seat files compile to Claude Code subagents and Roo Code modes as first targets, then OpenCode, Codex, oh-my-pi and an Agent Companies package per a capability matrix; tool authority uses abstract classes; cadence, budget and escalation sit in a runtime manifest.
- Rationale: R04 documents each harness's fields (Claude Code subagent frontmatter, Roo Code's eight mode keys and its irremovable built-in tools, OpenCode steps and permission maps, Codex role files, oh-my-pi agent folders, Paperclip sidecars).

### D14. Hosting environment of the build session
- Finding: this environment blocks market-data hosts and the deployment API; the owner has been told which hosts and secrets to allow (ledger 028).
- Consequence: tests use recorded fixtures; deployment falls back to a dry run with a documented manual step until access exists.

## Verification backlog for the build

1. Workers Paid limits: Workflow steps per instance, concurrency, step payload size, sleep limits; Durable Object alarm semantics; D1 size and write limits; Cron Trigger count.
2. Model routes: endpoints, model identifiers, prices, rate limits, structured-output support, caching behavior, training flags.
3. Data hosts: response shapes, rate limits, terms for automated use, US eligibility, Kalshi production and demo hostnames, Alpaca IEX and options data, FRED and Treasury endpoints, vast.ai and RunPod price endpoints, EDGAR User-Agent and rate limit.
4. Fees: Coinbase, Kraken, Kalshi maker and taker; Section 31 and FINRA rates.
5. Scheme case facts used in recorded fixtures (dates, orders, figures).
6. Paper identifiers cited in R05 and R06 marked unresolved.
