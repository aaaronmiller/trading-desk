# Backtest methodology — extracted from TradingAgents

> Source: TauricResearch/TradingAgents @ 1394a3f72aa4393e1a98f51b382434c4b4c2d972
> (`tradingagents/backtest.py`, `tradingagents/dataflows/date_window.py`,
> decision-settling in the memory log). Methodology only — no graph code.

## What a backtest is here
One run yields one decision, which says nothing about decision quality. The
backtest runs the same machinery over a grid of (ticker, date) cells and reads
the aggregate. It evaluates **decision quality, not portfolio performance**:
it is explicitly not a portfolio simulator — turning a rating into a filled
order would need quantity, fill price, and a cash ledger, and inventing those
would smuggle an execution model into an evaluation tool. Cells are
independent; a supplied portfolio is the same standing book for every cell,
never a position carried forward.

## Settling
Every run records its rating; the memory log later settles each decision with
realized return and alpha return against the instrument's regional benchmark.
The backtest reads the settled log — there is nothing to record separately.

## Point-in-time discipline (the part worth stealing)
All dated paths serve data **as of the run's date**:

- `as_of` / `as_of_window`: any date or window the model asks for is clamped
  to the trade date, so no tool ever reaches a vendor with a later date.
- `in_window`: dated items (news, social posts) are trimmed to the analysis
  window; timestamps normalized to UTC; the upper bound exclusive at midnight
  after `end`. An **undated item is kept only when the window reaches the
  present** — a backtest cannot prove it isn't from the future.
- `coverage_gap`: a window a feed cannot reach is reported as *unavailable*,
  never as *empty*. Feeds that only serve recent items must not let "none
  found" masquerade as a real absence over a window they never observed.
- `withhold_live_profile`: present-day company snapshots (names,
  classifications) are withheld from historical runs — companies rename and
  get reclassified.

## Grid rules
- Analysis dates run from start date up to today; a future date has no outcome
  to settle against, so the grid stops at the present.
- Date bounds are validated strictly (YYYY-MM-DD).

## What this means for the harness rebuild
The evaluation contract to preserve: every data access is date-clamped to the
decision date; undated content is excluded from historical runs; feed coverage
gaps are labeled, not zero-filled; decisions settle against realized + alpha
return later. This discipline is framework-agnostic — it is a set of rules any
tool layer can enforce.
