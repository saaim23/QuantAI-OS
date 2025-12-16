"""
Linear Models - ElasticNet implementation using sklearn Pipeline
"""

import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class ElasticNetPredictor:
    """SGD Classifier with ElasticNet regularization for market prediction"""
    
    def __init__(self):
        self.pipeline: Pipeline = None
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
        Train ElasticNet model and make prediction on latest data
        
        Uses sklearn Pipeline to prevent data leakage - scaler is fitted
        only on training data within the pipeline.
        
        Args:
            X: Feature DataFrame
            y: Target Series
            test_size: Fraction for test set
            
        Returns:
            Tuple of (prediction, confidence)
        """
        X_train_test = X.iloc[:-1]
        y_train_test = y.iloc[:-1]
        X_latest = X.iloc[-1:]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_train_test, y_train_test,
            test_size=test_size,
            shuffle=False
        )
        
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', SGDClassifier(
                loss='log_loss',
                penalty='elasticnet',
                l1_ratio=0.5,
                alpha=0.001,
                max_iter=2000,
                tol=1e-4,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1,
                n_iter_no_change=10
            ))
        ])
        
        self.pipeline.fit(X_train, y_train)
        
        self._accuracy = self.pipeline.score(X_test, y_test)
        
        self._prediction = int(self.pipeline.predict(X_latest)[0])
        
        proba = self.pipeline.predict_proba(X_latest)[0]
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
            "model": "ElasticNet",
            "prediction": self.prediction,
            "direction": self.direction,
            "confidence_pct": round(self.confidence * 100, 1),
            "accuracy_pct": round(self.accuracy * 100, 1)
        }
