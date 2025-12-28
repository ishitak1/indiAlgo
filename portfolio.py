"""
Portfolio simulation and management module.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
from analytics import Analytics


class Portfolio:
    """Manages portfolio simulation and analysis."""
    
    def __init__(self, initial_capital: float = 100000):
        """Initialize portfolio with initial capital."""
        self.initial_capital = initial_capital
        self.holdings = {}  # {symbol: shares}
        self.cash = initial_capital
        self.trades = []
    
    def add_position(self, symbol: str, shares: int, price: float, date: datetime, commission: float = 0.001):
        """Add a position to the portfolio."""
        cost = shares * price * (1 + commission)
        if cost <= self.cash:
            if symbol in self.holdings:
                self.holdings[symbol] += shares
            else:
                self.holdings[symbol] = shares
            
            self.cash -= cost
            self.trades.append({
                'date': date,
                'symbol': symbol,
                'action': 'BUY',
                'shares': shares,
                'price': price,
                'value': cost
            })
            return True
        return False
    
    def remove_position(self, symbol: str, shares: int, price: float, date: datetime, commission: float = 0.001):
        """Remove a position from the portfolio."""
        if symbol in self.holdings and self.holdings[symbol] >= shares:
            proceeds = shares * price * (1 - commission)
            self.holdings[symbol] -= shares
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            
            self.cash += proceeds
            self.trades.append({
                'date': date,
                'symbol': symbol,
                'action': 'SELL',
                'shares': shares,
                'price': price,
                'value': proceeds
            })
            return True
        return False
    
    def get_portfolio_value(self, prices: Dict[str, float]) -> float:
        """Get current portfolio value."""
        holdings_value = sum(self.holdings.get(symbol, 0) * price for symbol, price in prices.items())
        return self.cash + holdings_value
    
    def rebalance(
        self,
        target_weights: Dict[str, float],
        prices: Dict[str, float],
        date: datetime,
        commission: float = 0.001
    ):
        """Rebalance portfolio to target weights."""
        current_value = self.get_portfolio_value(prices)
        
        for symbol, target_weight in target_weights.items():
            if symbol not in prices:
                continue
            
            target_value = current_value * target_weight
            target_shares = int(target_value / prices[symbol])
            current_shares = self.holdings.get(symbol, 0)
            
            if target_shares > current_shares:
                # Buy more
                shares_to_buy = target_shares - current_shares
                self.add_position(symbol, shares_to_buy, prices[symbol], date, commission)
            elif target_shares < current_shares:
                # Sell some
                shares_to_sell = current_shares - target_shares
                self.remove_position(symbol, shares_to_sell, prices[symbol], date, commission)
    
    def simulate_portfolio(
        self,
        data_dict: Dict[str, pd.DataFrame],
        weights: Dict[str, float],
        rebalance_frequency: str = 'M',  # 'D', 'W', 'M'
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Simulate portfolio performance.
        
        Args:
            data_dict: Dictionary of {symbol: DataFrame} with OHLCV data
            weights: Target weights for each symbol
            rebalance_frequency: How often to rebalance
            start_date: Start date for simulation
            end_date: End date for simulation
        
        Returns:
            DataFrame with portfolio value over time
        """
        # Align all dataframes
        all_dates = set()
        for df in data_dict.values():
            if 'date' in df.columns:
                df = df.set_index('date')
            all_dates.update(df.index)
        
        all_dates = sorted(list(all_dates))
        
        if start_date:
            all_dates = [d for d in all_dates if d >= pd.to_datetime(start_date)]
        if end_date:
            all_dates = [d for d in all_dates if d <= pd.to_datetime(end_date)]
        
        portfolio_values = []
        
        for date in all_dates:
            # Get prices for this date
            prices = {}
            for symbol, df in data_dict.items():
                if 'date' in df.columns:
                    df = df.set_index('date')
                if date in df.index:
                    prices[symbol] = df.loc[date, 'close']
            
            # Rebalance if needed
            if date == all_dates[0] or self._should_rebalance(date, all_dates, rebalance_frequency):
                self.rebalance(weights, prices, date)
            
            # Calculate portfolio value
            portfolio_value = self.get_portfolio_value(prices)
            portfolio_values.append({
                'date': date,
                'portfolio_value': portfolio_value,
                'cash': self.cash,
                'holdings_value': portfolio_value - self.cash
            })
        
        return pd.DataFrame(portfolio_values)
    
    def _should_rebalance(self, current_date: pd.Timestamp, all_dates: List, frequency: str) -> bool:
        """Check if portfolio should be rebalanced."""
        if frequency == 'D':
            return True
        elif frequency == 'W':
            # Rebalance weekly (every 7 days or on Monday)
            idx = all_dates.index(current_date)
            if idx == 0:
                return False
            prev_date = all_dates[idx - 1]
            return (current_date - prev_date).days >= 7 or current_date.weekday() == 0
        elif frequency == 'M':
            # Rebalance monthly (first trading day of month)
            idx = all_dates.index(current_date)
            if idx == 0:
                return False
            prev_date = all_dates[idx - 1]
            return current_date.month != prev_date.month
        return False
    
    def compare_with_benchmark(
        self,
        portfolio_values: pd.DataFrame,
        benchmark_df: pd.DataFrame,
        benchmark_symbol: str = 'NIFTY 50'
    ) -> Dict:
        """Compare portfolio performance with benchmark."""
        # Align dates
        portfolio_df = portfolio_values.set_index('date')
        if 'date' in benchmark_df.columns:
            benchmark_df = benchmark_df.set_index('date')
        
        common_dates = portfolio_df.index.intersection(benchmark_df.index)
        
        portfolio_returns = portfolio_df.loc[common_dates, 'portfolio_value'].pct_change().dropna()
        benchmark_returns = benchmark_df.loc[common_dates, 'close'].pct_change().dropna()
        
        # Calculate metrics
        portfolio_total_return = (portfolio_df.loc[common_dates[-1], 'portfolio_value'] / portfolio_df.loc[common_dates[0], 'portfolio_value'] - 1) * 100
        benchmark_total_return = (benchmark_df.loc[common_dates[-1], 'close'] / benchmark_df.loc[common_dates[0], 'close'] - 1) * 100
        
        # Calculate alpha (excess return)
        alpha = portfolio_total_return - benchmark_total_return
        
        # Calculate beta
        if benchmark_returns.std() > 0:
            beta = portfolio_returns.cov(benchmark_returns) / benchmark_returns.var()
        else:
            beta = 0
        
        # Calculate correlation
        correlation = portfolio_returns.corr(benchmark_returns)
        
        return {
            'portfolio_return': portfolio_total_return,
            'benchmark_return': benchmark_total_return,
            'alpha': alpha,
            'beta': beta,
            'correlation': correlation,
            'outperformance': alpha
        }



