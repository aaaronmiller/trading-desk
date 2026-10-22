---
date: 2026-10-03 17:30:00 PDT
ver: 1.0.0
author: Muse Spark (system-owned)
model: Muse Spark
tags: [strata, play, system-owned]
---

# Play: deploy

## Reads
- Deployment constraint: intent.md section 3 (single rented virtual
  server, unattended 24/7, restart recovery)
- Hosting derivation: context.md section 6

## Preconditions
- Paper-run play is green; the human has ratified the live-trading bar AND
  paper results have cleared it (per SPEC-021); explicit human approval is
  recorded.
- Secrets are in the server environment, never in the repo.

## Steps
1. Read the deployment constraint from intent.md section 3 at execution
   time; do not use a cached target.
2. Provision per context.md section 6; persistent volume for the decision
   store; scheduled backups.
3. Verify restart recovery (SPEC-017) on the deployed instance before
   enabling scheduling.
4. Enable heartbeat scheduling; confirm the first cycle records correctly.

## Halt conditions
- Halt if the deployment constraint in intent.md changed since context.md
  was derived: regenerate context.md section 6 first, never patch it.
- Halt if secrets would land in the repo or logs.
- Halt if restart recovery fails on the deployed instance.

## Ledger emission
- Decision: deployment target and verification results; outcome: live or
  rolled back.
