"""
Advanced stock grouping and categorization system.
"""

import pandas as pd
from typing import List, Dict, Optional, Tuple
from config import Config
from data_manager import DataManager


class StockGrouper:
    """Manages stock grouping, categorization, and universe selection."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.predefined_groups = Config.get_stock_groups()
    
    def create_group(
        self,
        group_name: str,
        symbols: List[str],
        exchange: str = 'NSE',
        description: Optional[str] = None
    ):
        """Create a custom stock group."""
        self.data_manager.create_stock_group(group_name, symbols, exchange)
    
    def get_group(self, group_name: str) -> List[Tuple[str, str]]:
        """Get stocks in a group."""
        # Check predefined groups first
        if group_name in self.predefined_groups:
            return [(s, 'NSE') for s in self.predefined_groups[group_name]]
        
        # Check custom groups
        return self.data_manager.get_stock_group(group_name)
    
    def list_groups(self) -> Dict[str, List[str]]:
        """List all available groups."""
        groups = {}
        
        # Predefined groups
        for name, symbols in self.predefined_groups.items():
            groups[name] = symbols
        
        # Custom groups
        custom_groups = self.data_manager.list_stock_groups()
        for group_name in custom_groups:
            if group_name not in groups:
                group_stocks = self.get_group(group_name)
                groups[group_name] = [s[0] for s in group_stocks]
        
        return groups
    
    def filter_universe(
        self,
        exchange: Optional[str] = None,
        sectors: Optional[List[str]] = None,
        market_caps: Optional[List[str]] = None,
        group_name: Optional[str] = None,
        min_market_cap: Optional[float] = None,
        exclude_sectors: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Filter stock universe by multiple criteria.
        
        Args:
            exchange: NSE or BSE
            sectors: List of sectors to include
            market_caps: List of market cap categories
            group_name: Specific group name
            min_market_cap: Minimum market cap value
            exclude_sectors: Sectors to exclude
        
        Returns:
            DataFrame with filtered stocks
        """
        df = self.data_manager.get_stock_universe(
            exchange=exchange,
            sector=sectors[0] if sectors and len(sectors) == 1 else None,
            market_cap=market_caps[0] if market_caps and len(market_caps) == 1 else None,
            group_name=group_name
        )
        
        # Additional filtering if needed
        if sectors and len(sectors) > 1:
            # Would need to join with metadata for multiple sectors
            pass
        
        if exclude_sectors:
            # Would need to join with metadata
            pass
        
        return df
    
    def get_sector_stocks(self, sector: str, exchange: str = 'NSE') -> List[str]:
        """Get all stocks in a sector."""
        df = self.data_manager.get_stock_universe(exchange=exchange, sector=sector)
        return df['symbol'].tolist()
    
    def get_market_cap_stocks(self, market_cap: str, exchange: str = 'NSE') -> List[str]:
        """Get all stocks in a market cap category."""
        df = self.data_manager.get_stock_universe(exchange=exchange, market_cap=market_cap)
        return df['symbol'].tolist()
    
    def compare_groups(
        self,
        group1_name: str,
        group2_name: str,
        metric: str = 'returns'
    ) -> pd.DataFrame:
        """Compare performance between two groups."""
        # Implementation for group comparison
        pass
    
    def get_group_statistics(self, group_name: str) -> Dict:
        """Get statistics for a stock group."""
        stocks = self.get_group(group_name)
        
        return {
            'group_name': group_name,
            'stock_count': len(stocks),
            'exchanges': list(set([s[1] for s in stocks])),
            'stocks': [s[0] for s in stocks]
        }



