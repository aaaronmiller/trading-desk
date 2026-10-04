# Venue Tool Interface Spec — DRAFT

> Status: draft design, written 2026-10-03 (PDT). Implements SPEC-019/020
> and the date-clamp contract from sources/tradingagents/backtest-methodology.md.
> No venue integration is built from this; it is the interface every future
> adapter must satisfy. Ratified intent/spec still gate the scaffold play.

## The clamp contract (every adapter, every dated read)

From the upstream evaluation discipline:

1. **Clamp**: any date or window the model asks for is clamped to the
   decision date (`as_of` / `as_of_window`). No tool ever reaches a vendor
   with a later date.
2. **Trim**: dated items (news, social posts) are trimmed to the analysis
   window; the upper bound is exclusive at midnight after `end`.
3. **Undated**: an undated item is kept only when the window reaches the
   present. A backtest cannot prove it isn't from the future.
4. **Gaps**: a window a feed cannot reach is reported as *unavailable*, never
   as *empty*. "None found" must not masquerade as a real absence over a
   window the feed never observed.
5. **Live profile withheld**: present-day snapshots (names, classifications)
   are withheld from historical runs — companies rename and get reclassified.
6. **Sentiment caveat**: social feeds (Reddit, StockTwits) are not archived;
   historical sentiment inputs are not point-in-time unless the harness
   archives its own feeds. State the limitation on every historical
   sentiment read.

## Common adapter interface

Every venue-class adapter implements:

- `history(instrument, start, end, decision_date)` — date-clamped historical
  reads; rules 1–5 apply.
- `snapshot(instrument, decision_date)` — deterministic point-in-time quote /
  state for settling decisions.
- `coverage(window)` — reports which windows the feed actually covers, so
  rule 4 can label the rest unavailable.
- `submit(order)` — routes to the **simulated venue by default**. A live
  path exists only if a human enabled it (SPEC-021), and every live order
  still requires a portfolio approval (SPEC-011). The live path is additive,
  never a flag flip.
- `health()` — venue reachability; an unreachable venue marks affected work
  `blocked-by-venue`, leaves positions flat, and never cascades (SPEC-020).
- `limits()` — the venue class's configured risk limits (per-position size,
  drawdown), so SPEC-015/016 can be enforced before any order.

## Per-class adapters

### Stocks — Alpaca (paper first)
- Same REST/WebSocket API for paper and live (paper-to-live fidelity per
  the proposed bar in docs/open-questions.md).
- Commission-free live; free basic data; 200 req/min. Fractional shares.
- Paper path: free paper account. Live: KYC, PDT rule hard-floors
  day-trading at $25k.

### Crypto — Alpaca (same account) or Kraken
- Alpaca paper covers crypto 24/7, same account as stocks.
- Kraken alternative: Pro tier fees (maker/taker) must be modeled in paper;
  fee math dominates small size.

### Forex — OANDA v20 (practice first)
- Free fxTrade Practice account with the full v20 REST API at real market
  prices; identical API for live.
- US = NFA-regulated, leverage capped 50:1.

### Prediction markets — Kalshi (demo first); Polymarket read-only
- Kalshi: CFTC-regulated, USD; demo endpoint for paper; REST with RSA
  signing (~10 req/s; limit and market orders only). KYC required for live.
- Polymarket: US persons are geoblocked from trading. Polymarket serves the
  desk only as a **read-only prediction-data feed** (market-implied
  probabilities, volume, resolution dates), never as an execution venue.
  Polymarket US: track for future access, do not plan on it.

## Order record (all venues)

Every order record carries: venue, class, instrument, side, quantity/size,
limit or market, the portfolio approval it links to (SPEC-004), the venue's
response (fill, partial fill, rejection with reason), and whether it was
simulated or live. No order is prepared without the approval link; no order
is submitted live without the enabled flag plus the approval.
