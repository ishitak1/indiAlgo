"""
Comprehensive screener that processes all stocks with custom algorithms.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Callable
from datetime import datetime
import time

from data_fetcher import DataFetcher
from stock_list_fetcher import StockListFetcher
from fundamental_data import FundamentalData
from analytics import Analytics
from rule_engine import RuleEngine
from algorithm_builder import AlgorithmBuilder


class ComprehensiveScreener:
    """Screens all stocks using custom algorithms."""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.stock_list_fetcher = StockListFetcher()
        self.fundamental_data = FundamentalData()
        self.algorithm_builder = AlgorithmBuilder()
        self.cache = {}
    
    def screen_stocks(
        self,
        algorithm: Dict,
        exchange: str = 'NSE',
        sectors: Optional[List[str]] = None,
        market_cap_filter: Optional[str] = None,
        max_stocks: Optional[int] = None,
        use_fundamentals: bool = True,
        use_technical: bool = True
    ) -> pd.DataFrame:
        """
        Screen stocks using a custom algorithm.
        
        Args:
            algorithm: Algorithm dictionary from AlgorithmBuilder
            exchange: 'NSE' or 'BSE'
            sectors: Filter by sectors
            market_cap_filter: 'Large Cap', 'Mid Cap', 'Small Cap'
            max_stocks: Maximum number of stocks to process
            use_fundamentals: Include fundamental data
            use_technical: Include technical indicators
        
        Returns:
            DataFrame with matching stocks and their metrics
        """
        # Get stock list
        print(f"Fetching stock list for {exchange}...")
        all_stocks = self.stock_list_fetcher.get_all_stocks(exchange)
        
        # Apply filters
        if sectors:
            all_stocks = all_stocks[all_stocks['sector'].isin(sectors)]
        if market_cap_filter:
            all_stocks = all_stocks[all_stocks['market_cap'] == market_cap_filter]
        
        if max_stocks:
            all_stocks = all_stocks.head(max_stocks)
        
        print(f"Processing {len(all_stocks)} stocks...")
        
        results = []
        total = len(all_stocks)
        
        for idx, row in all_stocks.iterrows():
            symbol = row['symbol']
            print(f"Processing {symbol} ({idx+1}/{total})...", end='\r')
            
            try:
                # Fetch data
                df = self._get_stock_data(symbol, exchange)
                if df.empty:
                    continue
                
                # Prepare data for screening
                screening_data = self._prepare_screening_data(
                    df, symbol, exchange, use_fundamentals, use_technical
                )
                
                # Evaluate algorithm
                matches = self._evaluate_algorithm(algorithm, screening_data)
                
                if matches:
                    result = {
                        'symbol': symbol,
                        'exchange': exchange,
                        'name': row.get('name', symbol),
                        'sector': row.get('sector', 'N/A'),
                        'market_cap': row.get('market_cap', 'N/A'),
                        'current_price': screening_data.get('current_price', None),
                        'matches': True,
                    }
                    
                    # Add metrics
                    result.update(screening_data)
                    results.append(result)
            
            except Exception as e:
                print(f"\nError processing {symbol}: {e}")
                continue
            
            time.sleep(0.1)  # Rate limiting
        
        print(f"\nScreening complete! Found {len(results)} matches.")
        return pd.DataFrame(results)
    
    def _get_stock_data(self, symbol: str, exchange: str, period: str = '1y') -> pd.DataFrame:
        """Get stock data with caching."""
        cache_key = f"{exchange}_{symbol}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            df = self.data_fetcher.fetch_data(symbol, exchange, period=period)
            self.cache[cache_key] = df
            return df
        except:
            return pd.DataFrame()
    
    def _prepare_screening_data(
        self,
        df: pd.DataFrame,
        symbol: str,
        exchange: str,
        use_fundamentals: bool,
        use_technical: bool
    ) -> Dict:
        """Prepare data dictionary for algorithm evaluation."""
        data = {}
        
        # Technical data
        if use_technical and not df.empty:
            analytics = Analytics(df)
            analytics.compute_all_indicators()
            df_analytics = analytics.get_dataframe()
            
            if len(df_analytics) > 0:
                latest = df_analytics.iloc[-1]
                data['current_price'] = latest['close']
                data['open'] = latest['open']
                data['high'] = latest['high']
                data['low'] = latest['low']
                data['close'] = latest['close']
                data['volume'] = latest['volume']
                
                # Add technical indicators
                for col in df_analytics.columns:
                    if col not in ['date', 'symbol', 'exchange', 'open', 'high', 'low', 'close', 'volume']:
                        data[col] = latest[col]
        
        # Fundamental data
        if use_fundamentals:
            try:
                fundamentals = self.fundamental_data.get_fundamentals(symbol, exchange)
                data.update(fundamentals)
            except:
                pass
        
        return data
    
    def _evaluate_algorithm(self, algorithm: Dict, data: Dict, df: pd.DataFrame = None) -> bool:
        """Evaluate if stock matches algorithm conditions."""
        try:
            conditions = algorithm.get('conditions', [])
            
            # Convert conditions to expression
            expression = self.algorithm_builder.conditions_to_expression(conditions)
            
            # Create a simple evaluator
            # For technical conditions, we need the full dataframe
            # For fundamental conditions, we can evaluate directly
            
            # Split conditions into technical and fundamental
            tech_conditions = []
            fund_conditions = []
            
            for condition in conditions:
                field = condition['field']
                if any(ind in field for ind in ['rsi', 'sma', 'ema', 'macd', 'bb', 'price', 'close', 'volume']):
                    tech_conditions.append(condition)
                else:
                    fund_conditions.append(condition)
            
            # Evaluate fundamental conditions
            fund_match = True
            if fund_conditions:
                for condition in fund_conditions:
                    field = condition['field']
                    operator = condition['operator']
                    value = condition['value']
                    
                    field_value = data.get(field)
                    if field_value is None:
                        fund_match = False
                        break
                    
                    # Evaluate condition
                    if operator == '>':
                        if not (field_value > value):
                            fund_match = False
                            break
                    elif operator == '<':
                        if not (field_value < value):
                            fund_match = False
                            break
                    elif operator == '>=':
                        if not (field_value >= value):
                            fund_match = False
                            break
                    elif operator == '<=':
                        if not (field_value <= value):
                            fund_match = False
                            break
                    elif operator == '==':
                        if not (field_value == value):
                            fund_match = False
                            break
            
            # Evaluate technical conditions if we have dataframe
            tech_match = True
            if df is not None and tech_conditions:
                try:
                    analytics = Analytics(df)
                    analytics.compute_all_indicators()
                    df_analytics = analytics.get_dataframe()
                    
                    if len(df_analytics) > 0:
                        rule_engine = RuleEngine(df_analytics)
                        # Convert technical conditions to expression
                        tech_expression = self.algorithm_builder.conditions_to_expression(tech_conditions)
                        tech_mask = rule_engine.evaluate_rule(tech_expression)
                        tech_match = tech_mask.iloc[-1] if len(tech_mask) > 0 else False
                except:
                    tech_match = True  # Default to True if evaluation fails
            
            return fund_match and tech_match
        
        except Exception as e:
            print(f"Error evaluating algorithm: {e}")
            return False
    
    def batch_screen(
        self,
        algorithms: List[Dict],
        exchange: str = 'NSE',
        **kwargs
    ) -> Dict[str, pd.DataFrame]:
        """Screen stocks with multiple algorithms."""
        results = {}
        for algorithm in algorithms:
            name = algorithm['name']
            print(f"\nRunning algorithm: {name}")
            results[name] = self.screen_stocks(algorithm, exchange, **kwargs)
        return results

