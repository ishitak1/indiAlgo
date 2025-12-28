# Quick Start - Enhanced Version

## 🚀 Run the Enhanced App

```bash
streamlit run app_enhanced.py
```

## 📋 Step-by-Step Guide

### Step 1: Create Your First Algorithm

1. Open the app and go to **"🔧 Algorithm Builder"**
2. Click on **"Create Algorithm"** tab
3. Enter:
   - **Name**: "Value Stocks Finder"
   - **Type**: Screener
   - **Description**: "Find undervalued stocks with good fundamentals"
4. Add conditions:
   - **Condition 1**: 
     - Field: `pe_ratio`
     - Operator: `<`
     - Value: `20`
   - **Condition 2**:
     - Field: `roe`
     - Operator: `>`
     - Value: `15`
   - **Condition 3**:
     - Field: `debt_to_equity`
     - Operator: `<`
     - Value: `1.0`
5. Click **"💾 Save Algorithm"**

### Step 2: Browse Stock Database

1. Go to **"📊 Stock Database"**
2. Select:
   - Exchange: NSE
   - Sector: All (or specific sector)
   - Market Cap: All
3. Click **"Load Stock Database"**
4. Browse or search stocks
5. Download as CSV if needed

### Step 3: Run Comprehensive Screening

1. Go to **"🔍 Comprehensive Screener"**
2. Select your algorithm: "Value Stocks Finder"
3. Set options:
   - Exchange: NSE
   - Sectors: (Optional - leave empty for all)
   - Market Cap: Large Cap (optional)
   - Max Stocks: 100 (start small for testing)
   - ✅ Include Fundamental Data
   - ✅ Include Technical Indicators
4. Click **"🚀 Run Comprehensive Screen"**
5. Wait for results (progress shown in console)
6. View results table
7. Download results as CSV

### Step 4: Analyze Results

1. Review matching stocks
2. Check summary metrics:
   - Total matches
   - Sector distribution
   - Average price
3. Export for further analysis

## 💡 Example Algorithms

### Growth Stock Algorithm
```
Name: Growth Stocks
Conditions:
- revenue_growth > 20
- earnings_growth > 15
- roe > 20
```

### Technical Momentum Algorithm
```
Name: Oversold Momentum
Conditions:
- rsi(14) < 30
- price > sma(200)
- volume > 1000000
```

### Balanced Algorithm
```
Name: Balanced Value
Conditions:
- pe_ratio < 25
- roe > 12
- revenue_growth > 10
- debt_to_equity < 1.5
```

## 🎯 Tips

1. **Start Small**: Test with max_stocks=50 first
2. **Use Filters**: Filter by sector to reduce processing time
3. **Check Data**: Some stocks may not have complete fundamental data
4. **Combine Factors**: Mix technical and fundamental for better results
5. **Save Algorithms**: Build a library of useful algorithms

## ⚠️ Important Notes

- Screening takes time (depends on number of stocks)
- Fundamental data availability varies by stock
- Some metrics may be None for certain stocks
- Use reasonable values in conditions

## 🔧 Troubleshooting

**Screening takes too long?**
- Reduce max_stocks
- Filter by sector
- Disable technical indicators if not needed

**No matches found?**
- Check condition values are reasonable
- Some stocks may not have fundamental data
- Try broader criteria

**Algorithm not saving?**
- Ensure all fields are filled
- Check at least one condition is added
- Verify condition values are valid



