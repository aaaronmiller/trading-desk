---
date: 2026-10-21 16:40:00 UTC
ver: 1.1.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [plan, architecture, derived, autonomous-trading-firm, cloud, durable-agents]
layer: derived
---
# Implementation Plan: Autonomous Trading Firm

**Branch**: `001-autonomous-trading-firm` | **Date**: 2026-10-21 | **Spec**: `specs/001-autonomous-trading-firm/spec.md`

**Input**: Feature specification from `specs/001-autonomous-trading-firm/spec.md`, intent from `intent.md`, research waves 1 and 2 (`research.md`), and the legacy pack in `sources/legacy/`.

## Summary

Build a 32-seat autonomous investment firm whose canonical definition (seats, skills, rules, cycles, personas, strategies) is plain markdown with frontmatter, compiled into harness workspaces for Claude Code, Roo Code, OpenCode, Codex, oh-my-pi and an Agent Companies package. The always-on run plane is a set of Cloudflare Workers: Cron Triggers start deterministic, idempotent Workflow instances for each 15-minute research cycle, hourly analysis and daily, weekly and monthly rhythms; one Durable Object per book serializes order handling; D1 is the system of record; R2 holds transcripts, reports and archives. A runtime-agnostic TypeScript core (data, virtual market, plan compiler, risk, predictions, tribunal, reports, ledger) runs unchanged on a local Bun runtime with SQLite for tests, replays, the quickstart and local harness use through an MCP server. Each cycle is deterministic first: code ingests data, computes signals, gates risk and executes; models are called only where judgment is needed and the budget allows, which keeps the run plane inside the monthly ceiling. Live venue adapters are built against recorded responses and stay disabled behind the operator's recorded switch.

## Technical Context

**Language/Version**: TypeScript 5.9 (strict), ECMAScript 2023 target; Bun 1.3 for local runtime, scripts and tests; Workers runtime (compatibility date pinned at build time, `nodejs_compat` flag) for cloud.

**Primary Dependencies**: Hono 4 (API Worker), SvelteKit 2 with Svelte 5 and `@sveltejs/adapter-cloudflare` (owner portal), shadcn-svelte and LayerChart (portal UI and charts), Zod 4 (schemas and output contracts), `@modelcontextprotocol/sdk` (local harness tool server), Wrangler 4 (build and deploy). No agent framework dependency (constitution VI).

**Storage**: D1 (system of record, SQLite dialect) with Time Travel; R2 (transcripts, reports, archives, daily exports); Durable Object storage only for per-book working-order queues and alarms; `bun:sqlite` behind the same storage port locally.

**Testing**: `bun test` for core packages (unit, property, golden, contract, fault injection); Vitest with `@cloudflare/vitest-pool-workers` for Worker, Workflow, Durable Object and D1 integration; Playwright (preinstalled Chromium) for portal end-to-end and visual checks; the patched spec-prep validator and project gate scripts in `.specify/gates/`.

**Target Platform**: Cloudflare Workers Paid plan (about 5 US dollars per month) for the run plane, API and portal; any machine with Bun for the local runtime and harness workspaces.

**Project Type**: Bun-workspace monorepo with core packages, a cloud Worker app, a SvelteKit portal app, a CLI and an MCP server.

**Performance Goals**: 15-minute cycle completes in under 8 minutes wall clock at normal load; minute-level market ingestion for crypto; daily report published by 06:00 Pacific; feasibility simulation of 100,000 paths in under 20 seconds of CPU.

**Constraints**: run plane at or under 25 US dollars per month all in (default); no model call in risk or order paths; agent-facing text never reveals simulation; no outbound order requests while live is off; build environment may lack data and deploy access (tests use recorded fixtures).

**Scale/Scope**: 32 seat types, 20 personas at launch (28 defined), about 40 strategy templates, about 150 instruments across ten classes, about 96 research cycles per day, about 170 million input and 28 million output tokens per month at full activity before throttling.

## Constitution Check

*GATE: passed before research; re-checked after design (below, both columns).* Principle headings are copied verbatim from `.specify/memory/constitution.md` (11 principles).

| Principle | Pre-research | Post-design | Justification |
|---|---|---|---|
| I. Simulation by Default, Live Only by Owner Act | PASS | PASS | Virtual market is the only sink; live adapters compiled but gated by an operator change event (CTX-017); no credential is read while live is off; network spy test (SPEC-146). |
| II. Deterministic Risk Authority | PASS | PASS | `packages/risk` and the order path import no model client (static check, SPEC-081); envelope ceilings writable only through the operator action handler (CTX-012). |
| III. Point-in-Time Integrity | PASS | PASS | Every datum carries three times; the point-in-time reader enforces as-of reads; commit-reveal registry with hash chain; leak suite with planted rows (CTX-006, CTX-011). |
| IV. Honest Measurement and Reporting | PASS | PASS | Mode labels injected by templates, costs on every report, feasibility engine with intervals, evaluator separation (CTX-014, CTX-019). |
| V. Durable, Idempotent Operation | PASS | PASS | Deterministic Workflow instance identifiers, idempotency keys on every write, single-writer book objects, fault-injection suite (CTX-003, CTX-004). |
| VI. One Canonical Firm Definition, Many Harnesses | PASS | PASS | `firm/` is canonical; `packages/compilers` generates every harness workspace with source hashes and a drift check; no agent framework dependency (CTX-016). |
| VII. Cost Discipline | PASS | PASS | Budget meter on every call, throttle policy with reserved seats, routes in `firm/routes/models.yaml` only (CTX-009, CTX-010). |
| VIII. Security and Untrusted Input | PASS | PASS | Untrusted-content envelope, tool authority classes, PBKDF2 owner auth, secrets only in Worker secrets, license checks on dependencies (CTX-018). |
| IX. Evidence-Gated Delivery | PASS | PASS | Every task in `tasks.md` names gate commands; `.specify/gates/check-task-evidence.py` refuses completion without evidence; ledger and standing updated per task (CTX-020). |
| X. Owner Sovereignty with Humans Outside the Loop | PASS | PASS | No workflow step awaits owner input; owner actions are asynchronous inputs; operator-only envelope actions; agent context lint (CTX-012, CTX-013). |
| XI. Lawful Market Conduct | PASS | PASS | Conduct checks in the order layer, restricted list with acknowledgments, outbound messages limited to owner accounts (CTX-015). |

## Derivation summary

Derived from intent sections 3 and 4 (cloud, unattended, 15-minute cadence, 25-dollar ceiling, harness portability, simulation first), the owners' stack preferences (TypeScript on Bun, Hono, Svelte with shadcn, Cloudflare Workers), and empirical memory from the legacy ledger: entries 002 to 005 chose harness-over-framework, paper-first, four venue classes and a management layer; entry 014 proved the point-in-time clamp pattern with keyless tests; R11 found that clamp date-only and its leak test blind to future price rows, so both are redesigned here. No prior project ledger records a deployed outcome, so durable-runtime choices rest on research (R09, R12) rather than experience; `substrate.md` states this.

## Architecture overview

