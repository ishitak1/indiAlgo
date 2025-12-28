"""
Strategy management with versioning and persistence.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from config import Config


class StrategyManager:
    """Manages strategy creation, storage, versioning, and retrieval."""
    
    def __init__(self):
        Config.initialize_directories()
        self.strategies_dir = Config.STRATEGIES_DIR
        self.strategies = {}
        self._load_all_strategies()
    
    def create_strategy(
        self,
        name: str,
        description: str,
        strategy_type: str,  # 'screener' or 'backtest'
        buy_conditions: Optional[List[Dict]] = None,
        sell_conditions: Optional[List[Dict]] = None,
        screener_conditions: Optional[List[Dict]] = None,
        parameters: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        is_preset: bool = False
    ) -> Dict:
        """
        Create a new strategy.
        
        Args:
            name: Strategy name
            description: Strategy description
            strategy_type: 'screener' or 'backtest'
            buy_conditions: Buy conditions (for backtest)
            sell_conditions: Sell conditions (for backtest)
            screener_conditions: Screening conditions (for screener)
            parameters: Strategy parameters (position size, stop loss, etc.)
            tags: Tags for categorization
            is_preset: Whether this is a preset strategy
        """
        strategy_id = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        strategy = {
            'id': strategy_id,
            'name': name,
            'description': description,
            'type': strategy_type,
            'buy_conditions': buy_conditions or [],
            'sell_conditions': sell_conditions or [],
            'screener_conditions': screener_conditions or [],
            'parameters': parameters or {},
            'tags': tags or [],
            'is_preset': is_preset,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': 1,
            'performance_metrics': {}
        }
        
        self.strategies[strategy_id] = strategy
        self._save_strategy(strategy)
        
        return strategy
    
    def update_strategy(
        self,
        strategy_id: str,
        **updates
    ) -> Dict:
        """Update a strategy (creates new version)."""
        if strategy_id not in self.strategies:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        strategy = self.strategies[strategy_id].copy()
        strategy['version'] += 1
        strategy['updated_at'] = datetime.now().isoformat()
        
        # Update fields
        for key, value in updates.items():
            if key in strategy:
                strategy[key] = value
        
        # Create versioned copy
        versioned_id = f"{strategy_id}_v{strategy['version']}"
        strategy['id'] = versioned_id
        strategy['parent_id'] = strategy_id
        
        self.strategies[versioned_id] = strategy
        self._save_strategy(strategy)
        
        return strategy
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict]:
        """Get strategy by ID."""
        return self.strategies.get(strategy_id)
    
    def list_strategies(
        self,
        strategy_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_preset: Optional[bool] = None
    ) -> List[Dict]:
        """List strategies with optional filters."""
        strategies = list(self.strategies.values())
        
        if strategy_type:
            strategies = [s for s in strategies if s['type'] == strategy_type]
        
        if tags:
            strategies = [s for s in strategies if any(tag in s.get('tags', []) for tag in tags)]
        
        if is_preset is not None:
            strategies = [s for s in strategies if s.get('is_preset', False) == is_preset]
        
        return strategies
    
    def delete_strategy(self, strategy_id: str):
        """Delete a strategy."""
        if strategy_id in self.strategies:
            del self.strategies[strategy_id]
            
            # Delete file
            strategy_file = self.strategies_dir / f"{strategy_id}.json"
            if strategy_file.exists():
                strategy_file.unlink()
    
    def get_preset_strategies(self) -> List[Dict]:
        """Get all preset strategies."""
        return [
            {
                'name': 'SMA Crossover',
                'description': 'Buy when short MA crosses above long MA, sell on reverse',
                'type': 'backtest',
                'buy_conditions': [
                    {'field': 'sma(20)', 'operator': '>', 'value': 'sma(50)'}
                ],
                'sell_conditions': [
                    {'field': 'sma(20)', 'operator': '<', 'value': 'sma(50)'}
                ],
                'parameters': {
                    'position_size': 1.0,
                    'stop_loss': 0.05,
                    'take_profit': None
                },
                'tags': ['trend', 'momentum', 'technical']
            },
            {
                'name': 'RSI Mean Reversion',
                'description': 'Buy oversold (RSI < 30), sell overbought (RSI > 70)',
                'type': 'backtest',
                'buy_conditions': [
                    {'field': 'rsi(14)', 'operator': '<', 'value': 30}
                ],
                'sell_conditions': [
                    {'field': 'rsi(14)', 'operator': '>', 'value': 70}
                ],
                'parameters': {
                    'position_size': 1.0,
                    'stop_loss': 0.05,
                    'take_profit': 0.10
                },
                'tags': ['mean_reversion', 'oscillator', 'technical']
            },
            {
                'name': 'Breakout Strategy',
                'description': 'Buy on price breakout above resistance with volume confirmation',
                'type': 'backtest',
                'buy_conditions': [
                    {'field': 'close', 'operator': '>', 'value': 'sma(50)'},
                    {'field': 'volume', 'operator': '>', 'value': 'volume_sma(20)'}
                ],
                'sell_conditions': [
                    {'field': 'rsi(14)', 'operator': '>', 'value': 70}
                ],
                'parameters': {
                    'position_size': 1.0,
                    'stop_loss': 0.05
                },
                'tags': ['breakout', 'momentum', 'technical']
            },
            {
                'name': 'Value Screener',
                'description': 'Find undervalued stocks with good fundamentals',
                'type': 'screener',
                'screener_conditions': [
                    {'field': 'pe_ratio', 'operator': '<', 'value': 20},
                    {'field': 'roe', 'operator': '>', 'value': 15},
                    {'field': 'debt_to_equity', 'operator': '<', 'value': 1.0}
                ],
                'tags': ['value', 'fundamental', 'screener']
            },
            {
                'name': 'Growth Screener',
                'description': 'Find high-growth stocks',
                'type': 'screener',
                'screener_conditions': [
                    {'field': 'revenue_growth', 'operator': '>', 'value': 20},
                    {'field': 'earnings_growth', 'operator': '>', 'value': 15},
                    {'field': 'roe', 'operator': '>', 'value': 20}
                ],
                'tags': ['growth', 'fundamental', 'screener']
            }
        ]
    
    def _save_strategy(self, strategy: Dict):
        """Save strategy to file."""
        strategy_file = self.strategies_dir / f"{strategy['id']}.json"
        with open(strategy_file, 'w') as f:
            json.dump(strategy, f, indent=2)
    
    def _load_all_strategies(self):
        """Load all strategies from disk."""
        if not self.strategies_dir.exists():
            return
        
        for strategy_file in self.strategies_dir.glob("*.json"):
            try:
                with open(strategy_file, 'r') as f:
                    strategy = json.load(f)
                    self.strategies[strategy['id']] = strategy
            except Exception as e:
                print(f"Error loading strategy {strategy_file}: {e}")



