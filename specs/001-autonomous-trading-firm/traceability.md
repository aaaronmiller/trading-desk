---
date: 2026-10-22 08:37:18 UTC
ver: 1.0.0
author: Claude Code session (system-derived)
model: Claude (Claude Code session)
tags: [traceability, provenance, disposition, coverage, autonomous-trading-firm]
---
# Traceability: Autonomous Trading Firm

Source to intent to clause to evaluation to decision to task. Generated from the artifacts by script during preparation and checked for gaps: every working requirement maps to a clause or a governance rule, every clause maps to a plan decision and at least one task, every user story maps to clauses. Re-generate after any change to intent, spec, plan or tasks.

## 1. Source disposition

| Source | Location | Disposition | Where it landed |
|---|---|---|---|
| Owner statements T1 to T9 | intake `sources/originals/conversation-intent-2026-10-20.md` (private) | Incorporated | intent sections 1 to 12; requirements v0.2.0; spec stories and clauses |
| Pasted resources A to F (earlier prompts, cycle note, ambiguities, fast-trading prompts, trending projects, research template) | intake `sources/originals/pasted-resources-2026-10-21.md` | Incorporated | CYC, PLAN, DSL, RPT, QA requirements; SPEC-021 to SPEC-025, SPEC-039, SPEC-118, SPEC-156; intent section 10 |
| 2025 architecture draft (orchestrator, researcher, planner, coder, analyst, personas, data sources) | intake `sources/originals/investment-ai-architecture-2025-10-14.md` | Modified | Roles split per R03 (SPEC-002, SPEC-007); executable plan classes rejected for a closed plan language (CTX-008); 20 personas kept (SPEC-043); shared-filesystem logs replaced by the durable store (CTX-004) |
| Legacy contract pack (intent, spec SPEC-001 to SPEC-021, context, plays, substrate, tokens, evals) | `sources/legacy/strata-2026-10-03/` | Superseded | Clause dispositions in section 2; ledger continued in `ledger/` |
| Legacy harness drafts (role bindings, debate protocol, venue interfaces, date clamp) | `harness/` moved by task T001 | Superseded | `packages/agents`, `packages/tribunal`, `contracts/order-interface.md`, `packages/data` |
| TradingAgents role prompts (Apache-2.0, pinned) | `sources/tradingagents/` | Incorporated as source text with provenance | seat prose (T014) |
| Paperclip template and orchestration model | `sources/paperclip/` | Concept only | Agent Companies export (CTX-016); runtime rejected (CTX-002) |
| Research reports R01 to R09, R11 to R16 | intake `sources/research/` (private) | Incorporated | research.md decisions D1 to D14; intent section 10; refinement clauses SPEC-163 to SPEC-174 |
| Research report R10 (starred repositories) | intake (pending when this map was generated) | Deferred | Folded in by a later ledger entry if it changes any decision |
| Working requirements v0.2.0 | intake `sources/research/REQUIREMENTS-working.md` | Incorporated | section 3 |
| Vantage planning set, portal and ledger code | `/home/user/vantage` (owner workspace) | Concepts incorporated | owner portal auth and ledger concepts (CTX-018, `packages/ledger`); seat budget shares (CTX-010) |
| Investment thesis practice and data labeling rules | `aaaronmiller/investment` (private) | Incorporated as conventions | provenance labels (SPEC-038), institution and research reports |
| Owner's scheme-forensics brief | `aaaronmiller/texitcoin` (public site) | Incorporated as method | SCHEME requirements; SPEC-106 to SPEC-109, SPEC-163; ethical counterparty notes (SPEC-119) |
| Held-out evaluations EVAL-001 to EVAL-174 | intake `evaluator-only/` (private, outside this repository) | Bound | spec section 5; evaluator handoff T158 |

## 2. Legacy clause dispositions

