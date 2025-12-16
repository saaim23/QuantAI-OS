"""
Configuration module for QuantAI-OS
Handles environment variables and application settings via .env file
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables"""
    
    groq_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("GROQ_API_KEY"),
        description="Groq API key for AI commentary"
    )
    
    default_lookback_days: int = Field(
        default=252,
        description="Default number of trading days to fetch"
    )
    
    reports_dir: Path = Field(
        default=Path("reports"),
        description="Directory for generated reports"
    )
    
    logs_dir: Path = Field(
        default=Path("logs"),
        description="Directory for system logs"
    )
    
    database_path: Path = Field(
        default=Path("trade_history.db"),
        description="Path to SQLite database file"
    )
    
    n_regimes: int = Field(
        default=3,
        description="Number of market regimes for HMM"
    )
    
    groq_model: str = Field(
        default="llama-3.1-8b-instant",
        description="Groq model for AI commentary"
    )
    
    def ensure_reports_dir(self) -> None:
        """Create reports directory if it doesn't exist"""
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def ensure_logs_dir(self) -> None:
        """Create logs directory if it doesn't exist"""
        self.logs_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
