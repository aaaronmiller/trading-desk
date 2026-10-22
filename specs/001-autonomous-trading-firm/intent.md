---
date: 2026-10-21 15:40:00 UTC
ver: 1.0.0
author: Aaron Miller (owner statements T1 to T9) compiled by Claude Code session; system-drafted, ratified by launching the build
model: Claude (Claude Code session)
tags: [intent, autonomous-trading-firm, constraints, personas, user-stories, prior-art]
layer: human
---
# Autonomous Trading Firm Intent v1.0

Provenance: every statement below comes from the owners' own words recorded in the intake (`sources/originals/conversation-intent-2026-10-20.md`, statements T1 to T9, and `pasted-resources-2026-10-21.md`, sections A to F), from the legacy pack and planning documents the owners commissioned, or from research waves 1 and 2. Statements that are the system's reading rather than an owner's statement carry [INFERENCE]. Launching the build with the reset handoff ratifies this intent, including every [INFERENCE] item.

## 1. Goal

Two owners get a self-running, around-the-clock investment firm of AI agents that hunts high-risk, high-upside opportunities across crypto and every automatable asset class, proves its judgment with a tamper-evident record, and teaches both owners finance through its daily reports, while risking no real money until the operator chooses to.

## 2. Intent level

- Consumer intent (epic): an autonomous trading firm the two owners observe, steer from outside, and learn from.
- Engineering intent (plays): a portable firm definition (roles, skills, rules, cycles as plain files) that runs unattended in the cloud and inside any agent harness from one canonical source.

## 3. Constraints

1. **Money**: the first build trades simulated money only. Real-order capability is built and tested but stays off until the operator owner switches it on (T7 "Simulate; live code off"). Credentials can trade but never withdraw and never reach a model (T3).
2. **Humans outside the loop**: the owners are not part of the organization; a virtual chief executive runs it hands-on and no agent waits for a human (T4). Owners hold only envelope powers: live switch and ceilings (operator), pause (either owner), heat dials within ceilings (either owner) (T3, T9).
3. **Agents are not told execution is simulated** (T6, resource A "the agent is not to know"). Honesty toward the owners comes from labels the agents cannot alter. The intake inventory recommended telling the agents; that dissent is recorded in the ledger.
4. **Hosting**: always-on parts run on the owners' chosen edge platform, Cloudflare (T1, T3, standing preferences), on its paid plan by assumption [NEEDS CLARIFICATION 1]. A local runtime exists for development and tests.
5. **Running cost**: run plane at or under 25 US dollars per month in total (hosting, model calls, data) unless an owner raises it (T7 default; R11 CO-12). The build subscription is the operator's own and outside this ceiling.
6. **Portability**: roles, skills and rules are markdown-first and work in any agent harness, at minimum Claude Code and Roo Code (T6), and do not depend on agent frameworks that bind them to a runtime; the owner named LangChain and LangSmith as examples to avoid (resource E).
7. **Data**: free and keyless sources first; paid data only after a strategy shows it needs it and an owner raises the budget (R11 CO-22, C-16). Sources whose terms forbid automated use are excluded (R11 C-23).
8. **Jurisdiction**: both owners are US persons; venue and data access follow from that, including read-only access where trading is unavailable to US persons (R11 CO-05).
9. **Conduct**: the firm never manipulates markets and never promotes or recruits for any asset; suspected payout schemes stay restricted for live capital unless an owner lifts the restriction per asset with an acknowledgment of legal exposure (T9; system reading of clawback exposure, R13 pending) [INFERENCE].
10. **Model routes**: prompts never carry credentials or account identifiers; routes that may train on prompts carry only content without account identifiers (R11 C-27, owner decision D-15).
11. **Formats**: every document carries the owners' frontmatter block, uses no em dashes and bumps its version on revision; code is complete with no placeholders (T8).

## 4. Scale and quality expectations

