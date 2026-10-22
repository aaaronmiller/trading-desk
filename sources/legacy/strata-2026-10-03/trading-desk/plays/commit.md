---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: commit

## Reads
- Changed files and the SPEC-IDs they advance (from the working diff).

## Preconditions
- Validation passes on the current tree.

## Steps
1. Group changed files by the concern they serve (one concern per commit).
2. Map each group to the SPEC-IDs it advances; write the mapping in the
   commit message.
3. Verify no secrets, keys, or `.env` content is staged.

## Halt conditions
- Halt if a change cannot be mapped to any SPEC-ID: either the change is
  out of contract (revert it) or the spec is missing a clause (draft it
  for human ratification first). System-owned strata artifacts (ledger,
  standing, eval manifest) are exempt: they record the process, they do
  not advance clauses.
- Halt if validation fails.

## Ledger emission
- Decision: commit SHAs with their SPEC-ID mappings; outcome: pushed or
  held for review.
