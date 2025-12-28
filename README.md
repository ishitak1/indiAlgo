# NSE/BSE Custom Strategy Backtester + Screener

A comprehensive platform for analyzing, screening, and backtesting trading strategies on NSE and BSE stocks and indices.

##  Enhanced Version Available!

**For Algorithm Builder and Comprehensive Screening features, use `app_enhanced.py`**

The enhanced version includes:
-  **Algorithm Builder**: Create custom screening algorithms with visual condition builder
-  **Comprehensive Stock Database**: Access all NSE/BSE listed companies
-  **Batch Screening**: Screen hundreds of stocks simultaneously
-  **Fundamental Data**: P/E, ROE, Debt/Equity, Growth metrics, etc.

See [README_ENHANCED.md](README_ENHANCED.md) for details.

## Features

### Phase 1 - Foundation 
- Fetch and store daily OHLCV data for NSE & BSE equities and indices
- Basic analytics: Returns, Moving Averages, RSI, MACD, Volatility, Drawdowns
- Interactive UI for selecting exchange, tickers, date ranges, and metrics

### Phase 2 - Custom Rule Engine 
- Define custom screening rules using Python expressions
- Examples:
  - `price > sma(50) and rsi < 40 and volume > 1000000`
  - `rsi < 30 and price > sma(200)`

### Phase 3 - Backtesting Engine 
- Test custom buy/sell strategies
- Performance metrics: CAGR, Sharpe Ratio, Max Drawdown, Win/Loss %
- Equity curve visualization

### Phase 4 - Advanced Features 
- Portfolio simulator
- Strategy comparison vs Nifty
- Export to Excel/CSV
- Save and load strategies

## Installation

```bash
pip install -r requirements.txt
```

Note: For ta-lib, you may need to install system dependencies:
- macOS: `brew install ta-lib`
- Linux: `sudo apt-get install ta-lib`
- Windows: Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

## Usage

```bash
streamlit run app.py
```

## Project Structure

```
nse_bse_backtester/
├── app.py                 # Main Streamlit application
├── data_fetcher.py        # Data fetching from NSE/BSE
├── data_storage.py        # Database operations
├── analytics.py           # Technical indicators and analytics
├── rule_engine.py         # Custom rule parser and evaluator
├── backtester.py          # Backtesting engine
├── portfolio.py           # Portfolio simulation
├── utils.py               # Utility functions
└── requirements.txt       # Dependencies
```

## Examples

### Custom Screening Rule
```
rsi(14) < 30 and close > sma(200) and volume > 1000000
```

### Backtesting Strategy
- Buy: RSI < 30 and Price > 200DMA
- Sell: RSI > 70 or Stop Loss 5%
- Position Size: 10% of capital
- Rebalancing: Weekly

