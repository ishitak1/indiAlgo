# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
# Install system dependencies for ta-lib (macOS)
brew install ta-lib

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
streamlit run app.py
```

Or use the convenience script:
```bash
./run.sh
```

### Step 3: Open in Browser

The app will automatically open at `http://localhost:8501`

## 📖 Basic Workflow

### 1. Fetch Stock Data
- Go to **"Data & Analytics"** page
- Select **Exchange**: NSE or BSE
- Enter **Symbol**: e.g., "RELIANCE", "TCS", "HDFCBANK"
- Choose **Date Range** or **Period**
- Click **"Fetch Data"**
- View analytics, charts, and indicators

### 2. Screen Stocks
- Go to **"Screener"** page
- Enter multiple symbols (one per line)
- Enter a **Screening Rule**, e.g.:
  ```
  rsi(14) < 30 and price > sma(200)
  ```
- Click **"Run Screener"**
- View matching stocks

### 3. Backtest Strategy
- Go to **"Backtester"** page
- Select loaded data
- Enter **Buy Rule**: `rsi(14) < 30 and price > sma(200)`
- Enter **Sell Rule**: `rsi(14) > 70`
- Set parameters:
  - Initial Capital: ₹100,000
  - Position Size: 100% of capital
  - Stop Loss: 5%
  - Max Holding Period: 30 days
- Click **"Run Backtest"**
- View performance metrics and equity curve

## 💡 Example Rules

### Screening Rules
```
# Oversold stocks above 200-day MA
rsi(14) < 30 and price > sma(200)

# High volume breakouts
close > sma(50) and volume > 1000000

# Multiple conditions
rsi < 40 and price > sma(200) and volume > sma(20)
```

### Strategy Rules
```
# Buy: Oversold with trend confirmation
Buy: rsi(14) < 30 and price > sma(200)
Sell: rsi(14) > 70

# Buy: MACD crossover
Buy: macd() > macd_signal() and macd() > 0
Sell: macd() < macd_signal()
```

## 📊 Available Indicators

- **Moving Averages**: `sma(5)`, `sma(20)`, `sma(50)`, `sma(200)`, `ema(20)`, etc.
- **Momentum**: `rsi(14)`, `macd()`
- **Price**: `price`, `close`, `open`, `high`, `low`
- **Volume**: `volume`
- **Volatility**: `volatility(20)`

## 🎯 Tips

1. **Start Simple**: Begin with basic rules like `rsi(14) < 30`
2. **Test Multiple Symbols**: Try your strategy on different stocks
3. **Adjust Parameters**: Experiment with stop loss, position size, etc.
4. **Compare Results**: Use different date ranges to see strategy robustness
5. **Check Win Rate**: Aim for strategies with >50% win rate and good profit factor

## ⚠️ Important Notes

- Data is fetched from yfinance (may have rate limits)
- Backtesting results are for educational purposes only
- Past performance doesn't guarantee future results
- Always verify data accuracy before trading
- Consider transaction costs and slippage in real trading

## 🐛 Troubleshooting

**Issue**: ta-lib installation fails
- **Solution**: Use conda or install from source (see SETUP.md)

**Issue**: No data fetched
- **Solution**: Check internet connection, try different symbols, wait a few minutes (rate limiting)

**Issue**: Rule evaluation error
- **Solution**: Check rule syntax, ensure indicators are computed first

## 📚 Next Steps

- Read the full documentation in `README.md`
- Check `SETUP.md` for detailed installation instructions
- Run `example_usage.py` to see programmatic usage
- Explore all features in the Streamlit app

Happy Backtesting! 📈



