---
date: 2026-10-22 08:37:18 UTC
ver: 1.1.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [tasks, gated, dependency-ordered, spec-kit, autonomous-trading-firm]
layer: derived
---
# Tasks: Autonomous Trading Firm

**Input**: `spec.md` v1.1.0 (174 clauses), `plan.md` v1.1.0, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `.specify/memory/constitution.md` v1.0.0.

**Prerequisites**: the reset handoff was read, `python3 .specify/gates/verify-preparation.py` passed, and the session was started fresh (not as a subagent of the authoring session).

## Gate procedure (constitution Principle IX, applies to every task)

1. Read the clauses the task covers in `spec.md` and the decisions it cites in `plan.md`.
2. Write the tests first (unit, property, golden, contract or integration as named) and watch them fail for the right reason.
3. Implement until the task's Gate commands pass. Never weaken a test, threshold or gate to pass.
4. Run the global gate: `bun run typecheck && bun run lint && bun test` (from T002 onward) and `python3 .specify/gates/check-task-evidence.py`.
5. Record evidence in `specs/001-autonomous-trading-firm/evidence/T###.md` using `.specify/gates/evidence-template.md` (commands, exit codes, output digests, artifact hashes).
6. Append a ledger entry naming the task and overwrite `ledger/standing.md`.
7. Check the box, then commit with a message starting `T###:`. The commit hook refuses the commit if any checked task lacks evidence.
8. For tasks marked **Recovery**, write the recovery note in the evidence file before running the risky step.

Held-out evaluations live outside this repository; never open them. `[P]` marks tasks that touch disjoint files and may run in parallel. `[USn]` maps to the user stories in `spec.md` section 1.

## Phase 1: Setup

- [ ] T001 Move the legacy harness drafts out of the active tree: `git mv harness sources/legacy/harness-2026-10-03`, add a short section to `sources/legacy/README.md` explaining that `role-bindings.md`, `debate-protocol.md`, `venue-interfaces.md` and `date_clamp.py` are superseded by `packages/agents`, `packages/tribunal`, `contracts/order-interface.md` and `packages/data` respectively, and confirm no file content changed. This frees the `harness/` path for generated workspaces (plan, Project Structure) and keeps the legacy point-in-time tests as reference evidence for CTX-006.
  - Depends on: none. Paths: `harness/`, `sources/legacy/`. Covers: plan Structure Decision; SPEC-013 (path ownership).
  - Gate: `git status --porcelain | grep -c '^R'` equals the number of moved files; `git diff --stat -M HEAD -- sources/legacy | tail -1` shows only renames plus the README edit.

- [ ] T002 Create the Bun workspace root: `package.json` with workspaces `packages/*` and `apps/*`, `bunfig.toml`, `tsconfig.base.json` (strict, `noUncheckedIndexedAccess`, ES2023, bundler resolution), per-package `tsconfig.json` stubs for the fourteen packages and four apps named in plan.md, and extend `.gitignore` with `node_modules/`, `.wrangler/`, `dist/`, `.dev.vars`, `*.local.json`, `credentials*`, `harness/workspaces/**/node_modules`. Pin Bun in `package.json` `engines` and add a `packageManager` field. Commit the lockfile.
  - Depends on: T001. Paths: repository root, `packages/*/package.json`, `apps/*/package.json`. Covers: plan Technical Context; constitution VIII (secrets ignored).
  - Gate: `bun install --frozen-lockfile`; `git check-ignore -v .dev.vars credentials.local.json .wrangler/state` prints three matches; `git check-ignore specs/001-autonomous-trading-firm/spec.md` prints nothing.

- [ ] T003 Add tooling and scripts: Biome for lint and format, `bun run typecheck` (tsc build mode across workspaces), `lint`, `lint:routes` (fails on any model identifier literal outside `firm/routes/`), `lint:prose` (fails on cadence, budget or escalation numbers in `firm/seats/*.md` bodies), `test`, `test:worker`, `test:e2e`, `firm:check`, `firm:generate`, `dev`, `deploy:check`, `deploy`, `cli`, `eval:serve`, `ci`. Each script must work on an empty workspace (no-op passes) so later tasks only add content.
  - Depends on: T002. Paths: `package.json`, `biome.json`, `scripts/lint-routes.ts`, `scripts/lint-prose.ts`. Covers: SPEC-017, SPEC-139.
  - Gate: `bun run typecheck && bun run lint && bun run lint:routes && bun run lint:prose && bun test` all exit 0; a planted model identifier in a temporary file under `packages/` makes `lint:routes` exit non-zero (then remove it).

- [ ] T004 Activate the delivery gates: set `git config core.hooksPath .githooks`, add `.githooks/pre-commit` running `python3 .specify/gates/check-task-evidence.py`, confirm `.claude/settings.json` runs `.specify/gates/hook-guard-commit.py` on Bash and `.specify/gates/verify-preparation.py --brief` at session start, create `specs/001-autonomous-trading-firm/evidence/` with this task's own evidence as the first record, and add a gate self-test that plants a checked task without evidence in a temporary copy and confirms the checker fails.
  - Depends on: T003. Paths: `.githooks/`, `.claude/settings.json`, `.specify/gates/`, `tests/gates/`. Covers: constitution IX; plan CTX-020.
  - Gate: `python3 .specify/gates/check-task-evidence.py` exit 0; `bun test tests/gates` passes (the planted-violation case fails the checker as expected); a dry commit with an unevidenced checked task is refused by the hook.

- [ ] T005 [P] Add continuous integration in `.github/workflows/ci.yml` running `bun install --frozen-lockfile`, `bun run ci` (typecheck, lint, lint:routes, lint:prose, test, firm:check, gates, the patched spec-prep validator without the evaluator store, and a license check that fails on AGPL or GPL dependencies), with Bun pinned. Add `scripts/license-check.ts`. Local `bun run ci` must reproduce the workflow exactly so the gate can be run without the hosted runner.
  - Depends on: T003, T004. Paths: `.github/workflows/ci.yml`, `scripts/license-check.ts`. Covers: constitution VIII, IX; SPEC-161 (later wired).
  - Gate: `bun run ci` exit 0 locally; the license check flags a planted AGPL fixture package in `tests/fixtures/license/` and passes without it.

- [ ] T006 [P] Rewrite `README.md` for the new project: purpose (autonomous simulated-first trading firm for two owners), status (build in progress, live trading off), how to run the quickstart, repository layout from plan.md, where the specification, constitution and ledger live, and the evaluator boundary. Keep the legacy description only as a short history paragraph pointing to `sources/legacy/README.md`. No partner-identifying details (public repository).
  - Depends on: T001. Paths: `README.md`. Covers: constitution IV (honest status), R11 conflict C-25 (counts and missing validator claim).
  - Gate: `grep -c "Simulated" README.md` at least 1; `grep -ci "strata-validate.py" README.md` equals 0; Markdown lint via `bun run lint` passes.

## Phase 2: Foundation (blocks every user story)

- [ ] T010 Build `packages/core`: deterministic identifiers (`cycleId(kind, slot)`, `orderId(cycleId, planId, version, leg)` as the first 24 hex characters of SHA-256), time-ordered random identifiers (UUID version 7), a clock port with system and simulated implementations (accelerated replay), canonical JSON (sorted keys, no insignificant whitespace, integers as strings for bigint), SHA-256 helpers on Web Crypto (works in Bun and Workers), money and quantity types as scaled `bigint` with per-currency minor units and per-instrument scales, safe arithmetic with explicit rounding modes, and typed error classes.
  - Depends on: T003. Paths: `packages/core/src/*.ts`, `packages/core/test/*.test.ts`. Covers: data-model Conventions; SPEC-029, SPEC-070 (determinism foundations).
  - Gate: `bun test packages/core` with property tests (canonical JSON round trip and order independence, identifier determinism, arithmetic associativity within scale, rounding modes) all passing; coverage report at or above 95 percent lines for `packages/core`.

- [ ] T011 Build `packages/storage`: the storage port (repositories per aggregate), numbered SQL migrations implementing every table in `data-model.md` with unique keys for idempotency, append-only triggers that reject UPDATE and DELETE on ledger, logs, change events, predictions (commit columns), gate outcomes, tribunal rounds, decision log and call records, a `bun:sqlite` adapter and a D1 adapter sharing one SQL dialect, and an idempotent insert helper that returns the existing row on key conflict.
  - Depends on: T010. Paths: `packages/storage/src/`, `packages/storage/migrations/0001_init.sql` onward. Covers: SPEC-008, SPEC-113, SPEC-151 (append-only), SPEC-029 (idempotent writes).
  - Gate: `bun test packages/storage` passes on SQLite: migrations apply cleanly from empty, every append-only table rejects UPDATE and DELETE, duplicate inserts return the original row, every state-changing table rejects a row without `actor`.
  - Recovery: migrations are forward-only; a faulty migration is fixed by a new numbered migration, never by editing an applied one.

