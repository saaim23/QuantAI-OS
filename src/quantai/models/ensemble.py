"""
Ensemble Predictor - Combines multiple models
"""

import pandas as pd
from typing import Dict, List
from .trees import XGBoostPredictor
from .linear import ElasticNetPredictor


class EnsemblePredictor:
    """Combines predictions from multiple models"""
    
    def __init__(self):
        self.xgb = XGBoostPredictor()
        self.elastic = ElasticNetPredictor()
        self._ensemble_prediction: int = None
        self._ensemble_confidence: float = None
        self._win_probability: float = None
    
    def fit_predict(self, X: pd.DataFrame, y: pd.Series) -> Dict:
        """
        Train all models and get ensemble prediction
        
        Args:
            X: Feature DataFrame
            y: Target Series
            
        Returns:
            Dictionary with ensemble results
        """
        xgb_pred, xgb_conf = self.xgb.fit_predict(X, y)
        elastic_pred, elastic_conf = self.elastic.fit_predict(X, y)
        
        weights = {
            'xgb': 0.6,
            'elastic': 0.4
        }
        
        weighted_pred = (
            weights['xgb'] * xgb_pred + 
            weights['elastic'] * elastic_pred
        )
        
        self._ensemble_prediction = 1 if weighted_pred >= 0.5 else 0
        
        self._ensemble_confidence = (
            weights['xgb'] * xgb_conf +
            weights['elastic'] * elastic_conf
        )
        
        avg_accuracy = (
            weights['xgb'] * self.xgb.accuracy +
            weights['elastic'] * self.elastic.accuracy
        )
        
        if self._ensemble_prediction == 1:
            self._win_probability = self._ensemble_confidence * avg_accuracy
        else:
            self._win_probability = (1 - self._ensemble_confidence) * avg_accuracy
        
        self._win_probability = max(0.3, min(0.7, self._win_probability + 0.1))
        
        return self.get_summary()
    
    @property
    def prediction(self) -> int:
        """Get ensemble prediction"""
        if self._ensemble_prediction is None:
            raise ValueError("Models not fitted. Call fit_predict() first.")
        return self._ensemble_prediction
    
    @property
    def confidence(self) -> float:
        """Get ensemble confidence"""
        if self._ensemble_confidence is None:
            raise ValueError("Models not fitted. Call fit_predict() first.")
        return self._ensemble_confidence
    
    @property
    def direction(self) -> str:
        """Get human-readable direction"""
        return "LONG" if self.prediction == 1 else "SHORT"
    
    @property
    def win_probability(self) -> float:
        """Get estimated win probability for Kelly calculation"""
        if self._win_probability is None:
            raise ValueError("Models not fitted. Call fit_predict() first.")
        return self._win_probability
    
    def get_summary(self) -> Dict:
        """Get complete ensemble summary"""
        return {
            "xgboost": self.xgb.get_summary(),
            "elasticnet": self.elastic.get_summary(),
            "ensemble": {
                "prediction": self.prediction,
                "direction": self.direction,
                "confidence_pct": round(self.confidence * 100, 1),
                "win_probability": round(self.win_probability * 100, 1)
            }
        }
    
    def get_model_predictions(self) -> List[Dict]:
        """Get list of individual model predictions for display"""
        return [
            self.xgb.get_summary(),
            self.elastic.get_summary()
        ]