```
                       OWNERS (outside the firm)
          operator console + partner console (SvelteKit portal Worker)
                               |  HTTPS, session auth
                               v
  +-------------------- API Worker (Hono) -------------------------------+
  | owner actions | queries | reports | Q&A inbox | MCP remote endpoint  |
  +----------+-----------------------------------------------------------+
             | service binding
  +----------v----------------- RUN PLANE (Workers) ----------------------+
  | Cron: every minute -> ingest + working orders                         |
  |       every 15 min -> ResearchCycle Workflow (id cycle-YYYYMMDDTHHMM) |
  |       hourly       -> Dispatcher: BookAnalysis, daily/weekly/monthly  |
  |                                                                       |
  | Workflows: ResearchCycle, BookAnalysis, DailyRhythm, WeeklyReview,    |
  |            MonthlyStatement, Tribunal (sleeps through research window),|
  |            OwnerRequest, Export, Verify                               |
  |                                                                       |
  | Durable Objects: BookDesk (one per book: orders, fills, wallet writes) |
  |                  BudgetMeter (one per month: spend, throttles)         |
  |                                                                       |
  | Core packages (runtime-agnostic): data | market | plan | risk |      |
  |   predict | agents | tribunal | reports | ledger | registry          |
  +-----+--------------------+---------------------+---------------------+
        |                    |                     |
     D1 (records)        R2 (artifacts)      Model routes (config)
        |                                     bulk | typed | review |
        |                                     advocates | judge | deep
  Public data hosts (crypto, equities, FX, rates, filings, prediction markets, GPU)

  LOCAL: Bun runtime + SQLite + recorded tapes + MCP server -> harness workspaces
         (Claude Code, Roo Code, OpenCode, Codex, oh-my-pi, Agent Companies package)
```

## Decisions

**CTX-001: Runtime-agnostic TypeScript core with ports and adapters**
- Derived from: intent section 3 constraints 4 and 6 (cloud hosting plus harness portability), section 4 (local runtime for tests); SPEC-020, SPEC-142.
- Memory: legacy ledger 002 (harness over framework, outcome unknown); no deployed outcome on record.
- Options considered: (a) core coupled to Workers bindings; (b) core behind storage, clock, scheduler, model and network ports with cloud and local adapters; (c) separate implementations per runtime.
- Choice: (b). Packages never import Worker bindings; `packages/storage` defines the port with a D1 adapter and a `bun:sqlite` adapter sharing one SQL schema and migration set.
- Trade-offs accepted: a small adapter layer and two test runners; in exchange every behavior is testable in milliseconds on recorded data.

**CTX-002: Cloudflare Workers Paid as the run plane**
- Derived from: intent section 3 constraints 4 and 5; section 4 (24/7, minute ingestion, 15-minute cycles); SPEC-021, SPEC-028, SPEC-141.
- Memory: R09 (estimated 83,500 Workflow steps per month against 500,000 included; Paid plan about 5 dollars) [verify limits at build]; vantage D-12 chose the same platform for the portal.
- Options considered: Workers Paid; a 5-dollar virtual server running a long-lived process (single point of failure, owner maintenance); Paperclip on a server with harness processes (R12: governance strength, but per-heartbeat harness cost and an always-on server); Vercel (Hobby plan non-commercial, Pro 20 dollars breaks the ceiling); Inngest (R09: about 138 dollars per month at this volume).
- Choice: Workers Paid with Cron Triggers, Workflows, Durable Objects, D1, R2 and Workers Logs.
- Trade-offs accepted: platform limits (CPU per invocation, Workflow step counts, D1 size) bound the design; outbound streaming connections are avoided in favor of polling.

**CTX-003: Cycles are deterministic Workflow instances**
- Derived from: SPEC-021, SPEC-022, SPEC-029, SPEC-030, SPEC-135.
- Memory: R09 (Workflows batch creation skips duplicate instance identifiers; each step result is persisted and replayed on retry).
- Design: Cron fires; the handler computes the slot identifier (for example `cycle-20261021T1615Z`) and creates the instance through batch creation, so a duplicate trigger is a no-op. Every external effect (model call, data fetch, order submission, prediction commit) is its own step with explicit retry limits. The first step of every cycle reconciles books, open orders and prediction states against D1 and records any break before acting.
- Options considered: a single long Worker invocation per cycle (no durability across crashes); queue consumers (at-least-once without step memoization); Pi Durable on Durable Objects (experimental per R09; kept as a future adapter behind the scheduler port).
- Trade-offs accepted: Workflow step counts must stay modest; long research windows use `step.sleep` inside the Tribunal Workflow.

**CTX-004: One BookDesk Durable Object per book, D1 as the record**
- Derived from: SPEC-046, SPEC-063 to SPEC-072, SPEC-135, SPEC-151.
- Memory: R09 candidate (single writer per desk); legacy CTX-003 (one durable store).
- Design: all orders for a book pass through its BookDesk object, which serializes acceptance, fills and wallet updates, writes them to D1 in one batch keyed by deterministic identifiers (order identifier = hash of cycle, plan version and leg; fill identifier = order identifier plus sequence), and keeps working orders in its own storage with a one-minute alarm while any are open. D1 unique constraints make every write idempotent.
- Options considered: D1 only (concurrent cycles could race on a book); Durable Object storage as the record (hard to query for reports).
- Trade-offs accepted: two storage layers, but only the working-order queue lives outside D1.

**CTX-005: Market data through labeled adapters with polling and recorded fixtures**
- Derived from: SPEC-026, SPEC-031 to SPEC-035, SPEC-040, SPEC-068, SPEC-072; intent section 3 constraint 7.
- Memory: R07 (sources, limits, US eligibility); legacy vendor matrix; investment repository labeling rules.
- Design: each adapter declares host, feed label (exchange, consolidated, delayed, end of day, research-only, modeled), cadence, rate limit with backoff on 429, and response fixtures captured for tests. Defaults below; any adapter can be disabled by configuration.

| Class | Primary source (keyless unless noted) | Fallback | Cadence | Label |
|---|---|---|---|---|
| Crypto spot | Coinbase Exchange public candles and tickers | Kraken public OHLC | 1 minute | exchange |
| Crypto perpetuals (funding, open interest, mark) | Hyperliquid info API | Bybit public | 1 minute (marks), hourly (funding) | exchange, read-only for US persons |
| Crypto derivatives positioning and liquidations | Hyperliquid and Bybit public | none | 15 minutes | exchange |
| US stocks, funds, options | Alpaca market data (free key, IEX feed) | Yahoo chart and options endpoints | 1 minute in session | IEX or research-only |
| Foreign exchange | Frankfurter (central bank reference, daily) | Yahoo chart | daily and 15 minutes | reference or research-only |
| Commodities | Gold and oil via listed funds (Alpaca) and tokenized gold (Coinbase) | Yahoo futures chart | 15 minutes | IEX, exchange or research-only |
| Rates and bonds | FRED graph CSV and Treasury Fiscal Data | Alpaca bond funds | daily | official |
| Prediction markets | Polymarket Gamma and CLOB price history | Kalshi public market data, Manifold | 15 minutes | market |
| Data-center GPU index | vast.ai offers and RunPod GPU prices, composed into an index | manual snapshot | daily | modeled index |
| Filings and holdings | SEC EDGAR submissions and full-text search (User-Agent required) | none | daily | official |
| News and events | GDELT document API, publisher RSS feeds, SEC press releases | none | 15 minutes | news |
| Sentiment | Alternative.me fear and greed index | none | daily | index |
| On-chain | mempool.space, DefiLlama public endpoints | none | hourly | on-chain |

- Trade-offs accepted: free feeds carry delays and terms limits; Yahoo and similar sources are labeled research-only and never the sole basis of a fill; paid feeds wait for an owner budget increase. Hosts, fees and limits marked "(verify)" in R07 are checked by the first live smoke test and recorded in the ledger.

