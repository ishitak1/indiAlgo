"""
Configuration management for IndiaQuant platform.
"""

import os
from pathlib import Path
from typing import Dict, List
import json


class Config:
    """Central configuration for indiAlgo."""
    
    # Platform info
    PLATFORM_NAME = "indiAlgo"
    VERSION = "2.0.0"
    PREMIUM_ENABLED = True
    
    # Data paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    CACHE_DIR = DATA_DIR / "cache"
    STRATEGIES_DIR = BASE_DIR / "strategies"
    EXPORTS_DIR = BASE_DIR / "exports"
    
    # Database
    DB_PATH = DATA_DIR / "indiaquant.db"
    
    # Data settings
    DEFAULT_START_YEAR = 2015  # Default historical data start
    MAX_HISTORICAL_YEARS = 10
    CACHE_EXPIRY_DAYS = 1  # Cache expiry in days
    
    # API settings
    YFINANCE_TIMEOUT = 30
    REQUEST_DELAY = 0.2  # Delay between API calls (seconds)
    MAX_RETRIES = 3
    
    # Backtesting defaults
    DEFAULT_INITIAL_CAPITAL = 100000
    DEFAULT_COMMISSION = 0.001  # 0.1%
    DEFAULT_SLIPPAGE = 0.0005  # 0.05%
    
    # Stock grouping
    SECTORS = [
        "Banking", "IT", "FMCG", "Pharma", "Auto", "Oil & Gas",
        "Cement", "Metals", "Power", "Telecom", "Infrastructure",
        "Consumer Durables", "Paints", "Financial Services", "Insurance",
        "Real Estate", "Textiles", "Chemicals", "Media", "Retail"
    ]
    
    MARKET_CAP_CATEGORIES = ["Large Cap", "Mid Cap", "Small Cap", "Micro Cap"]
    
    # Technical indicators
    DEFAULT_MA_PERIODS = [5, 10, 20, 50, 100, 200]
    DEFAULT_RSI_PERIOD = 14
    DEFAULT_MACD_FAST = 12
    DEFAULT_MACD_SLOW = 26
    DEFAULT_MACD_SIGNAL = 9
    
    # Performance metrics
    RISK_FREE_RATE = 6.0  # Annual risk-free rate (%)
    TRADING_DAYS_PER_YEAR = 252
    
    @classmethod
    def initialize_directories(cls):
        """Create necessary directories."""
        for directory in [cls.DATA_DIR, cls.CACHE_DIR, cls.STRATEGIES_DIR, cls.EXPORTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_stock_groups(cls) -> Dict[str, List[str]]:
        """Get predefined stock groups."""
        return {
            "Nifty 50": [
                "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK",
                "KOTAKBANK", "LT", "SBIN", "BHARTIARTL", "ITC", "AXISBANK",
                "ASIANPAINT", "MARUTI", "TITAN", "ULTRACEMCO", "NESTLEIND",
                "WIPRO", "ONGC", "POWERGRID", "BAJFINANCE", "HDFC", "SBILIFE",
                "HDFCLIFE", "SUNPHARMA", "DRREDDY", "CIPLA", "TATASTEEL",
                "JSWSTEEL", "HINDALCO", "VEDL", "NTPC", "TATAPOWER", "M&M",
                "TATAMOTORS", "BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO"
            ],
            "Banking": [
                "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "SBIN",
                "INDUSINDBK", "FEDERALBNK", "BANDHANBNK", "PNB", "UNIONBANK"
            ],
            "IT": [
                "TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", "LTIM", "MPHASIS",
                "PERSISTENT", "MINDTREE", "COFORGE"
            ],
            "Pharma": [
                "SUNPHARMA", "DRREDDY", "CIPLA", "LUPIN", "TORNTPHARM",
                "GLENMARK", "CADILAHC", "DIVISLAB", "BIOCON"
            ],
            "FMCG": [
                "HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR",
                "MARICO", "GODREJCP", "EMAMILTD"
            ]
        }



