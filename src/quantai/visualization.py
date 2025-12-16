"""
ASCII Visualization Module for QuantAI-OS
Provides Bloomberg Terminal-style charts and sparklines
"""

import pandas as pd
import numpy as np
from typing import List


class ASCIIChart:
    """Generate ASCII charts for terminal display"""
    
    CHARS = {
        'up': '^',
        'down': 'v',
        'flat': '-',
        'bar_full': '#',
        'bar_empty': '.',
        'sparkline': ['_', '.', '-', '~', '^']
    }
    
    @staticmethod
    def sparkline(data: pd.Series, width: int = 30) -> str:
        """
        Generate a simple sparkline for price data
        
        Args:
            data: Price series (last N days)
            width: Width of sparkline in characters
            
        Returns:
            ASCII sparkline string
        """
        if data.empty or len(data) < 2:
            return "-" * width
        
        values = data.tail(width).values
        
        min_val = np.min(values)
        max_val = np.max(values)
        
        if max_val == min_val:
            return "-" * len(values)
        
        chars = ['_', '.', '-', '~', '^']
        
        normalized = (values - min_val) / (max_val - min_val)
        
        indices = (normalized * (len(chars) - 1)).astype(int)
        indices = np.clip(indices, 0, len(chars) - 1)
        
        sparkline = ''.join([chars[i] for i in indices])
        
        return sparkline
    
    @staticmethod
    def horizontal_bar(value: float, max_value: float = 100, width: int = 20) -> str:
        """
        Generate a horizontal bar chart
        
        Args:
            value: Current value
            max_value: Maximum value for scaling
            width: Bar width in characters
            
        Returns:
            ASCII bar string
        """
        if max_value <= 0:
            return '[' + '.' * width + ']'
        
        filled = int((value / max_value) * width)
        filled = max(0, min(width, filled))
        
        bar = '#' * filled + '.' * (width - filled)
        return f"[{bar}]"
    
    @staticmethod
    def price_trend(prices: pd.Series, days: int = 5) -> str:
        """
        Generate a simple trend indicator
        
        Args:
            prices: Price series
            days: Days to analyze for trend
            
        Returns:
            Trend string with direction
        """
        if len(prices) < days:
            return "N/A"
        
        recent = prices.tail(days)
        change = (recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0] * 100
        
        if change > 1:
            direction = "UP"
            arrow = "^"
        elif change < -1:
            direction = "DOWN"
            arrow = "v"
        else:
            direction = "FLAT"
            arrow = "-"
        
        return f"{arrow} {direction} ({change:+.2f}%)"
    
    @staticmethod
    def mini_histogram(data: pd.Series, bins: int = 10, width: int = 20) -> List[str]:
        """
        Generate a mini ASCII histogram
        
        Args:
            data: Data series
            bins: Number of histogram bins
            width: Maximum bar width
            
        Returns:
            List of histogram lines
        """
        if data.empty:
            return ["No data"]
        
        hist, bin_edges = np.histogram(data.dropna(), bins=bins)
        max_count = max(hist) if max(hist) > 0 else 1
        
        lines = []
        for i, count in enumerate(hist):
            bar_len = int((count / max_count) * width)
            bar = '#' * bar_len
            label = f"{bin_edges[i]:>7.2f}"
            lines.append(f"{label} | {bar}")
        
        return lines
    
    @staticmethod
    def regime_indicator(regime: int) -> str:
        """
        Generate regime indicator without emojis
        
        Args:
            regime: Regime index (0=bearish, 1=neutral, 2=bullish)
            
        Returns:
            Text indicator
        """
        indicators = {
            0: "[HIGH VOL]",
            1: "[MED VOL]",
            2: "[LOW VOL]"
        }
        return indicators.get(regime, "[UNKNOWN]")
    
    @staticmethod
    def signal_indicator(signal: float) -> str:
        """
        Generate signal strength indicator
        
        Args:
            signal: Signal strength (0-1)
            
        Returns:
            Signal indicator string
        """
        if signal >= 0.7:
            strength = "STRONG"
        elif signal >= 0.5:
            strength = "MODERATE"
        else:
            strength = "WEAK"
        
        direction = "LONG" if signal >= 0.5 else "SHORT"
        
        return f"{signal:.2f} ({direction} - {strength})"
    
    @staticmethod
    def format_price_table_row(label: str, value: str, width: int = 50) -> str:
        """
        Format a table row with consistent width
        
        Args:
            label: Row label
            value: Row value
            width: Total width
            
        Returns:
            Formatted row string
        """
        label_width = 20
        value_width = width - label_width - 3
        return f"| {label:<{label_width}} | {value:<{value_width}} |"
