---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (authoring session; preparation only)
model: Claude (Claude Code session)
tags: [reset-handoff, initiation, autonomous-trading-firm, spec-prep, fresh-session]
---
# Reset handoff: autonomous trading firm

## Build root and authority

- Build root: `aaaronmiller/trading-desk`, branch `001-autonomous-trading-firm` (draft pull request aaaronmiller/trading-desk#1). The repository is public until the owners change it.
- Intake (owner statements, research, held-out evaluations): `aaaronmiller/new-assignments`, branch `autonomous-trading-firm-intake`, folder `autonomous-trading-firm/` (private; draft pull request aaaronmiller/new-assignments#1).
- Initiation authority: a fresh session launched by the owner with the restart prompt below. That session may implement every task in `tasks.md`, run tests, commit and push to the branch, and deploy when deployment credentials exist. It may never enable live trading, place a real order, or handle exchange credentials. A subagent of the authoring session has no initiation authority.

## Canonical artifacts

| Role | Path |
|---|---|
| Constitution | `.specify/memory/constitution.md` (v1.0.0, 11 principles) |
| Session instructions | `AGENTS.md`, `CLAUDE.md` (generated constitution copy, sync-checked) |
| Intent | `specs/001-autonomous-trading-firm/intent.md` (v1.2.0) |
| Specification | `specs/001-autonomous-trading-firm/spec.md` (v1.2.0, SPEC-001 to SPEC-174) |
| Plan | `specs/001-autonomous-trading-firm/plan.md` (v1.1.0, CTX-001 to CTX-021) |
| Supporting | `research.md`, `data-model.md`, `contracts/` (9), `quickstart.md`, `checklists/requirements.md` |
| Tasks | `specs/001-autonomous-trading-firm/tasks.md` (v1.1.0, 90 gated tasks) |
| Traceability | `specs/001-autonomous-trading-firm/traceability.md` |
| Continuity | `specs/001-autonomous-trading-firm/ledger/ledger.md` (entries 001 to 034), `ledger/standing.md` |
| Substrate | `specs/001-autonomous-trading-firm/substrate.md` (S3) |
| Gates | `.specify/gates/` (validator copy, evidence checker, commit hook, preparation verifier, constitution sync) |
| Receipt | `preparation.json` |

## Preparation results (captured in preparation.json)

- spec-prep validator (patched project copy): passed with 174 clauses bound to 174 external evaluations, separation armed with 51 harvested tokens; a planted-violation run failed as expected.
- Depth check: requirement-like lines 83 in sources, 222 in intent and spec; 93 of 93 working requirements and 21 of 21 legacy clauses have dispositions.
- Spec Kit prerequisites (`check-prerequisites.sh --require-tasks --include-tasks`): passed.
- Spec Kit analysis: 0 critical; high and medium findings remediated (ledger 033).
- Constitution sync: passed (11 principles in CLAUDE.md copy and in the plan's Constitution Check).
- Task evidence gate: passed (no task checked yet); shown to block an unevidenced checked task.

## Unresolved items

1. Hosting plan and monthly ceiling (intent question 1). Default: Cloudflare Workers Paid, 25 dollars per month all in, enforced by throttling.
2. Model-route policy for the always-on loop (intent question 2). Default: economy-api profile.
3. Reference institution (intent question 3). Default: multi-manager platform, believability-weighted debate, public-filings study stream.
4. Environment: network access to data hosts and `api.cloudflare.com`, plus `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`, are needed for live smoke tests and deployment. Without them the build uses recorded fixtures and stops at a deployment dry run.
5. Research report R10 (the owner's starred repositories) was still running when preparation closed; fold it in through a ledger entry if it changes a decision.

## Next task

T001 (move the legacy harness drafts), then the tasks in dependency order. Phases 1 to 3 deliver the minimum viable firm (User Story 1); validate it with T050 before moving on.

## Restart prompt (paste into a new session)

```text
Build the autonomous trading firm prepared in aaaronmiller/trading-desk on branch 001-autonomous-trading-firm. This is the project-initiation session; I launched it fresh after specification preparation, so you have initiation authority for the tasks in the repository and nothing beyond them.

1. Attach and check out aaaronmiller/trading-desk at branch 001-autonomous-trading-firm. Attach aaaronmiller/new-assignments (branch autonomous-trading-firm-intake) read-only for the owner statements and research in autonomous-trading-firm/sources/. Never open autonomous-trading-firm/evaluator-only/ yourself; it is held-out evaluation material for a separate evaluator context.
2. Read reset-handoff.md, then specs/001-autonomous-trading-firm/ledger/standing.md and the last ten ledger entries, then .specify/memory/constitution.md in full, then intent.md, spec.md, plan.md and tasks.md.
3. Run: python3 .specify/gates/verify-preparation.py ; python3 .specify/gates/check-constitution-sync.py ; python3 .specify/gates/check-task-evidence.py ; export SPECIFY_FEATURE_DIRECTORY=specs/001-autonomous-trading-firm && bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks. If any fails, stop and report why before writing code.
4. Create your todo list from tasks.md and work task by task in dependency order, starting at T001. For every task follow the gate procedure at the top of tasks.md: tests first, implement, run the task's gate commands and the global gate, write evidence to specs/001-autonomous-trading-firm/evidence/T###.md from the template, append a ledger entry naming the task, overwrite standing.md, check the box, commit with a message starting "T###:", and push the branch. Never weaken a test, threshold or gate; if a task cannot pass honestly, record why in the ledger and move to the next task that does not depend on it.
5. After Phase 3, validate User Story 1 (T050) before continuing. After each later user story, re-run bun run ci, the fault suite and the User Story 1 acceptance.
6. Simulation only: never enable live trading, never place a real order, never request or handle exchange credentials. Deploy (T157) only if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are present and api.cloudflare.com is reachable; otherwise stop at the dry run and document the remaining steps.
7. At the end (T158), brief a separate evaluator subagent with only the evaluator-only folder path, the quickstart and bun run eval:serve; record its report and pass rate; then write docs/readiness-report.md and give me a plain summary of what works, what failed, costs and the open intent questions.
Keep iterating until every task is complete with evidence and every gate passes, or until a blocker needs a decision from me.
```
