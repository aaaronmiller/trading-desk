---
date: 2026-10-21 17:20:00 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [data-model, schema, entities, state-machines, derived]
layer: derived
---
# Data Model: Autonomous Trading Firm

Derived from spec section 2.2 (key entities) and plan CTX-001 to CTX-021. One SQL schema serves D1 (cloud) and `bun:sqlite` (local) through `packages/storage`; migrations are numbered SQL files applied in order by both adapters.

## Conventions

- **Identifiers**: deterministic where idempotency matters. Cycle identifier = kind plus slot instant (`research-20261021T1615Z`). Order identifier = first 24 hex characters of SHA-256 over `cycleId|planId|planVersion|leg`. Fill identifier = order identifier plus a sequence. Other records use time-ordered random identifiers (UUID version 7).
- **Numbers**: money in integer minor units (`bigint`, cents for USD; native minor units per currency); quantities and prices as scaled integers with a per-instrument scale (default 10^8), never floating point in stored records. Probabilities stored as integers in parts per million.
- **Time**: UTC instants in ISO 8601 with milliseconds. Every market datum carries `effective_at`, `retrieved_at` and `source`. Display converts to America/Los_Angeles.
- **Append-only tables**: ledger entries, logs, change events, predictions (commit fields), gate outcomes, tribunal rounds, call records. Updates are forbidden by triggers; corrections are new rows.
- **Hash chains**: ledger, predictions, decision log and change events carry `prev_hash` and `hash` (SHA-256 over canonical JSON of the row without `hash`). Genesis previous hash is 64 zeros.
- **Actor**: every state-changing row has `actor` (`seat:<id>`, `owner:<operator|partner>`, `system:<component>`) and `created_at`.

## Entities and tables

### Governance
| Table | Key fields | Notes |
|---|---|---|
| owners | id, role (operator, partner), username, pw_hash, salt, iterations, failed_count, locked_until | exactly two rows (SPEC-125) |
| sessions | id, owner_id, expires_at, csrf_token | expired rows purged daily |
| change_events | id, actor, kind, scope, prior_json, new_json, phrase_ok, created_at, prev_hash, hash | live switch, ceilings, lifts, pauses, resumes, dials, route profile (SPEC-010, SPEC-147) |
| envelope | key, value_json, updated_by, updated_at | ceilings; written only by the owner action handler |
| heat_dials | scope_kind (firm, persona, strategy, book), scope_id, value, ceiling, effective_from_cycle | history in heat_history |
| restricted_list | asset, reason, score_ref, added_at, lifted_by, ack_text, lifted_at | SPEC-080, SPEC-109 |
| notifications | id, owner_id, kind, body, created_at, read_at | partner bodies end with 786110 except error, loss and alert kinds |

### Organization
| Table | Key fields | Notes |
|---|---|---|
| seats | id, seat_type, def_version, def_hash, status (active, paused, retired), reports_to, route_family | loaded from `firm/seats` |
| seat_versions | seat_id, version, def_hash, body_key, reason, record_ref, actor, created_at | SPEC-005 |
| heartbeats | seat_id, cycle_id, at | SPEC-140 |
| incidents | id, kind, detail_json, opened_at, closed_at, resolution | heartbeats, breaks, divergences |
| believability | seat_id, domain, weight, sample, computed_at | SPEC-162 |

### Cycles and calls
| Table | Key fields | Notes |
|---|---|---|
| cycles | id, kind, slot_at, started_at, ended_at, status (running, complete, partial, failed, skipped), cause | unique id makes duplicates no-ops |
| cycle_steps | cycle_id, seq, name, status, started_at, ended_at, record_ref | SPEC-022 order |
| call_records | id, cycle_id, step, seat_id, route, model_served, in_tokens, out_tokens, cost_micro_usd, latency_ms, outcome, transcript_key, inputs_hash | SPEC-143, SPEC-155 |
| budget | month, seat_id, share_ppm, spent_micro_usd, alert_50, alert_80, paused | SPEC-136, SPEC-137 |

