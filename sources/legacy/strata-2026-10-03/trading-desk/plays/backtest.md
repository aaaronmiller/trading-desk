---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: backtest

## Reads
- Evaluation contract: sources/tradingagents/backtest-methodology.md
- Target contract: SPEC-005..008
- Decision-date discipline: intent.md section 3 (honest evaluation)

## Preconditions
- Extract play has run; harness agents exist.
- A (ticker, date) grid and the settlement horizon are defined.

## Steps
1. Run the harness over the date grid; every dated tool call is clamped to
   the decision date by the tool layer.
2. Exclude undated items from windows ending before the present; label
   coverage gaps as unavailable, never empty.
3. Settle each decision after the horizon with realized and
   benchmark-relative returns.
4. Run SPEC-005..008 evals, including the adversarial fixtures (future-dated
   items, undated items, uncovered windows).

## Halt conditions
- Halt if any SPEC-005..007 eval fails: the date-clamp contract is broken
  and all results are suspect. Do not tune prompts to compensate.
- Halt if the grid cannot settle (no outcomes yet): record as pending and
  resume on a re-check cadence (re-run the unsettled cells when the window
  settles); do not extrapolate.

## Ledger emission
- Decision: backtest grid parameters and per-cell outcomes; outcome:
  aggregate decision-quality read.
