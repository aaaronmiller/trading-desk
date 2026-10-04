# Harness Role Bindings — DRAFT

> Status: draft, written 2026-10-03 (PDT). The system prompts live in
> `sources/tradingagents/agents/` (corrected in cycle 1: the shared
> collaboration preamble applies ONLY to the three tool-calling analysts;
> the sentiment analyst uses its own shortened variant; the other eight
> roles have no preamble upstream). This file defines what each
> `{placeholder}` binds to in the harness, plus each role's tool wiring and
> output contract. No role executes from this file; it is input to the
> extract play.

## Shared bindings

- `{current_date}` — the cycle's decision date (YYYY-MM-DD), not wall-clock
  time. In historical runs this is the cell date; in paper runs it is today.
- `{instrument_context}` — instrument identity block: symbol, name, venue
  class, quote currency, exchange/chain, company profile snapshot withheld
  from historical runs per the clamp contract rule 5.
- `{portfolio_context}` — current standing book (positions, cash, realized
  and unrealized P&L), identical for every cell in a backtest grid — never
  carried forward between cells.
- `{target_label}` — "stock" for equities, "asset" otherwise.
- `{history}` — the debate's conversation history so far, in order.

## Analysts

### Fundamentals Analyst — `fundamentals-analyst.md`
- Preamble: shared collaboration preamble (tool-calling variant).
- `{tool_names}`: `get_fundamentals, get_balance_sheet, get_cashflow,
  get_income_statement, get_insider_transactions`
- Tools bound: all five, date-clamped to `{current_date}`.
- Output: report + markdown table of key points.

### Technical (Market) Analyst — `technical-analyst.md`
- Preamble: shared collaboration preamble (tool-calling variant).
- Tools: `get_stock_data, get_indicators, get_verified_market_snapshot`
  (verify exact tool tuple in the extracted file).
- Output: technical report with price structure (current price,
  support/resistance, ATR) — this report is what grounds the trader's
  entry/stop levels (see debate-protocol.md).

### News Analyst — `news-analyst.md`
- Preamble: shared collaboration preamble (tool-calling variant).
- Tools: `get_news, get_global_news`
- Output: news report trimmed to the analysis window (upper bound exclusive
  at midnight after `end`).

### Sentiment Analyst — `sentiment-analyst.md`
- Preamble: the SHORTENED variant — no tool-range wording, carries
  `{NO_EXTERNAL_TOOLS}` ("Use only the evidence provided in this prompt...").
  Its tools list is empty upstream; data is pre-fetched into the prompt.
- Placeholders: `{ticker}`, `{start_date}`, `{end_date}`, `{news_block}`,
  `{stocktwits_block}`, `{reddit_block}`, `{subreddits}`, `{character}`.
- Limitation: social feeds are not archived; historical sentiment inputs are
  not point-in-time. State this on every historical sentiment read.

## Debate researchers

### Bull Researcher / Bear Researcher — `bull-researcher.md`, `bear-researcher.md`
- No preamble. Prompt is the complete prompt text.
- Placeholders: `{instrument_context}`, `{market_research_report}`,
  `{sentiment_report}`, `{news_report}`, `{fundamentals_label}`,
  `{fundamentals_report}`, `{history}`, `{current_response}` (opponent's
  last argument, or the "has not spoken yet" marker for the first speaker).
- No tools. Output: conversational argument engaging the opponent's claims.

## Risk debators — `risk-debator-{aggressive,conservative,neutral}.md`

- No preamble. Prompt is the complete prompt text.
- Placeholders: `{trader_decision}`, `{instrument_context}`,
  `{portfolio_context}`, the four analyst reports, `{history}`,
  `{current_aggressive_response}`, `{current_conservative_response}`,
  `{current_neutral_response}`.
- No tools. Output: conversational argument per stance.

## Trader — `trader.md`

- No preamble. System prompt + user-message template (both in the extracted
  file); the prompt below is the complete prompt text.
- Placeholders: `{grounding}` (the price-structure grounding instruction,
  included only when the market report has content), `{company_name}`,
  `{instrument_context}`, `{report_section}` (technical market report block),
  `{portfolio_context}`, `{investment_plan}`.
- No external tools. Output: **Action** (Buy/Hold/Sell; Overweight=Buy,
  Underweight=Sell), **Reasoning**, **Entry Price / Stop Loss / Position
  Sizing** as absolute price levels, never percentages.

## Managers

### Research Manager — `research-manager.md`
- No preamble. Prompt is the complete prompt text.
- Placeholders: `{instrument_context}`, `{history}`.
- No external tools. Output: **Recommendation** (5-point scale),
  **Rationale**, **Strategic Actions** sized against a standard allocation.
- Its investment plan is what the trader acts on.

### Portfolio Manager — `portfolio-manager.md`
- No preamble. Prompt is the complete prompt text.
- Placeholders: `{instrument_context}`, `{portfolio_context}`,
  `{research_plan}`, `{trader_plan}`, `{lessons_line}` (prior-decision
  lessons, or empty), `{history}` (risk-debate history).
- No external tools. Output: **Rating** (Buy/Overweight/Hold/Underweight/
  Sell) on its own first line, **Executive Summary**, **Investment Thesis**.
  Its rating is the run's final rating.

## Pipeline order (SPEC-001..004)

analysts (independent, timestamped) → bull/bear debate (mutually
referential) → research manager plan → trader proposal → risk debate →
portfolio approval → order preparation. Every handoff recorded; the
portfolio approval gates order preparation.
