# Data-Vendor Cost & Rate-Limit Matrix

> Researched 2026-10-03 (PDT) from current docs and third-party comparisons.
> Pricing drifts; re-check before signing anything. "Free" means free to
> access, not free to redistribute. Covers the vendors the upstream
> TradingAgents inventory uses plus the venues the desk plans to add.

## Market data (prices, indicators, fundamentals)

| Vendor | Cost | Rate limit | Notes |
|---|---|---|---|
| **Alpha Vantage** | Free: 25 req/day (5/min). Paid: $49.99/mo (75 RPM) → $249.99/mo (1200 RPM); real-time US data from ~$99.99/mo | 25/day free; 75–1200 RPM paid, "no daily limits" on paid | NASDAQ-licensed; 50+ pre-computed technical indicators; fundamentals one symbol per call, no batch — S&P 500 statements refresh takes ~27 min at the $49.99 tier. Free tier non-viable for production |
| **Yahoo Finance (yfinance)** | Free, no key | Unofficial — throttled/429s under load, no published limits | Scraper, not an API: endpoints change/break frequently, quotes delayed, commercial use legally grey. Research and personal backtests only — never production |
| **FRED** (macro) | Free API key | 120 req/min (pace at 2/sec; FRED's own pages cite both 120/min and 2/sec) | 800k+ series; honors realtime vintages (point-in-time friendly). All users of an app must use their own key |
| **SEC EDGAR** (filings) | Free, no key | **10 req/s**, ten-minute block on breach; descriptive `User-Agent` (with contact) required or every request 403s | As-filed snapshots are inherently point-in-time. Parallelism buys nothing |
| **Alpaca market data** | Free Basic plan (IEX real-time); Algo Trader Plus **$99/mo** (full SIP + options, unlimited WS symbols, 10k historical req/min) | Trading API 200 req/min; historical data 10k/min on Plus | **Backtests on free IEX will not match live SIP execution** — IEX is a small fraction of consolidated volume. Historical from 2016 |
| **OANDA v20** (forex) | Free practice-account token; same API for live | Reported ~120 req/s | 70+ pairs, 19 timeframes (5s–1M), spread data included — good for realistic paper simulation |
| **Polymarket Gamma API** | Free, keyless public REST | No published limits (treat gently) | Read-only market data (events, prices, volume). US persons cannot trade Polymarket — data only |

## Sentiment / social

| Vendor | Cost | Rate limit | Notes |
|---|---|---|---|
| **Reddit** | Free tier 100 QPM per OAuth client (non-commercial); commercial ~$0.24/1k calls, enterprise from ~$12k/yr | 100 QPM free | Reddit's own help centre says academic research via the Data API is a policy violation — sanctioned route is Reddit For Researchers. Unauthenticated traffic blocked outright, not throttled. 1,000-post listing limit per subreddit |
| **StockTwits** | Free tier reported at 200 req/hour unauthenticated (400/hour with free app) | 200–400/hour | ~30 messages per ticker fetch. Note: developer docs path has been unreliable (redirects/404s observed); verify before building |
| **X / Twitter** | Pay-per-usage: $0.005 per post read, capped 3M reads/month, then Enterprise | Per usage | No free tier. Deriving/storing a user's "negative financial status" is prohibited; aggregate analysis without stored identifiers is the carve-out |

## Execution venues (paper paths)

| Venue | Paper path | Cost | Notes |
|---|---|---|---|
| **Alpaca** (stocks, crypto) | Free paper account; separate keys/hosts (`paper-api.alpaca.markets` vs `api.alpaca.markets`) | Commission-free live | ⚠️ Footgun: `alpaca-py` defaults to paper (safe); the **legacy `alpaca-trade-api` defaults to the LIVE host** unless `APCA_API_BASE_URL` is set. Never use the legacy library. Crypto orders support only `gtc`/`ioc`; fractional only `day` |
| **OANDA** (forex) | Free fxTrade Practice account | Spread-only cost; US leverage capped 50:1 (NFA) | Full v20 API on practice, real market prices |
| **Kalshi** (prediction markets) | Demo environment (separate keys from prod) | Fees ~1% of contract value; size must clear that | CFTC-regulated, USD; RSA-PSS request signing; demo book can be thin — use for order-path testing, not liquidity reads |

## Practical takeaways for this desk

1. **Free tiers don't compose into a production desk.** Alpha Vantage free (25/day) + Yahoo scraping + Reddit free (100 QPM) is fine for learning the extract play, not for running one.
2. **The two honest free workhorses are FRED and SEC EDGAR** — both keyless-ish, both point-in-time friendly. Build fundamentals and macro on these first.
3. **Budget realistically for phase 4+:** Alpha Vantage $50–100/mo OR Alpaca Algo Trader Plus $99/mo (not both to start); Kalshi fees sized into the strategy; Reddit commercial access is enterprise-priced — treat social sentiment as a backtest-only input unless the strategy justifies the spend.
4. **The upstream sentiment pipeline has an archival gap** (social feeds aren't archived; historical sentiment isn't point-in-time). Any vendor spend on social data should include an archiving plan, or the backtest discipline is theater for that feed.
5. **Re-verify before each phase** — this matrix is a snapshot (2026-10-03), not a contract.