### Market data
| Table | Key fields | Notes |
|---|---|---|
| instruments | symbol, class, currency, calendar, price_source, fallback_source, staleness_s, fee_profile, short_forms, tick, lot, scale, adv, enabled | from `firm/instruments` |
| bars | instrument, effective_at, interval, open, high, low, close, volume, source, retrieved_at, label | minute bars older than 30 days archived to R2 |
| quotes | instrument, effective_at, bid, ask, source, retrieved_at, label | latest window only |
| data_items | id, kind (article, filing, indicator, funding, open_interest, liquidation, sentiment, onchain, market_probability), source, retrieved_at, effective_at, content_key, content_hash, labels, quarantined | SPEC-032 to SPEC-035 |
| gaps | source, instrument, window_start, window_end, reason | unavailable labels |

### Research and decisions
| Table | Key fields | Notes |
|---|---|---|
| analyses | id, cycle_id, seat_id, instrument, dimension, output_json, grounded_refs, transcript_key | SPEC-031, SPEC-036 |
| plans | id, version, book_id, seat_id, prose_key, compiled_json, status, reasons_json, parent_version | lifecycle below |
| proposals | id, plan_id, plan_version, direction, conviction_ppm, created_by, status | |
| cases | proposal_id, side (pro, con), seat_id, family, text_key | SPEC-085 |
| memos | id, proposal_id, premortem_key, redteam_key, approved_by | SPEC-093 |
| gate_outcomes | proposal_id, gate (confidence, review, risk), verdict, reasons_json, actor, family | SPEC-092 |
| tribunals | id, proposal_id, opened_at, window_ends_at, advocate_a, family_a, advocate_b, family_b, judge, family_judge, status, ruling_json | SPEC-086 to SPEC-090 |
| tribunal_rounds | tribunal_id, side, round (opening, rebuttal, cross, closing), text_key, refs_prior_round, quotes_verified | SPEC-088 |
| dossiers | tribunal_id, side, claims_json, source_refs | SPEC-087 |

### Books and execution
| Table | Key fields | Notes |
|---|---|---|
| personas | id, name, worldview, risk_profile, horizon, constraints_json, biases_json, starting_capital_minor, heat, status | 28 defined, 20 active |
| books | id, type (house, persona, strategy, sandbox, benchmark), owner_ref, base_currency, heat, ladder_json, limits_json, status (active, warned, halved, stopped, paused), hwm_minor | lifecycle below |
| wallet_cash | book_id, currency, cash_minor | |
| positions | book_id, instrument, side, qty, avg_cost, lots_json, margin_json, opened_at | |
| orders | id, book_id, plan_id, plan_version, leg, instrument, side, type, qty, limit_px, stop_px, tif, venue (virtual, live:adapter), status, reasons_json, decided_at | lifecycle below |
| fills | id, order_id, seq, qty, price, fee_minor, slippage, at, liquidity_ref | |
| accruals | id, book_id, instrument, kind (borrow, funding, dividend, interest, option_expiry), amount_minor, at | |
| nav_snapshots | book_id, at, nav_minor, realized_minor, unrealized_minor, fees_minor, financing_minor, controller_ok | SPEC-007, SPEC-046 |
| reconciliation | cycle_id, book_id, diff_json, status | SPEC-030 |
| conduct_records | id, book_id, pattern, detail_json, at | SPEC-111 |

### Predictions and graph
| Table | Key fields | Notes |
|---|---|---|
| predictions | id, seq, question, outcome_def, prob_ppm, horizon_at, resolution_source, created_by, content_hash, prev_hash, committed_at, revealed_at, outcome, resolved_at, brier_ppm, log_loss_ppm, market_ref, market_prob_ppm, market_at, late, unrevealed | lifecycle below; salt and content sealed in prediction_secrets until reveal |
| prediction_secrets | prediction_id, salt, content_json | readable only by the reveal step |
| drivers | id, kind (scheduled_event, reported_figure, policy_action, market_level, other), label, scheduled_at, resolved_at, outcome_json | |
| prediction_drivers | prediction_id, driver_id | |
| prediction_links | from_id, to_id, sign, strength_ppm, lag_s | |
| coherence_flags | id, prediction_ids, rule, detail, created_at, cleared_at | SPEC-103 |
| calibration | seat_id, horizon_bucket, class, n, brier_ppm, ece_ppm, slope_ppm, intercept_ppm, computed_at | SPEC-097, SPEC-101 |
| anchors | chain, head_hash, anchored_at, location | daily external anchoring of chain heads |

