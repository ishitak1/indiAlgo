"""
Example usage of the NSE/BSE Backtester modules.
This demonstrates how to use the modules programmatically.
"""

from data_fetcher import DataFetcher
from data_storage import DataStorage
from analytics import Analytics
from rule_engine import RuleEngine
from backtester import Backtester

def example_fetch_and_analyze():
    """Example: Fetch data and compute analytics."""
    print("=" * 50)
    print("Example 1: Fetch and Analyze Data")
    print("=" * 50)
    
    # Initialize
    fetcher = DataFetcher()
    storage = DataStorage()
    
    # Fetch data
    print("\nFetching RELIANCE data from NSE...")
    df = fetcher.fetch_data("RELIANCE", exchange="NSE", period="1y")
    print(f"Fetched {len(df)} records")
    
    # Store data
    storage.store_data(df, "RELIANCE", "NSE")
    print("Data stored in database")
    
    # Compute analytics
    analytics = Analytics(df)
    analytics.compute_all_indicators()
    df_analytics = analytics.get_dataframe()
    
    # Get summary stats
    stats = analytics.get_summary_stats()
    print("\nSummary Statistics:")
    print(f"Total Return: {stats['total_return']:.2f}%")
    print(f"CAGR: {stats['annualized_return']:.2f}%")
    print(f"Current Price: ₹{stats['current_price']:.2f}")
    print(f"Max Drawdown: {stats['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
    
    return df_analytics


def example_screening():
    """Example: Screen stocks using custom rules."""
    print("\n" + "=" * 50)
    print("Example 2: Stock Screening")
    print("=" * 50)
    
    fetcher = DataFetcher()
    
    # Fetch data for multiple stocks
    symbols = ["RELIANCE", "TCS", "HDFCBANK"]
    print(f"\nFetching data for {symbols}...")
    
    for symbol in symbols:
        try:
            df = fetcher.fetch_data(symbol, exchange="NSE", period="1y")
            
            # Compute analytics
            analytics = Analytics(df)
            analytics.compute_all_indicators()
            df_analytics = analytics.get_dataframe()
            
            # Apply screening rule
            rule_engine = RuleEngine(df_analytics)
            rule = "rsi(14) < 30 and price > sma(200)"
            filtered = rule_engine.filter_by_rule(rule)
            
            if len(filtered) > 0:
                latest = filtered.iloc[-1]
                print(f"\n{symbol}: MATCHES RULE")
                print(f"  Current Price: ₹{latest['close']:.2f}")
                print(f"  RSI: {latest.get('rsi', 'N/A'):.2f}")
                print(f"  SMA 200: ₹{latest.get('sma_200', 'N/A'):.2f}")
            else:
                print(f"\n{symbol}: Does not match rule")
        
        except Exception as e:
            print(f"\n{symbol}: Error - {str(e)}")


def example_backtest():
    """Example: Backtest a trading strategy."""
    print("\n" + "=" * 50)
    print("Example 3: Backtest Strategy")
    print("=" * 50)
    
    fetcher = DataFetcher()
    
    # Fetch data
    print("\nFetching RELIANCE data...")
    df = fetcher.fetch_data("RELIANCE", exchange="NSE", period="2y")
    
    # Compute analytics
    analytics = Analytics(df)
    analytics.compute_all_indicators()
    df_analytics = analytics.get_dataframe()
    
    # Define strategy
    buy_rule = "rsi(14) < 30 and price > sma(200)"
    sell_rule = "rsi(14) > 70"
    
    print(f"\nBuy Rule: {buy_rule}")
    print(f"Sell Rule: {sell_rule}")
    
    # Run backtest
    backtester = Backtester(df_analytics, initial_capital=100000)
    results = backtester.backtest(
        buy_rule=buy_rule,
        sell_rule=sell_rule,
        position_size=1.0,
        stop_loss=0.05,  # 5% stop loss
        max_holding_period=30  # Max 30 days
    )
    
    # Display results
    print("\nBacktest Results:")
    print(f"Initial Capital: ₹{results['initial_capital']:,.2f}")
    print(f"Final Equity: ₹{results['final_equity']:,.2f}")
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"CAGR: {results['cagr']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
    print(f"Total Trades: {results['total_trades']}")
    print(f"Win Rate: {results['win_rate']:.2f}%")
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    
    if len(results['trades']) > 0:
        print("\nFirst 5 Trades:")
        trades_df = results['trades']
        print(trades_df.head().to_string())


if __name__ == "__main__":
    try:
        # Run examples
        df_analytics = example_fetch_and_analyze()
        example_screening()
        example_backtest()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)
    
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        import traceback
        traceback.print_exc()



