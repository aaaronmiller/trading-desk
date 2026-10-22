---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: scaffold

## Reads
- Project structure: context.md section 9
- Human-authored contract: intent.md, spec.md (for scope only, never values)

## Preconditions
- intent.md and spec.md exist and are human-ratified (not DRAFT).
- The strata tree has passed validation.

## Steps
1. Create the directory layout from context.md section 9.
2. Verify each directory's purpose against the contract; create no
   implementation files yet.
3. Confirm the eval manifest is outside the build tree and every SPEC-ID's
   EVAL-ID resolves.
4. Advance SPEC-017 (durable store exists) by scaffolding only.

## Halt conditions
- Halt if intent.md or spec.md is still marked DRAFT: scaffolding from an
  unratified contract bakes in unapproved assumptions.
- Halt if validation fails: fix the artifacts, not the scaffold.

## Ledger emission
- Decision: scaffold created from context.md section 9; outcome: pending
  first implementation.
