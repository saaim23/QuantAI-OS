"""
Professional Logging System for QuantAI-OS
Handles system logging with proper formatting and file output
"""

import logging
from pathlib import Path
from typing import Optional


class QuantLogger:
    """Professional logging handler for QuantAI-OS"""
    
    _instance: Optional['QuantLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if QuantLogger._initialized:
            return
        
        self.log_dir = Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / "system.log"
        
        self.logger = logging.getLogger("quantai")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, mode='a')
            file_handler.setLevel(logging.DEBUG)
            
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-7s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        QuantLogger._initialized = True
    
    def info(self, message: str) -> None:
        """Log INFO level message"""
        self.logger.info(message)
    
    def debug(self, message: str) -> None:
        """Log DEBUG level message"""
        self.logger.debug(message)
    
    def warning(self, message: str) -> None:
        """Log WARNING level message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log ERROR level message"""
        self.logger.error(message)
    
    def log_analysis_start(self, ticker: str) -> None:
        """Log start of analysis"""
        self.info(f"Analysis started for {ticker}")
    
    def log_data_fetch(self, ticker: str, days: int) -> None:
        """Log data fetching"""
        self.info(f"Fetching data for {ticker} | Lookback: {days} days")
    
    def log_model_inference(self, model_name: str, elapsed_time: float) -> None:
        """Log model inference completion"""
        self.info(f"Model inference complete [{model_name}] | Time: {elapsed_time:.4f}s")
    
    def log_signal_saved(self, ticker: str, signal_id: int) -> None:
        """Log signal saved to database"""
        self.info(f"Signal saved to database | Ticker: {ticker} | ID: {signal_id}")
    
    def log_analysis_complete(self, ticker: str, total_time: float) -> None:
        """Log analysis completion"""
        self.info(f"Analysis complete for {ticker} | Total time: {total_time:.2f}s")


def get_logger() -> QuantLogger:
    """Get singleton logger instance"""
    return QuantLogger()