- [ ] T012 Build `packages/ledger`: balanced double-entry posting in integer minor units, hash sealing (SHA-256 over canonical JSON with the previous seal, genesis of 64 zeros), reversing-entry corrections, chain verification reporting the first divergent sequence, statement assembly with the chain head, export to newline-delimited JSON and import into a fresh store with verification. Port the vantage portal's ledger concepts (canonicalize, seal, verify) without copying its storage code.
  - Depends on: T011. Paths: `packages/ledger/src/`, `packages/ledger/test/`. Covers: SPEC-151, SPEC-153, SPEC-154, SPEC-117 (head quoting).
  - Gate: `bun test packages/ledger` with property tests: every posted entry sums to zero per currency; tampering with any field of any entry is reported at exactly that sequence; export then import reproduces identical heads.

- [ ] T013 Build `packages/registry`: Zod schemas and loaders for seats (`contracts/seat-definition.md`), skills (folder name equals declared name, non-empty description, pinned external skills verified by commit and SHA-256), rules, cycle graphs (`contracts/cycle-graph.md`), personas, strategies, the heat map, the runtime manifest, model routes (`contracts/model-routes.md`) and the instrument catalog. Validation errors name the file, field and defect. Reporting lines must resolve to the chief executive within six hops without cycles; tool grants must fit authority classes; only the execution trader may hold order release.
  - Depends on: T010. Paths: `packages/registry/src/`, `packages/registry/test/fixtures/`. Covers: SPEC-001, SPEC-002 (structure), SPEC-016, SPEC-018, SPEC-019.
  - Gate: `bun test packages/registry` passes, including negative fixtures for a missing body section, an uncapped loop, a dangling input, an undeclared output, a renamed skill folder, a tampered pinned skill, a reporting cycle and an order-release grant to a non-trader seat; each is refused with the defect named.

- [ ] T014 Write the canonical office and investment seats in `firm/seats/`: chief executive, chief investment officer, house portfolio manager, persona portfolio manager (per-persona instances), strategy portfolio manager (per-strategy), macro strategist, crypto markets analyst, conventional markets analyst, news and event analyst, quantitative researcher, special situations analyst, prediction markets analyst and strategy compiler, plus `firm/company.md`. Base analyst and manager prose on the upstream TradingAgents role prompts already in `sources/tradingagents/` (Apache-2.0) with provenance fields, rewritten so no text mentions simulation, paper trading or virtual money.
  - Depends on: T013. Paths: `firm/company.md`, `firm/seats/*.md`. Covers: SPEC-001, SPEC-002, SPEC-052 (no simulation language), ORG-01 to ORG-08.
  - Gate: `bun run firm:check` loads every seat; `bun test packages/registry` passes; the context lint (`bun run lint:prose`) finds zero simulation terms and zero numeric cadence or budget values in seat bodies.

- [ ] T015 [P] Write the challenge, risk, compliance, operations, education and audit seats in `firm/seats/`: red team (advocates and judges), chief risk officer, market risk analyst, market integrity analyst, model validation, prediction scoring, chief compliance officer, pre-trade compliance, conduct surveillance, chief operating officer (including the triage function), execution trader, reconciliation, fund accounting, controller, data engineering, release control, records keeper, investor education and reporting, and internal audit (reports to owners). Each declares outputs with contract identifiers, authority classes, must-not lists and route constraints.
  - Depends on: T013. Paths: `firm/seats/*.md`. Covers: SPEC-002, SPEC-006, SPEC-007, SPEC-092 (family constraints), SPEC-162.
  - Gate: `bun run firm:check` shows 32 seat types; a test asserts only `execution-trader` holds order release, only `fund-accounting` holds booking, only `controller` holds NAV publication, and `internal-audit` reports to owners.

- [ ] T016 [P] Write skills and rules: `firm/skills/<name>/SKILL.md` for limit checks, drawdown ladder, stress scenarios, price structure, funding and basis, on-chain flows, news triage, filings reading, prediction writing, calibration, case writing, debate rounds, judging rubric, plan writing, plan compilation, concept explanation, glossary entry writing, idea notes, feasibility explanation and scheme forensics; `firm/rules/*.md` for numeric grounding, untrusted content, no simulation language, abstention, separation of duties and partner sign-off (786110).
  - Depends on: T013. Paths: `firm/skills/`, `firm/rules/`. Covers: SPEC-019, SPEC-036, SPEC-037, SPEC-058, SPEC-119, SPEC-132.
  - Gate: `bun run firm:check` passes; every skill referenced by a seat exists; every rule referenced exists; `lint:prose` passes.

- [ ] T017 Write `firm/cycles/*.yaml` for the shipped graphs in `contracts/cycle-graph.md`, `firm/manifest/runtime.yaml` (cadence per seat, budget shares summing to one million parts per million, essential reserve 20 percent, escalation paths), `firm/heat/heat-map.yaml` with the plan CTX-012 table, `firm/routes/models.yaml` with the economy-api and subscription profiles (unverified values marked so activation refuses them), and `firm/instruments/crypto.yaml` for the launch crypto set with fee profiles, scales, staleness limits and calendars.
  - Depends on: T013. Paths: `firm/cycles/`, `firm/manifest/`, `firm/heat/`, `firm/routes/`, `firm/instruments/`. Covers: SPEC-017, SPEC-018, SPEC-073, SPEC-137, SPEC-139.
  - Gate: `bun run firm:check` passes; a test asserts budget shares sum to 1,000,000 ppm, heat rows are monotonic in risk, and activating a route with an unverified placeholder fails.

- [ ] T018 Build `packages/data` point-in-time core: storage of bars, quotes and data items with source, retrieval time and effective time; the as-of reader (effective time at or before the decision); skew quarantine beyond five minutes; gap records and unavailable labels; undated-item exclusion; replay masking with consistent per-run aliases for symbols and dates; lesson gating by resolution time; static calendars for XNYS (2026 to 2028, holidays and early closes), CME Globex, spot foreign exchange and always-open crypto, each with recorded generation provenance.
  - Depends on: T011. Paths: `packages/data/src/pit/`, `packages/data/src/calendars/`, `packages/data/test/`. Covers: SPEC-026, SPEC-032, SPEC-033, SPEC-034, SPEC-035, SPEC-041, SPEC-042, SPEC-160.
  - Gate: `bun test packages/data` passes, including the leak suite (planted future price rows and future-dated articles never reach an as-of read; a deliberately leaking reader variant fails the suite), the skew quarantine test, masking tests and calendar tests for the 2026 holidays and early closes.

- [ ] T019 [P] Build public test fixtures in `tests/fixtures/`: a seeded generator (`tests/fixtures/generate.ts`, seed 786110) for crypto tapes (48 hours, six pairs, planted gap, stale period and gap move), a multi-asset week tape, scheme case series and manipulation tapes distinct from any evaluator material, plus recorded venue and data responses transcribed from each provider's public documentation or SDK examples with their source noted. Fixtures are deterministic and regenerated by script, never edited by hand.
  - Depends on: T010. Paths: `tests/fixtures/`. Covers: SPEC-063 to SPEC-072 (inputs), SPEC-106 to SPEC-110 (inputs), SPEC-145 (recorded responses).
  - Gate: `bun run tests/fixtures/generate.ts --check` regenerates byte-identical files; every recorded response file names its source URL and retrieval date in a sidecar `.source.json`.

## Phase 3: User Story 1, the firm runs itself on crypto (P1, MVP)

**Goal**: an unattended firm that researches, plans, compiles, gates, executes in the virtual market, commits predictions and logs, locally and in the cloud. **Independent test**: spec section 1, User Story 1.

- [ ] T030 [P] [US1] Implement crypto data adapters in `packages/data/src/sources/`: Coinbase Exchange public candles and tickers (primary spot), Kraken public OHLC (fallback), Hyperliquid info for funding, open interest, mark and index (read-only), each with host configuration, feed label, cadence, documented rate limits with backoff on 429, response validation with Zod, and conversion into point-in-time rows. Network access goes through an injectable fetch so tests replay recorded responses and the live smoke test (T190) can run against real hosts.
  - Depends on: T018, T019. Paths: `packages/data/src/sources/{coinbase,kraken,hyperliquid}.ts`. Covers: SPEC-031 (crypto dimensions), SPEC-032, SPEC-040, SPEC-072 (staleness inputs).
  - Gate: `bun test packages/data/test/sources` passes on recorded responses, including a 429 backoff case, a malformed payload rejected with a gap record, and a fallback switch from the primary to the secondary source.

