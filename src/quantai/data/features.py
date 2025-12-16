"""
Feature Engineering - Creates ML features from market data
"""

import pandas as pd
import numpy as np
from typing import Tuple


class FeatureEngineer:
    """Creates technical features for ML models"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self._features: pd.DataFrame = None
        self._target: pd.Series = None
    
    def create_features(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Create technical indicators and target variable
        
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        df = self.data.copy()
        
        df['Returns'] = df['Close'].pct_change()
        
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['Volatility_20'] = df['Returns'].rolling(window=20).std() * np.sqrt(252)
        
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        df['BB_Std'] = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
        df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        df['Momentum_10'] = df['Close'].pct_change(periods=10)
        df['Momentum_20'] = df['Close'].pct_change(periods=20)
        
        if 'Volume' in df.columns:
            df['Volume_SMA_20'] = df['Volume'].rolling(window=20).mean()
            df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA_20']
        else:
            df['Volume_Ratio'] = 1.0
        
        df['Target'] = (df['Returns'].shift(-1) > 0).astype(int)
        
        df = df.dropna()
        
        feature_columns = [
            'Returns', 'SMA_5', 'SMA_20', 'SMA_50',
            'MACD', 'MACD_Signal', 'RSI', 'Volatility_20',
            'BB_Width', 'Momentum_10', 'Momentum_20', 'Volume_Ratio'
        ]
        
        self._features = df[feature_columns]
        self._target = df['Target']
        
        return self._features, self._target
    
    @property
    def features(self) -> pd.DataFrame:
        """Get computed features"""
        if self._features is None:
            self.create_features()
        return self._features
    
    @property
    def target(self) -> pd.Series:
        """Get target variable"""
        if self._target is None:
            self.create_features()
        return self._target
    
    def get_latest_features(self) -> pd.Series:
        """Get the most recent feature values for prediction"""
        if self._features is None:
            self.create_features()
        return self._features.iloc[-1]
