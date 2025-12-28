"""
Premium features for indiAlgo Premium version.
"""

from typing import Dict, List, Optional
from datetime import datetime


class PremiumFeatures:
    """Premium features manager."""
    
    PREMIUM_FEATURES = {
        'unlimited_backtests': {
            'name': 'Unlimited Backtests',
            'description': 'Run unlimited strategy backtests',
            'free_limit': 10,
            'premium_limit': None
        },
        'advanced_analytics': {
            'name': 'Advanced Analytics',
            'description': 'Access to advanced risk metrics and analytics',
            'free_limit': None,
            'premium_limit': None
        },
        'priority_support': {
            'name': 'Priority Support',
            'description': 'Priority customer support',
            'free_limit': None,
            'premium_limit': None
        },
        'export_formats': {
            'name': 'Multiple Export Formats',
            'description': 'Export to PDF, Excel, JSON',
            'free_limit': 'CSV only',
            'premium_limit': 'All formats'
        },
        'api_access': {
            'name': 'API Access',
            'description': 'Programmatic access via API',
            'free_limit': None,
            'premium_limit': True
        },
        'custom_indicators': {
            'name': 'Custom Indicators',
            'description': 'Create and use custom technical indicators',
            'free_limit': None,
            'premium_limit': True
        },
        'strategy_sharing': {
            'name': 'Strategy Sharing',
            'description': 'Share strategies with community',
            'free_limit': None,
            'premium_limit': True
        },
        'real_time_data': {
            'name': 'Real-time Data',
            'description': 'Access to real-time market data',
            'free_limit': 'Delayed',
            'premium_limit': 'Real-time'
        }
    }
    
    @classmethod
    def check_feature_access(cls, user_tier: str, feature_name: str) -> bool:
        """Check if user has access to a feature."""
        if user_tier == 'premium':
            return True
        
        feature = cls.PREMIUM_FEATURES.get(feature_name)
        if not feature:
            return False
        
        # Free tier has limited access
        return feature['free_limit'] is not None
    
    @classmethod
    def get_feature_comparison(cls) -> Dict:
        """Get feature comparison between free and premium."""
        return {
            'free': {
                'backtests_per_month': 10,
                'export_formats': ['CSV'],
                'data_access': 'Historical (delayed)',
                'support': 'Community',
                'custom_indicators': False,
                'api_access': False,
                'strategy_sharing': False
            },
            'premium': {
                'backtests_per_month': 'Unlimited',
                'export_formats': ['CSV', 'Excel', 'PDF', 'JSON'],
                'data_access': 'Historical + Real-time',
                'support': 'Priority',
                'custom_indicators': True,
                'api_access': True,
                'strategy_sharing': True
            }
        }
    
    @classmethod
    def get_pricing_info(cls) -> Dict:
        """Get pricing information."""
        return {
            'free': {
                'price': 0,
                'currency': 'INR',
                'billing': 'Free forever'
            },
            'premium': {
                'price': 999,
                'currency': 'INR',
                'billing': 'Monthly',
                'annual_discount': 'Save 20% with annual plan'
            }
        }