- [ ] T031 [US1] Implement the virtual market engine in `packages/market/src/engine/`: market fills at the opposite quote plus square-root impact slippage, limit and stop triggering on observed crossings with gapped stops filled at the first available price, fee profiles per class and venue, participation cap (default 5 percent) with partial fills and working remainders, staleness refusal, market-calendar refusal or queueing by order type, and full determinism for identical prices, orders and seed.
  - Depends on: T010, T018. Paths: `packages/market/src/engine/`, `packages/market/test/engine/`. Covers: SPEC-063, SPEC-064, SPEC-065, SPEC-070, SPEC-071, SPEC-072, SPEC-027.
  - Gate: `bun test packages/market/test/engine` passes golden replays of the 48-hour crypto tape; two runs with seed 786110 produce byte-identical fill files; every fill timestamp is later than its decision timestamp.

- [ ] T032 [US1] Implement financing and margin in `packages/market/src/financing/`: perpetual funding accrual per venue interval (default 0.01 percent per 8 hours when history is missing), borrow cost on short sales, maintenance margin, liquidation at the modeled price with event records, and leverage accounting that the risk engine reads. Funding and borrow entries post to the ledger through fund accounting interfaces, never directly.
  - Depends on: T031, T012. Paths: `packages/market/src/financing/`. Covers: SPEC-066, SPEC-067.
  - Gate: `bun test packages/market/test/financing` passes: a 3x position driven through maintenance liquidates at the modeled price; six funding intervals produce six entries matching hand-computed amounts; borrow accrual over five days is within one cent.

- [ ] T033 [US1] Implement wallets and valuation in `packages/market/src/wallets/`: multi-currency cash, positions with lots and cost basis, realized and unrealized results, fees and financing separated, net asset value snapshots, the controller's independent recomputation with a publication block on breaks above tolerance (0.1 percent), per-cycle reconciliation against the ledger, and benchmark books (buy-and-hold bitcoin, broad US equity index fund, 60/40, cash).
  - Depends on: T031, T032, T012. Paths: `packages/market/src/wallets/`, `packages/runtime/src/benchmarks.ts`. Covers: SPEC-007, SPEC-044, SPEC-046, SPEC-047, SPEC-050.
  - Gate: `bun test packages/market/test/wallets` passes: independent recomputation matches to the cent on the tape run; a planted one-cent ledger difference produces a reconciliation break; a planted controller mismatch blocks publication.

- [ ] T034 [US1] Implement `packages/plan`: the `plan/v1` schema, the Pratt parser and type checker for the expression grammar with the whitelisted function table, and the compiler checks in `contracts/plan-language.md` (instrument and class enablement, short-side form availability, absolute grounded levels, stop on the loss side, persona constraints, size within limits, calendar fit, linked predictions), returning machine-readable reasons; plus plan status queries and versioning.
  - Depends on: T013, T018. Paths: `packages/plan/src/`, `packages/plan/test/`. Covers: SPEC-048, SPEC-053, SPEC-054, SPEC-055, SPEC-056, SPEC-057, SPEC-058, SPEC-059, SPEC-060, SPEC-061, SPEC-062.
  - Gate: `bun test packages/plan` passes, including ten invalid-plan fixtures each rejected with its reason and a fuzz run of 10,000 generated expressions where no evaluation reaches anything outside the whitelist and every unknown name fails compilation.

- [ ] T035 [US1] Implement `packages/risk` core: heat mapping from `firm/heat/heat-map.yaml` with envelope clamping, sizing at the heat-scaled fractional Kelly of shrunk measured edge with an exploratory cap (0.5 percent of book value under 30 resolved outcomes), hard limits (position, gross and net exposure, leverage ceiling, daily loss, order value, turnover), the three-level drawdown ladder with the operator-only house resume, daily loss stops, the average-daily-volume cap with staged exits, and veto finality within a cycle. The package must not import any model client.
  - Depends on: T013, T033. Paths: `packages/risk/src/`, `packages/risk/test/`. Covers: SPEC-073, SPEC-075, SPEC-076, SPEC-077, SPEC-081, SPEC-082, SPEC-083, SPEC-084.
  - Gate: `bun test packages/risk` passes with property tests (no generated order exceeds any limit; sizes never exceed the Kelly computation); a dependency check script (`scripts/check-no-model-imports.ts packages/risk packages/market/src/engine`) exits 0 and fails when a model client import is planted.

- [ ] T036 [US1] Implement `packages/predict` registry and scoring: commit with content hash, sequence, timestamp and previous hash before the horizon; sealed salt and content until reveal; rejection of reveals without commits; exclusion of late commits; worst-case scoring of unrevealed predictions; chain verification; Brier score, clipped log loss (clip 0.001), ten-bin calibration, expected calibration error and recalibration slope by logistic fit, per seat, horizon and class.
  - Depends on: T011. Paths: `packages/predict/src/registry/`, `packages/predict/src/scoring/`. Covers: SPEC-094, SPEC-095, SPEC-096, SPEC-097.
  - Gate: `bun test packages/predict` passes: metrics on a seeded 300-prediction set match an independent reference implementation in the test to four decimals; altering one stored record is reported at its sequence; a reveal without commit is refused.

- [ ] T037 [US1] Implement the seat runner in `packages/agents`: prompt assembly from compiled seat definitions, skills, rules and a context packet; an OpenAI-compatible client with JSON-schema output where supported and validated JSON otherwise (one repair attempt, then abstention); a tool loop limited by the seat's authority classes and turn cap; the untrusted-content envelope; numeric grounding that rejects trade-relevant numbers absent from the run's tool results; transcript storage with hashes; call records with all eight fields; routing through `firm/routes/models.yaml` with fallbacks; and a scripted provider for tests.
  - Depends on: T013, T016, T017. Paths: `packages/agents/src/{runner,client,tools,grounding,envelope,routing}.ts`. Covers: SPEC-016, SPEC-020, SPEC-036, SPEC-037, SPEC-058, SPEC-138, SPEC-139, SPEC-143, SPEC-144.
  - Gate: `bun test packages/agents` passes: an injected ungrounded price is rejected naming the number; the 50-item public injection corpus in `tests/fixtures/injection/` triggers zero tool calls; a blocked primary route falls back; both routes blocked records a skipped step; no prompt contains planted credential patterns.

- [ ] T038 [P] [US1] Define output contracts for every seat type in `packages/agents/src/contracts/` (analysis per dimension, proposal, compiled plan, case, review verdict, risk verdict, ruling, agenda, allocation memo, staffing change, answer, report narrative) and implement the agent-context lint that scans every assembled prompt for the configured simulation-term denylist before sending, failing closed.
  - Depends on: T037. Paths: `packages/agents/src/contracts/`, `packages/agents/src/context-lint.ts`. Covers: SPEC-020, SPEC-052, SPEC-058.
  - Gate: `bun test packages/agents/test/contracts` passes; a context containing "paper trading" or "simulated" is refused before any provider call; every seat's declared output contract resolves to a schema.

- [ ] T039 [US1] Implement `packages/runtime`: the step-graph executor shared by local and cloud runtimes, the first-step reconciliation (books, open orders, predictions versus the store, recording breaks), the deterministic materiality scanner over strategy-template signals, cycle and step records, heartbeats and incident opening after three missed heartbeats, idempotent slot handling, and the local scheduler with an accelerated clock for replays and the quickstart.
  - Depends on: T013, T017, T037. Paths: `packages/runtime/src/`. Covers: SPEC-021, SPEC-022, SPEC-023, SPEC-028, SPEC-029, SPEC-030, SPEC-140.
  - Gate: `bun test packages/runtime` passes: duplicate slot triggers yield one cycle; a killed cycle after compilation releases nothing and the next cycle reconciles with zero unexplained differences; a silent seat opens one incident after three cycles.

- [ ] T040 [P] [US1] Write the persona and strategy library: `firm/personas/*.md` for the 28 personas from research report R08 (20 marked active at launch) with worldview, risk profile, horizon, constraints, behavioral bias parameters, starting capital and default heat; `firm/strategies/*.md` for the strategy templates (signal, entry, exit, sizing, rebalance, parameter ranges, heat hook and two failure regimes each). No text mentions simulation.
  - Depends on: T013. Paths: `firm/personas/`, `firm/strategies/`. Covers: SPEC-043, SPEC-048, SPEC-056, QA-01 inputs.
  - Gate: `bun run firm:check` passes; a test asserts twenty active personas with pairwise-distinct profiles and that every strategy template declares all required fields.

