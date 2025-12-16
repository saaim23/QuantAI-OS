"""
QuantAI-OS - Production-Grade Quantitative Analysis Engine
A professional CLI tool for quantitative stock analysis with ML models.
"""

__version__ = "2.0.0"
__author__ = "QuantAI Team"

from .logger import get_logger, QuantLogger
from .database import get_database, DatabaseManager, TradeSignal
from .visualization import ASCIIChart