**CTX-006: Point-in-time store with three timestamps and as-of reads**
- Derived from: SPEC-032 to SPEC-035, SPEC-041, SPEC-042, SPEC-160.
- Memory: legacy `date_clamp.py` (dates only; R11 found intraday blindness and a leak test that missed future price rows); FINSABER-2 practice (R05: next-open execution, undated news usable only from the next decision).
- Design: every row stores `source`, `retrieved_at`, `effective_at`; the reader takes `asOf` and filters `effective_at <= asOf`; skew beyond 5 minutes quarantines the row; undated items never enter historical windows; masking maps symbols and dates to stable aliases per replay run; lessons carry `resolved_at`. The leak suite plants future price rows and future text.
- Trade-offs accepted: storage grows by three timestamps per row; minute bars older than 30 days move to R2 archives.

**CTX-007: Seat runner with structured outputs, owned in-house**
- Derived from: SPEC-001, SPEC-016, SPEC-020, SPEC-036, SPEC-037, SPEC-058, SPEC-143, SPEC-144; constitution VI.
- Memory: R01 (frameworks bind roles to graph runtimes; LLM verdict without code gate is the common failure), R04 (harness formats lack output contracts), R05 (risk-manager prompts are the most attackable surface).
- Design: the runner assembles the compiled seat prompt, the seat's skills, rules and a context packet; calls the routed model through an OpenAI-compatible client with JSON-schema output where supported and validated JSON otherwise (one repair attempt, then abstention); exposes tools as typed actions checked against the seat's authority classes; wraps fetched text in an untrusted-content envelope; enforces numeric grounding by checking each trade-relevant number against the run's tool results; meters cost before and after every call; stores the transcript in R2 with its hash; every call is one Workflow step.
- Options considered: Pi Durable agent sessions (experimental; adapter kept possible), Paperclip heartbeats (cost), LangGraph (excluded by owner).
- Trade-offs accepted: the runner is ours to maintain; it stays small (target under 1,500 lines) and fully tested.

**CTX-008: Plan language with a closed expression grammar**
- Derived from: SPEC-053 to SPEC-062, SPEC-048.
- Memory: 2025 architecture draft (executable plan classes, rejected because they run arbitrary code); R08 template fields (signal, entry, exit, sizing, rebalance, parameter ranges, heat hook, failure regimes).
- Design: plans are JSON validated by a Zod schema; conditions use a hand-written Pratt parser over a whitelisted function table (`price`, `bar`, `sma`, `ema`, `rsi`, `atr`, `zscore`, `change`, `funding`, `basis`, `spread`, `iv`, `time`, `between`, `crosses`) with no member access, no calls outside the table, depth and length limits; compiler checks instruments, class enablement, calendars, persona constraints, absolute grounded levels and links.
- Trade-offs accepted: a fixed function set; new functions need a code change with tests.

**CTX-009: Model routes as configuration with three or more families**
- Derived from: SPEC-087, SPEC-089, SPEC-092, SPEC-138, SPEC-139; intent section 12 question 2.
- Memory: vantage plan (Muse Spark Contributor bulk, Jev typed decisions, DeepSeek overflow, premium for owner deep dives); R09 (prices; consumer-subscription and prompt-training cautions) [verify prices at build].
- Design: `firm/routes/models.yaml` maps route names (bulk, typed, review, advocate-a, advocate-b, judge, deep-dive) to provider endpoint, model identifier, family, training flag and prices. Default profile "economy-api": bulk on Muse Spark 1.3 Contributor (training-permitted, no identifiers ever), typed decisions on Jev, review and advocate-b on DeepSeek V4 Flash, judge on a Claude model from a third family, deep dives on the latest Claude Opus model. Profile "subscription" (owner opt-in) routes bulk through an OpenCode Go subscription and is excluded from the always-on loop unless the operator accepts its terms risk in a recorded change. Served model identifiers are logged per call.
- Trade-offs accepted: provider differences in structured-output support are absorbed by validation and repair.

**CTX-010: Deterministic-first cycles and a budget meter with throttling**
- Derived from: intent section 3 constraint 5, section 12 question 1; SPEC-136, SPEC-137.
- Memory: vantage seat budget shares; R09 cost estimate (23 to 44 dollars per month at full activity on bulk API routes) [verify].
- Design: each 15-minute cycle runs ingestion, indicators, strategy-template signals, scheme and integrity scores, risk checks and fills in code; a materiality filter selects which instruments and books need seat judgment; seat calls are admitted by the BudgetMeter object against seat shares and the monthly ceiling; when spend runs ahead of the month's pro-rata curve, non-essential work throttles in this order: optional analyst dimensions, persona planning frequency (hourly to four-hourly), case depth, then advocate research depth; risk, execution, records and reporting seats keep a reserved 20 percent.

| Activity per day at full rate | Calls | Input tokens | Output tokens |
|---|---|---|---|
| Triage (chief of staff function of the chief operating officer) | 96 | 0.38 M | 0.05 M |
| Analyst dimensions on material instruments | 290 | 1.45 M | 0.23 M |
| Portfolio manager proposals | 190 | 0.77 M | 0.15 M |
| Strategy compiler translations | 145 | 0.43 M | 0.09 M |
| Pro and con cases | 380 | 1.15 M | 0.19 M |
| Second-family reviews | 190 | 0.58 M | 0.06 M |
| Book annotations, daily rhythm, reports, education | 70 | 0.47 M | 0.09 M |
| Tribunals (about 2 per day) | 60 | 0.33 M | 0.06 M |
| Owner questions | 10 | 0.06 M | 0.01 M |
| Total | about 1,430 | about 5.6 M | about 0.93 M |

At default route prices this is roughly 25 to 30 dollars of model spend per month before caching, plus about 5 dollars of hosting, so the meter throttles to about 70 percent of full rate under the 25-dollar ceiling; raising the ceiling to 40 dollars removes throttling at the estimated load.

**CTX-011: Prediction registry, scoring and the prediction graph**
- Derived from: SPEC-094 to SPEC-105, SPEC-153.
- Memory: vantage commit-reveal design; owner's 2025 sealed-forecast protocol; R06 (Brier skill against markets, sample minimums, final-state resolution, market price at or before commit, logit pooling).
- Design: canonical JSON plus salt is hashed with SHA-256; commitments chain by previous hash and sequence; reveals verify salt and content; scoring computes Brier, clipped log loss (clip 0.001), ten-bin calibration, expected calibration error and recalibration slope by logistic fit of outcome on logit probability; baselines include base rate, persistence, coin flip and market price; recalibration applies a fitted slope and intercept per seat when the slope stays under 0.8 after 200 outcomes; drivers and links are tables; propagation is a breadth-first walk; coherence rules check joint versus marginal bounds and sign conflicts; multiplicity across personas is controlled with Holm adjustment in skill claims (R05, SPEC-169); chain heads are anchored daily outside the firm's stores, by default as a signed commit to a separate anchors repository chosen by the operator (SPEC-174).
- Trade-offs accepted: market matching is manual or rule-based per question template; unmatched questions score against the other baselines only.

**CTX-012: Owner envelope, heat dials and actions**
- Derived from: SPEC-010 to SPEC-012, SPEC-073 to SPEC-078, SPEC-130, SPEC-131, SPEC-134.
- Memory: MOU addendum 2.1 (3x leverage per position, 50 percent high-water stop, 100 percent accepted loss); R08 heat curve; R03 drawdown ladders.
- Design: `firm/heat/heat-map.yaml` holds the mapping below; envelope ceilings live in a D1 table writable only by the owner action handler, which checks the operator role and records change events; the house book defaults to heat 8, personas to their profile heat, strategies to 5.

