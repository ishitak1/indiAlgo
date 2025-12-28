# Setup Instructions

## Prerequisites

1. Python 3.8 or higher
2. pip package manager

## Installation Steps

### 1. Install System Dependencies (for ta-lib)

#### macOS
```bash
brew install ta-lib
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ta-lib
```

#### Windows
Download the ta-lib installer from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
Or use conda:
```bash
conda install -c conda-forge ta-lib
```

### 2. Install Python Dependencies

```bash
cd nse_bse_backtester
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Troubleshooting

### ta-lib Installation Issues

If you encounter issues with ta-lib installation:

1. **macOS**: Make sure you have Xcode command line tools installed:
   ```bash
   xcode-select --install
   ```

2. **Alternative**: You can comment out ta-lib specific imports and use the `ta` library instead, which is a pure Python implementation.

### Data Fetching Issues

- If yfinance fails to fetch data, try:
  - Checking your internet connection
  - Using different symbols
  - Trying again after a few minutes (rate limiting)

### Database Issues

- The SQLite database (`stock_data.db`) will be created automatically
- If you encounter database errors, delete `stock_data.db` and restart the app

## Usage Examples

### Example 1: Fetch and Analyze Data

1. Go to "Data & Analytics" page
2. Select exchange (NSE or BSE)
3. Enter symbol (e.g., "RELIANCE")
4. Select date range
5. Click "Fetch Data"
6. View analytics and charts

### Example 2: Screen Stocks

1. Go to "Screener" page
2. Enter multiple symbols (one per line)
3. Enter a screening rule, e.g.:
   ```
   rsi(14) < 30 and price > sma(200)
   ```
4. Click "Run Screener"
5. View matching stocks

### Example 3: Backtest Strategy

1. Go to "Backtester" page
2. Select loaded data
3. Enter buy rule: `rsi(14) < 30 and price > sma(200)`
4. Enter sell rule: `rsi(14) > 70`
5. Set parameters (capital, position size, stop loss, etc.)
6. Click "Run Backtest"
7. View performance metrics and equity curve

## Custom Rule Syntax

The rule engine supports Python-like expressions:

- **Functions**: `sma(50)`, `ema(20)`, `rsi(14)`, `macd()`, `volatility(20)`
- **Price data**: `price`, `close`, `open`, `high`, `low`, `volume`
- **Operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`, `and`, `or`, `not`
- **Numbers**: Direct numeric values

### Examples:
```
rsi(14) < 30 and price > sma(200)
close > sma(50) and volume > 1000000
rsi < 40 and price > sma(200) and volume > sma(20)
```

## Notes

- Data is fetched from yfinance, which may have rate limits
- Historical data availability depends on the symbol and exchange
- Backtesting results are for educational purposes only
- Always verify data accuracy before making trading decisions



