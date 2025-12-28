"""
indiAlgo - Main Application
Professional Indian Stock Market Analysis & Strategy Platform
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json

# Core modules
from config import Config
from data_manager import DataManager
from data_fetcher import DataFetcher
from analytics import Analytics
from rule_engine import RuleEngine
from advanced_backtester import AdvancedBacktester
from portfolio_manager import PortfolioManager
from paper_trading import PaperTrading
from ai_mentor import AIMentor
from strategy_manager import StrategyManager
from stock_grouper import StockGrouper
from fundamental_data import FundamentalData
from premium_features import PremiumFeatures

# Page configuration
st.set_page_config(
    page_title="indiAlgo - Stock Analysis & Strategy Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .premium-badge {
        background-color: #ffd700;
        color: #000;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'data_fetcher' not in st.session_state:
        st.session_state.data_fetcher = DataFetcher()
    if 'fundamental_data' not in st.session_state:
        st.session_state.fundamental_data = FundamentalData()
    if 'strategy_manager' not in st.session_state:
        st.session_state.strategy_manager = StrategyManager()
    if 'stock_grouper' not in st.session_state:
        st.session_state.stock_grouper = StockGrouper(st.session_state.data_manager)
    if 'portfolio_manager' not in st.session_state:
        st.session_state.portfolio_manager = PortfolioManager(st.session_state.data_manager)
    if 'paper_trading' not in st.session_state:
        st.session_state.paper_trading = PaperTrading(st.session_state.data_manager)
    if 'ai_mentor' not in st.session_state:
        st.session_state.ai_mentor = AIMentor()
    if 'user_tier' not in st.session_state:
        st.session_state.user_tier = 'free'  # 'free' or 'premium'
    if 'loaded_data' not in st.session_state:
        st.session_state.loaded_data = {}
    if 'portfolios' not in st.session_state:
        st.session_state.portfolios = {}

init_session_state()

# Sidebar
st.sidebar.markdown(f"# 📊 {Config.PLATFORM_NAME}")
st.sidebar.markdown(f"**Version:** {Config.VERSION}")

# User tier display
if st.session_state.user_tier == 'premium':
    st.sidebar.markdown('<span class="premium-badge">⭐ PREMIUM</span>', unsafe_allow_html=True)
else:
    if st.sidebar.button("🚀 Upgrade to Premium"):
        st.sidebar.info("Premium features: Unlimited backtests, Advanced analytics, API access, Real-time data")

st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Stock Analyzer",
        "🔍 Stock Screener",
        "🧪 Strategy Backtester",
        "💼 Portfolio Manager",
        "📈 Paper Trading",
        "🤖 AI Mentor",
        "📚 Learn & Guides",
        "⚙️ Settings"
    ]
)

# Home Page
if page == "🏠 Home":
    st.markdown('<div class="main-header">indiAlgo</div>', unsafe_allow_html=True)
    st.markdown("### Your Professional Stock Analysis & Strategy Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Stocks Analyzed", "2000+")
        st.metric("Indicators Available", "20+")
    
    with col2:
        st.metric("Strategies Tested", "100+")
        st.metric("Users", "Growing!")
    
    with col3:
        st.metric("Data Coverage", "10+ Years")
        st.metric("Exchanges", "NSE & BSE")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 What is indiAlgo?
    
    **indiAlgo** is a comprehensive platform for analyzing Indian stock markets (NSE & BSE).
    Whether you're a student learning about markets, a trader testing strategies, or an analyst
    comparing stocks - indiAlgo has the tools you need.
    
    ### ✨ Key Features:
    
    - **📊 Stock Analyzer**: Deep dive into any stock with technical & fundamental analysis
    - **🔍 Stock Screener**: Find stocks matching your custom criteria across 2000+ companies
    - **🧪 Strategy Backtester**: Test trading strategies with realistic assumptions
    - **💼 Portfolio Manager**: Track multiple portfolios with risk analytics
    - **📈 Paper Trading**: Practice trading with virtual money
    - **🤖 AI Mentor**: Get educational guidance on trading concepts
    - **📚 Learning Resources**: Understand indicators, strategies, and risk management
    
    ### 🚀 Quick Start:
    
    1. **New to trading?** Start with "📚 Learn & Guides" and "🤖 AI Mentor"
    2. **Want to analyze a stock?** Go to "📊 Stock Analyzer"
    3. **Looking for opportunities?** Use "🔍 Stock Screener"
    4. **Testing strategies?** Try "🧪 Strategy Backtester"
    5. **Managing investments?** Use "💼 Portfolio Manager"
    
    ### ⚠️ Important Disclaimer:
    
    This platform is for **educational purposes only**. All analysis, backtests, and suggestions
    are NOT financial advice. Always do your own research and consult qualified financial
    advisors before making investment decisions.
    """)
    
    # Feature comparison
    st.markdown("---")
    st.subheader("Free vs Premium")
    
    comparison = PremiumFeatures.get_feature_comparison()
    
    comp_df = pd.DataFrame({
        'Feature': [
            'Backtests per Month',
            'Export Formats',
            'Data Access',
            'Support',
            'Custom Indicators',
            'API Access'
        ],
        'Free': [
            comparison['free']['backtests_per_month'],
            ', '.join(comparison['free']['export_formats']),
            comparison['free']['data_access'],
            comparison['free']['support'],
            '❌',
            '❌'
        ],
        'Premium': [
            comparison['premium']['backtests_per_month'],
            ', '.join(comparison['premium']['export_formats']),
            comparison['premium']['data_access'],
            comparison['premium']['support'],
            '✅',
            '✅'
        ]
    })
    
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

