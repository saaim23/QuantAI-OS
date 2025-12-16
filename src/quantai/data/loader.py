"""
Data Loader - Fetches market data from Yahoo Finance
"""

from typing import Optional
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from ..config import settings


class DataLoader:
    """Handles fetching and validating market data"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self._data: Optional[pd.DataFrame] = None
        self._info: Optional[dict] = None
    
    def fetch(self, lookback_days: Optional[int] = None) -> pd.DataFrame:
        """
        Fetch historical data for the ticker
        
        Args:
            lookback_days: Number of days of history to fetch
            
        Returns:
            DataFrame with OHLCV data
            
        Raises:
            ValueError: If ticker is invalid or no data available
        """
        days = lookback_days or settings.default_lookback_days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(days * 1.5))
        
        try:
            stock = yf.Ticker(self.ticker)
            self._info = stock.info
            
            if not self._info or self._info.get('regularMarketPrice') is None:
                raise ValueError(f"Invalid ticker: {self.ticker}")
            
            self._data = stock.history(start=start_date, end=end_date)
            
            if self._data.empty:
                raise ValueError(f"No data available for ticker: {self.ticker}")
            
            self._data = self._data.tail(days)
            
            return self._data
            
        except Exception as e:
            if "Invalid ticker" in str(e) or "No data" in str(e):
                raise
            raise ValueError(f"Failed to fetch data for {self.ticker}: {str(e)}")
    
    @property
    def data(self) -> pd.DataFrame:
        """Get the fetched data"""
        if self._data is None:
            raise ValueError("Data not fetched. Call fetch() first.")
        return self._data
    
    @property
    def company_name(self) -> str:
        """Get the company name"""
        if self._info:
            return self._info.get('longName', self._info.get('shortName', self.ticker))
        return self.ticker
    
    @property
    def current_price(self) -> float:
        """Get the current price"""
        if self._info:
            return self._info.get('regularMarketPrice', 0.0)
        if self._data is not None and not self._data.empty:
            return float(self._data['Close'].iloc[-1])
        return 0.0
