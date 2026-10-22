---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: extract

## Reads
- Source role prompts: sources/tradingagents/agents/ (12 roles)
- Tool inventory: sources/tradingagents/tools.md
- Sourcing boundaries: sources/tradingagents/SOURCING.md (what was
  deliberately left behind)
- Target contract: SPEC-001..004

## Preconditions
- Scaffold play has run.
- The extraction sources are unchanged since SOURCING.md was written
  (re-verify the commit SHA if in doubt).

## Steps
1. For each of the 12 roles, create a harness agent carrying the extracted
   system prompt verbatim, with runtime placeholders bound to the harness's
   own context (date, instrument, prior reports).
2. Rebuild each role's tool set from sources/tradingagents/tools.md against
   the harness's tool layer; every dated tool enforces the date-clamp
   contract from sources/tradingagents/backtest-methodology.md.
3. Wire the pipeline order analysts → debate → trader → risk → portfolio
   approval, with each handoff recorded.
4. Do NOT port graph wiring, checkpointing, or CLI code (see SOURCING.md).
5. Run SPEC-001..004 evals against one paper cycle.

## Halt conditions
- Halt if a role prompt is missing from sources/: do not invent role
  content; record the gap.
- Halt if any SPEC-001..004 eval fails: the extraction is incomplete.

## Ledger emission
- Decision: roles extracted; which roles passed SPEC-001..004; outcome:
  recorded per role.
