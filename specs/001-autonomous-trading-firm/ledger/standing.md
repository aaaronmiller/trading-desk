---
date: 2026-10-21 17:05:00 UTC
ver: 2.0.0
author: Claude Code session (system-owned)
model: Claude (Claude Code session)
tags: [standing, continuity, autonomous-trading-firm, specification-preparation]
---

# Standing

## Where this is

The trading-desk repository is being prepared to build an autonomous, cloud-hosted AI trading firm for two owners: a 32-seat agent organization run by a virtual chief executive that researches crypto and every automatable asset class around the clock, trades simulated money at live prices, commits and scores predictions against prediction markets, debates serious targets in cross-model tribunals, and writes educational reports. Preparation is in Phase 4 of spec-prep: constitution, intent, specification (162 clauses), held-out evaluations (external), plan and substrate exist; research, data model, contracts, quickstart, tasks, traceability, refinement passes, validation and the reset handoff are in progress. No implementation code exists for this feature, and none may be written in the authoring session.

## Last decisions that matter

- [020] Conflicts resolved: humans outside the trading loop; operator holds live switch and ceilings; either owner pauses; leverage up to a 3x default ceiling; house book stops at 50 percent below its high-water mark.
- [022] Greenfield TypeScript core on a Cloudflare Workers run plane with deterministic Workflow cycles and one Durable Object per book; Paperclip is an export target, not the runtime.
- [023] Default model routes from at least three families; subscription routes excluded from the always-on loop unless the operator opts in.
- [026] Held-out evaluations live outside the repository; isolation is procedural only.
- [027] The installed validator is broken upstream; use `.specify/gates/spec-prep-validate.py`.

## Not yet decided

- Hosting plan and monthly ceiling (intent section 12 question 1). Default: paid edge plan, 25 dollars per month all in, enforced by throttling.
- Model-route policy for the always-on loop (intent question 2). Default: economy-api profile.
- Reference institution (intent question 3). Default: multi-manager platform, believability-weighted debate, public-filings study.
- Environment access for data hosts and deployment (ledger 028). Default: recorded fixtures and a deployment dry run.

## Next

Finish preparation: research.md, data-model.md, contracts, quickstart, checklists, tasks.md with gates, traceability, three refinement passes, depth check, validators and Spec Kit analysis, preparation.json, reset-handoff.md, session instructions; commit and push the branch; then hand the owner a restart prompt and stop.

## Substrate note

Declared S3 (see `../substrate.md`). Pre-locked: platform, stack, seat roster, heat table, route defaults, cadences, ceiling. Empirical memory is partial (legacy decisions without deployed outcomes); derivation is research-based. Revive protocol: read this file and the ledger tail before touching anything.
