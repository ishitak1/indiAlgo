"""
Fundamental data fetching module.
Fetches company fundamentals: P/E, P/B, ROE, Debt/Equity, etc.
"""

import pandas as pd
import yfinance as yf
from typing import Dict, Optional
import requests
import time


class FundamentalData:
    """Fetches and processes fundamental data for stocks."""
    
    def __init__(self):
        self.cache = {}
    
    def get_fundamentals(self, symbol: str, exchange: str = 'NSE') -> Dict:
        """
        Get fundamental data for a stock.
        
        Returns:
            Dictionary with fundamental metrics
        """
        try:
            # Format symbol for yfinance
            if exchange == 'NSE':
                yf_symbol = f"{symbol}.NS"
            elif exchange == 'BSE':
                yf_symbol = f"{symbol}.BO"
            else:
                raise ValueError(f"Unsupported exchange: {exchange}")
            
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            fundamentals = {
                'symbol': symbol,
                'exchange': exchange,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                
                # Valuation metrics
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'peg_ratio': info.get('pegRatio', None),
                'price_to_book': info.get('priceToBook', None),
                'price_to_sales': info.get('priceToSalesTrailing12Months', None),
                'enterprise_value': info.get('enterpriseValue', None),
                'market_cap': info.get('marketCap', None),
                
                # Profitability
                'roe': info.get('returnOnEquity', None),
                'roa': info.get('returnOnAssets', None),
                'profit_margin': info.get('profitMargins', None),
                'operating_margin': info.get('operatingMargins', None),
                'gross_margin': info.get('grossMargins', None),
                
                # Financial health
                'debt_to_equity': info.get('debtToEquity', None),
                'current_ratio': info.get('currentRatio', None),
                'quick_ratio': info.get('quickRatio', None),
                'cash_per_share': info.get('totalCashPerShare', None),
                
                # Growth
                'revenue_growth': info.get('revenueGrowth', None),
                'earnings_growth': info.get('earningsGrowth', None),
                'earnings_quarterly_growth': info.get('earningsQuarterlyGrowth', None),
                
                # Dividends
                'dividend_yield': info.get('dividendYield', None),
                'payout_ratio': info.get('payoutRatio', None),
                
                # Price data
                'current_price': info.get('currentPrice', None),
                '52w_high': info.get('fiftyTwoWeekHigh', None),
                '52w_low': info.get('fiftyTwoWeekLow', None),
                'beta': info.get('beta', None),
                
                # Volume
                'average_volume': info.get('averageVolume', None),
                'average_volume_10days': info.get('averageVolume10days', None),
                
                # Other
                'book_value': info.get('bookValue', None),
                'eps': info.get('trailingEps', None),
                'forward_eps': info.get('forwardEps', None),
            }
            
            return fundamentals
        
        except Exception as e:
            print(f"Error fetching fundamentals for {symbol}: {e}")
            return self._get_default_fundamentals(symbol, exchange)
    
    def _get_default_fundamentals(self, symbol: str, exchange: str) -> Dict:
        """Return default/empty fundamentals if fetch fails."""
        return {
            'symbol': symbol,
            'exchange': exchange,
            'company_name': symbol,
            'sector': 'N/A',
            'industry': 'N/A',
            'pe_ratio': None,
            'roe': None,
            'debt_to_equity': None,
            # Add other fields as None
        }
    
    def get_fundamentals_batch(self, symbols: list, exchange: str = 'NSE') -> pd.DataFrame:
        """Get fundamentals for multiple symbols."""
        results = []
        for symbol in symbols:
            try:
                fundamentals = self.get_fundamentals(symbol, exchange)
                results.append(fundamentals)
                time.sleep(0.2)  # Rate limiting
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def calculate_additional_metrics(self, fundamentals_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate additional derived metrics."""
        df = fundamentals_df.copy()
        
        # Price to earnings growth
        if 'pe_ratio' in df.columns and 'earnings_growth' in df.columns:
            df['peg_ratio_calc'] = df['pe_ratio'] / (df['earnings_growth'] * 100) if df['earnings_growth'].notna().any() else None
        
        # Market cap category
        if 'market_cap' in df.columns:
            def categorize_market_cap(mcap):
                if pd.isna(mcap):
                    return 'Unknown'
                mcap_cr = mcap / 1e7  # Convert to crores
                if mcap_cr >= 20000:
                    return 'Large Cap'
                elif mcap_cr >= 5000:
                    return 'Mid Cap'
                else:
                    return 'Small Cap'
            
            df['market_cap_category'] = df['market_cap'].apply(categorize_market_cap)
        
        # Valuation score (lower is better)
        valuation_cols = ['pe_ratio', 'price_to_book', 'price_to_sales']
        df['valuation_score'] = 0
        for col in valuation_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Normalize and add to score
                normalized = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-10)
                df['valuation_score'] += normalized.fillna(0)
        
        return df



