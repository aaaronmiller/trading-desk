# Trading Desk — draft answers to the three open questions
_Prepared 2026-10-03 (PDT) for Aaron to react to, not as decisions. Nothing here is ratified. Venue facts re-verified against current sources on 2026-10-03; Polymarket-US access status should be re-checked before any plan depends on it._

## Q1. Quantitative paper-to-live bar (proposal)

A strategy earns live capital only when ALL of these hold:

1. **Sample size**: >= 200 closed paper trades per strategy/venue, over >= 4 weeks (so it survives more than one regime).
2. **Edge**: positive expectancy net of ALL costs (commissions, spreads, fees, regulatory fees). For prediction markets, positive closing-line value (CLV) over >= 200 markets — judge by CLV, not backtest ROI.
3. **Risk**: annualized Sharpe >= 1.0 on daily paper PnL; max drawdown < 15% of allocated capital; no single-day loss > 5% of allocation.
4. **Out-of-sample**: parameters frozen before a 30% holdout window; holdout performance must retain >= 60% of in-sample expectancy (guards against overfit).
5. **Paper-to-live fidelity**: paper venue must be the SAME API as live (Alpaca paper -> Alpaca live; OANDA practice -> OANDA live; Kalshi demo -> Kalshi live). No switching venues at go-live.
6. **Operational**: kill switch tested, daily loss limit enforced in code, broker fills match backtest slippage assumptions within 2x.

Then: start live at 25-50% of the venue's allocated capital ("probation"), full size after 100 live trades confirm paper edge.

## Q2 + Q3. Venue shortlist with paper paths and starting capital

| Venue class | Venue | Paper path | Notes |
|---|---|---|---|
| Stocks | **Alpaca** | Free paper account, same REST/WebSocket API as live | Commission-free live; free basic data (IEX real-time, SIP delayed 15 min); options now supported; 200 req/min. Fractional shares. |
| Crypto | **Alpaca** (same account) or **Kraken** | Alpaca paper covers crypto 24/7 | Kraken Pro entry tier 0.40% maker / 0.80% taker — a market-order round trip costs ~1.6% before slippage, kills small-size scalping; prefer Alpaca or limit/post-only on Kraken. |
| Forex | **OANDA** | Free fxTrade Practice account, full v20 REST API, real market prices | US = NFA-regulated, leverage capped 50:1. v20 API free with practice account; same API for live. |
| Prediction markets | **Kalshi** | Kalshi demo environment (paper; canonical host `external-api.demo.kalshi.co`, legacy `demo-api.kalshi.co` still supported) | CFTC-regulated, USD, REST v2 API with RSA-PSS request signing (rate-limited, tiered). Demo and prod are separate envs with separate API keys; one report notes the demo book can be thin — use it for order-path testing, not liquidity reads. KYC required for live. Polymarket global CLOB API is real (py-clob-client-v2, EIP-712, deposit-wallet flow) but US persons are geoblocked from trading it — treat Polymarket as READ-ONLY data, not a venue. Polymarket US (api.polymarket.us) launched with programmatic access but retail onboarding was waitlist-gated in the millions as of April 2026 — track, don't plan on it. |

**Starting capital proposal** (per venue, live probation size):
- Stocks (Alpaca): $25k if day-trading (PDT rule hard-floors it), else $5-10k swing. Commissions are $0 so size can start small.
- Crypto: $2-5k — fee math dominates below that.
- Forex (OANDA): $1-2k in micro lots; leverage is the risk, not the capital.
- Prediction markets (Kalshi): $2-5k; fees run ~1% of contract value, so size must clear that.

**Latency note** (he flagged faster connections may be warranted): Alpaca, OANDA, and Kalshi are REST/WS retail APIs — none needs colocation for paper or early live. If any strategy's edge depends on sub-100ms fills (market-making, cross-venue arb), that strategy fails the fidelity bar until it runs on a VPS near the venue (NY4/NY5 for US equities/forex) — make that a per-strategy requirement, not a day-one spend. Hetzner VPS (already recommended for the desk) is fine for start; FOREX.com FIX / IBKR only if a strategy proves latency-sensitive.

## What still needs Aaron (decision, not research)
- Ratify or rewrite the paper-to-live bar numbers above.
- Starting capital per venue class (his risk call).
- Which venues he actually has accounts at / will open (Alpaca KYC, OANDA practice, Kalshi KYC are all user-side actions).
