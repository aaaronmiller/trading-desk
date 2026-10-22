---
date: 2026-10-21 15:00:00 UTC
ver: 1.0.0
author: Claude Code session (system-owned)
model: Claude (Claude Code session)
tags: [legacy, superseded, provenance, strata, trading-desk]
---
# Legacy sources

`strata-2026-10-03/` is the first contract pack for this repository (kickoff 2026-10-03). It was never ratified. It is preserved unchanged as source evidence for the current specification in `specs/001-autonomous-trading-firm/`, which supersedes it.

- Its ledger moved to `specs/001-autonomous-trading-firm/ledger/` and continues there (entries 001 to 016 are the legacy entries; 017 onward belong to the current specification).
- Every legacy clause has a disposition (incorporated, modified, superseded or rejected, with the reason) in `specs/001-autonomous-trading-firm/traceability.md`.
- `strata-2026-10-03/evals/evals.md` was the legacy evaluation manifest. It sat inside the repository, which the current method forbids, and it binds only legacy clause identifiers. The current held-out evaluations live outside this repository and are not referenced here by path on purpose.
- Nothing in this folder is an instruction to the current build. Read it as history.
