# indiAlgo 📊

**Professional Indian Stock Market Analysis & Strategy Platform**

indiAlgo is a comprehensive platform for analyzing NSE/BSE stocks, testing trading strategies, managing portfolios, and learning about markets. Built for students, traders, and analysts.

---

## ✨ Features

### 🎯 Core Modules

1. **📊 Stock Analyzer**
   - Multi-year historical data (up to 10 years)
   - Technical indicators (RSI, MACD, Moving Averages, etc.)
   - Fundamental analysis (P/E, ROE, Growth metrics)
   - Interactive charts and visualizations

2. **🔍 Stock Screener**
   - Screen 2000+ NSE/BSE stocks
   - Custom algorithm builder
   - Filter by sector, market cap, exchange
   - Export results

3. **🧪 Strategy Backtester**
   - Test custom buy/sell strategies
   - Realistic assumptions (slippage, commission)
   - Comprehensive metrics (CAGR, Sharpe, Drawdown)
   - Benchmark comparison

4. **💼 Portfolio Manager**
   - Multiple portfolio support
   - Real-time P&L tracking
   - Risk analytics (volatility, correlation)
   - Sector allocation
   - Benchmark comparison

5. **📈 Paper Trading**
   - Virtual trading with ₹1,00,000
   - Market, Limit, Stop orders
   - Trade history & journal
   - Performance dashboard
   - Daily summaries

6. **🤖 AI Mentor**
   - Educational chatbot
   - Explains indicators & concepts
   - Helps interpret results
   - Student-friendly guidance

7. **📚 Learning Resources**
   - Indicator guides
   - Strategy templates
   - Risk management education
   - Best practices

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/indialgo.git
cd indialgo

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run indialgo_app.py
```

### First Run

1. Application opens at `http://localhost:8501`
2. Start with **Home** page for overview
3. Try **Stock Analyzer** to analyze a stock
4. Use **AI Mentor** for learning
5. Practice with **Paper Trading**

---

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for full list

### System Dependencies (for ta-lib)

**macOS:**
```bash
brew install ta-lib
```

**Linux:**
```bash
sudo apt-get install ta-lib
```

**Windows:**
Download from [ta-lib website](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)

---

## 🎓 For Students

### Learning Path

1. **Week 1**: Basics - Analyze stocks, understand charts
2. **Week 2**: Indicators - Learn RSI, MACD, Moving Averages
3. **Week 3**: Screening - Find stocks matching criteria
4. **Week 4**: Backtesting - Test trading strategies
5. **Week 5**: Portfolio - Manage multiple stocks
6. **Week 6**: Practice - Paper trading

### Features for Learning

- ✅ Friendly, non-intimidating UI
- ✅ Clear explanations and tooltips
- ✅ Preset strategies and templates
- ✅ AI Mentor for guidance
- ✅ Paper trading for practice
- ✅ Educational disclaimers

---

## 💎 Free vs Premium

### Free Tier
- ✅ 10 backtests per month
- ✅ CSV export
- ✅ Historical data (delayed)
- ✅ Community support
- ✅ Basic features

### Premium Tier (₹999/month)
- ✅ Unlimited backtests
- ✅ All export formats (CSV, Excel, PDF, JSON)
- ✅ Real-time data
- ✅ Priority support
- ✅ Custom indicators
- ✅ API access
- ✅ Strategy sharing

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy automatically
4. Access via `your-app.streamlit.app`

### Option 2: Heroku
```bash
heroku create indialgo-app
git push heroku main
```

### Option 3: AWS/GCP/Azure
- Deploy on cloud server
- Use Docker
- Configure Nginx reverse proxy
- Add SSL certificate

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions**

---

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user manual
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide

---

## 🏗️ Architecture

```
indialgo/
├── indialgo_app.py          # Main application
├── config.py                # Configuration
├── data_manager.py          # Data management & caching
├── analytics.py             # Technical indicators
├── advanced_backtester.py    # Backtesting engine
├── portfolio_manager.py     # Portfolio management
├── paper_trading.py         # Paper trading system
├── ai_mentor.py             # AI chatbot
├── strategy_manager.py      # Strategy management
├── stock_grouper.py         # Stock grouping
├── fundamental_data.py      # Fundamental analysis
└── premium_features.py      # Premium features
```

---

## 🔧 Configuration

Edit `config.py` for:
- Default settings
- API keys
- Database paths
- Feature flags

---

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: Not financial advice
- **Past Performance**: Doesn't guarantee future results
- **Risk Warning**: Trading involves risk of loss
- **Do Your Research**: Always verify information
- **Consult Advisors**: Seek professional financial advice

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

- **Documentation**: Check guides in repository
- **AI Mentor**: Ask questions in-app
- **GitHub Issues**: Report bugs
- **Email**: support@indialgo.com (if configured)

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- Built with Streamlit
- Data from yfinance
- Technical indicators from ta-lib
- Visualization with Plotly

---

## 🎯 Roadmap

- [ ] Real-time data integration
- [ ] Mobile app
- [ ] Advanced AI features
- [ ] Community features
- [ ] More exchanges
- [ ] Options trading support

---

**Made with ❤️ for the Indian Stock Market Community**

**Start Learning. Start Trading. Start Growing. 📈**

