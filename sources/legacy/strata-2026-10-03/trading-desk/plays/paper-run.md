---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: paper-run

## Reads
- Live gate: intent.md section 3 (paper-first, human governance)
- Target contract: SPEC-009..018
- Risk limits: intent.md section 6

## Preconditions
- Backtest play has run with no integrity failures.
- Spend ceilings, position limits, and drawdown limits are configured.
- Live execution is disabled (verify, do not assume).

## Steps
1. Start heartbeat scheduling for all roles per the management layer.
2. Route every approved order to the simulated venue; record simulated
   fills per SPEC-009.
3. Enforce spend ceilings (SPEC-012), high-risk approval gates (SPEC-013),
   position limits (SPEC-015), and drawdown halts (SPEC-016).
4. Record every decision per SPEC-017; verify replay per SPEC-018.
5. Run the adversarial live-lockout eval (SPEC-010).

## Halt conditions
- Halt if SPEC-010 fails for any input: a live leak is a stop-everything
  defect, not a bug to fix forward. (Note: trivially green before phase 6,
  when no live path exists; the halt gains meaning once a live path is
  built.)
- Halt if the human has not configured risk limits: paper trading without
  limits teaches nothing about live behavior.
- Halt on any unapproved high-risk action attempt: surface to the human.

## Ledger emission
- Decision: paper-run started with configured limits; per-cycle outcomes;
  outcome: running aggregate for the live-gate review.
