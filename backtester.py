"""
Backtesting engine for testing trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime
from rule_engine import RuleEngine


class Backtester:
    """Backtests trading strategies."""
    
    def __init__(
        self,
        df: pd.DataFrame,
        initial_capital: float = 100000,
        commission: float = 0.001  # 0.1% commission
    ):
        """
        Initialize backtester.
        
        Args:
            df: DataFrame with OHLCV data and indicators
            initial_capital: Starting capital
            commission: Commission per trade (as fraction)
        """
        self.df = df.copy()
        if 'date' in self.df.columns:
            self.df = self.df.set_index('date')
        self.df = self.df.sort_index()
        
        self.initial_capital = initial_capital
        self.commission = commission
        
        self.rule_engine = RuleEngine(self.df)
    
    def backtest(
        self,
        buy_rule: str,
        sell_rule: str,
        position_size: float = 1.0,  # Fraction of capital per trade
        stop_loss: Optional[float] = None,  # Stop loss as fraction (e.g., 0.05 for 5%)
        take_profit: Optional[float] = None,  # Take profit as fraction
        max_holding_period: Optional[int] = None,  # Max days to hold
        rebalance_frequency: Optional[str] = None  # 'D', 'W', 'M' for daily, weekly, monthly
    ) -> Dict:
        """
        Backtest a strategy.
        
        Returns:
            Dictionary with performance metrics and equity curve
        """
        # Get signals
        signals_df = self.rule_engine.get_rule_signals(buy_rule, sell_rule)
        signals_df = signals_df.set_index('date')
        
        # Initialize tracking variables
        capital = self.initial_capital
        position = 0  # Number of shares
        entry_price = 0
        entry_date = None
        equity_curve = []
        trades = []
        
        # Track stop loss and take profit
        stop_loss_price = None
        take_profit_price = None
        
        for date, row in signals_df.iterrows():
            current_price = row['close']
            signal = row['signal']
            
            # Check stop loss and take profit
            if position > 0:
                if stop_loss_price and current_price <= stop_loss_price:
                    signal = -1  # Force sell
                elif take_profit_price and current_price >= take_profit_price:
                    signal = -1  # Force sell
                
                # Check max holding period
                if max_holding_period and entry_date:
                    days_held = (date - entry_date).days
                    if days_held >= max_holding_period:
                        signal = -1  # Force sell
            
            # Execute trades
            if signal == 1 and position == 0:  # Buy signal
                # Calculate position size
                trade_value = capital * position_size
                shares = int(trade_value / current_price)
                
                if shares > 0:
                    cost = shares * current_price * (1 + self.commission)
                    if cost <= capital:
                        position = shares
                        entry_price = current_price
                        entry_date = date
                        capital -= cost
                        
                        # Set stop loss and take profit
                        if stop_loss:
                            stop_loss_price = entry_price * (1 - stop_loss)
                        if take_profit:
                            take_profit_price = entry_price * (1 + take_profit)
            
            elif signal == -1 and position > 0:  # Sell signal
                # Sell position
                proceeds = position * current_price * (1 - self.commission)
                capital += proceeds
                
                # Record trade
                pnl = proceeds - (position * entry_price * (1 + self.commission))
                pnl_pct = (pnl / (position * entry_price * (1 + self.commission))) * 100
                
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'shares': position,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'holding_period': (date - entry_date).days
                })
                
                position = 0
                entry_price = 0
                entry_date = None
                stop_loss_price = None
                take_profit_price = None
            
            # Calculate current equity
            current_equity = capital + (position * current_price if position > 0 else 0)
            equity_curve.append({
                'date': date,
                'equity': current_equity,
                'capital': capital,
                'position': position,
                'price': current_price
            })
        
        # Close any open position at the end
        if position > 0:
            last_price = signals_df['close'].iloc[-1]
            proceeds = position * last_price * (1 - self.commission)
            capital += proceeds
            
            pnl = proceeds - (position * entry_price * (1 + self.commission))
            pnl_pct = (pnl / (position * entry_price * (1 + self.commission))) * 100
            
            trades.append({
                'entry_date': entry_date,
                'exit_date': signals_df.index[-1],
                'entry_price': entry_price,
                'exit_price': last_price,
                'shares': position,
                'pnl': pnl,
                'pnl_pct': pnl_pct,
                'holding_period': (signals_df.index[-1] - entry_date).days
            })
        
        # Calculate performance metrics
        equity_df = pd.DataFrame(equity_curve)
        equity_df = equity_df.set_index('date')
        
        final_equity = equity_df['equity'].iloc[-1]
        total_return = (final_equity / self.initial_capital - 1) * 100
        
        # Calculate CAGR
        days = (equity_df.index[-1] - equity_df.index[0]).days
        years = days / 365.25
        if years > 0:
            cagr = ((final_equity / self.initial_capital) ** (1 / years) - 1) * 100
        else:
            cagr = 0
        
        # Calculate Sharpe ratio
        returns = equity_df['equity'].pct_change().dropna()
        if len(returns) > 0 and returns.std() > 0:
            sharpe = (returns.mean() * np.sqrt(252)) / (returns.std() * np.sqrt(252))
        else:
            sharpe = 0
        
        # Calculate max drawdown
        equity_df['running_max'] = equity_df['equity'].expanding().max()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['running_max']) / equity_df['running_max']
        max_drawdown = equity_df['drawdown'].min() * 100
        
        # Trade statistics
        trades_df = pd.DataFrame(trades)
        if len(trades_df) > 0:
            winning_trades = trades_df[trades_df['pnl'] > 0]
            losing_trades = trades_df[trades_df['pnl'] <= 0]
            
            win_rate = (len(winning_trades) / len(trades_df)) * 100 if len(trades_df) > 0 else 0
            avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
            avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
            profit_factor = abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum()) if len(losing_trades) > 0 and losing_trades['pnl'].sum() != 0 else 0
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_equity': final_equity,
            'total_return': total_return,
            'cagr': cagr,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'total_trades': len(trades_df),
            'winning_trades': len(winning_trades) if len(trades_df) > 0 else 0,
            'losing_trades': len(losing_trades) if len(trades_df) > 0 else 0,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'equity_curve': equity_df,
            'trades': trades_df
        }