- Continuous operation 24/7; a research-to-plan cycle about every 15 minutes; hourly analysis of every active book; daily, weekly and monthly reporting (resource B, T6).
- Organization of about 32 seat types (with one portfolio manager per persona), 20 personas at launch (expandable), two owner sandboxes, strategy books, a house book and four benchmark books (resource B, R03, T4).
- Instrument coverage: crypto spot and perpetual futures first, then stocks, funds, options, bonds, foreign exchange, commodities, prediction-market contracts and a data-center GPU price index (resource A, T6, T9).
- Decisions take minutes; this is not a high-frequency system (R11 CO-07).
- Reliability: at least 99 percent of scheduled cycles complete in any rolling week; no lost or duplicated record after any restart; daily off-store export with a verified restore (T7, R11).
- Daily report ready by 06:00 Pacific time, before the US equity open (T9 "daily written reports").
- Track-record significance: at least 200 resolved predictions before any skill claim; about 800 to 1,800 paired questions to establish a 0.02 Brier edge against markets (R06).
- Cost: at or under the monthly ceiling in constraint 5, enforced continuously.

## 5. Success conditions

1. **Calibrated forecasts**: after 200 resolved predictions, calibration slope between 0.8 and 1.2 and skill reported against market prices and naive baselines (T7).
2. **Net simulated profit after all costs** for the house book over the first 90 days, reported alongside benchmarks (T7).
3. **Opportunity hit rate** measured per goodness-score band, with the top bands beating the bottom bands (T7, resource D).
4. **Reliability**: cycle completion and restart guarantees in section 4 met for the first 30 days (T7).
5. **Target calibration**: a weekly feasibility report the owners trust, stating how attainable 1, 2 and 3 percent per day are at current and required risk, with intervals (T7 partner mandate).
6. **Learning**: both owners can follow every decision's reasoning, concept, counterparty and lesson from the reports alone (T9).
7. **Portability**: every seat runs from the same canonical files in the cloud and in both named harnesses (T6).
8. **Honesty**: every record verifies; no output presents the target as promised (T1, constitution IV).

## 6. Failure conditions

1. **Data unavailable or stale**: inputs are labeled unavailable, scope shrinks, no fill on stale prices, nothing guessed.
2. **Model provider outage**: retry, fall back to an alternate route, otherwise skip the step; never record a partial decision as complete.
3. **Budget exhaustion**: the capped seat pauses and the chief executive reallocates; at the firm ceiling, non-essential seats throttle first while risk, execution, records and reporting keep running.
4. **Crash or restart at any point**: resume with nothing lost and nothing duplicated.
5. **Book drawdown**: warn, then halve new risk, then stop new risk with a post-mortem; the house book's final stop (50 percent below its high-water mark by default) resumes only by the operator (addendum 2.1).
6. **Daily loss limit hit**: no new risk in that book until the next trading day.
7. **Invalid or ungrounded plan**: rejected with reasons; nothing reaches the market.
8. **Prompt injection in fetched content**: treated as text, flagged, never obeyed.
9. **Payout scheme deterioration**: staged exit when hazard passes the payout rate; if withdrawals stop first, the position is marked impaired and the miss becomes a lesson.
10. **Manipulation detected**: entries blocked in the flagged instrument for a window.
11. **Owner conflict on a dial**: the more conservative value applies and both owners are told.
12. **Live venue rejects an order** (once live): reason recorded, position not opened, owners notified.
13. **Tampering or record divergence**: verification names the first divergent record and an incident opens.
14. **Clock skew**: skewed data is quarantined and labeled.

## 7. Personas

- **Operator owner (Aaron Miller, "Ice-ninja")**: builder and operator. Goal: a firm that runs itself, proves itself and earns, plus experience with the stack. Frustration: babysitting, barriers created for no reason, flattering numbers. Context: builds with agent harnesses, holds the live switch. Technical sophistication: high in software, learning institutional finance.
- **Partner owner**: funding partner and experienced business owner. Goal: aggressive returns (an appetite of 1 to 3 percent per day) and an understanding of how the machine invests. Frustration: opacity. Context: asks questions, proposes trades, runs mock portfolios, reads reports; every message to him ends with 786110. Technical sophistication: business-expert, non-technical.
- **Virtual chief executive (agent)**: runs the firm day to day inside the owners' envelope; not a human persona but the owners' counterpart.
- **Evaluator (separate context)**: grades the build against held-out evaluations without access by the implementer.
- **Virtual investors (twenty personas)**: simulated people with worldviews and risk profiles whose books the firm manages; they are data, not users.