- [ ] T041 [US1] Bootstrap books and organization behavior in `packages/runtime/src/firm/`: create the house book (heat 8, theoretical 100,000 US dollars), twenty persona books, strategy books, owner sandbox capability and four benchmark books; implement the chief executive agenda, allocation changes with ceiling checks, staffing revisions that cannot touch limits or scoring rules, and the separation-of-duties approval check used by every gate.
  - Depends on: T033, T035, T039, T040. Paths: `packages/runtime/src/firm/`. Covers: SPEC-002, SPEC-003, SPEC-004, SPEC-005, SPEC-006, SPEC-007, SPEC-043, SPEC-044.
  - Gate: `bun test packages/runtime/test/firm` passes: self-approval and approval by the analysis author are refused; an allocation over a ceiling is refused naming it; a staffing change editing a limit is refused while a prompt-only revision is stored with both versions.

- [ ] T042 [US1] Implement the gate chain and cases in `packages/runtime/src/gates/`: pro and con cases from the red team for every proposal, the confidence gate on calibrated probability, review by a seat on a different model family from the proposer, the deterministic risk gate, stop at the first veto, and release by the execution trader only through BookDesk or the local equivalent.
  - Depends on: T035, T037, T041. Paths: `packages/runtime/src/gates/`. Covers: SPEC-085, SPEC-092, SPEC-006, SPEC-007, SPEC-082.
  - Gate: `bun test packages/runtime/test/gates` passes: four seeded proposals stop at confidence, review, risk and none respectively; proposer and reviewer families differ in every record; a vetoed item resubmitted with new wording is not released in the same cycle.

- [ ] T043 [US1] Wire the full research cycle locally in `apps/cli` and `packages/runtime`: reconcile, snapshot, scan, triage, analysts on material instruments, proposals, compilation, cases, gates, release, prediction commits and log appends, using the scripted provider and the 48-hour crypto tape; add `bun run cli run --local --tape ... --speed ... --hours ...` and `bun run cli verify --local`.
  - Depends on: T030, T034, T036, T042. Paths: `apps/cli/src/`, `packages/runtime/src/cycles/research.ts`. Covers: SPEC-021, SPEC-022, SPEC-031, SPEC-053, SPEC-094, SPEC-113, SPEC-142.
  - Gate: `bun test tests/integration/us1-local.test.ts` passes the User Story 1 independent test on the 48-hour tape (at least 191 of 192 cycles complete; every executed plan has a compiled structure, fills, wallet updates, committed predictions and log entries); `bun run cli verify --local` reports all chains clean.

- [ ] T044 [US1] Build the fault-injection harness in `tests/fault/`: crash points before commit, after commit, after submit and after acknowledgment across 100 seeded trials; duplicate trigger delivery 1 to 40 seconds apart; and comparison of prediction, order, fill and ledger counts with a no-crash reference run.
  - Depends on: T043. Paths: `tests/fault/`. Covers: SPEC-029, SPEC-135, DUR-01.
  - Gate: `bun test tests/fault` passes with zero lost and zero duplicated records in all 100 trials; the summary is written to the evidence file.

- [ ] T045 [US1] Create the cloud run plane in `apps/worker`: `wrangler.jsonc` for the `firm-run` Worker (D1 `firm`, R2 `firm-artifacts`, Workflows ResearchCycle, BookAnalysis, DailyRhythm, WeeklyReview, MonthlyStatement, Tribunal, OwnerRequest, Export, VerifyAndAnchor, IngestMinute; Durable Objects BookDesk and BudgetMeter; Cron Triggers every minute, every 15 minutes and hourly; compatibility date pinned; `nodejs_compat`), the D1 storage adapter wiring, and Cron handlers that create Workflow instances with deterministic identifiers through batch creation so duplicates are skipped.
  - Depends on: T039, T043. Paths: `apps/worker/wrangler.jsonc`, `apps/worker/src/{index,cron,workflows/*}.ts`. Covers: SPEC-021, SPEC-029, SPEC-135, plan CTX-002, CTX-003.
  - Gate: `bun run test:worker` passes Workers-pool integration tests: a cron fired twice for one slot yields one instance; a ResearchCycle instance completes against recorded responses; migrations apply to the local D1.
  - Recovery: binding names and migration order are recorded in `docs/deploy.md`; a broken deploy rolls back with `wrangler rollback`.

- [ ] T046 [US1] Implement the BookDesk Durable Object in `apps/worker/src/objects/book-desk.ts`: per-book serialization of order acceptance, pre-submission checks, fills, wallet updates and ledger postings written to D1 in one batch keyed by deterministic identifiers; working orders kept in object storage with a one-minute alarm while any are open; idempotent resubmission returning the original acknowledgment.
  - Depends on: T045, T031, T033. Paths: `apps/worker/src/objects/book-desk.ts`. Covers: SPEC-063 to SPEC-072, SPEC-069, SPEC-135, SPEC-151.
  - Gate: `bun run test:worker` passes: concurrent submissions to one book serialize without double fills; an alarm evaluates a working limit order when price crosses; an object restart mid-batch leaves no partial ledger entry.

- [ ] T047 [US1] Implement the BudgetMeter Durable Object and throttle policy in `apps/worker/src/objects/budget-meter.ts` and `packages/agents/src/budget.ts`: per-seat and firm metering in micro-dollars, alerts at 50 and 80 percent, seat pause at 100 percent with chief executive reassignment or deferral, pro-rata month curve, essential reserve of 20 percent, and the throttle order from plan CTX-010.
  - Depends on: T045, T037. Paths: `apps/worker/src/objects/budget-meter.ts`, `packages/agents/src/budget.ts`. Covers: SPEC-136, SPEC-137, SPEC-143.
  - Gate: `bun run test:worker` passes a simulated month at three times normal load that stays under the 25-dollar ceiling, throttles non-essential seats first and never pauses risk, execution, records or reporting seats.

- [ ] T048 [US1] Implement owner envelope actions in `apps/worker/src/api/actions.ts` with change events: operator-only live switch, ceilings, restricted-list lifts and house resume; either-owner pause, resume and heat changes effective next cycle with clamping to ceilings, conflict resolution to the more conservative value within a cycle, and notifications to the other owner. Seats have no route to these handlers.
  - Depends on: T045, T035. Paths: `apps/worker/src/api/actions.ts`, `packages/runtime/src/envelope.ts`. Covers: SPEC-010, SPEC-011, SPEC-012, SPEC-074, SPEC-078, SPEC-134.
  - Gate: `bun run test:worker` passes the role matrix (partner refused for operator actions, both owners can pause), the same-cycle conflict case and the clamp case; every applied action has a change event with prior and new values.

- [ ] T049 [US1] Implement running logs and daily annotations in `packages/reports/src/logs.ts`: append-only position and book logs fed by fills, hourly analyses and daily assessments, with the hourly BookAnalysis workflow analyzing every active book.
  - Depends on: T043. Paths: `packages/reports/src/logs.ts`, `packages/runtime/src/cycles/book-analysis.ts`. Covers: SPEC-023, SPEC-113, SPEC-114.
  - Gate: `bun test packages/reports/test/logs` passes: 24 hourly entries per active book over a replayed day; an edit attempt is rejected; each book has a daily assessment referencing that day's entries.

- [ ] T050 [US1] Run the User Story 1 acceptance in the Workers runtime: a 48-hour accelerated replay through `firm-run` in local mode with recorded responses, verifying completion rate, plan structures, fills, wallet updates, predictions, logs, zero order-endpoint requests and the fault-injection subset at Worker boundaries; record the summary as evidence and in the ledger.
  - Depends on: T044, T046, T047, T048, T049. Paths: `tests/integration/us1-worker.test.ts`. Covers: User Story 1; SPEC-009, SPEC-028, SPEC-146.
  - Gate: `bun run test:worker -- us1-worker` passes; the evidence lists completion rate, cycle counts, record counts and the network spy summary.

## Phase 4: User Story 2, the owners learn from reports (P1)

- [ ] T060 [US2] Implement the daily report builder in `packages/reports/src/daily.ts` per `contracts/reports.md`: twelve sections, the education block on every decision (concept card, glossary link, other side of the trade, change-of-mind condition with a numeric falsifier, lesson when resolved), glossary creation on first use, spaced review scheduling, two retrieval questions on earlier concepts, deterministic mode labels and provenance on every figure; publication by 06:00 Pacific with daylight saving handled in code.
  - Depends on: T049, T036. Paths: `packages/reports/src/{daily,education,glossary}.ts`, `firm/cycles/daily-rhythm.yaml`. Covers: SPEC-024, SPEC-038, SPEC-051, SPEC-115, SPEC-119, SPEC-120, SPEC-173.
  - Gate: `bun test packages/reports/test/daily` passes golden reports for a replayed week, including a daylight-saving transition day; every decision carries all five education elements; every figure has source and time.

