# Tool inventory — `tradingagents/agents/tools.py`

> Source: TauricResearch/TradingAgents @ 1394a3f72aa4393e1a98f51b382434c4b4c2d972
> One-line purpose + signature per tool. Implementation (API wiring,
> caching, retries) deliberately NOT included — reimplement against
> the harness's own tool layer.

## `get_stock_data(symbol, start_date, end_date, trade_date)`

Retrieve stock price data (OHLCV) for the instrument under analysis.

## `get_indicators(symbol, indicator, curr_date, look_back_days, trade_date)`

Retrieve a single technical indicator for the instrument under analysis.

## `get_verified_market_snapshot(symbol, curr_date, look_back_days, trade_date)`

Deterministic verification snapshot for exact market-data claims.

## `get_fundamentals(ticker, curr_date, trade_date)`

Retrieve comprehensive fundamental data for the instrument under analysis.

## `get_balance_sheet(ticker, freq, curr_date, trade_date)`

Retrieve balance sheet data for the instrument under analysis.

## `get_cashflow(ticker, freq, curr_date, trade_date)`

Retrieve cash flow statement data for the instrument under analysis.

## `get_income_statement(ticker, freq, curr_date, trade_date)`

Retrieve income statement data for the instrument under analysis.

## `get_news(ticker, start_date, end_date, trade_date)`

Retrieve news data for the instrument under analysis.

## `get_global_news(curr_date, look_back_days, limit, trade_date)`

Retrieve global news data.

## `get_insider_transactions(ticker, trade_date)`

Retrieve insider transaction information about a company.

## `get_macro_indicators(indicator, curr_date, look_back_days, trade_date)`

Retrieve a macroeconomic indicator time series from FRED (Federal Reserve
Economic Data): policy rates, Treasury yields, inflation, labor, and growth,
for the US and, through FRED's mirrored series, the euro area. Friendly
aliases accepted ('cpi', 'unemployment', 'fed_funds_rate', '10y_treasury',
'yield_curve', 'real_gdp', 'vix', euro-area aliases) as well as raw FRED
series IDs (e.g. 'CPIAUCSL'). Returns the series title, units, frequency,
latest value, change over the window, and a recent observation table.
Defaults to a 1-year trailing window when `look_back_days` is omitted.

## `get_prediction_markets(topic, limit, trade_date)`

Retrieve live, market-implied probabilities for forward-looking events from
prediction markets (Polymarket): Fed decisions, recession, elections,
geopolitics, crypto. Returns the most-traded open markets matching the
topic, each with its implied probability, traded volume, resolution date,
and recent move. Defaults to 6 markets when `limit` is omitted.
