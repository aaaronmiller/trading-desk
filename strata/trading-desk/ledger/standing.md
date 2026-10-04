---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, standing, system-owned]
---

# Standing

## Where this is
The trading-desk project is at kickoff. Sources are curated (23 files:
12 extracted role prompts, tool and dataflow inventories, backtest
methodology, orchestration model summary, trading-firm template).
Cycle 1 of the audit-improve loop (2026-10-03) re-verified all source SHAs,
fixed extraction fidelity (per-role preambles), completed truncated tool and
dataflow entries, corrected stale facts (Paperclip star count, file count,
TA license), and drafted the first harness-layer artifacts under `harness/`
(role bindings, debate protocol, venue tool interfaces — all DRAFT).
The strata tree is authored and awaiting human ratification of intent.md and
spec.md (both marked DRAFT). No executable implementation exists yet.

## Last decisions that matter
- [001] Kickoff from the approved lab-vs-firm plan; repo created.
- [002] Harness-over-framework for the live path; research framework kept
  as reference lab.
- [003] Paper-first gate is non-negotiable; live execution not built in
  phase 1.
- [005] Management layer adopted for scheduling, budgets, approvals, audit.
- [006] Three [NEEDS CLARIFICATION] items recorded instead of stalling.

## Not yet decided
- Paper-to-live quantitative bar (intent section 11, first marker).
- Starting capital per venue class (intent section 11, second marker).
- Specific venues and accounts (intent section 11, third marker).
- intent.md / spec.md ratification — nothing downstream builds until done.

## Next
Aaron reviews and ratifies intent.md and spec.md (answering the three
clarifications). Then: scaffold play → extract play → backtest play, per
context.md section 8.

## Substrate note
Declared S3 (see substrate.md). Empirical memory is empty; context
derivation was intuition-based. The revive protocol: read this file and the
ledger tail before touching anything.