- [ ] T061 [P] [US2] Implement weekly and monthly reports in `packages/reports/src/{weekly,monthly}.ts`: strategy review with promotions and demotions, baselines and ablation summary, tribunal and judge scores, feasibility, institution note slot, macro review, calibration by complexity bucket and curriculum topics; monthly statements per book quoting the ledger head and anchor reference.
  - Depends on: T060, T012. Paths: `packages/reports/src/`. Covers: SPEC-025, SPEC-116, SPEC-117, SPEC-105 (report part).
  - Gate: `bun test packages/reports/test/weekly` passes on an 8-day replay; the monthly statement's head equals the ledger head at statement time.

- [ ] T062 [US2] Implement the target-feasibility engine in `packages/reports/src/feasibility.ts`: required win rate for 1, 2 and 3 percent per day at the measured payoff ratio and trade frequency, realized edge, seeded resampling of the realized trade distribution (100,000 paths) for 30- and 90-day attainment at current sizing, required sizing per target, risk of ruin to the house stop at current and required sizing, and the daily 95 percent value-at-risk equivalent, each with an interval and a plain-language verdict that never calls a target expected unless the record supports it.
  - Depends on: T033, T036. Paths: `packages/reports/src/feasibility.ts`. Covers: SPEC-121, RISK-02.
  - Gate: `bun test packages/reports/test/feasibility` matches an independent analytic and Monte Carlo reference within 0.5 percentage points on a 120-trade fixture and completes 100,000 paths in under 20 seconds of CPU.

- [ ] T063 [P] [US2] Implement the opportunity list, goodness scoring with reasons and track-record figures, measured hit rate per score band, idea notes with all seven parts, and the readiness scorecard (resolved predictions, weeks of record, calibration, net return after costs, maximum drawdown, feasibility) labeled as guidance.
  - Depends on: T060, T062. Paths: `packages/reports/src/{opportunities,scorecard}.ts`. Covers: SPEC-118, SPEC-133, SPEC-173.
  - Gate: `bun test packages/reports/test/opportunities` passes; track-record figures equal the scored record; the scorecard matches recomputation.

- [ ] T064 [P] [US2] Implement the deep research report format and the owner-request workflow for on-demand reports in `packages/reports/src/deep.ts` and `firm/cycles/owner-request.yaml`: nine sections with stored sources and verbatim quotes checked against stored text.
  - Depends on: T037, T060. Paths: `packages/reports/src/deep.ts`. Covers: SPEC-039, SPEC-122.
  - Gate: `bun test packages/reports/test/deep` passes on a scripted request; every quote matches stored source text exactly.

## Phase 5: User Story 3, the owners steer from outside (P2)

- [ ] T070 [US3] Implement the Hono API in `apps/worker/src/api/` per `contracts/owner-api.md`: PBKDF2-SHA-256 password hashing (310,000 iterations, per-user salt), signed session cookies with a D1 session table and expiry, lockout after ten failures, CSRF tokens on mutations, exactly two owner accounts seeded by `bun run cli seed:owners` (credentials printed once, only hashes stored), every read endpoint and the mode field from the envelope.
  - Depends on: T048, T060. Paths: `apps/worker/src/api/`, `apps/cli/src/seed-owners.ts`. Covers: SPEC-125, SPEC-126, SPEC-152.
  - Gate: `bun run test:worker -- api` passes authentication, lockout, expiry, CSRF and role tests; a third account cannot be created through the API.
  - Recovery: credentials are rotated by re-running `seed:owners --rotate`; nothing secret is committed.

- [ ] T071 [US3] Build the SvelteKit portal in `apps/portal` (Svelte 5, shadcn-svelte, LayerChart, `@sveltejs/adapter-cloudflare`, service binding to the API Worker): sign-in, overview with the deterministic mode label, books with positions, ladders and logs, reports reader, predictions with scores and graph views, tribunal records, organization chart with seat status and budgets, costs, ledger with verification status; light theme default for documents, responsive layout, reduced-motion support, the 786110 motif used subtly and never on error, loss or alert views.
  - Depends on: T070. Paths: `apps/portal/src/`. Covers: SPEC-051, SPEC-126, SPEC-132.
  - Gate: `bun run test:e2e -- portal-views` passes in the preinstalled Chromium for both accounts; screenshots of each view are attached to the evidence; an accessibility scan reports no critical issues.

- [ ] T072 [US3] Implement owner questions and ideas end to end: portal forms, API endpoints, the OwnerRequest workflow routing a question to the named seat and an idea to the chief executive, attributed answers citing record identifiers within one cycle, acknowledgments within one cycle and dispositions with reasons within one day, partner-facing replies ending with 786110.
  - Depends on: T070, T071, T037. Paths: `apps/worker/src/workflows/owner-request.ts`, `apps/portal/src/routes/console/`. Covers: SPEC-127, SPEC-128, SPEC-132, SPEC-009.
  - Gate: `bun run test:worker -- owner-request` and `bun run test:e2e -- console` pass; a replayed day with 20 questions answers at least 19 within one cycle while cycle completion stays at or above 99 percent.

- [ ] T073 [P] [US3] Implement sandboxes: open with theoretical cash (default 10,000 US dollars), trade at live prices with the same costs, close, propose trades for seat review, and compare against agent books and benchmarks, in the API and portal. Review packets sent to seats label the book as an owner account with no mode words, and the context lint (T038) covers these packets.
  - Depends on: T070, T046. Paths: `apps/worker/src/api/sandboxes.ts`, `apps/portal/src/routes/sandboxes/`. Covers: SPEC-045, SPEC-129.
  - Gate: `bun run test:worker -- sandboxes` passes: a sandbox and an agent book buying the same quantity in the same minute get identical fills and fees; a proposal receives a seat review record.

- [ ] T074 [P] [US3] Implement dial and pause controls in the portal: current, effective, ceiling and history for every dial; changes effective next cycle; conflict notices; pause and resume of the firm or any book; operator-only envelope editor, restricted-list lift with acknowledgment text, house resume, and the live switch with the exact confirmation phrase and the readiness scorecard beside it.
  - Depends on: T048, T063, T071. Paths: `apps/portal/src/routes/{dials,controls}/`. Covers: SPEC-010, SPEC-011, SPEC-074, SPEC-130, SPEC-131.
  - Gate: `bun run test:e2e -- controls` passes for both accounts: the partner sees no live switch or envelope editor; a wrong phrase is refused; dial history matches records.

- [ ] T075 [P] [US3] Implement notifications: envelope changes, book stops, budget alerts, live switch changes, pauses and conflicts delivered to both owners within one cycle in the portal (and email later if the owners add a mail route), with partner messages ending in 786110 except error, loss and alert kinds.
  - Depends on: T048, T071. Paths: `apps/worker/src/notify.ts`, `apps/portal/src/routes/notifications/`. Covers: SPEC-132, SPEC-134.
  - Gate: `bun run test:worker -- notify` passes for all five event kinds; a scan of alert and loss notifications finds no 786110.

## Phase 6: User Story 4, every automatable asset class (P2)

- [ ] T080 [US4] Extend the instrument catalog in `firm/instruments/` for stocks, funds (including inverse funds), options, bonds and bond funds, foreign exchange, gold and oil references, crypto perpetuals, binary event contracts and the GPU index, each with calendar, price source and fallback, staleness limit, fee profile, short-side forms, scale and lot rules; extend calendars for options expiries and event-contract settlement.
  - Depends on: T017, T018. Paths: `firm/instruments/*.yaml`, `packages/data/src/calendars/`. Covers: SPEC-026, SPEC-059, SPEC-068, SPEC-071.
  - Gate: `bun run firm:check` passes; calendar tests cover the 2026 XNYS holidays and early closes, CME Globex hours and the foreign-exchange weekly boundary.

- [ ] T081 [P] [US4] Implement equity, fund and options adapters: Alpaca market data with an optional operator key (IEX feed labeled), Yahoo chart and options endpoints as labeled research-only fallback, and corporate-action handling (splits and dividends) in positions; recorded fixtures for each response type.
  - Depends on: T030, T080. Paths: `packages/data/src/sources/{alpaca,yahoo}.ts`, `packages/market/src/corporate-actions.ts`. Covers: SPEC-031, SPEC-032, SPEC-068.
  - Gate: `bun test packages/data/test/sources/equities` passes on recorded responses; a split fixture adjusts quantity and cost basis exactly.

- [ ] T082 [P] [US4] Implement foreign exchange, commodity and rates adapters: central-bank reference rates (daily) with a research-only intraday fallback, gold and oil through listed funds and tokenized gold, FRED graph CSV and Treasury fiscal data for yields, with bond pricing from yields where funds are not used.
  - Depends on: T030, T080. Paths: `packages/data/src/sources/{frankfurter,fred,treasury}.ts`, `packages/market/src/bonds.ts`. Covers: SPEC-031, SPEC-068.
  - Gate: `bun test packages/data/test/sources/macro` passes; bond price from a recorded yield matches a reference duration computation.