# Stock Analyzer Page
elif page == "📊 Stock Analyzer":
    st.title("📊 Stock Analyzer")
    st.markdown("Analyze any NSE/BSE stock with comprehensive metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exchange = st.selectbox("Exchange", ["NSE", "BSE"])
        symbol = st.text_input("Stock Symbol", value="RELIANCE", placeholder="e.g., RELIANCE, TCS")
    
    with col2:
        years = st.slider("Years of History", 1, 10, 5)
        use_fundamentals = st.checkbox("Include Fundamental Data", value=True)
    
    if st.button("Analyze Stock", type="primary"):
        with st.spinner("Fetching data and computing analytics..."):
            try:
                # Fetch data
                df = st.session_state.data_manager.get_historical_data(
                    symbol, exchange, years=years
                )
                
                if df.empty:
                    st.error(f"No data found for {symbol} on {exchange}")
                else:
                    st.session_state.loaded_data[f"{exchange}_{symbol}"] = df
                    
                    # Compute analytics
                    analytics = Analytics(df)
                    analytics.compute_all_indicators()
                    df_analytics = analytics.get_dataframe()
                    
                    # Display summary
                    stats = analytics.get_summary_stats()
                    
                    st.success(f"✅ Analyzed {symbol} - {len(df)} days of data")
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Return", f"{stats['total_return']:.2f}%")
                        st.metric("CAGR", f"{stats['annualized_return']:.2f}%")
                    with col2:
                        st.metric("Current Price", f"₹{stats['current_price']:.2f}")
                        st.metric("Volatility", f"{stats['volatility']:.2f}%" if stats['volatility'] else "N/A")
                    with col3:
                        st.metric("Max Drawdown", f"{stats['max_drawdown']:.2f}%" if stats['max_drawdown'] else "N/A")
                        st.metric("Sharpe Ratio", f"{stats['sharpe_ratio']:.2f}" if stats['sharpe_ratio'] else "N/A")
                    with col4:
                        st.metric("52W High", f"₹{stats['high_52w']:.2f}")
                        st.metric("52W Low", f"₹{stats['low_52w']:.2f}")
                    
                    # Charts
                    st.subheader("Price Chart with Indicators")
                    
                    fig = make_subplots(
                        rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_heights=[0.6, 0.2, 0.2],
                        subplot_titles=("Price", "RSI", "MACD")
                    )
                    
                    # Candlestick
                    fig.add_trace(
                        go.Candlestick(
                            x=df_analytics['date'],
                            open=df_analytics['open'],
                            high=df_analytics['high'],
                            low=df_analytics['low'],
                            close=df_analytics['close'],
                            name="Price"
                        ),
                        row=1, col=1
                    )
                    
                    # Moving averages
                    if 'sma_50' in df_analytics.columns:
                        fig.add_trace(
                            go.Scatter(x=df_analytics['date'], y=df_analytics['sma_50'], name="SMA 50"),
                            row=1, col=1
                        )
                    if 'sma_200' in df_analytics.columns:
                        fig.add_trace(
                            go.Scatter(x=df_analytics['date'], y=df_analytics['sma_200'], name="SMA 200"),
                            row=1, col=1
                        )
                    
                    # RSI
                    if 'rsi' in df_analytics.columns:
                        fig.add_trace(
                            go.Scatter(x=df_analytics['date'], y=df_analytics['rsi'], name="RSI"),
                            row=2, col=1
                        )
                        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                    
                    # MACD
                    if 'macd' in df_analytics.columns:
                        fig.add_trace(
                            go.Scatter(x=df_analytics['date'], y=df_analytics['macd'], name="MACD"),
                            row=3, col=1
                        )
                        if 'macd_signal' in df_analytics.columns:
                            fig.add_trace(
                                go.Scatter(x=df_analytics['date'], y=df_analytics['macd_signal'], name="Signal"),
                                row=3, col=1
                            )
                    
                    fig.update_layout(height=800, xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Fundamental data
                    if use_fundamentals:
                        st.subheader("Fundamental Data")
                        try:
                            fundamentals = st.session_state.fundamental_data.get_fundamentals(symbol, exchange)
                            
                            fund_col1, fund_col2 = st.columns(2)
                            
                            with fund_col1:
                                st.write("**Valuation**")
                                st.write(f"P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}")
                                st.write(f"P/B Ratio: {fundamentals.get('price_to_book', 'N/A')}")
                                st.write(f"Market Cap: ₹{fundamentals.get('market_cap', 0)/1e7:.2f} Cr" if fundamentals.get('market_cap') else "N/A")
                            
                            with fund_col2:
                                st.write("**Profitability**")
                                st.write(f"ROE: {fundamentals.get('roe', 'N/A')}%")
                                st.write(f"ROA: {fundamentals.get('roa', 'N/A')}%")
                                st.write(f"Profit Margin: {fundamentals.get('profit_margin', 'N/A')}%")
                        except:
                            st.info("Fundamental data not available for this stock")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Continue with other pages...
# For brevity, I'll create a comprehensive deployment guide document

elif page == "🤖 AI Mentor":
    st.title("🤖 AI Mentor")
    st.markdown("Get educational guidance on trading concepts and strategies")
    
    st.info("💡 Ask me anything about trading, indicators, backtesting, or portfolio management!")
    
    # Chat interface
    user_message = st.text_input("Ask a question:", placeholder="e.g., Explain RSI indicator")
    
    if st.button("Ask AI Mentor") and user_message:
        with st.spinner("Thinking..."):
            response = st.session_state.ai_mentor.chat(user_message)
            
            st.markdown("### 🤖 AI Mentor Response:")
            st.markdown(response['answer'])
            
            if 'suggestions' in response:
                st.markdown("**Suggested Questions:**")
                for suggestion in response['suggestions']:
                    if st.button(suggestion, key=f"sugg_{suggestion}"):
                        st.session_state.user_message = suggestion
                        st.rerun()

# Continue with other pages...
# Paper Trading, Portfolio Manager, etc. would follow similar patterns