| Legacy clause | Topic | Disposition | Current clauses |
|---|---|---|---|
| SPEC-001 (legacy) | independent analyst reports before debate | Incorporated | SPEC-031 |
| SPEC-002 (legacy) | bull and bear adversarial review | Incorporated, strengthened | SPEC-085, SPEC-088 |
| SPEC-003 (legacy) | plan required after debate | Incorporated | SPEC-053 |
| SPEC-004 (legacy) | no order without portfolio approval | Incorporated as gate chain | SPEC-092, SPEC-007 |
| SPEC-005 to SPEC-007 (legacy) | no future data, undated items, gaps labeled | Incorporated, extended to timestamps | SPEC-033, SPEC-034, SPEC-035, SPEC-160 |
| SPEC-008 (legacy) | settle every decision | Incorporated | SPEC-095, SPEC-097 |
| SPEC-009, SPEC-010 (legacy) | paper sink; no real order while live disabled | Incorporated | SPEC-146 |
| SPEC-011 (legacy) | live path only with approval | Modified (operator change event) | SPEC-147 |
| SPEC-012 (legacy) | spend cap pause until a human resumes | Modified (chief executive reallocates; owners set the firm cap) | SPEC-136, SPEC-137 |
| SPEC-013, SPEC-014 (legacy) | human approval of high-risk actions | Superseded by humans outside the loop; envelope actions only | SPEC-009, SPEC-010 |
| SPEC-015 (legacy) | position limits | Incorporated | SPEC-076 |
| SPEC-016 (legacy) | drawdown halt until human review | Modified (ladder; operator resumes house book) | SPEC-077 |
| SPEC-017, SPEC-018 (legacy) | decision record and history | Incorporated | SPEC-152, SPEC-155 |
| SPEC-019 (legacy) | instrument classes | Incorporated, widened | SPEC-068, intent section 4 |
| SPEC-020 (legacy) | venue unreachable | Incorporated | SPEC-040, SPEC-144, SPEC-149 |
| SPEC-021 (legacy) | live only after a ratified bar | Modified (advisory scorecard) | SPEC-133 |

## 3. Working requirements to clauses

