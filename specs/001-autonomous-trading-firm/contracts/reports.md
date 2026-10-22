---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, reports, education, feasibility, templates]
layer: derived
---
# Contract: reports

Clauses: SPEC-038, SPEC-039, SPEC-051, SPEC-113 to SPEC-124, SPEC-133, SPEC-168, SPEC-173. Builders live in `packages/reports`; numbers come from code, narrative from the investor education and reporting seat with numeric grounding. Every report starts with the deterministic mode label and the generation time, and every figure carries source and time.

## Daily report (by 06:00 Pacific)

1. Firm summary (net asset value, day and month to date, versus benchmarks, costs).
2. House book (positions, changes, heat, ladder state).
3. Other books in brief (personas, strategies, sandboxes, benchmarks).
4. Decisions with reasons; each decision carries the education block below.
5. Tribunal outcomes (rulings, conviction, judge flip checks).
6. Predictions committed and resolved (with scores).
7. Calibration (per seat summary, alerts).
8. Risk events (limit hits, ladder moves, integrity flags, gates).
9. Costs (inference by seat and route, data, hosting, budget status).
10. Lessons (resolved outcomes and what changed).
11. Watch list for the next day (scheduled drivers with times).
12. Retrieval questions (two, on earlier concepts) and the glossary review list (SPEC-173).

Education block per decision (SPEC-119): concept card in plain language; glossary link; "who is on the other side of this trade"; "what would change our mind" with a numeric falsifier; lesson once resolved.

## Weekly report

Strategy review with promotions and demotions; baselines and ablations summary (SPEC-168); tribunal and judge scores (SPEC-091); target feasibility (below); institution study note (SPEC-123); macro book review (SPEC-124); calibration by complexity bucket (SPEC-105); curriculum topics for the week (SPEC-120).

## Monthly statement

Per book: opening and closing value, flows, results by source (realized, unrealized, fees, financing), costs allocated, ledger chain head and anchor reference (SPEC-117, SPEC-174).

## Target feasibility (weekly and on request, SPEC-121)

Inputs: closed-position returns, trade frequency, current sizing by heat. Outputs with intervals: required win rate for 1, 2 and 3 percent per day at current payoff ratio and frequency; realized edge; probability of averaging each target over 30 and 90 days at current sizing (100,000 seeded resampled paths); sizing each target would require; risk of ruin (house stop) at current and required sizing; daily 95 percent value-at-risk budget equivalent to each target; plain-language verdict that never calls a target expected unless the record supports it.

## Deep research (SPEC-039, SPEC-122)

Sections: executive summary; actor map; method with justification; timeline with follow-the-money analysis; patterns; verbatim quotes with sources; methodological defense; quality evaluation (coverage checklist, validation questions, four-level rubric); meta-learning note.

## Opportunity list and idea notes (SPEC-118, SPEC-173)

Each entry: instrument, direction, goodness 1 to 10 with reasons, track record of the strategy and seats behind it, measured hit rate for the score band; idea note with thesis, valuation sensitivities, bull, base and bear cases, dated catalysts, risks, falsifiers.

## Rendering

Markdown and HTML stored in R2 and served by the portal; light theme default for documents; partner-facing messages end with 786110 on its own line; no 786110 on error, loss or alert views.
