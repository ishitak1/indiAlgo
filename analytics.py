"""
Technical analysis and analytics module.
Computes indicators, returns, volatility, drawdowns, etc.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict
import ta
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands


class Analytics:
    """Computes technical indicators and analytics."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with OHLCV DataFrame.
        
        Expected columns: date, open, high, low, close, volume
        """
        self.df = df.copy()
        if 'date' in self.df.columns:
            self.df = self.df.set_index('date')
        self.df = self.df.sort_index()
    
    def add_returns(self, periods: list = [1, 5, 10, 30, 60, 90, 252]) -> pd.DataFrame:
        """Add returns for various periods."""
        for period in periods:
            self.df[f'return_{period}d'] = self.df['close'].pct_change(period)
        return self.df
    
    def add_moving_averages(self, periods: list = [5, 10, 20, 50, 100, 200]) -> pd.DataFrame:
        """Add simple and exponential moving averages."""
        for period in periods:
            sma = SMAIndicator(close=self.df['close'], window=period)
            self.df[f'sma_{period}'] = sma.sma_indicator()
            
            ema = EMAIndicator(close=self.df['close'], window=period)
            self.df[f'ema_{period}'] = ema.ema_indicator()
        return self.df
    
    def add_rsi(self, period: int = 14) -> pd.DataFrame:
        """Add RSI indicator."""
        rsi = RSIIndicator(close=self.df['close'], window=period)
        self.df['rsi'] = rsi.rsi()
        return self.df
    
    def add_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Add MACD indicator."""
        macd = MACD(close=self.df['close'], window_fast=fast, window_slow=slow, window_sign=signal)
        self.df['macd'] = macd.macd()
        self.df['macd_signal'] = macd.macd_signal()
        self.df['macd_diff'] = macd.macd_diff()
        return self.df
    
    def add_bollinger_bands(self, period: int = 20, std: float = 2) -> pd.DataFrame:
        """Add Bollinger Bands."""
        bb = BollingerBands(close=self.df['close'], window=period, window_dev=std)
        self.df['bb_upper'] = bb.bollinger_hband()
        self.df['bb_middle'] = bb.bollinger_mavg()
        self.df['bb_lower'] = bb.bollinger_lband()
        return self.df
    
    def add_volatility(self, period: int = 20) -> pd.DataFrame:
        """Add volatility (standard deviation of returns)."""
        returns = self.df['close'].pct_change()
        self.df['volatility'] = returns.rolling(window=period).std() * np.sqrt(252)  # Annualized
        return self.df
    
    def add_drawdown(self) -> pd.DataFrame:
        """Add drawdown metrics."""
        # Calculate running maximum
        self.df['running_max'] = self.df['close'].expanding().max()
        
        # Calculate drawdown
        self.df['drawdown'] = (self.df['close'] - self.df['running_max']) / self.df['running_max']
        
        # Calculate running drawdown
        self.df['running_drawdown'] = self.df['drawdown'].expanding().min()
        
        return self.df
    
    def compute_all_indicators(self) -> pd.DataFrame:
        """Compute all available indicators."""
        self.add_returns()
        self.add_moving_averages()
        self.add_rsi()
        self.add_macd()
        self.add_bollinger_bands()
        self.add_volatility()
        self.add_drawdown()
        return self.df
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics."""
        stats = {
            'total_return': (self.df['close'].iloc[-1] / self.df['close'].iloc[0] - 1) * 100,
            'annualized_return': ((self.df['close'].iloc[-1] / self.df['close'].iloc[0]) ** (252 / len(self.df)) - 1) * 100,
            'volatility': self.df['volatility'].iloc[-1] if 'volatility' in self.df.columns else None,
            'max_drawdown': self.df['drawdown'].min() * 100 if 'drawdown' in self.df.columns else None,
            'sharpe_ratio': None,
            'current_price': self.df['close'].iloc[-1],
            'high_52w': self.df['high'].rolling(252).max().iloc[-1] if len(self.df) >= 252 else self.df['high'].max(),
            'low_52w': self.df['low'].rolling(252).min().iloc[-1] if len(self.df) >= 252 else self.df['low'].min(),
        }
        
        # Calculate Sharpe ratio if we have returns
        if 'return_1d' in self.df.columns:
            returns = self.df['return_1d'].dropna()
            if len(returns) > 0:
                mean_return = returns.mean() * 252  # Annualized
                std_return = returns.std() * np.sqrt(252)  # Annualized
                if std_return > 0:
                    stats['sharpe_ratio'] = mean_return / std_return
        
        return stats
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the processed DataFrame."""
        return self.df.reset_index()



