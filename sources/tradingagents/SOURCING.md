# SOURCING — TauricResearch/TradingAgents (curated extraction)

- Source repo: https://github.com/TauricResearch/TradingAgents
- Commit fetched: `1394a3f72aa4393e1a98f51b382434c4b4c2d972` (2026-10-03)
- License: check upstream repo (see upstream LICENSE)
- Paper: https://arxiv.org/abs/2412.20138

## What was taken (domain content only)
- `agents/` — 12 role prompts extracted verbatim from the agent modules
  (4 analysts, 2 researchers, 3 risk debators, trader, 2 managers), with
  runtime interpolations shown as `{placeholders}`. Shared collaboration
  preamble included once.
- `tools.md` — inventory of the 12 agent tools: name, signature, one-line
  purpose. No API wiring, caching, or retry logic.
- `dataflows.md` — inventory of data vendors (Alpha Vantage, Yahoo, FRED,
  SEC EDGAR, Reddit, StockTwits, Polymarket): what each provides. No keys,
  endpoints, or fetch implementations.
- `backtest-methodology.md` — the evaluation contract: decision-quality
  scoring over (ticker, date) grids, decision settling, and the point-in-time
  discipline (date clamping, undated-item exclusion, coverage-gap labeling).

## Deliberately left behind
- LangGraph graph wiring (`tradingagents/graph/`) — the orchestration layer
  being replaced by the harness approach.
- CLI (`cli/`) — interactive setup, model selection, ticker parsing.
- Checkpointing / resume, Docker files, `default_config.py`.
- LLM client/provider registry (`llm_clients/`) — provider choice belongs to
  the harness layer.
- All fetch implementations, API keys, `.env` files (none were copied).

## Why this split
Per the approved plan: the durable value is the domain content (prompts,
tools, evaluation discipline); the framework scaffolding is commoditized and
is being replaced, not ported.
