"""
Main Streamlit application for NSE/BSE Backtester and Screener.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

from data_fetcher import DataFetcher
from data_storage import DataStorage
from analytics import Analytics
from rule_engine import RuleEngine
from backtester import Backtester
from portfolio import Portfolio
from utils import validate_date_range, format_number, format_percentage, get_default_date_range

# Page configuration
st.set_page_config(
    page_title="NSE/BSE Backtester & Screener",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'data_storage' not in st.session_state:
    st.session_state.data_storage = DataStorage()
if 'data_fetcher' not in st.session_state:
    st.session_state.data_fetcher = DataFetcher()
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = {}

# Sidebar navigation
st.sidebar.title("📈 NSE/BSE Backtester")
st.sidebar.markdown("**Note:** For Algorithm Builder and Comprehensive Screening, use `app_enhanced.py`")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Data & Analytics", "🔍 Screener", "🧪 Backtester", "💼 Portfolio", "📈 Compare"]
)

# Home Page
if page == "🏠 Home":
    st.title("NSE/BSE Custom Strategy Backtester + Screener")
    st.markdown("""
    Welcome to the comprehensive platform for analyzing, screening, and backtesting trading strategies 
    on NSE and BSE stocks and indices.
    
    ### Features:
    - **Data & Analytics**: Fetch and analyze stock data with technical indicators
    - **Screener**: Find stocks matching your custom criteria
    - **Backtester**: Test your trading strategies with historical data
    - **Portfolio**: Simulate and manage portfolios
    - **Compare**: Compare strategies against benchmarks
    
    ### Quick Start:
    1. Go to **Data & Analytics** to fetch stock data
    2. Use **Screener** to find stocks matching your rules
    3. Test strategies in **Backtester**
    4. Build portfolios in **Portfolio**
    """)

# Data & Analytics Page
elif page == "📊 Data & Analytics":
    st.title("Data & Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exchange = st.selectbox("Exchange", ["NSE", "BSE"])
        symbol_input = st.text_input("Symbol", value="RELIANCE", help="Enter stock symbol (e.g., RELIANCE, TCS)")
    
    with col2:
        date_range_type = st.radio("Date Range", ["Custom", "Preset"])
        
        if date_range_type == "Preset":
            period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
            start_date = None
            end_date = None
        else:
            start_date, end_date = get_default_date_range(365)
            start_date = st.date_input("Start Date", value=pd.to_datetime(start_date))
            end_date = st.date_input("End Date", value=pd.to_datetime(end_date))
            period = None
    
    if st.button("Fetch Data", type="primary"):
        with st.spinner("Fetching data..."):
            try:
                if date_range_type == "Preset":
                    df = st.session_state.data_fetcher.fetch_data(
                        symbol_input, exchange, period=period
                    )
                else:
                    df = st.session_state.data_fetcher.fetch_data(
                        symbol_input, exchange,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=end_date.strftime('%Y-%m-%d')
                    )
                
                # Store data
                st.session_state.data_storage.store_data(df, symbol_input, exchange)
                st.session_state.loaded_data[f"{exchange}_{symbol_input}"] = df
                
                st.success(f"Data fetched successfully! {len(df)} records.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display analytics if data is loaded
    if st.session_state.loaded_data:
        st.subheader("Select Symbol for Analysis")
        selected_key = st.selectbox("Loaded Data", list(st.session_state.loaded_data.keys()))
        
        if selected_key:
            df = st.session_state.loaded_data[selected_key].copy()
            
            # Compute analytics
            analytics = Analytics(df)
            analytics.compute_all_indicators()
            df_analytics = analytics.get_dataframe()
            
            # Display summary stats
            st.subheader("Summary Statistics")
            stats = analytics.get_summary_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Return", format_percentage(stats['total_return']))
                st.metric("CAGR", format_percentage(stats['annualized_return']))
            with col2:
                st.metric("Current Price", format_number(stats['current_price']))
                st.metric("Volatility", format_percentage(stats['volatility']) if stats['volatility'] else "N/A")
            with col3:
                st.metric("Max Drawdown", format_percentage(stats['max_drawdown']) if stats['max_drawdown'] else "N/A")
                st.metric("Sharpe Ratio", format_number(stats['sharpe_ratio'], 2) if stats['sharpe_ratio'] else "N/A")
            with col4:
                st.metric("52W High", format_number(stats['high_52w']))
                st.metric("52W Low", format_number(stats['low_52w']))
            
            # Charts
            st.subheader("Price Chart with Indicators")
            
            # Select indicators to display
            indicators = st.multiselect(
                "Select Indicators",
                ["SMA 50", "SMA 200", "RSI", "MACD", "Bollinger Bands"],
                default=["SMA 50", "SMA 200"]
            )
            
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
            
            # Add moving averages
            if "SMA 50" in indicators and 'sma_50' in df_analytics.columns:
                fig.add_trace(
                    go.Scatter(x=df_analytics['date'], y=df_analytics['sma_50'], name="SMA 50"),
                    row=1, col=1
                )
            if "SMA 200" in indicators and 'sma_200' in df_analytics.columns:
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
            
            # Data table
            st.subheader("Data Table")
            st.dataframe(df_analytics.tail(100), use_container_width=True)

# Screener Page
elif page == "🔍 Screener":
    st.title("Stock Screener")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exchange = st.selectbox("Exchange", ["NSE", "BSE"])
        symbols_input = st.text_area(
            "Symbols (one per line)",
            value="RELIANCE\nTCS\nHDFCBANK\nINFY",
            help="Enter stock symbols, one per line"
        )
    
    with col2:
        start_date, end_date = get_default_date_range(365)
        start_date = st.date_input("Start Date", value=pd.to_datetime(start_date))
        end_date = st.date_input("End Date", value=pd.to_datetime(end_date))
    
    st.subheader("Custom Screening Rule")
    st.markdown("""
    **Example rules:**
    - `rsi(14) < 30 and price > sma(200)`
    - `close > sma(50) and volume > 1000000`
    - `rsi < 40 and price > sma(200) and volume > sma(20)`
    """)
    
    rule = st.text_input(
        "Screening Rule",
        value="rsi(14) < 30 and price > sma(200)",
        help="Enter a Python-like expression"
    )
    
    if st.button("Run Screener", type="primary"):
        symbols = [s.strip() for s in symbols_input.split('\n') if s.strip()]
        
        if not symbols:
            st.error("Please enter at least one symbol")
        elif not rule:
            st.error("Please enter a screening rule")
        else:
            with st.spinner("Running screener..."):
                results = []
                
                for symbol in symbols:
                    try:
                        # Fetch data
                        df = st.session_state.data_fetcher.fetch_data(
                            symbol, exchange,
                            start_date=start_date.strftime('%Y-%m-%d'),
                            end_date=end_date.strftime('%Y-%m-%d')
                        )
                        
                        # Compute analytics
                        analytics = Analytics(df)
                        analytics.compute_all_indicators()
                        df_analytics = analytics.get_dataframe()
                        
                        # Apply rule
                        rule_engine = RuleEngine(df_analytics)
                        filtered = rule_engine.filter_by_rule(rule)
                        
                        if len(filtered) > 0:
                            latest = filtered.iloc[-1]
                            results.append({
                                'Symbol': symbol,
                                'Exchange': exchange,
                                'Current Price': latest['close'],
                                'RSI': latest.get('rsi', 'N/A'),
                                'SMA 50': latest.get('sma_50', 'N/A'),
                                'SMA 200': latest.get('sma_200', 'N/A'),
                                'Volume': latest['volume'],
                                'Matches': len(filtered)
                            })
                    
                    except Exception as e:
                        st.warning(f"Error processing {symbol}: {str(e)}")
                        continue
                
                if results:
                    results_df = pd.DataFrame(results)
                    st.success(f"Found {len(results)} matching stocks!")
                    st.dataframe(results_df, use_container_width=True)
                else:
                    st.info("No stocks matched the criteria")

# Backtester Page
elif page == "🧪 Backtester":
    st.title("Strategy Backtester")
    
    # Select data
    if not st.session_state.loaded_data:
        st.warning("Please fetch data first in the Data & Analytics page")
    else:
        selected_key = st.selectbox("Select Data", list(st.session_state.loaded_data.keys()))
        df = st.session_state.loaded_data[selected_key].copy()
        
        # Compute analytics
        analytics = Analytics(df)
        analytics.compute_all_indicators()
        df_analytics = analytics.get_dataframe()
        
        st.subheader("Strategy Rules")
        
        col1, col2 = st.columns(2)
        with col1:
            buy_rule = st.text_input(
                "Buy Rule",
                value="rsi(14) < 30 and price > sma(200)",
                help="Condition to enter a position"
            )
        with col2:
            sell_rule = st.text_input(
                "Sell Rule",
                value="rsi(14) > 70",
                help="Condition to exit a position"
            )
        
        st.subheader("Strategy Parameters")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            initial_capital = st.number_input("Initial Capital", value=100000, min_value=1000, step=10000)
            position_size = st.slider("Position Size (% of capital)", 0.1, 1.0, 1.0, 0.1)
        with col2:
            stop_loss = st.number_input("Stop Loss (%)", value=5.0, min_value=0.0, max_value=50.0, step=0.5) / 100
            take_profit = st.number_input("Take Profit (%)", value=0.0, min_value=0.0, max_value=100.0, step=1.0) / 100
        with col3:
            max_holding = st.number_input("Max Holding Period (days)", value=0, min_value=0, step=1)
            max_holding = max_holding if max_holding > 0 else None
        
        if st.button("Run Backtest", type="primary"):
            with st.spinner("Running backtest..."):
                try:
                    backtester = Backtester(df_analytics, initial_capital=initial_capital)
                    results = backtester.backtest(
                        buy_rule=buy_rule,
                        sell_rule=sell_rule,
                        position_size=position_size,
                        stop_loss=stop_loss if stop_loss > 0 else None,
                        take_profit=take_profit if take_profit > 0 else None,
                        max_holding_period=max_holding
                    )
                    
                    # Display results
                    st.subheader("Performance Metrics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Return", format_percentage(results['total_return']))
                        st.metric("CAGR", format_percentage(results['cagr']))
                    with col2:
                        st.metric("Sharpe Ratio", format_number(results['sharpe_ratio'], 2))
                        st.metric("Max Drawdown", format_percentage(results['max_drawdown']))
                    with col3:
                        st.metric("Total Trades", results['total_trades'])
                        st.metric("Win Rate", format_percentage(results['win_rate']))
                    with col4:
                        st.metric("Profit Factor", format_number(results['profit_factor'], 2))
                        st.metric("Final Equity", format_number(results['final_equity']))
                    
                    # Equity curve
                    st.subheader("Equity Curve")
                    equity_df = results['equity_curve']
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=equity_df.index,
                        y=equity_df['equity'],
                        mode='lines',
                        name='Equity',
                        line=dict(color='blue', width=2)
                    ))
                    fig.add_hline(
                        y=initial_capital,
                        line_dash="dash",
                        line_color="gray",
                        annotation_text="Initial Capital"
                    )
                    fig.update_layout(
                        title="Equity Curve",
                        xaxis_title="Date",
                        yaxis_title="Portfolio Value",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Trades table
                    if len(results['trades']) > 0:
                        st.subheader("Trade History")
                        trades_df = results['trades']
                        st.dataframe(trades_df, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error running backtest: {str(e)}")

# Portfolio Page
elif page == "💼 Portfolio":
    st.title("Portfolio Simulator")
    st.info("Portfolio simulation feature - Coming soon with full implementation")

# Compare Page
elif page == "📈 Compare":
    st.title("Strategy Comparison")
    st.info("Strategy comparison feature - Coming soon with full implementation")