## 8. User stories

Epic A: The firm runs itself
- A1. As the operator, I want the firm to research, plan, execute and record around the clock without me, so that it earns a record while I build other things. Given a deployed firm and no owner activity, when a day passes, then at least 95 cycles complete with plans, fills, predictions and logs. Verified by SPEC-001 to SPEC-012, SPEC-021 to SPEC-030, SPEC-053 to SPEC-072, SPEC-094, SPEC-113, SPEC-135.
- A2. As the operator, I want staffing to change by performance, so that weak seats are revised or retired without me. Given a seat with a poor scored record, when the weekly review runs, then the chief executive records a revision or retirement with reasons and envelope limits stay untouched. Verified by SPEC-005, SPEC-025, SPEC-091, SPEC-162.

Epic B: The owners learn
- B1. As both owners, I want an educational daily report before the market opens, so that we understand each decision. Given a completed day, when 06:00 Pacific arrives, then the report exists with every section and every decision carries its five teaching elements. Verified by SPEC-114 to SPEC-120, SPEC-038, SPEC-039.
- B2. As the partner, I want a weekly honest answer on the 1 to 3 percent per day appetite, so that I can choose my risk with open eyes. Given 30 closed positions, when the weekly report runs, then it states required win rate, edge, attainment probabilities, required sizing and ruin risk with intervals. Verified by SPEC-121, SPEC-133.
- B3. As both owners, I want to study how a major institution invests, so that we learn large-scale practice. Given a week, when the weekly report runs, then it includes an institution study note citing primary filings or documents. Verified by SPEC-123.

Epic C: The owners steer from outside
- C1. As either owner, I want to ask any seat a question and send the chief executive ideas, so that I can probe and influence the firm without stopping it. Given a question or idea, when the next cycle completes, then an attributed answer or acknowledgment exists and cycles stayed on schedule. Verified by SPEC-127, SPEC-128, SPEC-009.
- C2. As either owner, I want heat dials on the firm, personas and strategies, so that we can turn risk up or down at any time. Given a dial change, when the next cycle starts, then new orders follow the new limits, the change is logged and the other owner is told. Verified by SPEC-073, SPEC-074, SPEC-012, SPEC-130.
- C3. As either owner, I want my own sandbox with theoretical cash, so that I can test ideas against the firm. Given a sandbox, when I trade it, then it fills like any book and compares with agent books and benchmarks. Verified by SPEC-045, SPEC-129.
- C4. As either owner, I want to pause the firm or a book, so that I can stop risk instantly. Given a pause, when the next release step runs, then nothing in scope is released. Verified by SPEC-011, SPEC-010.

Epic D: The firm decides well and both ways
- D1. As the partner, I want pro and con advocates on different models to debate serious targets with a third model judging, so that decisions survive real argument. Given a serious target, when the window closes, then a full four-round debate and a ruling with direction and conviction exist. Verified by SPEC-085 to SPEC-093.
- D2. As both owners, I want the firm to profit from falls as well as rises, so that a negative view is still a trade. Given a bearish ruling, when the plan compiles, then it uses an available short-side form with its costs. Verified by SPEC-059, SPEC-066.
- D3. As both owners, I want each prediction linked to its drivers and to other predictions, so that the firm sees correlated bets and cascades. Given a driver resolution, when the next cycle runs, then dependents are flagged and shared-driver exposure stays capped. Verified by SPEC-102 to SPEC-105, SPEC-079.

Epic E: The record is honest
- E1. As both owners, I want every prediction sealed before its outcome and scored against markets and baselines, so that the track record carries weight. Given a prediction, when it resolves, then it is scored, compared and verifiable. Verified by SPEC-094 to SPEC-101, SPEC-153.
- E2. As both owners, I want point-in-time integrity in every historical evaluation, so that backtests do not lie. Given a replay, when a future row is planted, then it never reaches a decision and the suite fails if it does. Verified by SPEC-031 to SPEC-042, SPEC-160.

