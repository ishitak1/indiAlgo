# Enhanced NSE/BSE Algorithm Builder & Stock Screener

## 🚀 Overview

This is an enhanced version of the NSE/BSE backtester with comprehensive algorithm building capabilities. Users can create custom algorithms to screen all publicly listed companies on NSE and BSE.

## ✨ Key Features

### 1. Algorithm Builder
- **Visual Condition Builder**: Create algorithms using a user-friendly interface
- **Technical Indicators**: RSI, MACD, Moving Averages, Bollinger Bands, Volume
- **Fundamental Metrics**: P/E, P/B, ROE, Debt/Equity, Growth rates, etc.
- **Save & Reuse**: Save algorithms for future use
- **Templates**: Pre-built algorithm templates for common strategies

### 2. Comprehensive Stock Database
- **All Listed Companies**: Access to all NSE and BSE listed stocks
- **Search & Filter**: By exchange, sector, market cap
- **Fundamental Data**: P/E ratios, ROE, growth metrics, etc.
- **Export**: Download stock lists as CSV

### 3. Comprehensive Screener
- **Batch Processing**: Screen hundreds of stocks simultaneously
- **Progress Tracking**: Real-time progress updates
- **Multiple Filters**: By sector, market cap, exchange
- **Results Export**: Download screening results

### 4. Enhanced Analytics
- **Technical Analysis**: Full suite of technical indicators
- **Fundamental Analysis**: Valuation, profitability, growth metrics
- **Performance Metrics**: Returns, volatility, drawdowns, Sharpe ratio

## 📋 Available Factors

### Technical Indicators
- **Moving Averages**: `sma(5)`, `sma(20)`, `sma(50)`, `sma(200)`, `ema(20)`, etc.
- **Momentum**: `rsi(14)`, `macd()`
- **Volatility**: Bollinger Bands, ATR
- **Volume**: `volume`, `volume_sma(20)`
- **Price**: `price`, `close`, `open`, `high`, `low`

### Fundamental Metrics
- **Valuation**: `pe_ratio`, `price_to_book`, `price_to_sales`, `peg_ratio`
- **Profitability**: `roe`, `roa`, `profit_margin`, `operating_margin`
- **Financial Health**: `debt_to_equity`, `current_ratio`, `quick_ratio`
- **Growth**: `revenue_growth`, `earnings_growth`
- **Dividends**: `dividend_yield`, `payout_ratio`
- **Size**: `market_cap`

## 🎯 Usage Examples

### Example 1: Value Stock Algorithm
```
Conditions:
- pe_ratio < 20
- roe > 15
- debt_to_equity < 1.0
```

### Example 2: Growth Stock Algorithm
```
Conditions:
- revenue_growth > 20
- earnings_growth > 15
- roe > 20
```

### Example 3: Technical Momentum Algorithm
```
Conditions:
- rsi(14) < 30
- price > sma(200)
- volume > 1000000
```

## 🏃 Quick Start

### 1. Run Enhanced App
```bash
streamlit run app_enhanced.py
```

### 2. Create Algorithm
1. Go to **Algorithm Builder**
2. Click **Create Algorithm** tab
3. Enter algorithm name and description
4. Add conditions (field, operator, value)
5. Click **Save Algorithm**

### 3. Screen Stocks
1. Go to **Comprehensive Screener**
2. Select your algorithm
3. Choose exchange, sectors, filters
4. Click **Run Comprehensive Screen**
5. View and download results

### 4. Browse Database
1. Go to **Stock Database**
2. Filter by exchange, sector, market cap
3. Search by name or symbol
4. View and download stock lists

## 📁 Project Structure

```
nse_bse_backtester/
├── app_enhanced.py              # Enhanced main application
├── algorithm_builder.py         # Algorithm creation and management
├── stock_list_fetcher.py        # Fetch all NSE/BSE stocks
├── fundamental_data.py          # Fundamental data fetching
├── comprehensive_screener.py    # Batch stock screening
├── data_fetcher.py              # Historical price data
├── analytics.py                 # Technical indicators
├── rule_engine.py               # Rule evaluation
├── backtester.py                # Strategy backtesting
└── requirements.txt             # Dependencies
```

## 🔧 Technical Details

### Algorithm Structure
Algorithms are stored as JSON with:
- Name and description
- Type (screener/strategy)
- List of conditions
- Metadata (created date, etc.)

### Condition Format
```json
{
  "field": "pe_ratio",
  "operator": "<",
  "value": 20,
  "logical_operator": "AND"
}
```

### Screening Process
1. Fetch stock list (filtered by exchange/sector)
2. For each stock:
   - Fetch price data (if technical conditions)
   - Fetch fundamental data (if fundamental conditions)
   - Compute technical indicators
   - Evaluate algorithm conditions
   - Store if matches
3. Return results as DataFrame

## 📊 Performance Considerations

- **Rate Limiting**: Built-in delays to respect API limits
- **Caching**: Stock data cached to avoid redundant fetches
- **Batch Processing**: Process stocks in batches
- **Progress Tracking**: Real-time progress updates

## 🎨 UI Features

- **Multi-page Navigation**: Organized by functionality
- **Interactive Forms**: Easy algorithm creation
- **Real-time Preview**: See algorithm expression
- **Results Visualization**: Tables and metrics
- **Export Options**: CSV/Excel downloads

## 🔮 Future Enhancements

- Algorithm marketplace/sharing
- Performance tracking for algorithms
- Backtesting with algorithms
- Portfolio optimization
- Real-time alerts
- API access

## 📝 Notes

- Fundamental data depends on yfinance availability
- Some stocks may not have complete fundamental data
- Screening large numbers of stocks takes time
- Use filters to reduce processing time

## 🐛 Troubleshooting

**Issue**: No fundamental data
- **Solution**: Some stocks may not have fundamental data in yfinance. Try different stocks.

**Issue**: Screening takes too long
- **Solution**: Use filters (sector, market cap) or reduce max_stocks parameter.

**Issue**: Algorithm not matching stocks
- **Solution**: Check condition values are reasonable. Some metrics may be None for some stocks.



