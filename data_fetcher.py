"""
Data fetching module for NSE and BSE stocks and indices.
Supports yfinance and nsepython for data retrieval.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
from typing import Optional, List, Dict
import time


class DataFetcher:
    """Fetches stock data from NSE and BSE."""
    
    # Common NSE indices
    NSE_INDICES = {
        'NIFTY 50': '^NSEI',
        'NIFTY BANK': '^NSEBANK',
        'NIFTY IT': '^NSETIT',
        'NIFTY PHARMA': '^NSEPHARMA',
        'NIFTY FMCG': '^NSEFMCG',
        'NIFTY AUTO': '^NSEAUTO',
    }
    
    def __init__(self):
        self.cache = {}
    
    def get_nse_symbol(self, symbol: str) -> str:
        """Convert NSE symbol to yfinance format."""
        # NSE symbols typically need .NS suffix for yfinance
        if not symbol.endswith('.NS'):
            return f"{symbol}.NS"
        return symbol
    
    def get_bse_symbol(self, symbol: str) -> str:
        """Convert BSE symbol to yfinance format."""
        if not symbol.endswith('.BO'):
            return f"{symbol}.BO"
        return symbol
    
    def fetch_data(
        self,
        symbol: str,
        exchange: str = 'NSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = '1y'
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'TCS')
            exchange: 'NSE' or 'BSE'
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            period: Period if dates not specified ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Format symbol for yfinance
            if exchange == 'NSE':
                if symbol in self.NSE_INDICES:
                    yf_symbol = self.NSE_INDICES[symbol]
                else:
                    yf_symbol = self.get_nse_symbol(symbol)
            elif exchange == 'BSE':
                yf_symbol = self.get_bse_symbol(symbol)
            else:
                raise ValueError(f"Unsupported exchange: {exchange}")
            
            # Fetch data
            ticker = yf.Ticker(yf_symbol)
            
            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)
            
            if df.empty:
                raise ValueError(f"No data found for {symbol} on {exchange}")
            
            # Standardize column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            df.index.name = 'date'
            df = df.reset_index()
            
            # Ensure we have required columns
            required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            for col in required_cols:
                if col not in df.columns:
                    if col == 'volume' and 'vol' in df.columns:
                        df['volume'] = df['vol']
                    else:
                        raise ValueError(f"Missing required column: {col}")
            
            # Add metadata
            df['symbol'] = symbol
            df['exchange'] = exchange
            
            return df[['date', 'open', 'high', 'low', 'close', 'volume', 'symbol', 'exchange']]
        
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol} on {exchange}: {str(e)}")
    
    def fetch_multiple(
        self,
        symbols: List[str],
        exchange: str = 'NSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = '1y'
    ) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols."""
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.fetch_data(symbol, exchange, start_date, end_date, period)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Failed to fetch {symbol}: {e}")
                continue
        return results
    
    def get_available_indices(self, exchange: str = 'NSE') -> List[str]:
        """Get list of available indices."""
        if exchange == 'NSE':
            return list(self.NSE_INDICES.keys())
        return []
    
    def search_symbol(self, query: str, exchange: str = 'NSE') -> List[str]:
        """Search for symbols matching query."""
        # This is a simplified version - in production, you'd use a proper symbol database
        common_symbols = {
            'NSE': ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK', 
                   'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL', 'ITC', 'AXISBANK', 'ASIANPAINT',
                   'MARUTI', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'WIPRO', 'ONGC', 'POWERGRID'],
            'BSE': ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK']
        }
        
        query_upper = query.upper()
        return [s for s in common_symbols.get(exchange, []) if query_upper in s.upper()]



