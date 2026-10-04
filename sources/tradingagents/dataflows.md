# Data-vendor inventory — `tradingagents/dataflows/vendors/`

> Source: TauricResearch/TradingAgents @ 1394a3f72aa4393e1a98f51b382434c4b4c2d972
> What each vendor module provides. API keys, endpoints, and fetch
> implementations deliberately NOT included.
>
> The point-in-time discipline lives one level up, in
> `tradingagents/dataflows/date_window.py` (`as_of`, `as_of_window`,
> `in_window`, `coverage_gap`, `withhold_live_profile`) and is enforced by
> the vendor modules and the router (`router.py` selects the configured
> vendor per category; `config.py` picks which vendor serves each category).

## `alpha_vantage/`
One module per category, aggregated by `__init__.py`:
- `stock.py` — OHLCV price data
- `indicator.py` — technical indicators
- `fundamentals.py` — company fundamentals and statements
- `news.py` — news feed and insider transactions
- `common.py` — shared request plumbing

## `yahoo/`
One module per category, aggregated by `__init__.py`:
- `ohlcv.py` — OHLCV price data
- `market.py` — market data / indicators
- `fundamentals.py` — company profile, statements, insider filings
- `news.py` — news
- `snapshot.py` — deterministic verification snapshot for exact market-data
  claims (backs the `get_verified_market_snapshot` tool)
- `common.py` — shared request plumbing

## `fred.py`
FRED (Federal Reserve Economic Data) macro vendor. Honors FRED's
realtime-date semantics: the vintage pin is clamped to the as-of date so a
historical run reads the series as it was known then.

## `sec_edgar.py`
Company statements as they were filed, from SEC EDGAR — as-filed snapshots
are inherently point-in-time.

## `polymarket.py`
Polymarket prediction-market vendor: open markets matching a topic, with
implied probabilities, volume, resolution dates, and recent moves.

## `reddit.py`
Reddit search fetcher for ticker-specific discussion posts, with
per-instrument subreddit selection (`subreddits_for`) and crypto-community
variants; supports Jev screening of fetched posts.

## `stocktwits.py`
StockTwits public symbol-stream fetcher (Bullish/Bearish-tagged messages),
trimmed to the analysis window.

## Notable upstream behavior captured for the harness rebuild
- Social feeds (Reddit, StockTwits) serve recent items and are not archived:
  historical sentiment inputs are NOT point-in-time upstream — see the
  sentiment analyst's module notes. A harness that backtests sentiment must
  either accept this limitation or archive its own feeds.
- Coverage gaps are reported as unavailable, never as empty (see
  backtest-methodology.md).
