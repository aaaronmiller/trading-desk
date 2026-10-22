---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [contract, owner-api, portal, authentication, http]
layer: derived
---
# Contract: owner API (API Worker, consumed by the portal)

Clauses: SPEC-010 to SPEC-012, SPEC-045, SPEC-074, SPEC-122, SPEC-125 to SPEC-134, SPEC-147, SPEC-152. Base path `/api/v1`. JSON bodies. Session cookie `__Host-firm_session` (HttpOnly, Secure, SameSite=Strict); mutations require header `x-csrf-token`. Every response carries `mode: "simulated" | "live"` from the envelope, never from seat text.

| Method and path | Role | Purpose |
|---|---|---|
| POST /auth/login | none | username and password; lockout after 10 failures (SPEC-125) |
| POST /auth/logout | owner | end session |
| GET /firm/overview | owner | firm summary, house book, mode label, cycle health |
| GET /books, GET /books/:id | owner | books, wallet, positions, ladder, heat, logs |
| GET /reports?kind=&period= ; GET /reports/:id | owner | daily, weekly, monthly, feasibility, deep, opportunity, institution |
| GET /predictions?filter= ; GET /predictions/:id | owner | registry, scores, drivers, links, coherence flags |
| GET /tribunals/:id | owner | dossiers, rounds, ruling, scores |
| GET /decisions/:id/history | owner | full trail (SPEC-152) |
| GET /org | owner | seats, status, reporting lines, budgets, heartbeats |
| GET /costs?month= | owner | spend by seat and route |
| GET /ledger?from=&to= ; GET /ledger/verify | owner | entries and chain verification |
| POST /questions | owner | ask a seat (SPEC-127) |
| POST /ideas | owner | send the chief executive an idea (SPEC-128) |
| POST /sandboxes ; POST /sandboxes/:id/orders ; POST /sandboxes/:id/close | owner | sandbox lifecycle (SPEC-045, SPEC-129) |
| POST /sandboxes/:id/proposals | owner | propose a trade for seat review |
| GET /dials ; PUT /dials/:scope/:id | owner | heat dials within ceilings (SPEC-074, SPEC-130) |
| POST /pause ; POST /resume | owner | pause or resume firm or book (SPEC-011) |
| PUT /envelope/:key | operator | change a ceiling (SPEC-010, SPEC-078) |
| POST /restricted/:asset/lift | operator | lift with acknowledgment text (SPEC-080); refused if a regulator order exists (SPEC-163) |
| POST /books/house/resume | operator | resume after the house stop (SPEC-077) |
| GET /live/scorecard | operator | readiness scorecard (SPEC-133) |
| POST /live/enable ; POST /live/disable | operator | requires exact confirmation phrase; change event (SPEC-131, SPEC-147) |
| GET /notifications ; POST /notifications/:id/read | owner | events (SPEC-134) |

Errors: `{ error: { code, message } }` with HTTP 400 (validation), 401 (session), 403 (role), 409 (conflict, for example dial changed this cycle), 423 (locked account), 429 (rate). Error and alert payloads never contain 786110 (SPEC-132).

Remote MCP: `POST /mcp` exposes read-only tools to an authenticated operator session for harness use; write tools are available only through the local MCP server against a local runtime.
