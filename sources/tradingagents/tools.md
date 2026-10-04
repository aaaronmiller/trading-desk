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

## `get_prediction_markets(topic, limit, trade_date)`

Retrieve live, market-implied probabilities for forward-looking events from
