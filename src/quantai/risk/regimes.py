"""
Market Regime Detection using Hidden Markov Models
"""

import numpy as np
import pandas as pd
from typing import Dict
from hmmlearn import hmm
from ..config import settings


class RegimeDetector:
    """Detects market regimes using Hidden Markov Models"""
    
    REGIME_NAMES = {
        0: "HIGH VOL",
        1: "MED VOL",
        2: "LOW VOL"
    }
    
    REGIME_LABELS = {
        0: "[HIGH VOL]",
        1: "[MED VOL]",
        2: "[LOW VOL]"
    }
    
    def __init__(self, n_regimes: int = None):
        self.n_regimes = n_regimes or settings.n_regimes
        self.model: hmm.GaussianHMM = None
        self._current_regime: int = None
        self._regime_probs: np.ndarray = None
        self._volatilities: Dict[int, float] = {}
    
    def fit_predict(self, returns: pd.Series) -> int:
        """
        Fit HMM and predict current market regime
        
        Args:
            returns: Series of daily returns
            
        Returns:
            Current regime index (0=bearish, 1=neutral, 2=bullish)
        """
        returns_clean = returns.dropna()
        X = returns_clean.values.reshape(-1, 1)
        
        self.model = hmm.GaussianHMM(
            n_components=self.n_regimes,
            covariance_type="full",
            n_iter=500,
            tol=1e-4,
            random_state=42,
            init_params="stmc"
        )
        
        self.model.fit(X)
        
        hidden_states = self.model.predict(X)
        
        for i in range(self.n_regimes):
            state_returns = returns_clean[hidden_states == i]
            self._volatilities[i] = state_returns.std() * np.sqrt(252) if len(state_returns) > 0 else 0
        
        sorted_states = sorted(self._volatilities.keys(), key=lambda x: self._volatilities[x], reverse=True)
        state_mapping = {old: new for new, old in enumerate(sorted_states)}
        
        raw_current = hidden_states[-1]
        self._current_regime = state_mapping[raw_current]
        
        self._regime_probs = self.model.predict_proba(X[-1:].reshape(-1, 1))[0]
        reordered_probs = np.zeros(self.n_regimes)
        for old, new in state_mapping.items():
            reordered_probs[new] = self._regime_probs[old]
        self._regime_probs = reordered_probs
        
        return self._current_regime
    
    @property
    def current_regime(self) -> int:
        """Get current regime index"""
        if self._current_regime is None:
            raise ValueError("Model not fitted. Call fit_predict() first.")
        return self._current_regime
    
    @property
    def current_regime_name(self) -> str:
        """Get human-readable regime name"""
        return self.REGIME_NAMES.get(self.current_regime, "UNKNOWN")
    
    @property
    def current_regime_label(self) -> str:
        """Get regime label"""
        return self.REGIME_LABELS.get(self.current_regime, "[UNKNOWN]")
    
    @property
    def regime_probabilities(self) -> Dict[str, float]:
        """Get probabilities for each regime"""
        if self._regime_probs is None:
            raise ValueError("Model not fitted. Call fit_predict() first.")
        
        return {
            self.REGIME_NAMES[i]: float(self._regime_probs[i])
            for i in range(self.n_regimes)
        }
    
    def get_summary(self) -> Dict:
        """Get complete regime analysis summary"""
        return {
            "current_regime": self.current_regime,
            "regime_name": self.current_regime_name,
            "regime_label": self.current_regime_label,
            "probabilities": self.regime_probabilities
        }
