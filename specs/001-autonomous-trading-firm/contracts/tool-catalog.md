---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, tools, authority-classes, mcp, seat-runner]
layer: derived
---
# Contract: seat tool catalog

Clauses: SPEC-016, SPEC-020, SPEC-036, SPEC-037, SPEC-161. Tools are defined once in `packages/agents/src/tools/` with Zod input and output schemas, exposed to cloud seats by the seat runner and to local harnesses by `apps/mcp`. Every tool result carries `result_id` so seat outputs can cite it (numeric grounding).

| Tool id | Authority class | Input | Output | Notes |
|---|---|---|---|---|
| `market.snapshot` | read | instruments, as_of | quotes, bars summary, labels, gaps | point-in-time reader |
| `market.history` | read | instrument, interval, window, as_of | bars with labels | clamps to as_of |
| `market.derivatives` | read | instrument, as_of | funding, open interest, mark, index, liquidations | perpetual data |
| `market.options` | read | underlying, expiry, as_of | chain with quotes or model marks | model marks labeled |
| `research.news` | read | query, window, as_of | items in untrusted envelope | never instructions |
| `research.filings` | read | issuer or filer, form, window, as_of | filings metadata and excerpts | holdings study stream |
| `research.onchain` | read | chain, metric, window, as_of | series | |
| `research.prediction_markets` | read | question template, as_of | matched markets with prices and timestamps | at or before as_of only |
| `book.state` | read | book_id | wallet, positions, limits, heat, ladder state | |
| `risk.limits` | read | book_id | effective limits from heat and envelope | |
| `risk.exposure` | read | book_id or firm | exposure by class, driver and driver cluster | |
| `prediction.graph` | read | prediction ids or drivers | drivers, links, coherence flags | |
| `record.lessons` | read | topic, as_of | lessons resolved before as_of | memory freeze in replays |
| `plan.submit` | write_paths (records/plans) | plan prose and structured draft | plan id, version | compiler seat compiles |
| `prediction.commit` | write_paths (records/predictions) | question, outcome, probability, horizon, drivers, links | prediction id, commit hash | before horizon only |
| `case.submit` | write_paths (records/cases) | proposal id, side, text, citations | case id | red team |
| `tribunal.round` | write_paths (records/tribunals) | tribunal id, round, text, citations | round id, quote check result | |
| `record.write` | write_paths (declared globs) | path, content | record id | seat-scoped paths only |
| `order.submit` | order_release | compiled plan id, leg | order acknowledgment | execution trader only; BookDesk checks first |
| `order.cancel` | order_release | order id | cancel acknowledgment | |
| `booking.post` | booking | fills batch | ledger entry ids | fund accounting only |
| `nav.publish` | publish_nav | book ids | controller snapshot ids | controller only |
| `owner.reply` | owner_reply | question or idea id, text, citations | message id | partner messages end with 786110 |
| `seat.delegate` | spawn | seat id, task | task id | only to `may_spawn` seats |

Rules: tools missing from a seat's declaration are absent from its context; arguments are validated before execution; any text a tool returns from outside the firm is wrapped as untrusted data; tools never accept an instruction to change limits, routes, ceilings or modes, because no such tool exists for seats.