- [ ] T083 [P] [US4] Implement prediction-market and GPU sources: Polymarket market listings and price history, Kalshi public market data, Manifold as a fallback, each returning prices with their own timestamps; GPU index composition from vast.ai offers and RunPod GPU prices with a reliability haircut and a modeled-index label.
  - Depends on: T030, T080. Paths: `packages/data/src/sources/{polymarket,kalshi,manifold,gpu-index}.ts`. Covers: SPEC-068, SPEC-099 (inputs).
  - Gate: `bun test packages/data/test/sources/markets` passes on recorded responses; a market price stamped after a commit time is refused by the as-of reader.

- [ ] T084 [US4] Extend the market engine for the remaining forms: listed options priced from quotes or a labeled Black-Scholes model with observed or realized volatility, exercise and expiry, inverse funds, short sales with borrow, binary event contracts with settlement, and the GPU index; market-closed queueing and rejection rules per order type.
  - Depends on: T031, T032, T080. Paths: `packages/market/src/engine/forms/`. Covers: SPEC-059, SPEC-066, SPEC-071.
  - Gate: `bun test packages/market/test/forms` passes golden cases for each form; a bearish view compiles and fills in every class with a short form and is refused for the GPU index.

- [ ] T085 [US4] Run the User Story 4 acceptance on the multi-asset week tape: fills only in open hours, weekend and holiday handling, short and option effects, and the bearish-verdict path in each class.
  - Depends on: T081, T082, T083, T084. Paths: `tests/integration/us4-multi-asset.test.ts`. Covers: User Story 4; SPEC-026, SPEC-027, SPEC-059.
  - Gate: `bun test tests/integration/us4-multi-asset.test.ts` passes; the evidence lists fills by class and session.

## Phase 7: User Story 5, tribunals (P2)

- [ ] T090 [US5] Implement tribunal opening and research in `packages/tribunal` and the Tribunal workflow: triggers above the conviction or size threshold and on owner request, advocates from two different families, blind independent briefs, a research window (default 24 hours) using workflow sleep, and frozen, content-hashed evidence bundles shared with the judge.
  - Depends on: T042, T045. Paths: `packages/tribunal/src/`, `apps/worker/src/workflows/tribunal.ts`. Covers: SPEC-086, SPEC-087.
  - Gate: `bun test packages/tribunal` and `bun run test:worker -- tribunal` pass: tribunals open before any order for qualifying proposals; families differ; every dossier claim links to a stored source.

- [ ] T091 [US5] Implement debate rounds: opening, rebuttal, cross-examination and closing with staged visibility, each post-opening argument citing the opponent's prior argument, exact-match quote checks after Unicode normalization with unmatched quotes struck and counted, and equal length budgets.
  - Depends on: T090. Paths: `packages/tribunal/src/rounds.ts`. Covers: SPEC-088, SPEC-171.
  - Gate: `bun test packages/tribunal/test/rounds` passes: rounds in order, references present, a planted misquote struck, unequal budgets refused.

- [ ] T092 [US5] Implement judging and rulings: a judge from a third family ruling against the published rubric in both side orders with flips scored as ties, outputs of direction, probability, conviction interval, decisive claims with evidence identifiers and a falsifier; rulings set plan direction and conviction while size comes only from the risk gate; committee memos require a pre-mortem and red-team challenge.
  - Depends on: T091, T035. Paths: `packages/tribunal/src/judge.ts`, `packages/runtime/src/committee.ts`. Covers: SPEC-089, SPEC-090, SPEC-093, SPEC-171.
  - Gate: `bun test packages/tribunal/test/judge` passes: both orders run; a planted order dependence scores a tie; post-ruling size equals the risk gate output; a memo without a pre-mortem cannot be approved.

- [ ] T093 [US5] Implement judge and advocate scoring, believability weights from scored out-of-sample records (bounded and advisory, never altering limits), and the complexity budget harness that keeps added rounds or graph features disabled until they beat their parent on a time-split holdout.
  - Depends on: T092, T036. Paths: `packages/tribunal/src/scoring.ts`, `packages/runtime/src/believability.ts`, `packages/predict/src/holdout.ts`. Covers: SPEC-091, SPEC-162, SPEC-172.
  - Gate: `bun test packages/tribunal/test/scoring` passes on 20 resolved tribunals; a feature that worsens holdout Brier stays disabled.

## Phase 8: User Story 6, honest, calibrated and connected predictions (P2)

- [ ] T100 [US6] Implement the prediction graph in `packages/predict/src/graph/`: drivers (type, scheduled time), links (sign, strength with interval, lag), logical relations (complement, conjunction, partition, horizon monotonicity), coherence checks on every write (Frechet bounds, complements, partition sums, horizon monotonicity, sign conflicts) that block the write or open a repair task, and versioned edges.
  - Depends on: T036. Paths: `packages/predict/src/graph/`. Covers: SPEC-102, SPEC-103.
  - Gate: `bun test packages/predict/test/graph` passes: both seeded incoherence types are flagged; coherent sets pass; every stored link has sign, strength and lag.

- [ ] T101 [US6] Implement propagation and driver exposure: when a driver resolves, one joint propagation over shared ancestors in topological order flags every dependent prediction for the next cycle; positions map to drivers once each; exposure caps per driver and driver cluster feed the risk gate.
  - Depends on: T100, T035. Paths: `packages/predict/src/graph/propagate.ts`, `packages/risk/src/drivers.ts`. Covers: SPEC-079, SPEC-104.
  - Gate: `bun test packages/predict/test/propagate` passes the two-level chain case; `bun test packages/risk/test/drivers` blocks a position over the 25 percent driver cap naming the driver.

- [ ] T102 [US6] Implement market comparison and skill claims: matching predictions to prediction-market questions, market price at or before commit time, final-state resolutions only, exclusion of markets closed at commit, disagreement records, baselines (base rate, persistence, coin flip, market), minimum paired samples before claims, Holm adjustment across tested groups and resampling intervals.
  - Depends on: T036, T083. Paths: `packages/predict/src/skill/`. Covers: SPEC-098, SPEC-099, SPEC-169.
  - Gate: `bun test packages/predict/test/skill` passes: a late market price is refused; a group of 150 shows no skill claim; a persona significant only before adjustment shows no claim.

- [ ] T103 [US6] Implement recalibration and reporting splits: overconfidence alerts when a seat's slope is under 0.8 after 200 resolved predictions, fitted recalibration of that seat's future probabilities until recovery, trimmed-mean aggregation by default with logit pooling only after out-of-sample validation, forecast quality reported separately from trading return, and complexity-bucket calibration tables.
  - Depends on: T102, T061. Paths: `packages/predict/src/calibration/`. Covers: SPEC-100, SPEC-101, SPEC-105.
  - Gate: `bun test packages/predict/test/calibration` passes on a seeded overconfident seat (alert at 200, recalibrated outputs after) and a calibrated control (no alert).

- [ ] T104 [US6] Implement daily verification and external anchoring: the VerifyAndAnchor workflow recomputes every chain (ledger, predictions, decision log, change events), records divergences as incidents, and publishes chain heads outside the firm's stores to the operator-configured anchor location (default: a signed commit to a separate anchors repository through a scoped token stored as a secret), with verification comparing stored and published heads.
  - Depends on: T012, T036, T045. Paths: `apps/worker/src/workflows/verify-and-anchor.ts`, `packages/ledger/src/anchor.ts`. Covers: SPEC-153, SPEC-174.
  - Gate: `bun run test:worker -- verify-and-anchor` passes with a fake anchor sink: altering one record in each chain is reported at its first divergence and mismatches the published head.
  - Recovery: anchoring failures never block trading; they open an incident and retry next day.

## Phase 9: User Story 7, structural opportunities without getting eaten (P3)

- [ ] T110 [US7] Implement scheme scoring and regulator-order records in `packages/risk/src/special/`: time-stamped evidence records per indicator (payout promises above market rates, recruitment-linked rewards, unverifiable backing, operator history, withdrawal friction, capital diversion), score and classification (clean, watch, scheme), automatic live restricted-list entry, simulation eligibility only at the configured heat (default 7), and a regulator-order registry that hard-blocks live orders with no override.
  - Depends on: T035, T018. Paths: `packages/risk/src/special/`. Covers: SPEC-080, SPEC-106, SPEC-109, SPEC-163.
  - Gate: `bun test packages/risk/test/special` passes on the public scheme fixtures: schemes score above the threshold and ordinary assets below; a regulator-ordered asset stays blocked after an operator acknowledgment.

