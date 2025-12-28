"""
Custom rule engine for evaluating trading conditions.
Supports Python-like expressions for screening and strategy rules.
"""

import pandas as pd
import numpy as np
from typing import Dict, Callable, Any
import re


class RuleEngine:
    """Evaluates custom rules/conditions on stock data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with DataFrame containing technical indicators.
        
        Args:
            df: DataFrame with columns like close, sma_50, rsi, volume, etc.
        """
        self.df = df.copy()
        if 'date' in self.df.columns:
            self.df = self.df.set_index('date')
        self.df = self.df.sort_index()
        
        # Available functions
        self.functions = {
            'sma': self._sma,
            'ema': self._ema,
            'rsi': self._rsi,
            'macd': self._macd,
            'price': self._price,
            'close': self._close,
            'open': self._open,
            'high': self._high,
            'low': self._low,
            'volume': self._volume,
            'volatility': self._volatility,
            'max': lambda x, y: np.maximum(x, y),
            'min': lambda x, y: np.minimum(x, y),
            'abs': np.abs,
        }
    
    def _sma(self, period: int) -> pd.Series:
        """Simple Moving Average."""
        col = f'sma_{period}'
        if col in self.df.columns:
            return self.df[col]
        return self.df['close'].rolling(window=period).mean()
    
    def _ema(self, period: int) -> pd.Series:
        """Exponential Moving Average."""
        col = f'ema_{period}'
        if col in self.df.columns:
            return self.df[col]
        return self.df['close'].ewm(span=period).mean()
    
    def _rsi(self, period: int = 14) -> pd.Series:
        """RSI indicator."""
        if 'rsi' in self.df.columns:
            return self.df['rsi']
        # Calculate RSI if not present
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _macd(self) -> pd.Series:
        """MACD indicator."""
        if 'macd' in self.df.columns:
            return self.df['macd']
        ema12 = self.df['close'].ewm(span=12).mean()
        ema26 = self.df['close'].ewm(span=26).mean()
        return ema12 - ema26
    
    def _price(self) -> pd.Series:
        """Current price (alias for close)."""
        return self.df['close']
    
    def _close(self) -> pd.Series:
        """Close price."""
        return self.df['close']
    
    def _open(self) -> pd.Series:
        """Open price."""
        return self.df['open']
    
    def _high(self) -> pd.Series:
        """High price."""
        return self.df['high']
    
    def _low(self) -> pd.Series:
        """Low price."""
        return self.df['low']
    
    def _volume(self) -> pd.Series:
        """Volume."""
        return self.df['volume']
    
    def _volatility(self, period: int = 20) -> pd.Series:
        """Volatility."""
        if 'volatility' in self.df.columns:
            return self.df['volatility']
        returns = self.df['close'].pct_change()
        return returns.rolling(window=period).std() * np.sqrt(252)
    
    def _parse_expression(self, expression: str) -> str:
        """Parse and convert expression to valid Python code."""
        # Replace common patterns
        expr = expression.strip()
        
        # Replace function calls like sma(50) with function calls
        # This is a simplified parser - for production, use a proper AST parser
        pattern = r'(\w+)\s*\(\s*(\d+)\s*\)'
        
        def replace_func(match):
            func_name = match.group(1)
            arg = match.group(2)
            if func_name in self.functions:
                return f"self.functions['{func_name}']({arg})"
            return match.group(0)
        
        expr = re.sub(pattern, replace_func, expr)
        
        # Replace standalone function names (like price, close, volume)
        # Do this in reverse order to avoid partial matches
        func_names = ['volatility', 'macd', 'rsi', 'volume', 'price', 'close', 'open', 'high', 'low']
        for func_name in func_names:
            if func_name in self.functions:
                # Replace standalone words (not part of other words)
                pattern = r'\b' + func_name + r'\b'
                # Only replace if not already a function call
                if not re.search(r'\b' + func_name + r'\s*\(', expr):
                    expr = re.sub(pattern, f"self.functions['{func_name}']()", expr)
        
        return expr
    
    def evaluate_rule(self, rule: str) -> pd.Series:
        """
        Evaluate a custom rule expression.
        
        Examples:
            "rsi(14) < 30 and price > sma(200)"
            "close > sma(50) and volume > 1000000"
            "rsi < 40 and price > sma(200) and volume > sma(20)"
        
        Returns:
            Boolean Series indicating where rule is True
        """
        try:
            # Parse the expression
            parsed = self._parse_expression(rule)
            
            # Create a safe evaluation context
            safe_dict = {
                'self': self,
                'pd': pd,
                'np': np,
                'True': True,
                'False': False,
                'and': lambda x, y: x & y,
                'or': lambda x, y: x | y,
                'not': lambda x: ~x,
            }
            
            # Evaluate
            result = eval(parsed, {"__builtins__": {}}, safe_dict)
            
            if isinstance(result, pd.Series):
                return result.fillna(False)
            elif isinstance(result, (bool, np.bool_)):
                return pd.Series([result] * len(self.df), index=self.df.index)
            else:
                raise ValueError(f"Rule evaluation returned unexpected type: {type(result)}")
        
        except Exception as e:
            raise ValueError(f"Error evaluating rule '{rule}': {str(e)}")
    
    def filter_by_rule(self, rule: str) -> pd.DataFrame:
        """Filter DataFrame by rule, returning only rows where rule is True."""
        mask = self.evaluate_rule(rule)
        return self.df[mask].reset_index()
    
    def get_rule_signals(self, buy_rule: str, sell_rule: str) -> pd.DataFrame:
        """
        Get buy and sell signals based on rules.
        
        Returns:
            DataFrame with 'signal' column (1 for buy, -1 for sell, 0 for hold)
        """
        buy_mask = self.evaluate_rule(buy_rule)
        sell_mask = self.evaluate_rule(sell_rule)
        
        signals = pd.Series(0, index=self.df.index)
        signals[buy_mask] = 1
        signals[sell_mask] = -1
        
        result = self.df.copy()
        result['signal'] = signals
        return result.reset_index()