| Requirement | Clauses |
|---|---|
| ORG-01 | SPEC-002 |
| ORG-02 | SPEC-003, SPEC-004, SPEC-005 |
| ORG-03 | SPEC-009 |
| ORG-04 | SPEC-010, SPEC-011, SPEC-128, SPEC-134 |
| ORG-05 | SPEC-004, SPEC-010, SPEC-078 |
| ORG-06 | SPEC-006, SPEC-007, SPEC-082 |
| ORG-07 | SPEC-008, SPEC-152, SPEC-154, SPEC-155 |
| ORG-08 | SPEC-002, SPEC-162 |
| ROLE-01 | SPEC-001 |
| ROLE-02 | SPEC-013, SPEC-020, SPEC-142 |
| ROLE-03 | SPEC-013, SPEC-014, SPEC-015 |
| ROLE-04 | SPEC-018 |
| ROLE-05 | SPEC-016 |
| ROLE-06 | SPEC-017 |
| ROLE-07 | SPEC-019 |
| CYC-01 | SPEC-021 |
| CYC-02 | SPEC-022 |
| CYC-03 | SPEC-023 |
| CYC-04 | SPEC-025 |
| CYC-05 | SPEC-026 |
| CYC-06 | SPEC-003, SPEC-024 |
| CYC-07 | SPEC-027 |
| RES-01 | SPEC-031 |
| RES-02 | SPEC-039, SPEC-122 |
| RES-03 | SPEC-033, SPEC-034, SPEC-035, SPEC-040 |
| RES-04 | SPEC-036 |
| RES-05 | SPEC-037 |
| RES-06 | SPEC-032, SPEC-038 |
| PLAN-01 | SPEC-043, SPEC-048 |
| PLAN-02 | SPEC-056, SPEC-060 |
| PLAN-03 | SPEC-051, SPEC-052 |
| DSL-01 | SPEC-053, SPEC-054, SPEC-055 |
| DSL-02 | SPEC-068 |
| DSL-03 | SPEC-057 |
| DSL-04 | SPEC-058 |
| DIR-01 | SPEC-059, SPEC-066, SPEC-167 |
| MKT-01 | SPEC-063, SPEC-064, SPEC-065, SPEC-066, SPEC-070, SPEC-072 |
| MKT-02 | SPEC-026, SPEC-071 |
| MKT-03 | SPEC-069 |
| WAL-01 | SPEC-044, SPEC-046 |
| WAL-02 | SPEC-043 |
| WAL-03 | SPEC-045, SPEC-047, SPEC-129 |
| WAL-04 | SPEC-049 |
| RISK-01 | SPEC-121 |
| RISK-02 | SPEC-121 |
| RISK-03 | SPEC-075 |
| RISK-04 | SPEC-067, SPEC-076, SPEC-083, SPEC-167 |
| RISK-05 | SPEC-077 |
| HEAT-01 | SPEC-073 |
| HEAT-02 | SPEC-012, SPEC-074, SPEC-130 |
| SCHEME-01 | SPEC-106, SPEC-107 |
| SCHEME-02 | SPEC-084, SPEC-108 |
| SCHEME-03 | SPEC-080, SPEC-109, SPEC-163 |
| SCHEME-04 | SPEC-112 |
| MANIP-01 | SPEC-110, SPEC-164, SPEC-165, SPEC-166 |
| MANIP-02 | SPEC-111 |
| TRIB-01 | SPEC-085, SPEC-093 |
| TRIB-02 | SPEC-086, SPEC-087, SPEC-088, SPEC-089, SPEC-171 |
| TRIB-03 | SPEC-090 |
| TRIB-04 | SPEC-091, SPEC-171 |
| TRIB-05 | SPEC-081, SPEC-092 |
| PRED-01 | SPEC-094, SPEC-095, SPEC-096, SPEC-174 |
| PRED-02 | SPEC-097, SPEC-098, SPEC-100, SPEC-101, SPEC-169 |
| PRED-03 | SPEC-099 |
| PRED-04 | SPEC-095 |
| GRAPH-01 | SPEC-102 |
| GRAPH-02 | SPEC-079, SPEC-103, SPEC-104 |
| GRAPH-03 | SPEC-105, SPEC-172 |
| LOG-01 | SPEC-023, SPEC-062, SPEC-113 |
| LOG-02 | SPEC-061, SPEC-114 |
| RPT-01 | SPEC-115, SPEC-116 |
| RPT-02 | SPEC-118 |
| EDU-01 | SPEC-119, SPEC-120, SPEC-173 |
| INST-01 | SPEC-116, SPEC-123 |
| MACRO-01 | SPEC-116, SPEC-124 |
| DUR-01 | SPEC-029, SPEC-135, SPEC-141 |
| DUR-02 | SPEC-028, SPEC-140 |
| DUR-03 | SPEC-030, SPEC-144 |
| COST-01 | SPEC-050, SPEC-137, SPEC-139 |
| COST-02 | SPEC-136, SPEC-143 |
| COST-03 | SPEC-138 |
| LIVE-01 | SPEC-131, SPEC-145, SPEC-146, SPEC-147, SPEC-149, SPEC-150 |
| LIVE-02 | SPEC-138, SPEC-148 |
| LIVE-03 | SPEC-131, SPEC-133 |
| PORT-01 | SPEC-125, SPEC-126 |
| PORT-02 | SPEC-132 |
| PORT-03 | SPEC-127 |
| LEDGER-01 | SPEC-046, SPEC-117, SPEC-151, SPEC-153, SPEC-174 |
| QA-01 | SPEC-025, SPEC-156, SPEC-157, SPEC-158, SPEC-159, SPEC-168 |
| QA-02 | Governance, not a system clause: constitution Development Workflow (Definition of done) and task T158 |
| QA-03 | SPEC-033, SPEC-042, SPEC-160, SPEC-170 |
| QA-04 | SPEC-041, SPEC-170 |
| QA-05 | SPEC-016, SPEC-161 |

## 4. User stories to clauses