| Heat | Kelly fraction | Risk per trade (book value) | Target volatility | Leverage cap | Stop distance (ATR multiple) | Eligible classes tier | Ladder (warn, halve, stop) below high-water |
|---|---|---|---|---|---|---|---|
| 1 | 0.10 | 0.25% | 4% | 1.0x | 1.50 | 1: cash, bonds, broad funds | 3%, 5%, 8% |
| 2 | 0.15 | 0.33% | 6% | 1.0x | 1.40 | 1 | 4%, 7%, 10% |
| 3 | 0.20 | 0.42% | 8% | 1.0x | 1.30 | 2: plus large-cap stocks, gold | 5%, 9%, 13% |
| 4 | 0.25 | 0.50% | 10% | 1.15x | 1.20 | 2 | 6%, 11%, 16% |
| 5 | 0.30 | 0.60% | 12% | 1.35x | 1.10 | 3: plus major crypto, FX, options bought | 8%, 14%, 20% |
| 6 | 0.40 | 0.75% | 14% | 1.65x | 1.00 | 4: plus perpetuals, options sold covered | 10%, 18%, 25% |
| 7 | 0.50 | 0.90% | 17.5% | 2.0x | 0.90 | 5: plus small caps, altcoins, event contracts, special situations | 12%, 22%, 30% |
| 8 | 0.60 | 1.20% | 22% | 2.35x | 0.85 | 5 | 15%, 26%, 35% |
| 9 | 0.80 | 1.60% | 28% | 2.65x | 0.80 | 6: plus payout schemes, memecoins | 18%, 32%, 42% |
| 10 | 1.00 | 2.00% | 35% | 3.0x | 0.75 | 6 | 20%, 35%, 50% |

Heats 1 to 7 follow R08's curve; 8 to 10 extend it for the partner mandate up to the envelope ceiling. Full Kelly (heat 10) is the growth-optimal maximum on a correctly measured edge; because measured edges are noisy, the feasibility report shows growth and ruin at each heat so the owners see why higher heat stops paying.

**CTX-013: Organization roster and seat families**
- Derived from: SPEC-002, SPEC-006, SPEC-007, SPEC-085 to SPEC-093, SPEC-162; intent section 12 question 3.
- Memory: R03 29-role chart with splits of the old coder and analyst roles; R01 role prompts (TradingAgents, Apache-2.0) as source text with provenance; vantage 15-seat chart.
- Design: 32 seat types in `firm/seats/` grouped as office of the chief executive, investment (chief investment officer, house, persona and strategy portfolio managers, analysts, researcher, compiler), challenge (red team advocates and judges), risk (chief risk officer, market risk, market integrity, model validation, prediction scoring), compliance (chief compliance officer, pre-trade compliance, conduct surveillance), operations (chief operating officer, execution trader, reconciliation, fund accounting, controller, data engineering, release control, records), investor education and reporting, and internal audit reporting to the owners. Proposers and reviewers draw from different families by route; believability weights come from scored records.
- Trade-offs accepted: many seats are invoked rarely; their cost is bounded by cadence and budget shares.

**CTX-014: Reports as deterministic templates with seat-written narrative**
- Derived from: SPEC-113 to SPEC-124, SPEC-038, SPEC-039, SPEC-051, SPEC-132.
- Memory: owner research template (resource F); owner's TexitCoin brief (ethical "other side" notes, scenario tables); R15 pending for educational structure.
- Design: report builders assemble numbers, tables and labels in code; narrative sections come from the investor education and reporting seat with numeric grounding; every report renders to Markdown and HTML in R2 and to the portal; the glossary and curriculum are tables; the feasibility engine runs a seeded resampling simulation (100,000 paths) over the realized trade distribution plus analytic Kelly and ruin figures with intervals.
- Trade-offs accepted: PDFs are optional (rendered on demand by the CLI with Chromium); the portal is the primary reading surface.

**CTX-015: Special situations and market integrity as scored detectors**
- Derived from: SPEC-106 to SPEC-112, SPEC-080, SPEC-084.
- Memory: owner's TexitCoin brief (indicators, scenario probabilities, ethics notes); R13 (regulatory record of the case study, clawback precedent, exit rule with recovery and clawback terms, liquidity arithmetic); R14 (venue quality, pump, spoof, sweep, cascade, depeg, launch, unlock and squeeze gates).
- Design: scheme score is a weighted checklist over time-stamped evidence records (clean, watch, scheme); the hazard model maps net-inflow trend, its rate of change, withdrawal friction, operator diversion and liquidity into a daily hazard with an interval, calibrated on recorded cases; the exit rule holds while (1 - R) h + h lambda (G / B) stays below r - rho - c'/(1 - c), per SPEC-108; regulator orders hard-block live trading (SPEC-163); integrity detectors compute venue quality and adjusted volume (SPEC-164), pump flags, spoof-aware book features, sweep confirmation, the cascade and depeg gate (SPEC-165), launch, unlock and squeeze gates (SPEC-166, SPEC-167); conduct checks reject self-crossing, rapid large cancel patterns and coordinated cross-book orders.
- Trade-offs accepted: detectors start rule-based and are scored like seats before any learned model replaces them.

**CTX-016: Canonical firm definition and harness compilers**
- Derived from: SPEC-013 to SPEC-020, SPEC-161; intent section 3 constraint 6.
- Memory: R02 (Agent Companies format, HyperGrok multi-harness manifests, single external write role), R04 (field-level formats for Claude Code, Roo Code, OpenCode, Codex, oh-my-pi, Paperclip).
- Design: each seat is `firm/seats/<id>.md` with YAML frontmatter (id slug, title, reports_to, authority classes, outputs contract, skills, rules, budget share reference) and body sections; generators write `harness/workspaces/<harness>/` with each harness's native files plus an MCP configuration pointing at `apps/mcp`; every generated file embeds the source hash; `bun run firm:check` regenerates in memory and fails on any difference.
- Trade-offs accepted: Roo Code cannot remove some built-in tools (R04), so its modes carry an explicit prohibition and the capability report lists the gap.

**CTX-017: Live adapters built, disabled and contract-tested**
- Derived from: SPEC-069, SPEC-145 to SPEC-150.
- Memory: legacy D-29 (Alpaca, OANDA, Kalshi paper paths), R07 (US eligibility; production, testnet and demo hosts set explicitly).
- Design: adapters for Coinbase Advanced Trade (crypto spot), Alpaca (stocks, funds, options, crypto) and Kalshi (event contracts) implement the shared order interface; each sets production and sandbox base URLs explicitly and refuses production unless the live flag is set by the operator change event; credentials load only inside the adapter; perpetuals stay simulation-only for US persons.
- Trade-offs accepted: forex and perpetual live paths are deferred.

**CTX-018: Security model**
- Derived from: SPEC-037, SPEC-125, SPEC-138, SPEC-146, SPEC-148; constitution VIII.
- Memory: vantage portal (generated passwords; lighter hashing chosen for free-plan CPU); R05 poisoning results.
- Design: owner passwords hashed with PBKDF2-SHA-256 (310,000 iterations, per-user salt) now that the paid plan allows the CPU; sessions in signed cookies backed by a D1 session table with expiry, lockout after ten failures, CSRF tokens on mutations; secrets only in Worker secrets; untrusted text envelope plus injection heuristics and a 50-item injection corpus in CI; dependency licenses checked in CI (no AGPL or GPL).
- Trade-offs accepted: two owner accounts are seeded by a CLI command that prints credentials once to the operator's terminal and stores only hashes.