Epic F: Aggressive but not eaten
- F1. As the partner, I want the firm to find and ride structural opportunities such as payout schemes with disciplined exits, so that the aggressive mandate has a method. Given a held scheme asset, when hazard passes the payout rate, then a staged exit within liquidity begins. Verified by SPEC-106 to SPEC-109, SPEC-084.
- F2. As both owners, I want manipulation recognized and avoided, so that the firm feeds among sharks without being eaten. Given a flagged pump, when an entry is proposed within the window, then it is blocked. Verified by SPEC-110, SPEC-111.

Epic G: Portable and ready for live
- G1. As the operator, I want any seat to run in Claude Code or Roo Code from the same files, so that the firm is not locked to one runtime. Given a canonical edit, when generation runs, then every harness file updates and drift checks pass. Verified by SPEC-013 to SPEC-020, SPEC-142.
- G2. As the operator, I want live trading built, tested and off, so that switching on later is one recorded act. Given live off, when the firm runs, then no order-endpoint request occurs; given the operator's confirmed switch, then a change event records it. Verified by SPEC-145 to SPEC-150, SPEC-131.

Epic H: Personas and books
- H1. As the operator, I want twenty virtual investors with worldviews and dials, so that strategies are tested across temperaments. Given a persona's constraints, when a plan breaches them, then compilation rejects it. Verified by SPEC-043 to SPEC-052.

## 9. Scope boundaries

| In scope | Out of scope | Rationale |
|----------|-------------|-----------|
| Simulated execution at live prices for all automatable classes | Real-money trading in this build (built, tested, off) | T7 owner decision |
| Owner portal with two accounts and console | Additional user accounts, third-party clients | T3, R11 C-06 |
| Educational reports for the two owners | Advice or promotion to third parties | Conduct constraint 9 |
| Prediction-market prices as priors and benchmarks | Trading prediction markets live where US persons cannot | Constraint 8 |
| Payout-scheme study, simulation and exit modeling | Recruiting for, promoting or marketing any asset | T9, constraint 9 |
| Local runtime for development and harness use | Desktop application | Not requested |
| Historical replay with point-in-time integrity | Using replay results as live-price book history | R11 C-13 |
| Pricing agent for the partner's business | Out of this build | R11 C-06; separate pitch on hold |
| Profit-split accounting fields in the ledger | Legal entity formation | T4: entity only if capital grows |

## 10. Prior art

| Solution | Strength | Weakness | Gap this fills |
|----------|----------|----------|----------------|
| TauricResearch/TradingAgents (about 112k stars, Apache-2.0) | Analyst, bull and bear, trader, risk debate, portfolio manager; reflection loop; point-in-time filter for history (R01) | Portfolio manager is an LLM with no code gate; risk control is a prompt debate; graph-framework plumbing | Deterministic risk authority; durable 24/7 runtime; owners' envelope |
| virattt/ai-hedge-fund (about 64k, MIT) | Investor-persona signals, deterministic blend and clamps, pre-order validator, hash-chained ledger (R01) | No live path; simulated fills carry no costs | Realistic cost model; persona books with wallets; calibration registry |
| HKUDS/Vibe-Trading (about 36k, MIT) | 30 team presets, 119 agents, multi-asset data, paper accounts, live behind a separate mandate gate (R01, R12 best fit 18 of 26) | Debate presets have no rebuttal; no firm runtime or budget caps; reporting audit advisory only | Real rebuttal rounds and judge; budgets; owner governance |
| AI4Finance FinRobot (about 8k, Apache-2.0) | Code overwrites LLM verdicts on its research path; IC memo gate (R01) | Bull, bear and judge files present but not loaded | Working tribunal with scored judges |
| paperclipai Agent Companies and Paperclip (MIT) | Only vendor-neutral company format: COMPANY, TEAM, AGENTS, SKILL files plus sidecar; heartbeats, budgets, approvals (R02, R04, R12) | No trading; harness-process heartbeats cost far more per call than a lean runtime; needs an always-on server | Export target for the firm package; lean cloud runtime keeps cost under ceiling |
| HyperGrok Trading Desk (MIT) | Most complete harness-neutral desk: 7 roles, 17 skills, four harness manifests, approval by id, single order-writing role (R02) | Small; prompt hook is only a backstop | Deterministic gate plus generated multi-harness files with drift checks |
| tradermonty claude-trading-skills (MIT, 74 skills) | Workflow manifests with decision gates and artifacts (R02) | Verification flags mostly unverified | Gated step graphs with evidence |
| alliela compliance gate; AI Market Maker risk veto; swarm-trader validator (R02) | Hard controls in code, no model in the gate | AGPL or unlicensed in two cases | Same control pattern, written fresh |
| QuantConnect LEAN, NautilusTrader, Freqtrade, FinRL-X (R12) | Mature fill, risk and paper-to-live semantics | No agents, no owners | Fill and risk semantics borrowed as concepts only |
| Halawi et al. 2024; ForecastBench; PolyBench (R06) | LLM forecasting near crowd level on subsets; superforecasters still lead; models lose money while overconfident | Raw accuracy hides calibration and market skill | Brier skill against market prices, recalibration, sample minimums |
| Multi-manager pod platforms, Bridgewater, Berkshire, Jane Street, D. E. Shaw (R03) | Drawdown ladders, central risk, believability weighting, post-mortems, risk committees | Press-reported figures; human institutions | Agent seats under the same separations, with scored believability |
| Portfolio research: 1/N (DeMiguel et al. 2009), hierarchical risk parity, Black-Litterman, fractional Kelly (R08) | Robust allocation and sizing baselines | Optimizers rarely beat 1/N out of sample | 1/N benchmark in every persona report; shrunk-edge fractional Kelly |
| Owner's own prior work: trading-desk legacy pack, vantage portal and ledger, investment thesis practice, TexitCoin brief (R11, T9) | Point-in-time clamp, commit-reveal design, hash-sealed ledger, public grading of calls, scheme forensics with ethical notes | Unratified, partly conflicting, spot-only | Reconciled into one contract with conflicts resolved in the ledger |