| Story | Priority | Clauses exercised by its acceptance scenarios |
|---|---|---|
| US1: The firm runs itself around the clock on crypto | P1 | SPEC-009, SPEC-021, SPEC-022, SPEC-029, SPEC-046, SPEC-063, SPEC-113, SPEC-135 |
| US2: The owners learn from the firm's reports | P1 | SPEC-115, SPEC-119, SPEC-120, SPEC-121 |
| US3: The owners steer from outside the organization | P2 | SPEC-011, SPEC-073, SPEC-074, SPEC-127 |
| US4: The firm trades every asset class it can automate | P2 | SPEC-026, SPEC-027, SPEC-059, SPEC-066 |
| US5: Serious targets face a tribunal | P2 | SPEC-075, SPEC-087, SPEC-088, SPEC-090 |
| US6: Predictions are honest, calibrated and connected | P2 | SPEC-096, SPEC-102, SPEC-104, SPEC-153 |
| US7: The firm hunts structural opportunities without getting eaten | P3 | SPEC-080, SPEC-107, SPEC-108, SPEC-109 |
| US8: Any seat runs in any harness | P3 | SPEC-013, SPEC-014 |
| US9: Live trading is ready and off | P3 | SPEC-146, SPEC-147 |
| US10: Personas, an institution model and a macro book | P3 | SPEC-048, SPEC-054 |

Intent section 8 stories (epics A to H) list their verifying clauses directly.

## 5. Clause to evaluation, decision and tasks

