"""
Data storage module using SQLite for local storage.
"""

import pandas as pd
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
import os


class DataStorage:
    """Handles data storage and retrieval from SQLite database."""
    
    def __init__(self, db_path: str = 'stock_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create main data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, symbol, exchange)
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_symbol_date 
            ON stock_data(symbol, exchange, date)
        ''')
        
        # Create metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                first_date DATE,
                last_date DATE,
                last_updated TIMESTAMP,
                PRIMARY KEY (symbol, exchange)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_data(self, df: pd.DataFrame, symbol: str, exchange: str):
        """Store DataFrame to database."""
        if df.empty:
            return
        
        conn = sqlite3.connect(self.db_path)
        
        # Prepare data
        df_to_store = df.copy()
        df_to_store['symbol'] = symbol
        df_to_store['exchange'] = exchange
        
        # Store data (replace on conflict)
        df_to_store[['date', 'symbol', 'exchange', 'open', 'high', 'low', 'close', 'volume']].to_sql(
            'stock_data',
            conn,
            if_exists='append',
            index=False,
            method='multi'
        )
        
        # Update metadata
        first_date = df_to_store['date'].min()
        last_date = df_to_store['date'].max()
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (symbol, exchange, first_date, last_date, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, exchange, first_date, last_date, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_data(
        self,
        symbol: str,
        exchange: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """Retrieve data from database."""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT date, open, high, low, close, volume
            FROM stock_data
            WHERE symbol = ? AND exchange = ?
        '''
        params = [symbol, exchange]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date'
        
        df = pd.read_sql_query(query, conn, params=params, parse_dates=['date'])
        conn.close()
        
        return df
    
    def get_available_symbols(self, exchange: Optional[str] = None) -> List[Tuple[str, str]]:
        """Get list of available symbols."""
        conn = sqlite3.connect(self.db_path)
        
        if exchange:
            query = 'SELECT DISTINCT symbol, exchange FROM metadata WHERE exchange = ?'
            cursor = conn.cursor()
            cursor.execute(query, (exchange,))
        else:
            query = 'SELECT DISTINCT symbol, exchange FROM metadata'
            cursor = conn.cursor()
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_date_range(self, symbol: str, exchange: str) -> Tuple[Optional[str], Optional[str]]:
        """Get available date range for a symbol."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT first_date, last_date
            FROM metadata
            WHERE symbol = ? AND exchange = ?
        ''', (symbol, exchange))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        return None, None
    
    def clear_data(self, symbol: Optional[str] = None, exchange: Optional[str] = None):
        """Clear data for a symbol or all data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if symbol and exchange:
            cursor.execute('DELETE FROM stock_data WHERE symbol = ? AND exchange = ?', (symbol, exchange))
            cursor.execute('DELETE FROM metadata WHERE symbol = ? AND exchange = ?', (symbol, exchange))
        else:
            cursor.execute('DELETE FROM stock_data')
            cursor.execute('DELETE FROM metadata')
        
        conn.commit()
        conn.close()



