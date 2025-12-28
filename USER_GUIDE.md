# indiAlgo - User Guide

## 📖 How to Use indiAlgo

### Getting Started

1. **Launch the Application**
   ```bash
   streamlit run indialgo_app.py
   ```
   Or access via web URL if deployed.

2. **First Time Setup**
   - No registration required for free tier
   - Premium features require subscription
   - Data is cached locally for faster access

---

## 🏠 Home Page

- Overview of platform features
- Quick access to all modules
- Feature comparison (Free vs Premium)

---

## 📊 Stock Analyzer

### Analyze a Stock:

1. Select **Exchange** (NSE or BSE)
2. Enter **Stock Symbol** (e.g., RELIANCE, TCS)
3. Choose **Years of History** (1-10 years)
4. Toggle **Fundamental Data** if needed
5. Click **"Analyze Stock"**

### What You Get:

- **Price Chart** with candlesticks
- **Technical Indicators**: RSI, MACD, Moving Averages
- **Performance Metrics**: Returns, CAGR, Sharpe Ratio
- **Fundamental Data**: P/E, ROE, Market Cap (if available)
- **52-Week High/Low**

---

## 🔍 Stock Screener

### Screen Stocks:

1. **Create/Select Algorithm**
   - Use preset algorithms or create custom
   - Define conditions (e.g., RSI < 30, P/E < 20)

2. **Set Filters**
   - Exchange (NSE/BSE)
   - Sectors (Banking, IT, etc.)
   - Market Cap (Large/Mid/Small)

3. **Run Screener**
   - Process multiple stocks
   - View matching results
   - Export to CSV

### Example Algorithms:

- **Value Stocks**: P/E < 20, ROE > 15, Debt/Equity < 1
- **Growth Stocks**: Revenue Growth > 20%, Earnings Growth > 15%
- **Oversold**: RSI < 30, Price > 200DMA

---

## 🧪 Strategy Backtester

### Backtest a Strategy:

1. **Select Stock Data**
   - Choose from loaded data or fetch new

2. **Define Strategy**
   - **Buy Rule**: When to enter (e.g., RSI < 30)
   - **Sell Rule**: When to exit (e.g., RSI > 70)

3. **Set Parameters**
   - Initial Capital
   - Position Size (% of capital)
   - Stop Loss (%)
   - Take Profit (%)
   - Max Holding Period

4. **Run Backtest**
   - View performance metrics
   - Analyze equity curve
   - Review trade history

### Key Metrics Explained:

- **CAGR**: Annualized return
- **Sharpe Ratio**: Risk-adjusted return (>1 is good)
- **Max Drawdown**: Worst loss from peak
- **Win Rate**: % of profitable trades
- **Profit Factor**: Gross profit / Gross loss

---

## 💼 Portfolio Manager

### Create Portfolio:

1. Click **"Create New Portfolio"**
2. Enter name and initial capital
3. Select benchmark (NIFTY 50, etc.)

### Add Positions:

1. Select portfolio
2. Enter symbol, shares, price
3. Click **"Add Position"**

### View Analytics:

- **Portfolio Value**: Current total value
- **P&L**: Realized and Unrealized
- **Sector Allocation**: Visual breakdown
- **Risk Metrics**: Volatility, Sharpe, Correlation
- **Benchmark Comparison**: vs NIFTY

---

## 📈 Paper Trading

### Start Trading:

1. **Get Virtual Account**
   - Default: ₹1,00,000 virtual money
   - Practice without risk

2. **Place Orders**
   - **Market Order**: Execute immediately
   - **Limit Order**: Execute at specific price
   - **Stop Order**: Execute when price hits level

3. **Track Performance**
   - View account summary
   - Check trade history
   - Daily P&L summary
   - Trading journal

### Order Types:

- **BUY Market**: Buy at current price
- **SELL Market**: Sell at current price
- **BUY Limit**: Buy when price drops to limit
- **SELL Limit**: Sell when price rises to limit
- **BUY Stop**: Buy when price breaks above stop
- **SELL Stop**: Sell when price breaks below stop

---

## 🤖 AI Mentor

### Ask Questions:

1. Type your question in the chat
2. Get educational explanations
3. Follow suggested questions

### What AI Mentor Can Help With:

- **Indicators**: RSI, MACD, Moving Averages
- **Backtest Results**: Understanding metrics
- **Risk Management**: Diversification, volatility
- **Trading Concepts**: Strategies, patterns
- **Portfolio Management**: Allocation, rebalancing

### Example Questions:

- "Explain RSI indicator"
- "What is a good Sharpe ratio?"
- "How to read backtest results?"
- "Explain portfolio diversification"

---

## 📚 Learn & Guides

### Educational Content:

- **Indicator Guides**: How to use each indicator
- **Strategy Templates**: Pre-built strategies
- **Risk Management**: Understanding risk
- **Best Practices**: Trading tips
- **Glossary**: Trading terminology

---

## ⚙️ Settings

### Configure:

- **User Preferences**: Theme, default settings
- **Data Sources**: API keys, data refresh
- **Notifications**: Alerts, updates
- **Account**: Tier, subscription

---

## 💡 Tips for Best Experience

### Performance:

- Use caching for frequently accessed data
- Filter stocks by sector to reduce processing time
- Start with smaller date ranges for faster analysis

### Accuracy:

- Verify data sources
- Check for corporate actions (splits, dividends)
- Use realistic assumptions in backtesting

### Learning:

- Start with preset strategies
- Use AI Mentor for explanations
- Practice with Paper Trading
- Review backtest results carefully

---

## 🆘 Troubleshooting

### Data Not Loading:

1. Check internet connection
2. Verify symbol is correct
3. Try different exchange
4. Check if market is open

### Slow Performance:

1. Reduce date range
2. Filter stocks before screening
3. Clear cache if needed
4. Use premium tier for faster processing

### Errors:

1. Check error message
2. Verify inputs are correct
3. Try refreshing page
4. Contact support if persistent

---

## 📞 Support

- **Documentation**: Check this guide
- **AI Mentor**: Ask questions
- **GitHub Issues**: Report bugs
- **Email**: support@indialgo.com (if configured)

---

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: Not financial advice
- **Past Performance**: Doesn't guarantee future results
- **Risk Warning**: Trading involves risk
- **Do Your Research**: Always verify information
- **Consult Advisors**: Seek professional advice

---

## 🎓 For Students

### Learning Path:

1. **Week 1**: Learn basics (Home, Stock Analyzer)
2. **Week 2**: Understand indicators (AI Mentor)
3. **Week 3**: Practice screening (Stock Screener)
4. **Week 4**: Test strategies (Backtester)
5. **Week 5**: Manage portfolio (Portfolio Manager)
6. **Week 6**: Paper trading (Practice)

### Assignments:

- Analyze 5 stocks from different sectors
- Create and test 3 different strategies
- Build a diversified portfolio
- Paper trade for 1 month
- Write trading journal

---

**Happy Learning! 📊📈**