Patterns adopted: models propose and code disposes; one order-releasing role; deterministic gates and ladders; rebuttal-based debate with a cross-family judge; commit-before-horizon predictions scored against markets; generated harness files from canonical sources; trial registries with overfitting statistics; ethical "other side of the trade" notes from the owner's own brief.

Patterns avoided: LLM portfolio managers without code gates; debates without rebuttal; harness-process heartbeats for the always-on loop (cost); copying AGPL or unlicensed code; percentage stops without price structure; reporting accuracy without calibration; vote counting in place of judgment.

Search record: research reports R01 to R16 in the intake folder hold sources, access dates and unverified marks. The per-turn web search budget ran out mid-wave; affected claims are marked "(verify)" there.

## 11. Assumptions and dependencies

- Assumes reliable public price, filing, macro and prediction-market data reachable from the hosting platform; the build environment may reach none of it, so tests use recorded data (intake finding).
- Depends on hosted model routes from at least three model families, priced so the ceiling holds; route choice is a configuration decision [INFERENCE].
- Assumes the owners accept that agents are not told execution is simulated (T6), with honesty kept in owner-facing labels.
- Assumes theoretical capital: house book 100,000 US dollars, owner sandboxes 10,000 each, personas per profile [INFERENCE].
- Depends on the operator's environment allowing deployment credentials and outbound access to data hosts for live smoke tests; otherwise the build stops at a deployment dry run with a ready deploy procedure.
- External capabilities: market data feeds, prediction-market price history, public holdings filings, hosted model inference, durable scheduled execution, relational storage, object storage.

## 12. Open intent questions

1. [NEEDS CLARIFICATION] Hosting plan and monthly ceiling. Default if unanswered: the edge platform's paid plan (about 5 US dollars per month) and 25 US dollars per month in total, enforced by throttling. Research estimates bulk-model costs between about 23 and 44 US dollars per month at full activity, so the ceiling will throttle unless raised or cheaper routes hold.
2. [NEEDS CLARIFICATION] Model-route policy for the always-on loop. Default if unanswered: pay-as-you-go routes whose terms allow automated use; prompt-training routes only for content without account identifiers (owner decision D-15); subscription routes with unsettled automated-use terms excluded from the always-on loop (owner rule CO-13).
3. [NEEDS CLARIFICATION] Reference institution. Default if unanswered: a multi-manager platform for structure, Bridgewater-style believability-weighted debate for decisions, and a study stream of major funds' public holdings filings [INFERENCE].