- [ ] T111 [US7] Implement the hazard estimator and exit planner: daily hazard with an interval from net-inflow proxies, their rate of change, withdrawal friction, operator diversion and liquidity; the exit rule holding only while expected payout exceeds expected loss from hazard net of recovery, clawback exposure on withdrawn gains and withdrawal costs; staged exits under participation and impact budgets and withdrawal caps, starting early enough to finish before expected loss reaches twice the payout rate.
  - Depends on: T110, T035. Paths: `packages/risk/src/special/hazard.ts`, `packages/risk/src/special/exit.ts`. Covers: SPEC-084, SPEC-107, SPEC-108.
  - Gate: `bun test packages/risk/test/hazard` passes on the public scheme fixture with known collapse day; a variant without the clawback term starts later than the reference and the test asserts the reference start day.

- [ ] T112 [US7] Implement market-integrity detectors in `packages/risk/src/integrity/`: venue quality scores and quality-adjusted volume used by sizing and liquidity caps, pump flags (return, volume and no-catalyst test) blocking entries for the window and trimming exposure, spoof-aware book features, sweep confirmation before entries on wicks, the cascade and collateral depeg gate, launch eligibility (default ineligible for live), unlock gates and the short-squeeze gate.
  - Depends on: T035, T030. Paths: `packages/risk/src/integrity/`. Covers: SPEC-110, SPEC-164, SPEC-165, SPEC-166, SPEC-167.
  - Gate: `bun test packages/risk/test/integrity` passes on the public manipulation tapes: each flag type fires in its window, entries are blocked for 60 minutes after the last flag, clean tapes stay under the false-positive limit.

- [ ] T113 [US7] Implement conduct checks and outbound controls: refusal of self-crossing between books, rapid large place-and-cancel patterns and coordinated cross-book orders in thin instruments, with conduct records; outbound messages restricted to owner accounts; seat requests to draft external promotional content refused and recorded.
  - Depends on: T046, T037. Paths: `packages/risk/src/conduct.ts`, `apps/worker/src/notify.ts`. Covers: SPEC-111, SPEC-112.
  - Gate: `bun test packages/risk/test/conduct` passes each refusal case; `bun run test:worker -- outbound` confirms no non-owner recipient is possible.

- [ ] T114 [US7] Run the User Story 7 acceptance: on the public scheme fixture the hazard crosses before collapse and the exit plan stays within limits; on the pump tape entries inside the window are blocked; with live enabled on recorded responses a restricted asset is blocked until acknowledged and a regulator-ordered asset stays blocked.
  - Depends on: T111, T112, T113. Paths: `tests/integration/us7-special.test.ts`. Covers: User Story 7.
  - Gate: `bun test tests/integration/us7-special.test.ts` passes; the evidence records hazard crossing day, exit stages and blocked entries.

## Phase 10: User Story 8, any seat in any harness (P3)

- [ ] T120 [US8] Implement the Claude Code generator in `packages/compilers/src/claude-code.ts`: one subagent file per seat (name, description, tools derived from authority classes, model from the route, body sections), skills copied into the workspace, a PreToolUse write-path guard in the workspace settings for seats with path limits, an MCP configuration pointing at `apps/mcp`, and a source hash in each generated file.
  - Depends on: T013, T014, T015, T016. Paths: `packages/compilers/src/claude-code.ts`, `harness/workspaces/claude-code/`. Covers: SPEC-013, SPEC-014, SPEC-016.
  - Gate: `bun test packages/compilers/test/claude-code` passes golden output and schema validation; removing a required field fails validation.

- [ ] T121 [P] [US8] Implement the Roo Code generator in `packages/compilers/src/roo-code.ts`: `.roomodes` entries (slug, name, roleDefinition, customInstructions, groups with edit fileRegex for path limits), per-mode rules folders, an explicit prohibition for the built-in tools Roo Code cannot remove, the MCP configuration, and capability gaps reported.
  - Depends on: T120. Paths: `packages/compilers/src/roo-code.ts`, `harness/workspaces/roo-code/`. Covers: SPEC-014, SPEC-015.
  - Gate: `bun test packages/compilers/test/roo-code` passes golden output and schema validation; the capability report lists the irremovable-tool and model gaps for every seat.

- [ ] T122 [P] [US8] Implement OpenCode, Codex, oh-my-pi and Agent Companies generators per `contracts/harness-capability-matrix.md`, plus `harness/workspaces/CAPABILITIES.md` listing unsupported features per harness and seat.
  - Depends on: T120. Paths: `packages/compilers/src/{opencode,codex,oh-my-pi,agent-companies}.ts`. Covers: SPEC-015.
  - Gate: `bun test packages/compilers` passes golden outputs for all four; the capability report covers every seat and harness pair.

- [ ] T123 [US8] Implement the drift check and authority checks: `bun run firm:check` regenerates every workspace in memory and fails on any byte difference; generated grants never exceed declared authority classes; every tool referenced in seat prose or skills is on the seat's whitelist; the runtime manifest supplies cadence, budget and escalation for every seat.
  - Depends on: T120, T121, T122. Paths: `packages/compilers/src/check.ts`, `scripts/firm-check.ts`. Covers: SPEC-013, SPEC-016, SPEC-017, SPEC-161.
  - Gate: `bun run firm:check` exit 0; a hand edit to a generated file and an unlisted tool reference each make it fail naming the file or seat.

- [ ] T124 [US8] Implement `apps/mcp`: an MCP server exposing the tool catalog against the local runtime (stdio) with the same Zod schemas and authority checks, and a read-only remote endpoint behind the operator session in the API Worker.
  - Depends on: T037, T043, T070. Paths: `apps/mcp/src/`, `apps/worker/src/api/mcp.ts`. Covers: SPEC-020, SPEC-142.
  - Gate: `bun test apps/mcp` passes protocol tests; an order tool call from a seat without order-release authority is refused.

- [ ] T125 [US8] Prove harness equivalence: run the chief risk officer seat through the MCP server from a scripted harness session on recorded inputs and through the cloud runtime on the same inputs; both outputs validate against the seat's output contract.
  - Depends on: T123, T124. Paths: `tests/integration/us8-harness.test.ts`. Covers: User Story 8; SPEC-020.
  - Gate: `bun test tests/integration/us8-harness.test.ts` passes; the evidence includes both outputs' contract validation results.

## Phase 11: User Story 9, live trading ready and off (P3)

- [ ] T130 [US9] Implement the Coinbase Advanced Trade live adapter in `packages/market/src/live/coinbase.ts` against the shared order interface, with explicit production and sandbox base URLs, request signing loaded only inside the adapter from Worker secrets, permission checks refusing credentials that can withdraw, and recorded-response tests.
  - Depends on: T046, T019. Paths: `packages/market/src/live/coinbase.ts`. Covers: SPEC-069, SPEC-145, SPEC-148.
  - Gate: `bun test tests/contract/venue-port.test.ts -- coinbase` passes on recorded responses, including the withdrawal-permission refusal.
  - Recovery: the adapter is unreachable while live is disabled; removing its secrets disables it completely.

- [ ] T131 [P] [US9] Implement the Alpaca live adapter (stocks, funds, options, crypto) and the Kalshi live adapter (event contracts) with the same structure, explicit hosts and recorded-response contract tests.
  - Depends on: T130. Paths: `packages/market/src/live/{alpaca,kalshi}.ts`. Covers: SPEC-069, SPEC-145, SPEC-148.
  - Gate: `bun test tests/contract/venue-port.test.ts -- alpaca kalshi` passes on recorded responses.

- [ ] T132 [US9] Wire the live switch: the operator change event sets the envelope's live flag and version; BookDesk routes to a live adapter only when the flag and version match; with live disabled a network spy proves zero order-endpoint requests across a full replay; enabling from any non-operator source is refused and recorded; venue rejections record the reason, leave the position unopened and notify both owners; live fills are compared daily with virtual fills for the same orders.
  - Depends on: T048, T130, T131. Paths: `apps/worker/src/objects/book-desk.ts`, `packages/runtime/src/live.ts`, `tests/integration/us9-live-off.test.ts`. Covers: SPEC-146, SPEC-147, SPEC-149, SPEC-150, SPEC-163.
  - Gate: `bun run test:worker -- us9-live-off` passes; the network spy report shows zero order-endpoint requests; the divergence report matches recomputation on recorded live fills.

## Phase 12: User Story 10, personas, institution study and macro book (P3)

- [ ] T140 [US10] Activate the persona library: twenty active personas and eight in reserve, behavioral bias parameters drawn from their priors, persona plans compiled against persona constraints, 1/N and hierarchical-risk-parity allocation baselines in every persona report, and owner-added personas entering the next cycle.
  - Depends on: T040, T041, T061. Paths: `packages/runtime/src/personas.ts`, `packages/reports/src/persona.ts`. Covers: SPEC-043, SPEC-048.
  - Gate: `bun test packages/runtime/test/personas` passes: a leveraged plan for a no-leverage persona is rejected naming the constraint; an added persona plans in the next cycle.