**CTX-019: Evaluator separation and validation**
- Derived from: SPEC-156 to SPEC-162; constitution IV and IX.
- Memory: spec-prep rule 3; R05 (ablations, sample floors, multiplicity); R03 (trial registry, overfitting probability).
- Design: held-out evaluations live outside the repository; the build exposes an evaluator entry point (`bun run eval:serve` for fixtures supplied at runtime) without reading evaluator files; trial registry, deflated Sharpe and overfitting probability via combinatorial cross-validation; baselines and monthly ablations (no memory, no debate, no risk team) on replay (SPEC-168); memory frozen per replay window (SPEC-170); tribunal judgments run in both side orders with equal length budgets (SPEC-171); added stages stay off until they beat their parent on a holdout (SPEC-172).

**CTX-020: Delivery gates**
- Derived from: constitution IX; spec-prep task-gate contract.
- Design: `.specify/gates/check-task-evidence.py` parses `tasks.md` and `specs/001-autonomous-trading-firm/evidence/` and fails when a checked task lacks an evidence file with command, exit code and output digest; a pre-commit hook and the project Claude Code hooks run it; the patched validator runs in CI.

**CTX-021: Retention, export and restore**
- Derived from: SPEC-141, SPEC-154.
- Design: D1 Time Travel covers 30 days of point-in-time restore; the Export Workflow writes daily newline-delimited JSON per table to R2 with chain heads; the CLI restores into a fresh database and verifies chains.

## Data model

See `data-model.md` for entities, fields, relations, state transitions, identifiers and the D1 schema outline; `contracts/` holds the seat definition schema, cycle graph schema, plan schema and expression grammar, order interface, tool catalog, owner API and report schemas.

## Component specifications

| Component | Responsibility | Interface | Depends on | Failure surfacing |
|---|---|---|---|---|
| `packages/core` | identifiers, clocks, canonical JSON, hashing, money in minor units, errors | functions and types | none | typed errors |
| `packages/storage` | storage port, migrations, D1 and SQLite adapters, idempotent writes | repository interfaces | core | constraint violations as typed errors |
| `packages/registry` | load and validate the canonical firm definition | `loadFirm(dir)` | core | named validation errors (SPEC-001, SPEC-018, SPEC-019) |
| `packages/data` | source adapters, point-in-time reader, calendars, labels, masking | `fetch*`, `asOf(t)` | core, storage | unavailable labels, quarantine records |
| `packages/market` | virtual exchange engine, fee and slippage models, margin, options marks | `submit`, `evaluateWorking`, `mark` | core, data | rejection reasons |
| `packages/plan` | plan schema, expression parser, compiler | `compile(planText, ctx)` | core, data, registry | machine-readable rejection reasons |
| `packages/risk` | heat mapping, sizing, limits, ladders, restricted list, conduct checks | `gate(proposal, state)` | core, storage | veto records |
| `packages/predict` | registry, scoring, calibration, market priors, graph, coherence | `commit`, `reveal`, `score`, `propagate` | core, storage, data | chain divergence reports |
| `packages/agents` | seat runner, prompt assembly, tool registry, routing, budget client, grounding, injection envelope | `runSeat(seat, packet)` | core, registry, storage | abstentions, skipped-step records |
| `packages/tribunal` | tribunal protocol and scoring | `openTribunal`, `runRound`, `rule` | agents, predict | round records |
| `packages/reports` | report builders, education, glossary, curriculum, feasibility engine | `build*Report` | storage, predict, ledger | missing-section errors |
| `packages/ledger` | double-entry ledger, chains, verification, export and import | `post`, `verify`, `export` | core, storage | divergence reports |
| `packages/compilers` | harness generators, capability matrix, drift check | `generate`, `check` | registry | drift reports |
| `packages/runtime` | cycle step graphs, scheduler port, local scheduler, reconciliation | `runCycle`, `reconcile` | all core packages | incident records |
| `apps/worker` | Cron handlers, Workflows, Durable Objects, Hono API, owner actions | HTTP and bindings | runtime, packages | Workers Logs, incidents |
| `apps/portal` | SvelteKit owner portal | pages | API Worker | error pages without 786110 |
| `apps/cli` | local run, replay, generate, verify, export, seed owners, deploy helpers | commands | runtime, packages | exit codes |
| `apps/mcp` | MCP server exposing tool contracts to local harnesses | MCP tools | agents tool registry | tool errors |

## Hosting and deployment

- Two Workers: `firm-run` (Cron Triggers, Workflows, Durable Objects, Hono API) and `firm-portal` (SvelteKit), joined by a service binding; one D1 database `firm`; one R2 bucket `firm-artifacts`.
- Cron schedules (UTC): `* * * * *` ingestion and working orders; `*/15 * * * *` research cycles; `0 * * * *` dispatcher that starts book analysis and, when the configured Pacific-time slot matches, the daily, weekly and monthly rhythms (daylight saving handled in code, not in cron).
- Secrets: model route keys, optional data keys (Alpaca), owner session key, live venue keys (absent until the operator adds them). Set with `wrangler secret put` by the operator; never in the repository.
- Deployment requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment and network access to `api.cloudflare.com`; without them the build runs `wrangler deploy --dry-run` and documents the remaining manual step in `docs/deploy.md`.
- Regenerating this section on a hosting pivot is a ledger event; the core packages do not change.

## Security

See CTX-018. Threats addressed: prompt injection from fetched content (envelope, heuristics, authority classes, no instruction-following tool path); poisoning of risk judgments (no model in the risk path); credential exposure (secrets store, prompt scanning, trade-only permission check); owner account takeover (PBKDF2, lockout, CSRF, session expiry); supply chain (pinned dependencies, lockfile, license check, pinned external skills with content hashes); data tampering (hash chains with daily verification).

## Project Structure

### Documentation (this feature)

```text
specs/001-autonomous-trading-firm/
├── intent.md            # human layer: goals, constraints, stories, prior art
├── spec.md              # human layer: 174 clauses bound to held-out evaluations
├── plan.md              # this file (derived layer)
├── research.md          # Phase 0 decisions with sources
├── data-model.md        # entities, schema outline, state transitions
├── quickstart.md        # local run and validation walkthrough
├── contracts/           # schemas and interfaces
├── checklists/          # requirements-quality checklist
├── tasks.md             # gated, dependency-ordered tasks
├── traceability.md      # source disposition and story-clause-task map
├── substrate.md         # declared level and pre-locked decisions
├── evidence/            # per-task evidence records (created during build)
├── layer-allow.txt      # owner-stated names allowed in human layers
├── tech-tokens.txt      # project technology denylist
└── ledger/
    ├── ledger.md        # append-only decisions and outcomes (001 onward)
    └── standing.md      # overwritten current state
```

### Source Code (repository root)

