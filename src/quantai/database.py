"""
SQL Database Handler for QuantAI-OS
Uses SQLAlchemy with SQLite for trade signal persistence
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, List

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class TradeSignal(Base):
    """Trade Signal Model - stores analysis results"""
    
    __tablename__ = 'trade_signals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    regime = Column(Integer, nullable=False)
    regime_name = Column(String(50), nullable=False)
    signal_strength = Column(Float, nullable=False)
    model_allocation = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    xgb_confidence = Column(Float, nullable=True)
    elastic_confidence = Column(Float, nullable=True)
    ensemble_direction = Column(String(20), nullable=True)
    
    def __repr__(self):
        return (
            f"<TradeSignal(id={self.id}, ticker={self.ticker}, "
            f"regime={self.regime_name}, signal={self.signal_strength:.2f})>"
        )


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str = "trade_history.db"):
        self.db_path = Path(db_path)
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_signal(
        self,
        ticker: str,
        regime: int,
        regime_name: str,
        signal_strength: float,
        model_allocation: float,
        current_price: Optional[float] = None,
        xgb_confidence: Optional[float] = None,
        elastic_confidence: Optional[float] = None,
        ensemble_direction: Optional[str] = None
    ) -> int:
        """
        Save a trade signal to the database
        
        Args:
            ticker: Stock ticker symbol
            regime: Regime index (0=bearish, 1=neutral, 2=bullish)
            regime_name: Human-readable regime name
            signal_strength: Ensemble confidence/signal strength
            model_allocation: Recommended position size (Kelly)
            current_price: Current stock price
            xgb_confidence: XGBoost model confidence
            elastic_confidence: ElasticNet model confidence
            ensemble_direction: Ensemble prediction direction
            
        Returns:
            ID of the saved signal
        """
        session = self.Session()
        try:
            signal = TradeSignal(
                ticker=ticker.upper(),
                regime=regime,
                regime_name=regime_name,
                signal_strength=signal_strength,
                model_allocation=model_allocation,
                current_price=current_price,
                xgb_confidence=xgb_confidence,
                elastic_confidence=elastic_confidence,
                ensemble_direction=ensemble_direction
            )
            session.add(signal)
            session.commit()
            signal_id = signal.id
            return signal_id
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_signals_by_ticker(self, ticker: str, limit: int = 10) -> List[TradeSignal]:
        """Get recent signals for a specific ticker"""
        session = self.Session()
        try:
            signals = (
                session.query(TradeSignal)
                .filter(TradeSignal.ticker == ticker.upper())
                .order_by(TradeSignal.timestamp.desc())
                .limit(limit)
                .all()
            )
            return signals
        finally:
            session.close()
    
    def get_all_signals(self, limit: int = 50) -> List[TradeSignal]:
        """Get all recent signals"""
        session = self.Session()
        try:
            signals = (
                session.query(TradeSignal)
                .order_by(TradeSignal.timestamp.desc())
                .limit(limit)
                .all()
            )
            return signals
        finally:
            session.close()


_db_manager: Optional[DatabaseManager] = None


def get_database() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
