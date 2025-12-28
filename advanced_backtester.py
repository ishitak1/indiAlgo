"""
Advanced backtesting engine with realistic assumptions and comprehensive metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import Config
from analytics import Analytics
from rule_engine import RuleEngine


class AdvancedBacktester:
    """Advanced backtesting with realistic assumptions."""
    
    def __init__(
        self,
        initial_capital: float = None,
        commission: float = None,
        slippage: float = None
    ):
        self.initial_capital = initial_capital or Config.DEFAULT_INITIAL_CAPITAL
        self.commission = commission or Config.DEFAULT_COMMISSION
        self.slippage = slippage or Config.DEFAULT_SLIPPAGE
    
    def backtest_strategy(
        self,
        df: pd.DataFrame,
        buy_rule: str,
        sell_rule: str,
        position_size: float = 1.0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        max_holding_period: Optional[int] = None,
        rebalance_frequency: Optional[str] = None,
        entry_time: str = 'open',  # 'open', 'close', 'next_open'
        exit_time: str = 'close'  # 'open', 'close'
    ) -> Dict:
        """
        Backtest a strategy with realistic assumptions.
        
        Args:
            df: OHLCV DataFrame
            buy_rule: Buy condition expression
            sell_rule: Sell condition expression
            position_size: Fraction of capital per trade
            stop_loss: Stop loss as fraction (e.g., 0.05 for 5%)
            take_profit: Take profit as fraction
            max_holding_period: Maximum days to hold
            rebalance_frequency: 'D', 'W', 'M' for daily, weekly, monthly
            entry_time: When to enter ('open', 'close', 'next_open')
            exit_time: When to exit ('open', 'close')
        
        Returns:
            Comprehensive backtest results dictionary
        """
        # Prepare data
        if 'date' in df.columns:
            df = df.set_index('date')
        df = df.sort_index()
        
        # Compute indicators
        analytics = Analytics(df)
        analytics.compute_all_indicators()
        df_analytics = analytics.get_dataframe()
        df_analytics = df_analytics.set_index('date')
        
        # Get signals
        rule_engine = RuleEngine(df_analytics)
        buy_signals = rule_engine.evaluate_rule(buy_rule)
        sell_signals = rule_engine.evaluate_rule(sell_rule)
        
        # Initialize tracking
        capital = self.initial_capital
        position = 0
        entry_price = 0
        entry_date = None
        entry_index = None
        
        equity_curve = []
        trades = []
        daily_returns = []
        
        stop_loss_price = None
        take_profit_price = None
        
        for i, (date, row) in enumerate(df_analytics.iterrows()):
            current_price = row['close']
            current_open = row['open']
            current_high = row['high']
            current_low = row['low']
            
            # Determine entry/exit prices based on timing
            if entry_time == 'open':
                entry_price_used = current_open
            elif entry_time == 'next_open' and i > 0:
                entry_price_used = df_analytics.iloc[i-1]['open'] if i > 0 else current_open
            else:
                entry_price_used = current_price
            
            if exit_time == 'open':
                exit_price_used = current_open
            else:
                exit_price_used = current_price
            
            # Check stop loss and take profit
            if position > 0:
                # Check stop loss (intraday)
                if stop_loss_price and current_low <= stop_loss_price:
                    sell_signals.iloc[i] = True
                    exit_price_used = stop_loss_price
                
                # Check take profit (intraday)
                if take_profit_price and current_high >= take_profit_price:
                    sell_signals.iloc[i] = True
                    exit_price_used = take_profit_price
                
                # Check max holding period
                if max_holding_period and entry_date:
                    days_held = (date - entry_date).days
                    if days_held >= max_holding_period:
                        sell_signals.iloc[i] = True
            
            # Execute trades
            if buy_signals.iloc[i] and position == 0:
                # Calculate position size
                trade_value = capital * position_size
                shares = int(trade_value / entry_price_used)
                
                if shares > 0:
                    # Apply slippage and commission
                    effective_entry_price = entry_price_used * (1 + self.slippage)
                    cost = shares * effective_entry_price * (1 + self.commission)
                    
                    if cost <= capital:
                        position = shares
                        entry_price = effective_entry_price
                        entry_date = date
                        entry_index = i
                        
                        # Set stop loss and take profit
                        if stop_loss:
                            stop_loss_price = entry_price * (1 - stop_loss)
                        if take_profit:
                            take_profit_price = entry_price * (1 + take_profit)
                        
                        capital -= cost
            
            elif sell_signals.iloc[i] and position > 0:
                # Sell position
                effective_exit_price = exit_price_used * (1 - self.slippage)
                proceeds = position * effective_exit_price * (1 - self.commission)
                capital += proceeds
                
                # Record trade
                pnl = proceeds - (position * entry_price * (1 + self.commission))
                pnl_pct = (pnl / (position * entry_price * (1 + self.commission))) * 100
                holding_days = (date - entry_date).days if entry_date else 0
                
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': entry_price,
                    'exit_price': effective_exit_price,
                    'shares': position,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'holding_period': holding_days,
                    'return': pnl_pct / 100
                })
                
                position = 0
                entry_price = 0
                entry_date = None
                entry_index = None
                stop_loss_price = None
                take_profit_price = None
            
            # Calculate current equity
            current_equity = capital + (position * current_price if position > 0 else 0)
            equity_curve.append({
                'date': date,
                'equity': current_equity,
                'capital': capital,
                'position': position,
                'price': current_price,
                'returns': (current_equity / self.initial_capital - 1) * 100
            })
            
            # Daily returns
            if i > 0:
                prev_equity = equity_curve[-2]['equity'] if len(equity_curve) > 1 else self.initial_capital
                daily_return = (current_equity / prev_equity - 1) if prev_equity > 0 else 0
                daily_returns.append(daily_return)
        
        # Close any open position
        if position > 0:
            last_price = df_analytics['close'].iloc[-1]
            effective_exit_price = last_price * (1 - self.slippage)
            proceeds = position * effective_exit_price * (1 - self.commission)
            capital += proceeds
            
            pnl = proceeds - (position * entry_price * (1 + self.commission))
            pnl_pct = (pnl / (position * entry_price * (1 + self.commission))) * 100
            
            trades.append({
                'entry_date': entry_date,
                'exit_date': df_analytics.index[-1],
                'entry_price': entry_price,
                'exit_price': effective_exit_price,
                'shares': position,
                'pnl': pnl,
                'pnl_pct': pnl_pct,
                'holding_period': (df_analytics.index[-1] - entry_date).days if entry_date else 0,
                'return': pnl_pct / 100
            })
        
        # Calculate comprehensive metrics
        equity_df = pd.DataFrame(equity_curve)
        equity_df = equity_df.set_index('date')
        
        final_equity = equity_df['equity'].iloc[-1]
        total_return = (final_equity / self.initial_capital - 1) * 100
        
        # Time period
        days = (equity_df.index[-1] - equity_df.index[0]).days
        years = days / 365.25
        
        # CAGR
        if years > 0:
            cagr = ((final_equity / self.initial_capital) ** (1 / years) - 1) * 100
        else:
            cagr = 0
        
        # Returns analysis
        returns_series = pd.Series(daily_returns)
        
        # Sharpe ratio
        if len(returns_series) > 0 and returns_series.std() > 0:
            annualized_return = returns_series.mean() * Config.TRADING_DAYS_PER_YEAR
            annualized_vol = returns_series.std() * np.sqrt(Config.TRADING_DAYS_PER_YEAR)
            sharpe = (annualized_return - Config.RISK_FREE_RATE / 100) / annualized_vol
        else:
            sharpe = 0
        
        # Sortino ratio (downside deviation)
        downside_returns = returns_series[returns_series < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(Config.TRADING_DAYS_PER_YEAR)
            sortino = (annualized_return - Config.RISK_FREE_RATE / 100) / downside_std if downside_std > 0 else 0
        else:
            sortino = 0
        
        # Max drawdown
        equity_df['running_max'] = equity_df['equity'].expanding().max()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['running_max']) / equity_df['running_max']
        max_drawdown = equity_df['drawdown'].min() * 100
        max_drawdown_duration = self._calculate_max_drawdown_duration(equity_df)
        
        # Trade statistics
        trades_df = pd.DataFrame(trades) if trades else pd.DataFrame()
        
        if len(trades_df) > 0:
            winning_trades = trades_df[trades_df['pnl'] > 0]
            losing_trades = trades_df[trades_df['pnl'] <= 0]
            
            win_rate = (len(winning_trades) / len(trades_df)) * 100
            avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
            avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
            profit_factor = abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum()) if len(losing_trades) > 0 and losing_trades['pnl'].sum() != 0 else 0
            
            avg_holding_period = trades_df['holding_period'].mean()
            largest_win = trades_df['pnl'].max()
            largest_loss = trades_df['pnl'].min()
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
            avg_holding_period = 0
            largest_win = 0
            largest_loss = 0
        
        # Calmar ratio
        calmar = abs(cagr / max_drawdown) if max_drawdown != 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_equity': final_equity,
            'total_return': total_return,
            'cagr': cagr,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'calmar_ratio': calmar,
            'max_drawdown': max_drawdown,
            'max_drawdown_duration': max_drawdown_duration,
            'total_trades': len(trades_df),
            'winning_trades': len(winning_trades) if len(trades_df) > 0 else 0,
            'losing_trades': len(losing_trades) if len(trades_df) > 0 else 0,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'avg_holding_period': avg_holding_period,
            'largest_win': largest_win,
            'largest_loss': largest_loss,
            'equity_curve': equity_df,
            'trades': trades_df,
            'daily_returns': returns_series,
            'drawdown_curve': equity_df['drawdown'],
            'period_days': days,
            'period_years': years
        }
    
    def _calculate_max_drawdown_duration(self, equity_df: pd.DataFrame) -> int:
        """Calculate maximum drawdown duration in days."""
        equity_df = equity_df.copy()
        equity_df['is_drawdown'] = equity_df['drawdown'] < 0
        
        max_duration = 0
        current_duration = 0
        
        for is_dd in equity_df['is_drawdown']:
            if is_dd:
                current_duration += 1
                max_duration = max(max_duration, current_duration)
            else:
                current_duration = 0
        
        return max_duration
    
    def compare_with_benchmark(
        self,
        strategy_results: Dict,
        benchmark_df: pd.DataFrame,
        benchmark_name: str = 'NIFTY 50'
    ) -> Dict:
        """Compare strategy performance with benchmark."""
        equity_curve = strategy_results['equity_curve']
        
        # Align dates
        if 'date' in benchmark_df.columns:
            benchmark_df = benchmark_df.set_index('date')
        
        common_dates = equity_curve.index.intersection(benchmark_df.index)
        
        if len(common_dates) == 0:
            return {'error': 'No common dates between strategy and benchmark'}
        
        strategy_equity = equity_curve.loc[common_dates, 'equity']
        benchmark_price = benchmark_df.loc[common_dates, 'close']
        
        # Normalize to same starting value
        strategy_normalized = (strategy_equity / strategy_equity.iloc[0]) * 100
        benchmark_normalized = (benchmark_price / benchmark_price.iloc[0]) * 100
        
        # Calculate returns
        strategy_returns = strategy_normalized.pct_change().dropna()
        benchmark_returns = benchmark_normalized.pct_change().dropna()
        
        # Metrics
        strategy_total_return = (strategy_normalized.iloc[-1] / strategy_normalized.iloc[0] - 1) * 100
        benchmark_total_return = (benchmark_normalized.iloc[-1] / benchmark_normalized.iloc[0] - 1) * 100
        
        alpha = strategy_total_return - benchmark_total_return
        
        # Beta
        if benchmark_returns.std() > 0:
            beta = strategy_returns.cov(benchmark_returns) / benchmark_returns.var()
        else:
            beta = 0
        
        # Correlation
        correlation = strategy_returns.corr(benchmark_returns)
        
        # Information ratio
        excess_returns = strategy_returns - benchmark_returns
        if excess_returns.std() > 0:
            information_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(Config.TRADING_DAYS_PER_YEAR)
        else:
            information_ratio = 0
        
        return {
            'benchmark_name': benchmark_name,
            'strategy_return': strategy_total_return,
            'benchmark_return': benchmark_total_return,
            'alpha': alpha,
            'beta': beta,
            'correlation': correlation,
            'information_ratio': information_ratio,
            'outperformance': alpha,
            'strategy_normalized': strategy_normalized,
            'benchmark_normalized': benchmark_normalized
        }



