"""
AI Commentary Generator using Groq
"""

from typing import Dict, Optional
from ..config import settings


class AICommentary:
    """Generates AI-powered market commentary using Groq"""
    
    def __init__(self):
        self.client = None
        self._commentary: str = None
    
    def _init_client(self) -> bool:
        """Initialize Groq client if API key is available"""
        if not settings.groq_api_key:
            return False
        
        try:
            from groq import Groq
            self.client = Groq(api_key=settings.groq_api_key)
            return True
        except Exception:
            return False
    
    def generate(
        self,
        ticker: str,
        regime_data: Dict,
        model_data: Dict,
        sizing_data: Dict,
        current_price: float
    ) -> str:
        """
        Generate AI commentary based on analysis results
        
        Args:
            ticker: Stock ticker symbol
            regime_data: Market regime analysis results
            model_data: ML model predictions
            sizing_data: Position sizing recommendations
            current_price: Current stock price
            
        Returns:
            Generated commentary string
        """
        if not self._init_client():
            self._commentary = self._generate_fallback(
                ticker, regime_data, model_data, sizing_data, current_price
            )
            return self._commentary
        
        prompt = self._build_prompt(
            ticker, regime_data, model_data, sizing_data, current_price
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional quantitative analyst providing concise market commentary. Be direct, insightful, and focus on actionable insights. Keep responses under 200 words. Do not use emojis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            self._commentary = response.choices[0].message.content
            return self._commentary
            
        except Exception as e:
            self._commentary = self._generate_fallback(
                ticker, regime_data, model_data, sizing_data, current_price
            )
            return self._commentary
    
    def _build_prompt(
        self,
        ticker: str,
        regime_data: Dict,
        model_data: Dict,
        sizing_data: Dict,
        current_price: float
    ) -> str:
        """Build prompt for AI model"""
        ensemble = model_data.get('ensemble', {})
        
        return f"""
Analyze the following quantitative signals for {ticker} (Current Price: ${current_price:.2f}):

MARKET REGIME:
- Current State: {regime_data['regime_name']} ({regime_data['current_regime']})
- Regime Probabilities: {regime_data['probabilities']}

MODEL PREDICTIONS:
- XGBoost: {model_data['xgboost']['direction']} (Confidence: {model_data['xgboost']['confidence_pct']}%)
- ElasticNet: {model_data['elasticnet']['direction']} (Confidence: {model_data['elasticnet']['confidence_pct']}%)
- Ensemble Direction: {ensemble.get('direction', 'N/A')}

POSITION SIZING:
- Recommended Position: {sizing_data['recommended_pct']}% of portfolio
- Full Kelly: {sizing_data['full_kelly_pct']}%

Provide a brief, professional analysis covering:
1. What the regime detection suggests about current market conditions
2. Key takeaways from the model predictions
3. Risk considerations and recommended approach

Do not use emojis. Be concise and professional.
"""
    
    def _generate_fallback(
        self,
        ticker: str,
        regime_data: Dict,
        model_data: Dict,
        sizing_data: Dict,
        current_price: float
    ) -> str:
        """Generate fallback commentary when API is unavailable"""
        ensemble = model_data.get('ensemble', {})
        direction = ensemble.get('direction', 'Unknown')
        confidence = ensemble.get('confidence_pct', 0)
        
        regime_text = {
            0: "high volatility environment suggests elevated risk",
            1: "moderate volatility indicates a transitional market phase",
            2: "low volatility environment supports trend continuation"
        }
        
        regime_insight = regime_text.get(
            regime_data['current_regime'],
            "current conditions require careful monitoring"
        )
        
        return f"""AUTOMATED ANALYSIS SUMMARY: {ticker}

The market regime detection indicates a {regime_data['regime_name'].lower()} state, which suggests that the {regime_insight}. 

The ensemble of ML models (XGBoost + ElasticNet) shows a {direction.lower()} bias with {confidence}% confidence. The recommended position size of {sizing_data['recommended_pct']}% reflects both model confidence and current regime adjustments.

KEY CONSIDERATIONS:
- Regime-adjusted sizing provides risk management
- Model agreement: {'Strong' if model_data['xgboost']['prediction'] == model_data['elasticnet']['prediction'] else 'Mixed'} consensus between models
- Always use stop-losses and proper risk management

Note: This is an automated analysis. Consider additional fundamental and macro factors before trading.
"""
    
    @property
    def commentary(self) -> str:
        """Get generated commentary"""
        if self._commentary is None:
            raise ValueError("Commentary not generated. Call generate() first.")
        return self._commentary
