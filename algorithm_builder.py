"""
Algorithm builder module for creating custom stock screening and trading algorithms.
Supports visual condition building and code-based algorithms.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable
import json
from datetime import datetime


class AlgorithmBuilder:
    """Builds and manages custom algorithms for stock screening and trading."""
    
    def __init__(self):
        self.algorithms = {}
        self.available_functions = self._initialize_functions()
        self.available_indicators = self._initialize_indicators()
    
    def _initialize_functions(self) -> Dict:
        """Initialize available functions for algorithms."""
        return {
            'sma': {'name': 'Simple Moving Average', 'params': ['period']}, 
            'ema': {'name': 'Exponential Moving Average', 'params': ['period']},
            'rsi': {'name': 'Relative Strength Index', 'params': ['period']},
            'macd': {'name': 'MACD', 'params': []},
            'bb_upper': {'name': 'Bollinger Band Upper', 'params': ['period', 'std']},
            'bb_lower': {'name': 'Bollinger Band Lower', 'params': ['period', 'std']},
            'volume_sma': {'name': 'Volume SMA', 'params': ['period']},
            'price': {'name': 'Current Price', 'params': []},
            'close': {'name': 'Close Price', 'params': []},
            'open': {'name': 'Open Price', 'params': []},
            'high': {'name': 'High Price', 'params': []},
            'low': {'name': 'Low Price', 'params': []},
            'volume': {'name': 'Volume', 'params': []},
        }
    
    def _initialize_indicators(self) -> Dict:
        """Initialize available fundamental indicators."""
        return {
            'pe_ratio': {'name': 'P/E Ratio', 'type': 'valuation'},
            'price_to_book': {'name': 'Price to Book', 'type': 'valuation'},
            'roe': {'name': 'Return on Equity', 'type': 'profitability'},
            'roa': {'name': 'Return on Assets', 'type': 'profitability'},
            'debt_to_equity': {'name': 'Debt to Equity', 'type': 'financial_health'},
            'current_ratio': {'name': 'Current Ratio', 'type': 'financial_health'},
            'revenue_growth': {'name': 'Revenue Growth', 'type': 'growth'},
            'earnings_growth': {'name': 'Earnings Growth', 'type': 'growth'},
            'dividend_yield': {'name': 'Dividend Yield', 'type': 'dividend'},
            'profit_margin': {'name': 'Profit Margin', 'type': 'profitability'},
            'market_cap': {'name': 'Market Cap', 'type': 'size'},
        }
    
    def create_algorithm(
        self,
        name: str,
        description: str,
        conditions: List[Dict],
        algorithm_type: str = 'screener'  # 'screener' or 'strategy'
    ) -> Dict:
        """
        Create a custom algorithm.
        
        Args:
            name: Algorithm name
            description: Algorithm description
            conditions: List of condition dictionaries
            algorithm_type: 'screener' or 'strategy'
        
        Returns:
            Algorithm dictionary
        """
        algorithm = {
            'id': f"algo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': name,
            'description': description,
            'type': algorithm_type,
            'conditions': conditions,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }
        
        self.algorithms[algorithm['id']] = algorithm
        return algorithm
    
    def build_condition(
        self,
        field: str,
        operator: str,
        value: float,
        logical_operator: Optional[str] = None  # 'AND' or 'OR'
    ) -> Dict:
        """
        Build a condition for algorithm.
        
        Args:
            field: Field to check (e.g., 'rsi', 'pe_ratio', 'price')
            operator: Comparison operator ('>', '<', '>=', '<=', '==', '!=')
            value: Value to compare against
            logical_operator: How to combine with next condition ('AND', 'OR')
        """
        return {
            'field': field,
            'operator': operator,
            'value': value,
            'logical_operator': logical_operator
        }
    
    def conditions_to_expression(self, conditions: List[Dict]) -> str:
        """Convert condition list to Python expression string."""
        expression_parts = []
        
        for i, condition in enumerate(conditions):
            field = condition['field']
            operator = condition['operator']
            value = condition['value']
            
            # Format field (add function call if needed)
            if '(' in field or field in ['price', 'close', 'open', 'high', 'low', 'volume']:
                field_expr = field
            else:
                # Assume it's a function call
                field_expr = field
            
            # Build condition
            expr = f"{field_expr} {operator} {value}"
            expression_parts.append(expr)
            
            # Add logical operator
            if i < len(conditions) - 1 and condition.get('logical_operator'):
                expression_parts.append(condition['logical_operator'].lower())
        
        return ' '.join(expression_parts)
    
    def save_algorithm(self, algorithm_id: str, filepath: str):
        """Save algorithm to JSON file."""
        if algorithm_id in self.algorithms:
            with open(filepath, 'w') as f:
                json.dump(self.algorithms[algorithm_id], f, indent=2)
    
    def load_algorithm(self, filepath: str) -> Dict:
        """Load algorithm from JSON file."""
        with open(filepath, 'r') as f:
            algorithm = json.load(f)
        
        self.algorithms[algorithm['id']] = algorithm
        return algorithm
    
    def list_algorithms(self, algorithm_type: Optional[str] = None) -> List[Dict]:
        """List all algorithms, optionally filtered by type."""
        algorithms = list(self.algorithms.values())
        if algorithm_type:
            algorithms = [a for a in algorithms if a['type'] == algorithm_type]
        return algorithms
    
    def get_algorithm(self, algorithm_id: str) -> Optional[Dict]:
        """Get algorithm by ID."""
        return self.algorithms.get(algorithm_id)
    
    def delete_algorithm(self, algorithm_id: str):
        """Delete an algorithm."""
        if algorithm_id in self.algorithms:
            del self.algorithms[algorithm_id]
    
    def get_predefined_algorithms(self) -> List[Dict]:
        """Get predefined algorithm templates."""
        return [
            {
                'name': 'Value Stocks',
                'description': 'Stocks with low P/E, high ROE, low debt',
                'type': 'screener',
                'conditions': [
                    {'field': 'pe_ratio', 'operator': '<', 'value': 20, 'logical_operator': 'AND'},
                    {'field': 'roe', 'operator': '>', 'value': 15, 'logical_operator': 'AND'},
                    {'field': 'debt_to_equity', 'operator': '<', 'value': 1.0, 'logical_operator': None},
                ]
            },
            {
                'name': 'Growth Stocks',
                'description': 'Stocks with high revenue and earnings growth',
                'type': 'screener',
                'conditions': [
                    {'field': 'revenue_growth', 'operator': '>', 'value': 20, 'logical_operator': 'AND'},
                    {'field': 'earnings_growth', 'operator': '>', 'value': 15, 'logical_operator': 'AND'},
                    {'field': 'roe', 'operator': '>', 'value': 20, 'logical_operator': None},
                ]
            },
            {
                'name': 'Oversold Momentum',
                'description': 'Oversold stocks with positive momentum',
                'type': 'screener',
                'conditions': [
                    {'field': 'rsi(14)', 'operator': '<', 'value': 30, 'logical_operator': 'AND'},
                    {'field': 'price', 'operator': '>', 'value': 'sma(200)', 'logical_operator': 'AND'},
                    {'field': 'volume', 'operator': '>', 'value': 1000000, 'logical_operator': None},
                ]
            },
            {
                'name': 'Breakout Strategy',
                'description': 'Price breaking above resistance with volume',
                'type': 'strategy',
                'conditions': [
                    {'field': 'close', 'operator': '>', 'value': 'sma(50)', 'logical_operator': 'AND'},
                    {'field': 'volume', 'operator': '>', 'value': 'volume_sma(20)', 'logical_operator': 'AND'},
                    {'field': 'rsi(14)', 'operator': '<', 'value': 70, 'logical_operator': None},
                ]
            },
        ]



