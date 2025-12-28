"""
Utility functions for the backtester.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Tuple


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """Validate date range."""
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        if start > end:
            return False, "Start date must be before end date"
        
        if end > pd.Timestamp.now():
            return False, "End date cannot be in the future"
        
        return True, None
    except Exception as e:
        return False, f"Invalid date format: {str(e)}"


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with commas and decimals."""
    if pd.isna(num):
        return "N/A"
    return f"{num:,.{decimals}f}"


def format_percentage(num: float, decimals: int = 2) -> str:
    """Format percentage."""
    if pd.isna(num):
        return "N/A"
    return f"{num:.{decimals}f}%"


def get_default_date_range(days: int = 365) -> Tuple[str, str]:
    """Get default date range (last N days)."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def export_to_excel(data: pd.DataFrame, filename: str):
    """Export DataFrame to Excel."""
    data.to_excel(filename, index=False)
    return filename


def export_to_csv(data: pd.DataFrame, filename: str):
    """Export DataFrame to CSV."""
    data.to_csv(filename, index=False)
    return filename