- [ ] T141 [US10] Implement the institution study stream: an EDGAR adapter for 13F, Form 4, 13D and 13G with an operator-configured User-Agent contact, a request budget well under ten per second, caching and timestamps; quarterly holdings diffs for a configured set of filers; a weekly educational note on the reference institution's practices and filing changes, including what the filings cannot show; never a trading input.
  - Depends on: T030, T061. Paths: `packages/data/src/sources/edgar.ts`, `packages/reports/src/institution.ts`. Covers: SPEC-123.
  - Gate: `bun test packages/reports/test/institution` passes on recorded filings; the note cites at least one filing with retrieval time; a test asserts no plan reads holdings data.

- [ ] T142 [P] [US10] Implement the standing macro book: theme-tagged positions (recession and bear-market positioning, policy-shock hedges, contrarian positions), weekly review content in the weekly report, and links to macro drivers in the prediction graph.
  - Depends on: T041, T100. Paths: `packages/runtime/src/macro-book.ts`. Covers: SPEC-124.
  - Gate: `bun test packages/runtime/test/macro` passes; every macro position carries a theme tag and the weekly report includes the review.

## Phase 13: Validation, evaluator handoff, deployment and readiness

- [ ] T150 Implement the validation pipeline: trial registry including failures, out-of-sample validation against the promotion thresholds with signatures from seats other than the author, deflated Sharpe and probability of backtest overfitting, monthly re-validation and demotion, competing frameworks on identical windows, baselines (buy-and-hold, equal-weight, moving-average crossover) and monthly ablations (no memory, no debate, no risk team).
  - Depends on: T043, T093. Paths: `packages/runtime/src/validation/`. Covers: SPEC-156, SPEC-157, SPEC-158, SPEC-159, SPEC-168.
  - Gate: `bun test packages/runtime/test/validation` passes: only the passing framework is promoted; author self-signature refused; trial counts equal the registry; ablation differences reported.

- [ ] T151 Implement the replay harness: historical windows with point-in-time reads, masking of names and dates, memory and lessons frozen at window start with retrieval logs, next-price execution, and the leak suite as a mandatory gate.
  - Depends on: T018, T043. Paths: `packages/runtime/src/replay/`. Covers: SPEC-041, SPEC-042, SPEC-049, SPEC-160, SPEC-170.
  - Gate: `bun test packages/runtime/test/replay` passes; a planted future row and a planted future article each fail the suite naming the leak; replay records never reference live-price books.

- [ ] T152 [P] Implement audit views and exports: one-query decision history (inputs, analyses, cases, tribunal, gates, sizing, orders, fills, outcome), position-affecting action records with served model, definition version, inputs hash and time, and audit export of any date range re-importable into a fresh verifier.
  - Depends on: T043, T012. Paths: `packages/runtime/src/audit.ts`, `apps/worker/src/api/decisions.ts`. Covers: SPEC-152, SPEC-154, SPEC-155.
  - Gate: `bun test packages/runtime/test/audit` passes on 20 random decisions; export and re-import verify cleanly.

- [ ] T153 [P] Implement export and restore: the daily Export workflow writes newline-delimited JSON per table with chain heads to R2; `bun run cli restore` rebuilds a fresh database and verifies chains; document D1 Time Travel for point-in-time recovery.
  - Depends on: T045, T012. Paths: `apps/worker/src/workflows/export.ts`, `apps/cli/src/restore.ts`, `docs/runbook.md`. Covers: SPEC-141.
  - Gate: `bun run test:worker -- export` passes; restore reproduces record counts and every chain head.
  - Recovery: restore always targets a new database; it never overwrites the primary.

- [ ] T154 Security review and hardening: run the injection corpus through every seat type, scan all prompts for credential and identifier patterns, test owner authentication paths, check headers and CSRF, review secrets handling, dependency audit and license check, and record findings with fixes in the ledger.
  - Depends on: T070, T072, T113, T132. Paths: `tests/security/`. Covers: SPEC-037, SPEC-125, SPEC-138, constitution VIII.
  - Gate: `bun test tests/security` passes; `bun run ci` passes; no unresolved high finding remains.

- [ ] T155 [P] Write the operator documentation: `docs/runbook.md` (cycles, incidents, budget, pausing, restore), `docs/deploy.md` (secrets, bindings, migrations, routes, data hosts to allow, first smoke test), `docs/owner-guide.md` (how to read reports, dials, sandboxes, questions, the live switch and what the scorecard means), all in plain language for both owners.
  - Depends on: T071, T153. Paths: `docs/`. Covers: SPEC-133 (guidance framing), constitution IV.
  - Gate: documentation lint passes; every command in `docs/deploy.md` and `quickstart.md` was run and its outcome recorded in the evidence.

- [ ] T156 Performance and cost check: measure research-cycle wall time at normal and peak load (target under 8 minutes), feasibility CPU time (under 20 seconds for 100,000 paths), Workflow step counts per day against the plan's estimate, and modeled monthly cost against the ceiling at the throttled rate.
  - Depends on: T050, T062, T047. Paths: `tests/perf/`. Covers: plan Performance Goals; SPEC-137.
  - Gate: `bun test tests/perf` passes the thresholds; the evidence records measured values.

- [ ] T190 Live verification of the research backlog: with network access and credentials, confirm each data host's response shape, limits and terms, each model route's identifier, price and structured-output support, fees, and Cloudflare limits listed in `research.md`; record each observation in the ledger, update `firm/routes/models.yaml`, `firm/instruments/` and recorded fixtures accordingly. Without access, record the blocked hosts and leave affected routes or sources inactive.
  - Depends on: T050, T085. Paths: `firm/routes/models.yaml`, `firm/instruments/`, `tests/fixtures/recorded/`. Covers: research verification backlog; SPEC-139.
  - Gate: `bun run cli smoke --live` exit 0 with access (or a recorded "blocked" report naming each host); `bun run firm:check` passes after updates.

- [ ] T157 Deploy: `bun run deploy:check` (dry run for both Workers with migrations listed); with credentials, `bun run deploy`, `bun run cli seed:owners --remote`, and a first remote smoke run of one research cycle with live disabled; without credentials, stop after the dry run and record the remaining operator steps.
  - Depends on: T154, T155, T190. Paths: `apps/worker/wrangler.jsonc`, `apps/portal/wrangler.jsonc`. Covers: SPEC-002 (deployed), SPEC-146.
  - Gate: `bun run deploy:check` exit 0; when deployed, the remote cycle completes and the portal shows the "Simulated" label.
  - Recovery: `wrangler rollback` for each Worker; D1 Time Travel for data.

- [ ] T158 Evaluator handoff and readiness: start a separate evaluator context (a fresh subagent briefed only with the external store path, the quickstart and `bun run eval:serve`), never opening the store from the implementing context; record the evaluator's report location and pass rate in the ledger; then deliver a readiness report to the owners covering tests, gates, evaluator results, deployment state, known reach and the open intent questions.
  - Depends on: T150 to T157. Paths: `docs/readiness-report.md`, `specs/001-autonomous-trading-firm/ledger/`. Covers: constitution Definition of done; SC-001 to SC-012 (measured where time allows).
  - Gate: `python3 .specify/gates/check-task-evidence.py` passes with every task checked; `python3 .specify/gates/spec-prep-validate.py specs/001-autonomous-trading-firm --evals <store>` run by the evaluator passes; `bun run ci` passes.

## Dependencies and execution order

- Phase 1 then Phase 2 block everything. Within Phase 2, T014 to T017 can run in parallel after T013; T018 and T019 in parallel after T011 and T010.
- User Story 1 (Phase 3) is the MVP and blocks the other stories' integration tasks; within it, T030 to T034 run in parallel after Phase 2, then T035 to T039, then T041 to T050 in order.
- User Stories 2 and 3 depend on US1; US4 to US7 depend on US1 and can proceed in parallel; US8 depends on Phase 2 seats and US1's runtime; US9 depends on US1 and US3; US10 depends on US1, US2 and US6.
- Phase 13 runs last; T190 can run as soon as US1 and US4 exist and access is available.

## Implementation strategy

1. Finish Phases 1 to 3 and stop to validate User Story 1 independently (T050); this is a working, unattended crypto firm.
2. Add reports (US2) and the portal (US3) so the owners can watch and learn.
3. Add asset classes, tribunals, the prediction graph and special situations (US4 to US7) in any order the evidence suggests, re-running the US1 acceptance after each.
4. Add harness compilers, the live path and the persona library (US8 to US10).
5. Validate, hand off to the evaluator, deploy and report (Phase 13).

After every story, re-run `bun run ci`, the fault suite and the US1 acceptance, and update the ledger and standing.
