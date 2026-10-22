---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, cycle, step-graph, workflow, idempotency]
layer: derived
---
# Contract: cycle step graphs

Clauses: SPEC-018, SPEC-021 to SPEC-030, SPEC-135. Source: `firm/cycles/<id>.yaml`. The runtime executes a graph as one Workflow instance in the cloud and as an in-process run locally; both use the same step identifiers so results are comparable.

## Schema

```yaml
schema: cycles/v1
id: research-cycle
trigger: { cron: "*/15 * * * *" }          # or { dispatcher: daily-0500-pacific } or { event: owner-request }
instance_id: "research-{slotUtc}"           # deterministic; duplicates are skipped (SPEC-029)
max_duration: PT8M
steps:
  - id: reconcile                            # always first (SPEC-030)
    kind: code                               # code | seat | parallel | gate | sleep
    run: runtime.reconcile
    outputs: [reconciliation]
  - id: snapshot
    kind: code
    run: data.snapshot
    outputs: [market_snapshot]
  - id: scan
    kind: code
    run: runtime.materialityScan
    inputs: [market_snapshot]
    outputs: [scan_flags]
  - id: triage
    kind: seat
    seat: chief-operating-officer
    inputs: [scan_flags]
    outputs: [assignments]
    budget_class: essential
  - id: analyze
    kind: parallel
    over: assignments.items
    max_items: 12
    step: { kind: seat, seat: "{item.seat}", inputs: [market_snapshot], outputs: [analysis] }
    budget_class: throttleable
  - id: propose
    kind: parallel
    over: candidate_books
    step: { kind: seat, seat: "{book.manager}", outputs: [proposal] }
    budget_class: throttleable
  - id: compile
    kind: parallel
    over: proposals
    step: { kind: seat, seat: strategy-compiler, outputs: [compiled_plan] }
    verdict: { field: valid, on_false: reject }
  - id: cases
    kind: parallel
    over: compiled_plans
    step: { kind: seat, seat: red-team, outputs: [pro_case, con_case] }
  - id: gates
    kind: gate
    chain: [confidence, review, risk]       # SPEC-092; risk is code
  - id: release
    kind: code
    run: execution.release                  # BookDesk submission; idempotent order ids
  - id: commit-predictions
    kind: code
    run: predict.commit
  - id: logs
    kind: code
    run: reports.appendLogs
iteration_caps: { repair_attempts: 1, seat_tool_turns: 8 }
```

## Rules

- Every `inputs` entry must be produced by an earlier step or be a declared external input; every produced output must be declared (SPEC-018).
- Loops exist only as `parallel` fan-outs with `max_items` or as seat tool turns with `seat_tool_turns`; an uncapped loop fails loading.
- A `seat` step is one durable step per model call; retries replay stored results instead of calling again.
- `budget_class`: `essential` steps (reconcile, triage, gates, release, commit-predictions, logs, risk and records seats) never throttle; `throttleable` steps shrink in the order defined in plan CTX-010.
- A step that fails after its retries marks the cycle `partial`; `release` never runs after a failed or skipped upstream step on the same plan (SPEC-030).

## Shipped graphs

`research-cycle` (15 minutes), `book-analysis` (hourly), `daily-rhythm` (morning meeting, committee, risk report, end-of-day books, daily report), `weekly-review`, `monthly-statement`, `tribunal` (with `sleep` for the research window), `owner-request` (questions, ideas, deep research), `export`, `verify-and-anchor`, `ingest-minute`.
