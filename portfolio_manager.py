"""
Portfolio Manager module for indiAlgo.
Manages multiple portfolios with comprehensive analytics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import Config
from data_manager import DataManager
from analytics import Analytics


class PortfolioManager:
    """Manages user portfolios with comprehensive tracking."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.portfolios = {}
    
    def create_portfolio(
        self,
        portfolio_name: str,
        initial_capital: float = 100000,
        benchmark: str = 'NIFTY 50',
        description: Optional[str] = None
    ) -> Dict:
        """Create a new portfolio."""
        portfolio = {
            'name': portfolio_name,
            'initial_capital': initial_capital,
            'current_capital': initial_capital,
            'benchmark': benchmark,
            'description': description,
            'holdings': {},  # {symbol: {'shares': int, 'avg_price': float, 'entry_date': date}}
            'cash': initial_capital,
            'created_at': datetime.now().isoformat(),
            'trades': [],
            'realized_pnl': 0,
            'unrealized_pnl': 0
        }
        
        self.portfolios[portfolio_name] = portfolio
        return portfolio
    
    def add_position(
        self,
        portfolio_name: str,
        symbol: str,
        shares: int,
        price: float,
        exchange: str = 'NSE',
        commission: float = 0.001
    ) -> bool:
        """Add a position to portfolio."""
        if portfolio_name not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_name]
        cost = shares * price * (1 + commission)
        
        if cost > portfolio['cash']:
            return False
        
        # Update holdings
        if symbol in portfolio['holdings']:
            # Average price calculation
            old_shares = portfolio['holdings'][symbol]['shares']
            old_avg_price = portfolio['holdings'][symbol]['avg_price']
            total_cost = (old_shares * old_avg_price) + (shares * price)
            new_shares = old_shares + shares
            new_avg_price = total_cost / new_shares
            
            portfolio['holdings'][symbol] = {
                'shares': new_shares,
                'avg_price': new_avg_price,
                'entry_date': portfolio['holdings'][symbol]['entry_date'],
                'exchange': exchange
            }
        else:
            portfolio['holdings'][symbol] = {
                'shares': shares,
                'avg_price': price,
                'entry_date': datetime.now().isoformat(),
                'exchange': exchange
            }
        
        portfolio['cash'] -= cost
        portfolio['current_capital'] -= cost
        
        # Record trade
        portfolio['trades'].append({
            'date': datetime.now().isoformat(),
            'type': 'BUY',
            'symbol': symbol,
            'shares': shares,
            'price': price,
            'value': cost
        })
        
        return True
    
    def remove_position(
        self,
        portfolio_name: str,
        symbol: str,
        shares: int,
        price: float,
        commission: float = 0.001
    ) -> bool:
        """Remove a position from portfolio."""
        if portfolio_name not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_name]
        
        if symbol not in portfolio['holdings']:
            return False
        
        holding = portfolio['holdings'][symbol]
        
        if shares > holding['shares']:
            return False
        
        # Calculate P&L
        proceeds = shares * price * (1 - commission)
        cost_basis = shares * holding['avg_price'] * (1 + commission)
        pnl = proceeds - cost_basis
        
        # Update holdings
        if shares == holding['shares']:
            del portfolio['holdings'][symbol]
        else:
            holding['shares'] -= shares
        
        portfolio['cash'] += proceeds
        portfolio['current_capital'] += proceeds
        portfolio['realized_pnl'] += pnl
        
        # Record trade
        portfolio['trades'].append({
            'date': datetime.now().isoformat(),
            'type': 'SELL',
            'symbol': symbol,
            'shares': shares,
            'price': price,
            'value': proceeds,
            'pnl': pnl
        })
        
        return True
    
    def get_portfolio_value(
        self,
        portfolio_name: str,
        current_prices: Optional[Dict[str, float]] = None
    ) -> Dict:
        """Get current portfolio value and metrics."""
        if portfolio_name not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_name]
        holdings = portfolio['holdings']
        
        if not current_prices:
            # Fetch current prices
            current_prices = {}
            for symbol, holding in holdings.items():
                try:
                    df = self.data_manager.get_historical_data(
                        symbol, holding['exchange'], years=1
                    )
                    if not df.empty:
                        current_prices[symbol] = df['close'].iloc[-1]
                except:
                    current_prices[symbol] = holding['avg_price']
        
        # Calculate values
        total_value = portfolio['cash']
        unrealized_pnl = 0
        
        for symbol, holding in holdings.items():
            current_price = current_prices.get(symbol, holding['avg_price'])
            position_value = holding['shares'] * current_price
            cost_basis = holding['shares'] * holding['avg_price']
            position_pnl = position_value - cost_basis
            
            total_value += position_value
            unrealized_pnl += position_pnl
        
        portfolio['unrealized_pnl'] = unrealized_pnl
        total_pnl = portfolio['realized_pnl'] + unrealized_pnl
        total_return = (total_pnl / portfolio['initial_capital']) * 100
        
        return {
            'portfolio_name': portfolio_name,
            'initial_capital': portfolio['initial_capital'],
            'current_value': total_value,
            'cash': portfolio['cash'],
            'holdings_value': total_value - portfolio['cash'],
            'realized_pnl': portfolio['realized_pnl'],
            'unrealized_pnl': unrealized_pnl,
            'total_pnl': total_pnl,
            'total_return_pct': total_return,
            'holdings': holdings,
            'current_prices': current_prices
        }
    
    def get_sector_allocation(self, portfolio_name: str) -> Dict:
        """Get sector allocation of portfolio."""
        if portfolio_name not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_name]
        holdings = portfolio['holdings']
        
        # This would need sector data from stock metadata
        # For now, return placeholder
        sector_allocation = {}
        
        return sector_allocation
    
    def calculate_risk_metrics(
        self,
        portfolio_name: str,
        period_days: int = 252
    ) -> Dict:
        """Calculate portfolio risk metrics."""
        if portfolio_name not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_name]
        holdings = portfolio['holdings']
        
        # Get historical returns for all holdings
        returns_data = {}
        
        for symbol, holding in holdings.items():
            try:
                df = self.data_manager.get_historical_data(
                    symbol, holding['exchange'], years=2
                )
                if not df.empty and len(df) >= period_days:
                    returns = df['close'].pct_change().dropna()
                    returns_data[symbol] = returns.tail(period_days)
            except:
                continue
        
        if not returns_data:
            return {}
        
        # Calculate portfolio returns (weighted)
        portfolio_returns = None
        
        for symbol, returns in returns_data.items():
            holding = holdings[symbol]
            weight = (holding['shares'] * holding['avg_price']) / portfolio['initial_capital']
            
            if portfolio_returns is None:
                portfolio_returns = returns * weight
            else:
                # Align dates and add
                aligned = returns.reindex(portfolio_returns.index, fill_value=0)
                portfolio_returns += aligned * weight
        
        if portfolio_returns is None or len(portfolio_returns) == 0:
            return {}
        
        # Calculate metrics
        volatility = portfolio_returns.std() * np.sqrt(Config.TRADING_DAYS_PER_YEAR) * 100
        mean_return = portfolio_returns.mean() * Config.TRADING_DAYS_PER_YEAR * 100
        
        if volatility > 0:
            sharpe = (mean_return - Config.RISK_FREE_RATE) / volatility
        else:
            sharpe = 0
        
        # Max drawdown
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Correlation matrix
        returns_df = pd.DataFrame(returns_data)
        correlation_matrix = returns_df.corr()
        
        return {
            'volatility_pct': volatility,
            'sharpe_ratio': sharpe,
            'max_drawdown_pct': max_drawdown,
            'mean_return_pct': mean_return,
            'correlation_matrix': correlation_matrix,
            'portfolio_returns': portfolio_returns
        }
    
    def compare_with_benchmark(
        self,
        portfolio_name: str,
        benchmark_data: pd.DataFrame
    ) -> Dict:
        """Compare portfolio performance with benchmark."""
        portfolio_value = self.get_portfolio_value(portfolio_name)
        
        # Calculate portfolio returns over time
        # This would need historical portfolio values
        # For now, return placeholder
        
        return {
            'portfolio_return': portfolio_value.get('total_return_pct', 0),
            'benchmark_return': 0,  # Would calculate from benchmark_data
            'alpha': 0,
            'beta': 0
        }
    
    def list_portfolios(self) -> List[str]:
        """List all portfolio names."""
        return list(self.portfolios.keys())
    
    def get_portfolio(self, portfolio_name: str) -> Optional[Dict]:
        """Get portfolio details."""
        return self.portfolios.get(portfolio_name)
