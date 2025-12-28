"""
Enhanced data manager with multi-year historical data support and intelligent caching.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import pickle
import hashlib
from typing import Optional, List, Dict, Tuple
import sqlite3
import json
from config import Config
from data_fetcher import DataFetcher


class DataManager:
    """Manages stock data with caching and multi-year historical support."""
    
    def __init__(self):
        Config.initialize_directories()
        self.data_fetcher = DataFetcher()
        self.cache_dir = Config.CACHE_DIR
        self.db_path = Config.DB_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize database for metadata and cache tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Stock metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_metadata (
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                name TEXT,
                sector TEXT,
                industry TEXT,
                market_cap_category TEXT,
                first_available_date DATE,
                last_updated_date DATE,
                data_quality_score REAL,
                PRIMARY KEY (symbol, exchange)
            )
        ''')
        
        # Data cache tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_cache (
                cache_key TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                cached_date TIMESTAMP,
                row_count INTEGER,
                file_path TEXT
            )
        ''')
        
        # Stock groups
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_groups (
                group_name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (group_name, symbol, exchange)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_historical_data(
        self,
        symbol: str,
        exchange: str = 'NSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        years: Optional[int] = None,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Get historical data with intelligent caching.
        
        Args:
            symbol: Stock symbol
            exchange: NSE or BSE
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            years: Number of years of history (alternative to dates)
            use_cache: Use cached data if available
        
        Returns:
            DataFrame with OHLCV data
        """
        # Determine date range
        if years:
            end_date = datetime.now() if not end_date else pd.to_datetime(end_date)
            start_date = end_date - timedelta(days=years * 365)
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
        elif not start_date:
            # Default to max available
            start_date = f"{datetime.now().year - Config.MAX_HISTORICAL_YEARS}-01-01"
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Check cache
        cache_key = self._get_cache_key(symbol, exchange, start_date, end_date)
        
        if use_cache:
            cached_data = self._load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Fetch data
        try:
            df = self.data_fetcher.fetch_data(
                symbol, exchange, start_date=start_date, end_date=end_date
            )
            
            if not df.empty:
                # Clean and validate data
                df = self._clean_data(df)
                
                # Update metadata
                self._update_metadata(symbol, exchange, df)
                
                # Cache data
                if use_cache:
                    self._save_to_cache(cache_key, df, symbol, exchange, start_date, end_date)
            
            return df
        
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_multiple_stocks(
        self,
        symbols: List[str],
        exchange: str = 'NSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        years: Optional[int] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols with progress tracking."""
        results = {}
        total = len(symbols)
        
        for idx, symbol in enumerate(symbols):
            if progress_callback:
                progress_callback(idx + 1, total, symbol)
            
            df = self.get_historical_data(
                symbol, exchange, start_date, end_date, years
            )
            
            if not df.empty:
                results[symbol] = df
        
        return results
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate stock data."""
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date'], keep='last')
        
        # Sort by date
        df = df.sort_values('date')
        
        # Fill missing values (forward fill for OHLCV)
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].fillna(method='ffill')
        
        # Remove rows with invalid prices
        df = df[
            (df['close'] > 0) &
            (df['high'] >= df['low']) &
            (df['high'] >= df['close']) &
            (df['low'] <= df['close'])
        ]
        
        return df
    
    def _get_cache_key(self, symbol: str, exchange: str, start_date: str, end_date: str) -> str:
        """Generate cache key."""
        key_string = f"{exchange}_{symbol}_{start_date}_{end_date}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _save_to_cache(
        self,
        cache_key: str,
        df: pd.DataFrame,
        symbol: str,
        exchange: str,
        start_date: str,
        end_date: str
    ):
        """Save data to cache."""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            df.to_pickle(cache_file)
            
            # Update cache tracking
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO data_cache
                (cache_key, symbol, exchange, start_date, end_date, cached_date, row_count, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cache_key, symbol, exchange, start_date, end_date,
                datetime.now(), len(df), str(cache_file)
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error caching data: {e}")
    
    def _load_from_cache(self, cache_key: str) -> Optional[pd.DataFrame]:
        """Load data from cache if valid."""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if not cache_file.exists():
            return None
        
        # Check cache age
        cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if cache_age.days > Config.CACHE_EXPIRY_DAYS:
            return None
        
        try:
            df = pd.read_pickle(cache_file)
            return df
        except:
            return None
    
    def _update_metadata(self, symbol: str, exchange: str, df: pd.DataFrame):
        """Update stock metadata."""
        if df.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        first_date = df['date'].min()
        last_date = df['date'].max()
        
        # Calculate data quality score
        total_days = (pd.to_datetime(last_date) - pd.to_datetime(first_date)).days
        actual_days = len(df)
        quality_score = (actual_days / total_days) * 100 if total_days > 0 else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO stock_metadata
            (symbol, exchange, first_available_date, last_updated_date, data_quality_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, exchange, first_date, last_date, quality_score))
        
        conn.commit()
        conn.close()
    
    def create_stock_group(self, group_name: str, symbols: List[str], exchange: str = 'NSE'):
        """Create a custom stock group."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for symbol in symbols:
            cursor.execute('''
                INSERT OR REPLACE INTO stock_groups (group_name, symbol, exchange)
                VALUES (?, ?, ?)
            ''', (group_name, symbol, exchange))
        
        conn.commit()
        conn.close()
    
    def get_stock_group(self, group_name: str) -> List[Tuple[str, str]]:
        """Get stocks in a group."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT symbol, exchange FROM stock_groups
            WHERE group_name = ?
        ''', (group_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def list_stock_groups(self) -> List[str]:
        """List all stock groups."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT group_name FROM stock_groups')
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_stock_universe(
        self,
        exchange: Optional[str] = None,
        sector: Optional[str] = None,
        market_cap: Optional[str] = None,
        group_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Get filtered stock universe."""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT DISTINCT symbol, exchange FROM stock_metadata WHERE 1=1"
        params = []
        
        if exchange:
            query += " AND exchange = ?"
            params.append(exchange)
        
        if sector:
            query += " AND sector = ?"
            params.append(sector)
        
        if market_cap:
            query += " AND market_cap_category = ?"
            params.append(market_cap)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        # If group specified, filter by group
        if group_name:
            group_stocks = self.get_stock_group(group_name)
            group_symbols = [s[0] for s in group_stocks]
            df = df[df['symbol'].isin(group_symbols)]
        
        return df