### Special situations and integrity
| Table | Key fields | Notes |
|---|---|---|
| scheme_scores | asset, score_ppm, indicators_json, evidence_refs, computed_at | SPEC-106 |
| hazard_estimates | asset, day, hazard_ppm, payout_ppm, inputs_json | SPEC-107, SPEC-108 |
| integrity_flags | instrument, kind (pump, wash, spoof, cascade), window_start, window_end, evidence_json | SPEC-110 |

### Records, reports and owner interaction
| Table | Key fields | Notes |
|---|---|---|
| ledger_entries | seq, at, memo, ref, actor, lines_json, prev_hash, hash | balanced lines in minor units (SPEC-151) |
| logs | id, scope (position, book), scope_id, kind (fill, analysis, annotation, assessment), body, at | append-only (SPEC-113) |
| decision_log | seq, at, actor, action, refs_json, model_served, def_version, inputs_hash, prev_hash, hash | SPEC-155 |
| reports | id, kind (daily, weekly, monthly, feasibility, deep, opportunity, institution), period, md_key, html_key, published_at, mode_label | |
| report_decisions | report_id, decision_ref, concept, glossary_term, other_side, change_of_mind, lesson | SPEC-119 |
| glossary | term, explanation, first_used_at, first_report_id | SPEC-120 |
| curriculum | week, topics_json | |
| opportunities | id, report_id, instrument, direction, goodness, reasons, track_record_json | SPEC-118 |
| questions | id, owner_id, seat_id, text, asked_at, answer_key, answered_at | SPEC-127 |
| ideas | id, owner_id, text, ack_at, disposition (adopted, adapted, declined), reasons, decided_at | SPEC-128 |
| trials | id, framework, params_json, window, metrics_json, created_at | SPEC-157 |
| frameworks | id, status (candidate, promoted, demoted), signatures_json, metrics_json, revalidated_at | SPEC-156, SPEC-158 |
| exports | day, prefix, chain_heads_json | SPEC-141 |

## State transitions

- **Order**: new → working → partially_filled → filled; new or working → canceled; new → rejected (reasons). Only the execution trader's release step creates `new`; only BookDesk advances states.
- **Plan**: draft → compiled → approved → active → closed; draft or compiled → rejected (reasons). Revisions create a new version from any non-closed state.
- **Book ladder**: active → warned (level 1) → halved (level 2) → stopped (level 3); any → paused (owner) → prior state on resume; stopped house book returns to active only by operator change event.
- **Seat**: active → paused (budget or incident) → active (chief executive) ; active → retired (chief executive, recorded).
- **Cycle**: running → complete or partial or failed; scheduled but never started → skipped (cause recorded).
- **Prediction**: committed → revealed → resolved → scored; committed → late (excluded); committed → unrevealed (scored worst at resolution time).
- **Restricted entry**: listed → lifted (operator acknowledgment) → relisted when score rises again.
- **Tribunal**: opened → researching (window) → debating (rounds) → ruled → scored after outcome.

## Validation rules

- Ledger lines sum to zero per entry; currencies never mix within a line set without an explicit conversion line.
- A position's quantity equals the sum of its lots; a fill's quantity never exceeds remaining order quantity.
- A prediction's `committed_at` precedes `horizon_at`; a market probability is accepted only when `market_at <= committed_at`.
- Book NAV equals cash plus marked positions within one minor unit; the controller snapshot must match within tolerance before publication.
- Heat values are integers 1 to 10 and never exceed their ceiling.
