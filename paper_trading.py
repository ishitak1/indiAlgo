"""
Paper Trading module for indiAlgo.
Virtual trading with realistic simulation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from config import Config
from data_manager import DataManager


class PaperTrading:
    """Paper trading system with virtual money."""
    
    def __init__(self, data_manager: DataManager, user_id: str = 'default'):
        self.data_manager = data_manager
        self.user_id = user_id
        self.accounts = {}
        self.orders = {}
        self.trades = {}
        self._initialize_account(user_id)
    
    def _initialize_account(self, user_id: str, initial_balance: float = 100000):
        """Initialize a paper trading account."""
        self.accounts[user_id] = {
            'user_id': user_id,
            'cash': initial_balance,
            'initial_balance': initial_balance,
            'holdings': {},  # {symbol: {'shares': int, 'avg_price': float}}
            'created_at': datetime.now().isoformat(),
            'total_trades': 0,
            'realized_pnl': 0
        }
        
        self.orders[user_id] = []
        self.trades[user_id] = []
    
    def place_order(
        self,
        user_id: str,
        symbol: str,
        order_type: str,  # 'MARKET', 'LIMIT', 'STOP'
        side: str,  # 'BUY' or 'SELL'
        quantity: int,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        exchange: str = 'NSE',
        commission: float = 0.001,
        slippage: float = 0.0005
    ) -> Dict:
        """
        Place an order.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            order_type: 'MARKET', 'LIMIT', or 'STOP'
            side: 'BUY' or 'SELL'
            quantity: Number of shares
            price: Limit price (for LIMIT orders)
            stop_price: Stop price (for STOP orders)
            exchange: NSE or BSE
            commission: Commission rate
            slippage: Slippage rate
        """
        if user_id not in self.accounts:
            self._initialize_account(user_id)
        
        # Get current market price
        try:
            df = self.data_manager.get_historical_data(symbol, exchange, years=1)
            if df.empty:
                return {'success': False, 'error': 'No data available for symbol'}
            current_price = df['close'].iloc[-1]
        except:
            return {'success': False, 'error': 'Error fetching price data'}
        
        # Determine execution price
        if order_type == 'MARKET':
            execution_price = current_price
        elif order_type == 'LIMIT':
            if price is None:
                return {'success': False, 'error': 'Limit price required for LIMIT orders'}
            if side == 'BUY' and current_price > price:
                # Limit not reached
                execution_price = None
            elif side == 'SELL' and current_price < price:
                # Limit not reached
                execution_price = None
            else:
                execution_price = price
        elif order_type == 'STOP':
            if stop_price is None:
                return {'success': False, 'error': 'Stop price required for STOP orders'}
            if side == 'BUY' and current_price < stop_price:
                execution_price = None
            elif side == 'SELL' and current_price > stop_price:
                execution_price = None
            else:
                execution_price = stop_price
        else:
            return {'success': False, 'error': 'Invalid order type'}
        
        # If order can't execute, store as pending
        if execution_price is None:
            order = {
                'order_id': f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'user_id': user_id,
                'symbol': symbol,
                'order_type': order_type,
                'side': side,
                'quantity': quantity,
                'price': price,
                'stop_price': stop_price,
                'status': 'PENDING',
                'created_at': datetime.now().isoformat(),
                'exchange': exchange
            }
            self.orders[user_id].append(order)
            return {'success': True, 'order_id': order['order_id'], 'status': 'PENDING'}
        
        # Execute order
        return self._execute_order(
            user_id, symbol, side, quantity, execution_price,
            exchange, commission, slippage
        )
    
    def _execute_order(
        self,
        user_id: str,
        symbol: str,
        side: str,
        quantity: int,
        price: float,
        exchange: str,
        commission: float,
        slippage: float
    ) -> Dict:
        """Execute an order."""
        account = self.accounts[user_id]
        
        # Apply slippage
        if side == 'BUY':
            execution_price = price * (1 + slippage)
            total_cost = quantity * execution_price * (1 + commission)
            
            if total_cost > account['cash']:
                return {'success': False, 'error': 'Insufficient funds'}
            
            # Update holdings
            if symbol in account['holdings']:
                old_shares = account['holdings'][symbol]['shares']
                old_avg_price = account['holdings'][symbol]['avg_price']
                new_shares = old_shares + quantity
                new_avg_price = ((old_shares * old_avg_price) + (quantity * execution_price)) / new_shares
                
                account['holdings'][symbol] = {
                    'shares': new_shares,
                    'avg_price': new_avg_price
                }
            else:
                account['holdings'][symbol] = {
                    'shares': quantity,
                    'avg_price': execution_price
                }
            
            account['cash'] -= total_cost
        
        else:  # SELL
            if symbol not in account['holdings']:
                return {'success': False, 'error': 'No position to sell'}
            
            holding = account['holdings'][symbol]
            if quantity > holding['shares']:
                return {'success': False, 'error': 'Insufficient shares'}
            
            execution_price = price * (1 - slippage)
            proceeds = quantity * execution_price * (1 - commission)
            cost_basis = quantity * holding['avg_price'] * (1 + commission)
            pnl = proceeds - cost_basis
            
            # Update holdings
            if quantity == holding['shares']:
                del account['holdings'][symbol]
            else:
                holding['shares'] -= quantity
            
            account['cash'] += proceeds
            account['realized_pnl'] += pnl
        
        # Record trade
        trade = {
            'trade_id': f"TRD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_id': user_id,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': execution_price,
            'value': total_cost if side == 'BUY' else proceeds,
            'pnl': pnl if side == 'SELL' else None,
            'timestamp': datetime.now().isoformat(),
            'exchange': exchange
        }
        
        self.trades[user_id].append(trade)
        account['total_trades'] += 1
        
        return {
            'success': True,
            'trade_id': trade['trade_id'],
            'execution_price': execution_price,
            'pnl': pnl if side == 'SELL' else None
        }
    
    def get_account_summary(self, user_id: str) -> Dict:
        """Get account summary with current positions and P&L."""
        if user_id not in self.accounts:
            return {}
        
        account = self.accounts[user_id]
        holdings = account['holdings']
        
        # Get current prices
        current_prices = {}
        total_holdings_value = 0
        unrealized_pnl = 0
        
        for symbol, holding in holdings.items():
            try:
                df = self.data_manager.get_historical_data(symbol, 'NSE', years=1)
                if not df.empty:
                    current_price = df['close'].iloc[-1]
                    current_prices[symbol] = current_price
                    position_value = holding['shares'] * current_price
                    cost_basis = holding['shares'] * holding['avg_price']
                    position_pnl = position_value - cost_basis
                    
                    total_holdings_value += position_value
                    unrealized_pnl += position_pnl
            except:
                current_prices[symbol] = holding['avg_price']
        
        total_value = account['cash'] + total_holdings_value
        total_pnl = account['realized_pnl'] + unrealized_pnl
        total_return = (total_pnl / account['initial_balance']) * 100
        
        return {
            'user_id': user_id,
            'cash': account['cash'],
            'holdings_value': total_holdings_value,
            'total_value': total_value,
            'realized_pnl': account['realized_pnl'],
            'unrealized_pnl': unrealized_pnl,
            'total_pnl': total_pnl,
            'total_return_pct': total_return,
            'total_trades': account['total_trades'],
            'holdings': holdings,
            'current_prices': current_prices
        }
    
    def get_trade_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get trade history for user."""
        if user_id not in self.trades:
            return []
        
        trades = self.trades[user_id]
        return trades[-limit:] if limit else trades
    
    def get_daily_summary(self, user_id: str, date: Optional[datetime] = None) -> Dict:
        """Get daily trading summary."""
        if date is None:
            date = datetime.now()
        
        if user_id not in self.trades:
            return {}
        
        # Filter trades for the day
        date_str = date.strftime('%Y-%m-%d')
        daily_trades = [
            t for t in self.trades[user_id]
            if t['timestamp'].startswith(date_str)
        ]
        
        daily_pnl = sum(t.get('pnl', 0) for t in daily_trades if t.get('pnl'))
        num_trades = len(daily_trades)
        
        return {
            'date': date_str,
            'num_trades': num_trades,
            'daily_pnl': daily_pnl,
            'trades': daily_trades
        }
    
    def add_trading_journal_entry(
        self,
        user_id: str,
        trade_id: str,
        notes: str,
        rating: Optional[int] = None  # 1-5
    ):
        """Add a journal entry for a trade."""
        if user_id not in self.trades:
            return
        
        # Find trade and add journal entry
        for trade in self.trades[user_id]:
            if trade['trade_id'] == trade_id:
                trade['journal'] = {
                    'notes': notes,
                    'rating': rating,
                    'created_at': datetime.now().isoformat()
                }
                break

