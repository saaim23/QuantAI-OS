"""
Tree-based Models - HistGradientBoosting implementation (sklearn native)
"""

import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier


class XGBoostPredictor:
    """HistGradientBoosting classifier for market direction prediction
    
    Uses sklearn's HistGradientBoostingClassifier as a lightweight alternative
    to XGBoost while maintaining similar performance characteristics.
    """
    
    def __init__(self):
        self.model: HistGradientBoostingClassifier = None
        self._accuracy: float = None
        self._prediction: int = None
        self._confidence: float = None
    
    def fit_predict(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2
    ) -> Tuple[int, float]:
        """
        Train HistGradientBoosting model and make prediction on latest data
        
        Args:
            X: Feature DataFrame
            y: Target Series
            test_size: Fraction for test set
            
        Returns:
            Tuple of (prediction, confidence)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X.iloc[:-1], y.iloc[:-1],
            test_size=test_size,
            shuffle=False
        )
        
        self.model = HistGradientBoostingClassifier(
            max_iter=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10
        )
        
        self.model.fit(X_train, y_train)
        
        self._accuracy = self.model.score(X_test, y_test)
        
        latest_features = X.iloc[-1:]
        self._prediction = int(self.model.predict(latest_features)[0])
        
        proba = self.model.predict_proba(X.iloc[-1:])[0]
        self._confidence = float(max(proba))
        
        return self._prediction, self._confidence
    
    @property
    def prediction(self) -> int:
        """Get prediction (1=up, 0=down)"""
        if self._prediction is None:
            raise ValueError("Model not fitted. Call fit_predict() first.")
        return self._prediction
    
    @property
    def confidence(self) -> float:
        """Get prediction confidence (0-1)"""
        if self._confidence is None:
            raise ValueError("Model not fitted. Call fit_predict() first.")
        return self._confidence
    
    @property
    def accuracy(self) -> float:
        """Get test set accuracy"""
        if self._accuracy is None:
            raise ValueError("Model not fitted. Call fit_predict() first.")
        return self._accuracy
    
    @property
    def direction(self) -> str:
        """Get human-readable direction"""
        return "LONG" if self.prediction == 1 else "SHORT"
    
    def get_summary(self) -> dict:
        """Get model summary"""
        return {
            "model": "GradientBoosting",
            "prediction": self.prediction,
            "direction": self.direction,
            "confidence_pct": round(self.confidence * 100, 1),
            "accuracy_pct": round(self.accuracy * 100, 1)
        }
