---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [quickstart, local-run, validation, deploy, derived]
layer: derived
---
# Quickstart: run, verify and deploy the firm

This walkthrough is the acceptance path for SPEC-142 and the Definition of Done in the constitution. Every command must work from a clean clone after the build completes. Commands are written for macOS and Linux shells.

## 1. Prerequisites

- Bun 1.3 or later; Python 3.11 or later (gate scripts); Git.
- Optional for deployment: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment and network access to `api.cloudflare.com`.
- Optional for live data smoke tests: outbound access to the hosts in `docs/deploy.md` (data hosts section).

## 2. Install and check

```bash
bun install --frozen-lockfile
bun run typecheck            # strict TypeScript across workspaces
bun run lint                 # includes lint:routes (no model identifiers outside configuration)
bun run firm:check           # load and validate the canonical firm, regenerate harness workspaces in memory, fail on drift
python3 .specify/gates/check-task-evidence.py      # every checked task has evidence
python3 .specify/gates/spec-prep-validate.py specs/001-autonomous-trading-firm --evals "$SPEC_PREP_EVALS"   # evaluator store path supplied by the evaluator
```

## 3. Test suites

```bash
bun test                     # core: unit, property, golden, contract, leak and fault-injection suites
bun run test:worker          # Workers pool: Workflows, Durable Objects, D1 integration
bun run test:e2e             # portal end to end with the preinstalled Chromium
```

Expected: all green. The fault-injection suite reports 0 lost and 0 duplicated records across its crash points; the leak suite reports every planted future row and article caught.

## 4. Run the firm locally on a recorded tape

```bash
bun run cli seed:owners --local          # prints two generated credentials once; stores only hashes
bun run cli run --local --tape tests/fixtures/tapes/crypto-48h --speed 96 --hours 24
bun run cli report --local --kind daily --date latest
bun run cli verify --local               # recompute every chain; prints heads and anchors
```

Expected after a simulated day: about 96 research cycles complete with at least 99 percent completion, fills and wallet updates in each active book, predictions committed before their horizons, hourly analyses in every book log, a daily report with every section and education block, zero order-endpoint requests (network spy summary), and a cost summary under the configured ceiling.

## 5. Open the portal locally

```bash
bun run dev                  # API Worker and portal through local Workers runtime
```

Sign in with the operator credentials from step 4 and confirm: overview with the "Simulated" label, books, reports, predictions, a tribunal record from the tape run, heat dials, pause control; the live switch appears only for the operator and refuses a wrong phrase.

## 6. Use a seat from an agent harness

```bash
bun run firm:generate                      # writes harness/workspaces/*
cd harness/workspaces/claude-code && claude    # or open harness/workspaces/roo-code in an editor with Roo Code
```

The workspace's MCP configuration starts `apps/mcp` against the local runtime; asking the chief risk officer seat for a verdict returns output that validates against its contract (SPEC-020).

## 7. Deploy

```bash
bun run deploy:check         # wrangler deploy --dry-run for both Workers; migrations listed
bun run deploy               # requires deployment credentials; applies D1 migrations, deploys both Workers
bun run cli seed:owners --remote
```

Without credentials or network access, stop after `deploy:check`; `docs/deploy.md` lists the operator's remaining steps (secrets, routes, first smoke test).

## 8. Hand to the evaluator

```bash
bun run eval:serve           # exposes the build's public interfaces for a separate evaluator context
```

The evaluator reads the external store, generates its fixtures from the seeded rules, runs each EVAL against the public interfaces and writes a report outside the build repository. The implementing session does not open the store.