```text
firm/                          # canonical firm definition (edit here only)
├── company.md
├── seats/<seat-id>.md         # 32 seat types
├── skills/<skill>/SKILL.md
├── rules/*.md
├── cycles/*.yaml              # step graphs
├── personas/*.md              # 28 defined, 20 active at launch
├── strategies/*.md            # strategy templates
├── heat/heat-map.yaml
├── manifest/runtime.yaml      # cadence, budget shares, escalation
├── routes/models.yaml         # model routes and prices (configuration)
└── instruments/*.yaml         # instrument catalog, fee profiles, calendars
packages/
├── core/ storage/ registry/ data/ market/ plan/ risk/
├── predict/ agents/ tribunal/ reports/ ledger/ compilers/ runtime/
apps/
├── worker/                    # firm-run Worker (Cron, Workflows, Durable Objects, Hono API)
├── portal/                    # firm-portal SvelteKit app
├── cli/                       # Bun CLI
└── mcp/                       # MCP tool server for local harnesses
harness/workspaces/            # generated; never edit (drift-checked)
├── claude-code/ roo-code/ opencode/ codex/ oh-my-pi/ agent-companies/
tests/
├── fixtures/                  # public recorded tapes and venue responses (not evaluator material)
├── contract/ integration/ property/ fault/ e2e/
docs/                          # runbook, deploy, owner guide
sources/                       # legacy pack and upstream reference (read-only)
.specify/                      # Spec Kit, constitution, gates
```

**Structure Decision**: Bun-workspace monorepo. Core logic lives in runtime-agnostic packages so the cloud Worker, CLI, MCP server and tests share it; the canonical firm definition is data, not code, so owners and harnesses can read and edit it. The legacy `harness/` drafts move to `sources/legacy/harness-2026-10-03/` during setup.

## Build phases

Phase and step notation only; each phase validates the clauses listed.

- Phase 1 Setup: workspace, tooling, gates, legacy move. Validates SPEC-139 (configuration-only routes), constitution IX gates.
- Phase 2 Foundation: core, storage, registry, ledger, chains, point-in-time store, calendars. Validates SPEC-001, SPEC-008, SPEC-013 (registry part), SPEC-018, SPEC-019, SPEC-032 to SPEC-035, SPEC-151, SPEC-153.
- Phase 3 Firm runs on crypto (US1, MVP): data adapters for crypto, virtual market, plan compiler, risk gate, seat runner, routes, budget meter, research cycle, predictions, logs, local runtime, cloud Workflows and BookDesk. Validates SPEC-002 to SPEC-012, SPEC-021 to SPEC-031, SPEC-036 to SPEC-040, SPEC-043 to SPEC-076, SPEC-081 to SPEC-085, SPEC-092, SPEC-094 to SPEC-097, SPEC-113, SPEC-135 to SPEC-144.
- Phase 4 Reports and learning (US2): daily, weekly, monthly, feasibility, education. Validates SPEC-114 to SPEC-121, SPEC-133, SPEC-173.
- Phase 5 Owner portal and console (US3). Validates SPEC-122, SPEC-125 to SPEC-134.
- Phase 6 Multi-asset (US4). Validates SPEC-026, SPEC-059, SPEC-066, SPEC-068, SPEC-071 extended to all classes.
- Phase 7 Tribunal (US5). Validates SPEC-086 to SPEC-091, SPEC-093, SPEC-171, SPEC-172.
- Phase 8 Prediction graph and calibration (US6). Validates SPEC-098 to SPEC-105, SPEC-079.
- Phase 9 Special situations and integrity (US7). Validates SPEC-106 to SPEC-112, SPEC-077, SPEC-080, SPEC-084, SPEC-163 to SPEC-167.
- Phase 10 Harness compilers (US8). Validates SPEC-013 to SPEC-017, SPEC-020, SPEC-161.
- Phase 11 Live path disabled (US9). Validates SPEC-145 to SPEC-150.
- Phase 12 Personas, institution study, macro book (US10). Validates SPEC-043, SPEC-123, SPEC-124, SPEC-162.
- Phase 13 Validation, evaluator handoff, deploy and readiness. Validates SPEC-041, SPEC-042, SPEC-152, SPEC-154 to SPEC-160, SPEC-168 to SPEC-170, SPEC-174.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
|-----------|------------|-------------------------------------|
| Two Workers (run plane and portal) | Owners prefer Svelte for interfaces and Hono for services | One SvelteKit Worker would put Workflows and Durable Objects inside the UI app and couple deploys |
| Two test runners | Worker bindings need the Workers test pool; core tests need speed | Running everything in the Workers pool slows the core suite and complicates property and fault tests |
| Own seat runner instead of a framework | Owner excludes framework lock-in; harness formats carry no output contracts | Frameworks bind roles to their runtime (R01) |

## Clause coverage

Every specification clause, the component that implements it, its primary test kind and the deciding context entry. Held-out evaluations grade the same clauses independently.

