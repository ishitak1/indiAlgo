"""
Comprehensive NSE stock list fetcher.
Fetches all NSE listed stocks from online sources.
"""

import pandas as pd
import requests
from typing import List, Dict
import json


class NSEStockList:
    """Fetches comprehensive NSE stock list."""
    
    def __init__(self):
        self.nse_equity_list_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/csv',
        }
    
    def fetch_all_nse_stocks(self) -> pd.DataFrame:
        """
        Fetch all NSE listed stocks from NSE website.
        Returns DataFrame with symbol, name, and other details.
        """
        try:
            # Try to fetch from NSE
            response = requests.get(self.nse_equity_list_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                # Read CSV
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                
                # Standardize columns
                if 'SYMBOL' in df.columns:
                    df = df.rename(columns={'SYMBOL': 'symbol', 'NAME OF COMPANY': 'name'})
                
                df['exchange'] = 'NSE'
                return df[['symbol', 'name', 'exchange']]
        except Exception as e:
            print(f"Error fetching from NSE: {e}")
        
        # Fallback to comprehensive list
        return self._get_comprehensive_fallback_list()
    
    def _get_comprehensive_fallback_list(self) -> pd.DataFrame:
        """Comprehensive fallback list of NSE stocks."""
        stocks = []
        
        # Nifty 50 stocks
        nifty50 = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK', 'KOTAKBANK',
            'LT', 'SBIN', 'BHARTIARTL', 'ITC', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'TITAN',
            'ULTRACEMCO', 'NESTLEIND', 'WIPRO', 'ONGC', 'POWERGRID', 'BAJFINANCE', 'HDFC',
            'SBILIFE', 'HDFCLIFE', 'SUNPHARMA', 'DRREDDY', 'CIPLA', 'TATASTEEL', 'JSWSTEEL',
            'HINDALCO', 'VEDL', 'NTPC', 'TATAPOWER', 'M&M', 'TATAMOTORS', 'BAJAJ-AUTO',
            'EICHERMOT', 'HEROMOTOCO', 'ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'BAJAJFINSV',
            'BPCL', 'COALINDIA', 'DIVISLAB', 'GRASIM', 'HCLTECH', 'INDUSINDBK', 'JINDALSTEL',
            'MARICO', 'NTPC', 'RELIANCE', 'TECHM', 'ULTRACEMCO'
        ]
        
        # Banking
        banking = [
            'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'AXISBANK', 'SBIN', 'INDUSINDBK',
            'FEDERALBNK', 'BANDHANBNK', 'PNB', 'UNIONBANK', 'IDFCFIRSTB', 'RBLBANK',
            'YESBANK', 'SOUTHBANK', 'CANBK', 'BANKBARODA', 'CENTRALBK', 'INDIANB'
        ]
        
        # IT
        it = [
            'TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM', 'LTIM', 'MPHASIS', 'PERSISTENT',
            'MINDTREE', 'COFORGE', 'LTI', 'ZENSAR', 'CYIENT', 'HEXAWARE', 'NIITTECH'
        ]
        
        # Pharma
        pharma = [
            'SUNPHARMA', 'DRREDDY', 'CIPLA', 'LUPIN', 'TORNTPHARM', 'GLENMARK', 'CADILAHC',
            'DIVISLAB', 'BIOCON', 'AUROPHARMA', 'ALKEM', 'REDDY', 'ZYDUSLIFE', 'LAURUSLABS'
        ]
        
        # FMCG
        fmcg = [
            'HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR', 'MARICO', 'GODREJCP',
            'EMAMILTD', 'COLPAL', 'JUBLFOOD', 'TATACONSUM', 'RADICO', 'UNITEDSPIRIT'
        ]
        
        # Auto
        auto = [
            'MARUTI', 'M&M', 'TATAMOTORS', 'BAJAJ-AUTO', 'EICHERMOT', 'HEROMOTOCO',
            'ASHOKLEY', 'TVSMOTOR', 'BAJAJHOLD', 'FORCEMOT', 'MAHSCOOTER'
        ]
        
        # Oil & Gas
        oil_gas = [
            'RELIANCE', 'ONGC', 'IOC', 'BPCL', 'GAIL', 'HPCL', 'PETRONET', 'IGL', 'MGL'
        ]
        
        # Metals
        metals = [
            'TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'VEDL', 'JINDALSTEL', 'SAIL', 'NMDC',
            'MOIL', 'NALCO', 'HINDZINC'
        ]
        
        # Power
        power = [
            'NTPC', 'POWERGRID', 'TATAPOWER', 'ADANIPOWER', 'TORNTPOWER', 'NHPC', 'SJVN'
        ]
        
        # Telecom
        telecom = [
            'BHARTIARTL', 'RELIANCE', 'IDEA'
        ]
        
        # Infrastructure
        infra = [
            'LT', 'ADANIPORTS', 'IRCTC', 'RVNL', 'IRFC', 'CONCOR', 'GMRINFRA'
        ]
        
        # Consumer Durables
        consumer = [
            'TITAN', 'WHIRLPOOL', 'VOLTAS', 'BLUEDART', 'ORIENTELEC'
        ]
        
        # Cement
        cement = [
            'ULTRACEMCO', 'SHREECEM', 'ACC', 'AMBUJACEM', 'RAMCOCEM', 'JKLAKSHMI'
        ]
        
        # Paints
        paints = [
            'ASIANPAINT', 'BERGEPAINT', 'KANSAINER', 'AKZOINDIA'
        ]
        
        # Financial Services
        financial = [
            'BAJFINANCE', 'HDFC', 'SBILIFE', 'HDFCLIFE', 'ICICIPRULI', 'SHRIRAMFIN',
            'M&MFIN', 'CHOLAFIN', 'LICHSGFIN'
        ]
        
        # Combine all
        all_symbols = list(set(
            nifty50 + banking + it + pharma + fmcg + auto + oil_gas + metals + 
            power + telecom + infra + consumer + cement + paints + financial
        ))
        
        # Create DataFrame
        stocks = []
        for symbol in all_symbols:
            stocks.append({
                'symbol': symbol,
                'name': symbol,  # Name would come from actual data
                'exchange': 'NSE'
            })
        
        return pd.DataFrame(stocks)
    
    def get_stocks_by_sector(self, sector: str) -> List[str]:
        """Get stocks by sector."""
        sector_map = {
            'Banking': ['HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'AXISBANK', 'SBIN', 'INDUSINDBK'],
            'IT': ['TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM', 'LTIM'],
            'Pharma': ['SUNPHARMA', 'DRREDDY', 'CIPLA', 'LUPIN', 'TORNTPHARM'],
            'FMCG': ['HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR'],
            'Auto': ['MARUTI', 'M&M', 'TATAMOTORS', 'BAJAJ-AUTO', 'EICHERMOT'],
            'Oil & Gas': ['RELIANCE', 'ONGC', 'IOC', 'BPCL', 'GAIL'],
            'Metals': ['TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'VEDL'],
            'Power': ['NTPC', 'POWERGRID', 'TATAPOWER'],
            'Telecom': ['BHARTIARTL', 'RELIANCE'],
            'Infrastructure': ['LT', 'ADANIPORTS']
        }
        return sector_map.get(sector, [])

