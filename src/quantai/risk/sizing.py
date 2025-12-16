"""
Position Sizing using Kelly Criterion
"""

from typing import Dict
import numpy as np


class KellySizer:
    """Calculates optimal position sizes using Kelly Criterion"""
    
    def __init__(self, max_position: float = 0.25):
        """
        Initialize Kelly Sizer
        
        Args:
            max_position: Maximum allowed position size (default 25%)
        """
        self.max_position = max_position
        self._kelly_fraction: float = None
        self._adjusted_fraction: float = None
    
    def calculate(
        self,
        win_probability: float,
        avg_win: float,
        avg_loss: float,
        regime_factor: float = 1.0
    ) -> float:
        """
        Calculate optimal position size using Kelly Criterion
        
        Args:
            win_probability: Probability of winning trade (0-1)
            avg_win: Average winning trade return (positive)
            avg_loss: Average losing trade return (positive, will be treated as loss)
            regime_factor: Multiplier based on market regime (0.5-1.0)
            
        Returns:
            Recommended position size as fraction (0-max_position)
        """
        if avg_loss == 0:
            avg_loss = 0.01
        
        win_prob = np.clip(win_probability, 0.01, 0.99)
        loss_prob = 1 - win_prob
        
        b = avg_win / avg_loss
        
        kelly = (win_prob * b - loss_prob) / b
        
        self._kelly_fraction = max(0, kelly)
        
        half_kelly = self._kelly_fraction * 0.5
        
        regime_adjusted = half_kelly * regime_factor
        
        self._adjusted_fraction = min(regime_adjusted, self.max_position)
        
        return self._adjusted_fraction
    
    @property
    def full_kelly(self) -> float:
        """Get full Kelly fraction"""
        if self._kelly_fraction is None:
            raise ValueError("Kelly not calculated. Call calculate() first.")
        return self._kelly_fraction
    
    @property
    def recommended_size(self) -> float:
        """Get recommended (half-Kelly, regime-adjusted) position size"""
        if self._adjusted_fraction is None:
            raise ValueError("Kelly not calculated. Call calculate() first.")
        return self._adjusted_fraction
    
    def get_summary(self) -> Dict:
        """Get position sizing summary"""
        return {
            "full_kelly_pct": round(self.full_kelly * 100, 2),
            "recommended_pct": round(self.recommended_size * 100, 2),
            "max_allowed_pct": round(self.max_position * 100, 2)
        }
    
    @staticmethod
    def get_regime_factor(regime: int) -> float:
        """
        Get regime adjustment factor
        
        Args:
            regime: Regime index (0=bearish, 1=neutral, 2=bullish)
            
        Returns:
            Factor to multiply Kelly by (0.5-1.0)
        """
        factors = {
            0: 0.5,
            1: 0.75,
            2: 1.0
        }
        return factors.get(regime, 0.75)