| Clause | Evaluation | Traces (requirements) | Decision | Tasks |
|---|---|---|---|---|
| SPEC-001 | EVAL-001 | ROLE-01 | CTX-012, CTX-013 | T013, T014 |
| SPEC-002 | EVAL-002 | ORG-01, ORG-08 | CTX-012, CTX-013 | T013, T014, T015, T041, T157 |
| SPEC-003 | EVAL-003 | CYC-06, ORG-02 | CTX-012, CTX-013 | T041 |
| SPEC-004 | EVAL-004 | ORG-02, ORG-05 | CTX-012, CTX-013 | T041 |
| SPEC-005 | EVAL-005 | ORG-02 | CTX-012, CTX-013 | T041 |
| SPEC-006 | EVAL-006 | ORG-06 | CTX-012, CTX-013 | T015, T041, T042 |
| SPEC-007 | EVAL-007 | ORG-06 | CTX-012, CTX-013 | T015, T033, T041, T042 |
| SPEC-008 | EVAL-008 | ORG-07 | CTX-012, CTX-013 | T011 |
| SPEC-009 | EVAL-009 | ORG-03 | CTX-012, CTX-013 | T050, T072 |
| SPEC-010 | EVAL-010 | ORG-04, ORG-05 | CTX-012, CTX-013 | T048, T074 |
| SPEC-011 | EVAL-011 | ORG-04 | CTX-012, CTX-013 | T048, T074 |
| SPEC-012 | EVAL-012 | HEAT-02 | CTX-012, CTX-013 | T048 |
| SPEC-013 | EVAL-013 | ROLE-02, ROLE-03 | CTX-016 | T001, T120, T123 |
| SPEC-014 | EVAL-014 | ROLE-03 | CTX-016 | T120, T121 |
| SPEC-015 | EVAL-015 | ROLE-03 | CTX-016 | T121, T122 |
| SPEC-016 | EVAL-016 | QA-05, ROLE-05 | CTX-016 | T013, T037, T120, T123 |
| SPEC-017 | EVAL-017 | ROLE-06 | CTX-016 | T003, T017, T123 |
| SPEC-018 | EVAL-018 | ROLE-04 | CTX-016 | T013, T017 |
| SPEC-019 | EVAL-019 | ROLE-07 | CTX-016 | T013, T016 |
| SPEC-020 | EVAL-020 | ROLE-02 | CTX-016 | T037, T038, T124, T125 |
| SPEC-021 | EVAL-021 | CYC-01 | CTX-002, CTX-003 | T039, T043, T045 |
| SPEC-022 | EVAL-022 | CYC-02 | CTX-002, CTX-003 | T039, T043 |
| SPEC-023 | EVAL-023 | CYC-03, LOG-01 | CTX-002, CTX-003 | T039, T049 |
| SPEC-024 | EVAL-024 | CYC-06 | CTX-002, CTX-003 | T060 |
| SPEC-025 | EVAL-025 | CYC-04, QA-01 | CTX-002, CTX-003 | T061 |
| SPEC-026 | EVAL-026 | CYC-05, MKT-02 | CTX-002, CTX-003 | T018, T080, T085 |
| SPEC-027 | EVAL-027 | CYC-07 | CTX-002, CTX-003 | T031, T085 |
| SPEC-028 | EVAL-028 | DUR-02 | CTX-002, CTX-003 | T039, T050 |
| SPEC-029 | EVAL-029 | DUR-01 | CTX-002, CTX-003 | T010, T011, T039, T044, T045 |
| SPEC-030 | EVAL-030 | DUR-03 | CTX-002, CTX-003 | T039 |
| SPEC-031 | EVAL-031 | RES-01 | CTX-005, CTX-006, CTX-007 | T030, T043, T081, T082 |
| SPEC-032 | EVAL-032 | RES-06 | CTX-005, CTX-006, CTX-007 | T018, T030, T081 |
| SPEC-033 | EVAL-033 | QA-03, RES-03 | CTX-005, CTX-006, CTX-007 | T018 |
| SPEC-034 | EVAL-034 | RES-03 | CTX-005, CTX-006, CTX-007 | T018 |
| SPEC-035 | EVAL-035 | RES-03 | CTX-005, CTX-006, CTX-007 | T018 |
| SPEC-036 | EVAL-036 | RES-04 | CTX-005, CTX-006, CTX-007 | T016, T037 |
| SPEC-037 | EVAL-037 | RES-05 | CTX-005, CTX-006, CTX-007 | T016, T037, T154 |
| SPEC-038 | EVAL-038 | RES-06 | CTX-005, CTX-006, CTX-007 | T060 |
| SPEC-039 | EVAL-039 | RES-02 | CTX-005, CTX-006, CTX-007 | T064 |
| SPEC-040 | EVAL-040 | RES-03 | CTX-005, CTX-006, CTX-007 | T030 |
| SPEC-041 | EVAL-041 | QA-04 | CTX-005, CTX-006, CTX-007 | T018, T151 |
| SPEC-042 | EVAL-042 | QA-03 | CTX-005, CTX-006, CTX-007 | T018, T151 |
| SPEC-043 | EVAL-043 | PLAN-01, WAL-02 | CTX-004, CTX-014 | T040, T041, T140 |
| SPEC-044 | EVAL-044 | WAL-01 | CTX-004, CTX-014 | T033, T041 |
| SPEC-045 | EVAL-045 | WAL-03 | CTX-004, CTX-014 | T073 |
| SPEC-046 | EVAL-046 | LEDGER-01, WAL-01 | CTX-004, CTX-014 | T033 |
| SPEC-047 | EVAL-047 | WAL-03 | CTX-004, CTX-014 | T033 |
| SPEC-048 | EVAL-048 | PLAN-01 | CTX-004, CTX-014 | T034, T040, T140 |
| SPEC-049 | EVAL-049 | WAL-04 | CTX-004, CTX-014 | T151 |
| SPEC-050 | EVAL-050 | COST-01 | CTX-004, CTX-014 | T033 |
| SPEC-051 | EVAL-051 | PLAN-03 | CTX-004, CTX-014 | T060, T071 |
| SPEC-052 | EVAL-052 | PLAN-03 | CTX-004, CTX-014 | T014, T038 |
| SPEC-053 | EVAL-053 | DSL-01 | CTX-008 | T034, T043 |
| SPEC-054 | EVAL-054 | DSL-01 | CTX-008 | T034 |
| SPEC-055 | EVAL-055 | DSL-01 | CTX-008 | T034 |
| SPEC-056 | EVAL-056 | PLAN-02 | CTX-008 | T034, T040 |
| SPEC-057 | EVAL-057 | DSL-03 | CTX-008 | T034 |
| SPEC-058 | EVAL-058 | DSL-04 | CTX-008 | T016, T034, T037, T038 |
| SPEC-059 | EVAL-059 | DIR-01 | CTX-008 | T034, T080, T084, T085 |
| SPEC-060 | EVAL-060 | PLAN-02 | CTX-008 | T034 |
| SPEC-061 | EVAL-061 | LOG-02 | CTX-008 | T034 |
| SPEC-062 | EVAL-062 | LOG-01 | CTX-008 | T034 |
| SPEC-063 | EVAL-063 | MKT-01 | CTX-004, CTX-005 | T019, T031, T046 |
| SPEC-064 | EVAL-064 | MKT-01 | CTX-004, CTX-005 | T031 |
| SPEC-065 | EVAL-065 | MKT-01 | CTX-004, CTX-005 | T031 |
| SPEC-066 | EVAL-066 | DIR-01, MKT-01 | CTX-004, CTX-005 | T032, T084 |
| SPEC-067 | EVAL-067 | RISK-04 | CTX-004, CTX-005 | T032 |
| SPEC-068 | EVAL-068 | DSL-02 | CTX-004, CTX-005 | T080, T081, T082, T083 |
| SPEC-069 | EVAL-069 | MKT-03 | CTX-004, CTX-005 | T046, T130, T131 |
| SPEC-070 | EVAL-070 | MKT-01 | CTX-004, CTX-005 | T010, T031 |
| SPEC-071 | EVAL-071 | MKT-02 | CTX-004, CTX-005 | T031, T080, T084 |
| SPEC-072 | EVAL-072 | MKT-01 | CTX-004, CTX-005 | T019, T030, T031, T046 |
| SPEC-073 | EVAL-073 | HEAT-01 | CTX-010, CTX-012 | T017, T035 |
| SPEC-074 | EVAL-074 | HEAT-02 | CTX-010, CTX-012 | T048, T074 |
| SPEC-075 | EVAL-075 | RISK-03 | CTX-010, CTX-012 | T035 |
| SPEC-076 | EVAL-076 | RISK-04 | CTX-010, CTX-012 | T035 |
| SPEC-077 | EVAL-077 | RISK-05 | CTX-010, CTX-012 | T035 |
| SPEC-078 | EVAL-078 | ORG-05 | CTX-010, CTX-012 | T048 |
| SPEC-079 | EVAL-079 | GRAPH-02 | CTX-010, CTX-012 | T101 |
| SPEC-080 | EVAL-080 | SCHEME-03 | CTX-010, CTX-012 | T110 |
| SPEC-081 | EVAL-081 | TRIB-05 | CTX-010, CTX-012 | T035 |
| SPEC-082 | EVAL-082 | ORG-06 | CTX-010, CTX-012 | T035, T042 |
| SPEC-083 | EVAL-083 | RISK-04 | CTX-010, CTX-012 | T035 |
| SPEC-084 | EVAL-084 | SCHEME-02 | CTX-010, CTX-012 | T035, T111 |
| SPEC-085 | EVAL-085 | TRIB-01 | CTX-009, CTX-013 | T042 |
| SPEC-086 | EVAL-086 | TRIB-02 | CTX-009, CTX-013 | T090 |
| SPEC-087 | EVAL-087 | TRIB-02 | CTX-009, CTX-013 | T090 |
| SPEC-088 | EVAL-088 | TRIB-02 | CTX-009, CTX-013 | T091 |
| SPEC-089 | EVAL-089 | TRIB-02 | CTX-009, CTX-013 | T092 |
| SPEC-090 | EVAL-090 | TRIB-03 | CTX-009, CTX-013 | T092 |
| SPEC-091 | EVAL-091 | TRIB-04 | CTX-009, CTX-013 | T093 |
| SPEC-092 | EVAL-092 | TRIB-05 | CTX-009, CTX-013 | T015, T042 |
| SPEC-093 | EVAL-093 | TRIB-01 | CTX-009, CTX-013 | T092 |
| SPEC-094 | EVAL-094 | PRED-01 | CTX-011 | T036, T043 |
| SPEC-095 | EVAL-095 | PRED-01, PRED-04 | CTX-011 | T036 |
| SPEC-096 | EVAL-096 | PRED-01 | CTX-011 | T036 |
| SPEC-097 | EVAL-097 | PRED-02 | CTX-011 | T036 |
| SPEC-098 | EVAL-098 | PRED-02 | CTX-011 | T102 |
| SPEC-099 | EVAL-099 | PRED-03 | CTX-011 | T083, T102 |
| SPEC-100 | EVAL-100 | PRED-02 | CTX-011 | T103 |
| SPEC-101 | EVAL-101 | PRED-02 | CTX-011 | T103 |
| SPEC-102 | EVAL-102 | GRAPH-01 | CTX-011 | T100 |
| SPEC-103 | EVAL-103 | GRAPH-02 | CTX-011 | T100 |
| SPEC-104 | EVAL-104 | GRAPH-02 | CTX-011 | T101 |
| SPEC-105 | EVAL-105 | GRAPH-03 | CTX-011 | T061, T103 |
| SPEC-106 | EVAL-106 | SCHEME-01 | CTX-015 | T019, T110 |
| SPEC-107 | EVAL-107 | SCHEME-01 | CTX-015 | T111 |
| SPEC-108 | EVAL-108 | SCHEME-02 | CTX-015 | T111 |
| SPEC-109 | EVAL-109 | SCHEME-03 | CTX-015 | T110 |
| SPEC-110 | EVAL-110 | MANIP-01 | CTX-015 | T019, T112 |
| SPEC-111 | EVAL-111 | MANIP-02 | CTX-015 | T113 |
| SPEC-112 | EVAL-112 | SCHEME-04 | CTX-015 | T113 |
| SPEC-113 | EVAL-113 | LOG-01 | CTX-014 | T011, T043, T049 |
| SPEC-114 | EVAL-114 | LOG-02 | CTX-014 | T049 |
| SPEC-115 | EVAL-115 | RPT-01 | CTX-014 | T060 |
| SPEC-116 | EVAL-116 | INST-01, MACRO-01, RPT-01 | CTX-014 | T061 |
| SPEC-117 | EVAL-117 | LEDGER-01 | CTX-014 | T012, T061 |
| SPEC-118 | EVAL-118 | RPT-02 | CTX-014 | T063 |
| SPEC-119 | EVAL-119 | EDU-01 | CTX-014 | T016, T060 |
| SPEC-120 | EVAL-120 | EDU-01 | CTX-014 | T060 |
| SPEC-121 | EVAL-121 | RISK-01, RISK-02 | CTX-014 | T062 |
| SPEC-122 | EVAL-122 | RES-02 | CTX-014 | T064 |
| SPEC-123 | EVAL-123 | INST-01 | CTX-014 | T141 |
| SPEC-124 | EVAL-124 | MACRO-01 | CTX-014 | T142 |
| SPEC-125 | EVAL-125 | PORT-01 | CTX-012, CTX-018 | T070, T154 |
| SPEC-126 | EVAL-126 | PORT-01 | CTX-012, CTX-018 | T070, T071 |
| SPEC-127 | EVAL-127 | PORT-03 | CTX-012, CTX-018 | T072 |
| SPEC-128 | EVAL-128 | ORG-04 | CTX-012, CTX-018 | T072 |
| SPEC-129 | EVAL-129 | WAL-03 | CTX-012, CTX-018 | T073 |
| SPEC-130 | EVAL-130 | HEAT-02 | CTX-012, CTX-018 | T074 |
| SPEC-131 | EVAL-131 | LIVE-01, LIVE-03 | CTX-012, CTX-018 | T074 |
| SPEC-132 | EVAL-132 | PORT-02 | CTX-012, CTX-018 | T016, T071, T072, T075 |
| SPEC-133 | EVAL-133 | LIVE-03 | CTX-012, CTX-018 | T063, T155 |
| SPEC-134 | EVAL-134 | ORG-04 | CTX-012, CTX-018 | T048, T075 |
| SPEC-135 | EVAL-135 | DUR-01 | CTX-003, CTX-009, CTX-010, CTX-021 | T044, T045, T046 |
| SPEC-136 | EVAL-136 | COST-02 | CTX-003, CTX-009, CTX-010, CTX-021 | T047 |
| SPEC-137 | EVAL-137 | COST-01 | CTX-003, CTX-009, CTX-010, CTX-021 | T017, T047, T156 |
| SPEC-138 | EVAL-138 | COST-03, LIVE-02 | CTX-003, CTX-009, CTX-010, CTX-021 | T037, T154 |
| SPEC-139 | EVAL-139 | COST-01 | CTX-003, CTX-009, CTX-010, CTX-021 | T003, T017, T037, T190 |
| SPEC-140 | EVAL-140 | DUR-02 | CTX-003, CTX-009, CTX-010, CTX-021 | T039 |
| SPEC-141 | EVAL-141 | DUR-01 | CTX-003, CTX-009, CTX-010, CTX-021 | T153 |
| SPEC-142 | EVAL-142 | ROLE-02 | CTX-003, CTX-009, CTX-010, CTX-021 | T043, T124 |
| SPEC-143 | EVAL-143 | COST-02 | CTX-003, CTX-009, CTX-010, CTX-021 | T037, T047 |
| SPEC-144 | EVAL-144 | DUR-03 | CTX-003, CTX-009, CTX-010, CTX-021 | T037 |
| SPEC-145 | EVAL-145 | LIVE-01 | CTX-017 | T019, T130, T131 |
| SPEC-146 | EVAL-146 | LIVE-01 | CTX-017 | T050, T132, T157 |
| SPEC-147 | EVAL-147 | LIVE-01 | CTX-017 | T132 |
| SPEC-148 | EVAL-148 | LIVE-02 | CTX-017 | T130, T131 |
| SPEC-149 | EVAL-149 | LIVE-01 | CTX-017 | T132 |
| SPEC-150 | EVAL-150 | LIVE-01 | CTX-017 | T132 |
| SPEC-151 | EVAL-151 | LEDGER-01 | CTX-004, CTX-021 | T011, T012, T046 |
| SPEC-152 | EVAL-152 | ORG-07 | CTX-004, CTX-021 | T070, T152 |
| SPEC-153 | EVAL-153 | LEDGER-01 | CTX-004, CTX-021 | T012, T104 |
| SPEC-154 | EVAL-154 | ORG-07 | CTX-004, CTX-021 | T012, T152 |
| SPEC-155 | EVAL-155 | ORG-07 | CTX-004, CTX-021 | T152 |
| SPEC-156 | EVAL-156 | QA-01 | CTX-019, CTX-013 | T150 |
| SPEC-157 | EVAL-157 | QA-01 | CTX-019, CTX-013 | T150 |
| SPEC-158 | EVAL-158 | QA-01 | CTX-019, CTX-013 | T150 |
| SPEC-159 | EVAL-159 | QA-01 | CTX-019, CTX-013 | T150 |
| SPEC-160 | EVAL-160 | QA-03 | CTX-019, CTX-013 | T018, T151 |
| SPEC-161 | EVAL-161 | QA-05 | CTX-019, CTX-013 | T005, T123 |
| SPEC-162 | EVAL-162 | ORG-08 | CTX-019, CTX-013 | T015, T093 |
| SPEC-163 | EVAL-163 | SCHEME-03 | CTX-015 | T110, T132 |
| SPEC-164 | EVAL-164 | MANIP-01 | CTX-015 | T112 |
| SPEC-165 | EVAL-165 | MANIP-01 | CTX-015 | T112 |
| SPEC-166 | EVAL-166 | MANIP-01 | CTX-015 | T112 |
| SPEC-167 | EVAL-167 | DIR-01, RISK-04 | CTX-015 | T112 |
| SPEC-168 | EVAL-168 | QA-01 | CTX-019 | T150 |
| SPEC-169 | EVAL-169 | PRED-02 | CTX-019 | T102 |
| SPEC-170 | EVAL-170 | QA-03, QA-04 | CTX-019 | T151 |
| SPEC-171 | EVAL-171 | TRIB-02, TRIB-04 | CTX-013, CTX-019 | T091, T092 |
| SPEC-172 | EVAL-172 | GRAPH-03 | CTX-013, CTX-019 | T093 |
| SPEC-173 | EVAL-173 | EDU-01 | CTX-014 | T060, T063 |
| SPEC-174 | EVAL-174 | LEDGER-01, PRED-01 | CTX-011, CTX-021 | T104 |

## 6. Gap check (at generation)

- Working requirements without a clause: none (QA-02 is governance, mapped to the constitution and T158).
- Clauses without a plan decision: none. Clauses without a task: none.
- Clauses without a held-out evaluation: none (174 of 174 bound).