| Clause | Behavior (abridged) | Component | Primary test | Decision |
|---|---|---|---|---|
| SPEC-001 | THE system SHALL define every seat by a canonical role definition containing mission, responsibilities, ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-002 | THE system SHALL staff at minimum these seats, each with exactly one reporting line ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-003 | WHEN the daily cycle opens, THE system SHALL publish within 30 minutes a chief ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-004 | WHEN the chief executive or chief investment officer changes capital allocation between books, THE ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-005 | WHEN the chief executive creates, revises or retires a seat, THE system SHALL record ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-006 | THE system SHALL reject any approval in which the approving seat is the seat ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-007 | THE system SHALL release orders only from the execution trader seat class, SHALL book ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-008 | THE system SHALL attribute every record that changes state (decision, order, fill, allocation, dial, ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-009 | WHILE no owner is active, THE system SHALL complete every scheduled cycle without any ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-010 | THE system SHALL accept the owner envelope actions (enable or disable live execution, change ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-011 | WHEN an owner pauses the firm or a book, THE system SHALL release no ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-012 | IF both owners change the same dial within one cycle to different values, THEN ... | registry, runtime, worker owner actions | integration | CTX-012, CTX-013 |
| SPEC-013 | THE system SHALL keep exactly one canonical source for each seat, skill, rule, cycle, ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-014 | THE system SHALL generate for every seat a Claude Code subagent file and a ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-015 | THE system SHALL generate files for additional harnesses listed in its capability matrix and ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-016 | THE system SHALL declare each seat's tool authority in abstract classes (read, write paths, ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-017 | THE system SHALL keep cadence, budget and escalation settings in a runtime manifest separate ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-018 | THE system SHALL define every cycle as a step graph with declared inputs, outputs, ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-019 | THE system SHALL load a skill only when its folder name matches its declared ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-020 | WHEN a seat runs inside a local agent harness against recorded data, THE system ... | compilers, registry, mcp | golden and contract | CTX-016 |
| SPEC-021 | THE system SHALL start a research-to-plan cycle every 15 minutes, with each start within ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-022 | WHEN a research-to-plan cycle runs, THE system SHALL record, in order, market assessment, single ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-023 | THE system SHALL analyze every active book once per hour and append the analysis ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-024 | THE system SHALL run a daily rhythm of morning meeting, investment committee, risk report ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-025 | THE system SHALL run a weekly review that evaluates every plan to date, records ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-026 | THE system SHALL fill an order for an instrument only while that instrument's market ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-027 | WHEN an order is decided at time T, THE system SHALL fill it only ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-028 | THE system SHALL complete at least 99 percent of scheduled cycles in any rolling ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-029 | WHEN a scheduled trigger is delivered more than once for the same slot, THE ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-030 | IF a cycle fails or ends partially, THEN THE system SHALL release no orders ... | runtime, worker Cron and Workflows, data calendars | integration and fault | CTX-002, CTX-003 |
| SPEC-031 | WHEN a research cycle covers an instrument, THE system SHALL produce one analyst output ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-032 | THE system SHALL store every datum with its source, retrieval time and effective time. | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-033 | WHEN a decision is made at time T, THE system SHALL supply only data ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-034 | WHEN a historical window is assembled, THE system SHALL exclude items without an effective ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-035 | IF requested data does not cover a window, THEN THE system SHALL label the ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-036 | THE system SHALL reject any seat output whose trade-relevant numbers (prices, sizes, probabilities, levels, ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-037 | THE system SHALL treat text from fetched content, filings, social posts, other seats and ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-038 | THE system SHALL label every figure in an owner-facing report with its source and ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-039 | WHEN a deep research report is produced, THE system SHALL include the owner template ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-040 | IF a data source fails, THEN THE system SHALL continue the cycle with reduced ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-041 | WHERE historical replay is configured with masking, THE system SHALL replace instrument names and ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-042 | THE system SHALL include a stored lesson in a seat's input only if the ... | data, agents grounding and envelope, reports labels, runtime replay | unit, property, leak suite | CTX-005, CTX-006, CTX-007 |
| SPEC-043 | THE system SHALL start with twenty personas, each with a distinct worldview, risk profile, ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-044 | THE system SHALL maintain these book types, each with a multi-asset wallet of cash ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-045 | WHEN an owner opens a sandbox with theoretical cash (default 10,000 US dollars), THE ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-046 | THE system SHALL compute each book's net asset value as cash plus marked positions, ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-047 | THE system SHALL maintain benchmark books for buy-and-hold bitcoin, a broad US equity index ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-048 | WHEN a plan targets a persona book, THE system SHALL reject it at compilation ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-049 | THE system SHALL keep live-price books and historical replay runs separate, such that no ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-050 | WHERE running-cost allocation is enabled, THE system SHALL report each book's return net of ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-051 | THE system SHALL show the execution mode (simulated or live) on every owner-facing page, ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-052 | THE system SHALL keep agent-facing context free of statements that execution is simulated, virtual ... | storage books, market wallets, reports labels, agents context lint | unit and integration | CTX-004, CTX-014 |
| SPEC-053 | WHEN a portfolio manager seat issues a plan, THE system SHALL have the strategy ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-054 | IF a compiled plan fails validation, THEN THE system SHALL reject it with machine-readable ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-055 | THE system SHALL evaluate plan conditions only through a closed expression language whose functions ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-056 | THE system SHALL support single-instrument, multi-instrument within one class, cross-asset, and whole-book allocation plans. | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-057 | THE system SHALL require entry, stop and target levels to be absolute prices that ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-058 | WHEN a seat cannot form a view, THE system SHALL record an abstention with ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-059 | WHEN a view is bearish, THE system SHALL let the plan implement it through ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-060 | THE system SHALL answer, for any plan at any time, whether it is active, ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-061 | WHEN a plan is revised, THE system SHALL create a new version and retain ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-062 | THE system SHALL link every plan to its predictions, its tribunal record when one ... | plan compiler and expression grammar, agents compiler seat | unit, property, fuzz | CTX-008 |
| SPEC-063 | THE system SHALL fill market orders at the opposite side of the observed quote ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-064 | THE system SHALL charge fees from the fee profile of the instrument's class and ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-065 | THE system SHALL increase modeled slippage with order size relative to observed volume or ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-066 | THE system SHALL accrue borrow cost on short sales, funding on perpetual positions at ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-067 | WHEN a leveraged position's equity falls below maintenance margin, THE system SHALL liquidate it ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-068 | THE system SHALL provide prices for every instrument class it trades, including a data-center ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-069 | THE system SHALL present the same order interface to seats for the virtual market ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-070 | THE system SHALL produce identical fills for identical prices, orders and random seed. | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-071 | WHILE an instrument's market is closed, THE system SHALL queue orders whose type allows ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-072 | IF the latest price for an instrument is older than its class's staleness limit ... | market engine, data prices, worker BookDesk | golden replay and contract | CTX-004, CTX-005 |
| SPEC-073 | THE system SHALL attach a heat dial from 1 to 10 to the firm, ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-074 | WHEN an owner changes a heat dial, THE system SHALL apply it from the ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-075 | THE system SHALL size each position at no more than the heat-scaled fractional Kelly ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-076 | WHEN an order would breach a hard limit (maximum position, gross or net exposure, ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-077 | WHEN a book falls below its high-water mark by its ladder levels, THE system ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-078 | THE system SHALL change envelope ceilings only through the operator owner action of SPEC-010. | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-079 | WHEN open positions sharing a driver would exceed the configured share of book value ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-080 | WHILE live execution is enabled, THE system SHALL block live orders in assets on ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-081 | THE system SHALL execute the risk gate and order release with no model call ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-082 | WHEN the risk gate vetoes an item, THE system SHALL not release it in ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-083 | WHEN a book's loss for the day reaches its daily loss limit, THE system ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-084 | THE system SHALL cap any position at the configured share of the instrument's average ... | risk engine, worker owner actions, BookDesk | property and integration | CTX-010, CTX-012 |
| SPEC-085 | THE system SHALL attach a pro case and a con case to every position ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-086 | WHEN a proposal exceeds the tribunal conviction or size threshold, or an owner requests ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-087 | WHEN a tribunal opens, THE system SHALL assign two advocates from different model families, ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-088 | THE system SHALL run each debate as opening, rebuttal, cross-examination and closing rounds in ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-089 | THE system SHALL assign a judge from a third model family that rules against ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-090 | WHEN a tribunal rules, THE system SHALL take the ruling's direction and conviction as ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-091 | THE system SHALL score every judge and advocate on the outcomes of the positions ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-092 | THE system SHALL pass every proposal through a confidence gate, a review by a ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-093 | WHEN a committee memo proposes a new strategy or a position above the committee ... | tribunal, agents routing, risk gate chain | integration | CTX-009, CTX-013 |
| SPEC-094 | WHEN a prediction is made, THE system SHALL commit it with a content hash, ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-095 | THE system SHALL reject a reveal without a matching commitment, exclude late commitments from ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-096 | WHEN verification runs, THE system SHALL recompute every prediction chain and report the first ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-097 | WHEN predictions resolve, THE system SHALL compute Brier score, clipped log loss, calibration curve, ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-098 | THE system SHALL report each scored group's skill against the base rate, persistence, a ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-099 | THE system SHALL use a prediction-market price only if its timestamp is at or ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-100 | THE system SHALL report forecast quality separately from trading return in every performance report. | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-101 | WHEN a seat's recalibration slope is below 0.8 on at least 200 resolved predictions, ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-102 | THE system SHALL record for every prediction its drivers (each with a type and, ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-103 | THE system SHALL flag incoherent sets of related predictions, including a joint probability above ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-104 | WHEN a driver resolves, THE system SHALL flag every prediction linked to it, directly ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-105 | THE system SHALL report weekly the calibration and score of predictions grouped by analytical ... | predict registry, scoring, graph | unit, property, golden | CTX-011 |
| SPEC-106 | THE system SHALL score assets on the configured scheme indicators (including payout promises above ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-107 | WHEN a scheme-flagged asset is held, THE system SHALL publish a daily collapse-hazard estimate ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-108 | WHILE a scheme position is held, THE system SHALL keep it only while the ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-109 | THE system SHALL place every asset whose scheme score crosses the threshold on the ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-110 | THE system SHALL flag pump-and-dump activity, wash-traded volume, spoofing patterns and liquidation cascades from ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-111 | THE system SHALL refuse order patterns that would trade against the firm's own resting ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-112 | THE system SHALL produce no content addressed to third parties that promotes an asset ... | risk special situations, integrity detectors, conduct checks | replay on recorded cases | CTX-015 |
| SPEC-113 | THE system SHALL keep an append-only running log for every position and every book, ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-114 | THE system SHALL annotate each book's log at least daily with an assessment of ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-115 | THE system SHALL publish the daily report by 06:00 Pacific time with these sections: ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-116 | THE system SHALL publish a weekly report with strategy review, promotions and demotions, tribunal ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-117 | THE system SHALL publish a monthly statement per book that quotes the ledger chain ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-118 | THE system SHALL publish an opportunity list in which each high-conviction opportunity carries a ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-119 | THE system SHALL attach to every reported decision a plain-language explanation of the concept ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-120 | THE system SHALL maintain a glossary that gains an entry the first time a ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-121 | THE system SHALL publish a target-feasibility report weekly and on owner request stating, from ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-122 | WHEN an owner requests a report on a topic or asset, THE system SHALL ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-123 | THE system SHALL publish a weekly institution study note on the reference institution's practices ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-124 | THE system SHALL run a standing macro book covering recession and bear-market positioning, policy-shock ... | reports, education, feasibility engine, storage logs | golden and integration | CTX-014 |
| SPEC-125 | THE system SHALL provide exactly two owner accounts (operator and partner) with password authentication, ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-126 | THE system SHALL show owners the books, positions, logs, reports, predictions, tribunal records, seat ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-127 | WHEN an owner asks any seat a question, THE system SHALL deliver an attributed ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-128 | WHEN an owner sends the chief executive an idea or instruction, THE system SHALL ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-129 | THE system SHALL let each owner open, fund with theoretical cash, trade, and close ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-130 | THE system SHALL show both owners the current and effective heat of every dial, ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-131 | THE system SHALL show the live switch only to the operator account, require a ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-132 | THE system SHALL end every message to the partner with the line 786110, and ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-133 | THE system SHALL compute a readiness scorecard of resolved predictions, weeks of record, calibration, ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-134 | THE system SHALL send each owner a notification for envelope changes, book stops, budget ... | portal, API Worker, owner actions | end-to-end and integration | CTX-012, CTX-018 |
| SPEC-135 | WHEN the system restarts at any boundary (before commit, after commit, after submit, after ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-136 | THE system SHALL meter every model call against the calling seat's budget and the ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-137 | THE system SHALL keep total monthly running cost at or under the firm ceiling ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-138 | THE system SHALL keep credentials and account identifiers out of every model prompt, and ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-139 | THE system SHALL read model routes, model identifiers, endpoints and prices only from configuration. | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-140 | THE system SHALL record a heartbeat for every active seat each cycle and open ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-141 | THE system SHALL export all records daily to durable storage outside the primary store ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-142 | THE system SHALL run the whole firm on a local runtime against recorded data ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-143 | THE system SHALL log every model call with seat, route, model identifier served, input ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-144 | IF a model provider fails or times out, THEN THE system SHALL retry within ... | runtime, agents budget and routing, worker BudgetMeter and Export, cli | fault injection and integration | CTX-003, CTX-009, CTX-010, CTX-021 |
| SPEC-145 | THE system SHALL include live adapters for the configured venues that pass the shared ... | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-146 | WHILE live execution is disabled, THE system SHALL make no network request to any ... | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-147 | WHEN live execution is enabled, THE system SHALL record a change event with actor, ... | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-148 | WHEN live mode starts, THE system SHALL refuse credentials whose venue-reported permissions include withdrawal. | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-149 | WHEN a live venue rejects an order, THE system SHALL record the venue's reason, ... | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-150 | WHILE live execution is enabled, THE system SHALL compare live fills with the virtual ... | market live adapters, worker live switch | contract on recorded responses | CTX-017 |
| SPEC-151 | THE system SHALL record money movements as balanced double entries in integer minor units, ... | ledger, storage, audit export | property and integration | CTX-004, CTX-021 |
| SPEC-152 | WHEN an owner requests a decision's history, THE system SHALL return its inputs, analyses, ... | ledger, storage, audit export | property and integration | CTX-004, CTX-021 |
| SPEC-153 | THE system SHALL verify every hash chain (ledger, predictions, decision log) on demand and ... | ledger, storage, audit export | property and integration | CTX-004, CTX-021 |
| SPEC-154 | THE system SHALL export the audit trail for any date range in a documented ... | ledger, storage, audit export | property and integration | CTX-004, CTX-021 |
| SPEC-155 | THE system SHALL record for every position-affecting action the model identifier served, the seat ... | ledger, storage, audit export | property and integration | CTX-004, CTX-021 |
| SPEC-156 | THE system SHALL promote a strategy framework to capital only after out-of-sample validation clears ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-157 | THE system SHALL register every backtest trial, including failures, and SHALL report the probability ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-158 | THE system SHALL re-validate promoted frameworks monthly and demote any that fail. | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-159 | THE system SHALL test competing frameworks on the same out-of-sample data and record their ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-160 | THE system SHALL fail its validation suite when a planted future price row or ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-161 | THE system SHALL check automatically that every tool referenced by a seat's prompt or ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-162 | THE system SHALL weight seat opinions in committee summaries by scored out-of-sample track record ... | runtime validation, agents weights, compilers whitelist check | integration | CTX-019, CTX-013 |
| SPEC-163 | IF a regulator order, warning or enforcement release names an asset, its issuer or ... | risk special situations and integrity gates, data venue quality | replay on recorded cases | CTX-015 |
| SPEC-164 | THE system SHALL compute a quality score for each venue's reported volume and SHALL ... | risk special situations and integrity gates, data venue quality | replay on recorded cases | CTX-015 |
| SPEC-165 | WHEN open interest and funding both exceed their trailing 90th percentiles for an asset, ... | risk special situations and integrity gates, data venue quality | replay on recorded cases | CTX-015 |
| SPEC-166 | THE system SHALL treat newly launched tokens and unvetted micro-capitalization securities as ineligible for ... | risk special situations and integrity gates, data venue quality | replay on recorded cases | CTX-015 |
| SPEC-167 | WHEN borrow cost and near-the-money call open interest both spike for a stock, or ... | risk special situations and integrity gates, data venue quality | replay on recorded cases | CTX-015 |
| SPEC-168 | THE system SHALL report each strategy's results against buy-and-hold, equal-weight and moving-average crossover baselines, ... | runtime validation, replay harness | integration on replay | CTX-019 |
| SPEC-169 | WHEN skill is claimed for any of several personas, seats or strategies tested together, ... | runtime validation, replay harness | integration on replay | CTX-019 |
| SPEC-170 | WHEN a historical evaluation window starts, THE system SHALL freeze the memory and lessons ... | runtime validation, replay harness | integration on replay | CTX-019 |
| SPEC-171 | THE system SHALL run each tribunal judgment in both side orders, score a flipped ... | tribunal protocol, predict holdout comparisons | integration | CTX-013, CTX-019 |
| SPEC-172 | THE system SHALL keep any added tribunal round, driver class or link type disabled ... | tribunal protocol, predict holdout comparisons | integration | CTX-013, CTX-019 |
| SPEC-173 | THE system SHALL include in each daily report two retrieval questions on concepts introduced ... | reports education | golden | CTX-014 |
| SPEC-174 | THE system SHALL publish the head of every hash chain daily to a location ... | ledger and predict anchors, worker Verify workflow | integration | CTX-011, CTX-021 |
