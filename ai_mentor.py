"""
AI Mentor Chatbot for indiAlgo.
Educational assistant using open-source LLMs.
"""

from typing import Dict, List, Optional
import json
from datetime import datetime


class AIMentor:
    """AI mentor chatbot for educational guidance."""
    
    def __init__(self, model_name: str = "llama2", use_local: bool = True):
        self.model_name = model_name
        self.use_local = use_local
        self.conversation_history = []
        self.disclaimer = """
        ⚠️ DISCLAIMER: This AI mentor provides educational guidance only.
        It is NOT financial advice. Always do your own research and consult
        with qualified financial advisors before making investment decisions.
        """
    
    def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Chat with AI mentor.
        
        Args:
            user_message: User's question
            context: Optional context (current strategy, portfolio, etc.)
        
        Returns:
            Response dictionary with answer and explanations
        """
        # For now, use rule-based responses
        # In production, integrate with local LLM (Llama, Mistral, etc.)
        
        response = self._generate_response(user_message, context)
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'assistant': response['answer'],
            'context': context
        })
        
        return response
    
    def _generate_response(self, message: str, context: Optional[Dict]) -> Dict:
        """Generate response based on message."""
        message_lower = message.lower()
        
        # Indicator explanations
        if any(word in message_lower for word in ['rsi', 'relative strength']):
            return {
                'answer': self._explain_rsi(),
                'type': 'indicator_explanation',
                'suggestions': ['How to use RSI in trading?', 'What is a good RSI value?']
            }
        
        elif any(word in message_lower for word in ['macd', 'moving average convergence']):
            return {
                'answer': self._explain_macd(),
                'type': 'indicator_explanation',
                'suggestions': ['How to interpret MACD signals?', 'MACD vs RSI']
            }
        
        elif any(word in message_lower for word in ['moving average', 'sma', 'ema']):
            return {
                'answer': self._explain_moving_averages(),
                'type': 'indicator_explanation',
                'suggestions': ['SMA vs EMA', 'Which period to use?']
            }
        
        # Backtest explanations
        elif any(word in message_lower for word in ['backtest', 'backtesting', 'results']):
            return {
                'answer': self._explain_backtest_results(context),
                'type': 'backtest_help',
                'suggestions': ['What is a good Sharpe ratio?', 'How to improve my strategy?']
            }
        
        # Portfolio risk
        elif any(word in message_lower for word in ['risk', 'volatility', 'diversification']):
            return {
                'answer': self._explain_risk(context),
                'type': 'risk_education',
                'suggestions': ['How to reduce portfolio risk?', 'What is diversification?']
            }
        
        # General help
        else:
            return {
                'answer': self._general_help(message),
                'type': 'general',
                'suggestions': [
                    'Explain RSI indicator',
                    'What is Sharpe ratio?',
                    'How to read backtest results?',
                    'Explain portfolio diversification'
                ]
            }
    
    def _explain_rsi(self) -> str:
        return """
        **RSI (Relative Strength Index)** is a momentum oscillator that measures the speed and magnitude of price changes.
        
        **Key Points:**
        - RSI ranges from 0 to 100
        - **RSI < 30**: Oversold condition (potential buy signal)
        - **RSI > 70**: Overbought condition (potential sell signal)
        - **RSI = 50**: Neutral
        
        **How to Use:**
        - Look for RSI crossing above 30 (oversold recovery)
        - Look for RSI crossing below 70 (overbought reversal)
        - Combine with other indicators for confirmation
        
        **Remember:** RSI alone isn't enough. Always use it with price action and other indicators!
        """
    
    def _explain_macd(self) -> str:
        return """
        **MACD (Moving Average Convergence Divergence)** shows the relationship between two moving averages.
        
        **Components:**
        - **MACD Line**: Fast EMA (12) - Slow EMA (26)
        - **Signal Line**: 9-period EMA of MACD line
        - **Histogram**: Difference between MACD and Signal
        
        **Trading Signals:**
        - **Bullish**: MACD crosses above Signal line
        - **Bearish**: MACD crosses below Signal line
        - **Divergence**: Price makes new highs/lows but MACD doesn't (potential reversal)
        
        **Best Practices:**
        - Use with trend confirmation
        - Look for divergences for early signals
        - Combine with volume analysis
        """
    
    def _explain_moving_averages(self) -> str:
        return """
        **Moving Averages** smooth out price data to identify trends.
        
        **Types:**
        - **SMA (Simple MA)**: Average of last N periods
        - **EMA (Exponential MA)**: Gives more weight to recent prices
        
        **Common Periods:**
        - **20-day**: Short-term trend
        - **50-day**: Medium-term trend
        - **200-day**: Long-term trend (major support/resistance)
        
        **Trading Signals:**
        - **Golden Cross**: Short MA crosses above Long MA (bullish)
        - **Death Cross**: Short MA crosses below Long MA (bearish)
        - **Price above MA**: Uptrend
        - **Price below MA**: Downtrend
        
        **Tip:** Use multiple timeframes for better confirmation!
        """
    
    def _explain_backtest_results(self, context: Optional[Dict]) -> str:
        base = """
        **Understanding Backtest Results:**
        
        **Key Metrics:**
        - **CAGR**: Annualized return (higher is better, but be realistic!)
        - **Sharpe Ratio**: Risk-adjusted return (>1 is good, >2 is excellent)
        - **Max Drawdown**: Worst peak-to-trough decline (lower is better)
        - **Win Rate**: Percentage of profitable trades (>50% is good)
        
        **Red Flags:**
        - Very high returns (>50% CAGR) - might be overfitted
        - Very low Sharpe (<0.5) - poor risk-adjusted returns
        - High drawdown (>30%) - high risk
        
        **Remember:** Past performance doesn't guarantee future results!
        """
        
        if context and 'results' in context:
            results = context['results']
            specific = f"\n\n**Your Results:**\n"
            specific += f"- CAGR: {results.get('cagr', 'N/A')}%\n"
            specific += f"- Sharpe: {results.get('sharpe_ratio', 'N/A')}\n"
            specific += f"- Max Drawdown: {results.get('max_drawdown', 'N/A')}%\n"
            return base + specific
        
        return base
    
    def _explain_risk(self, context: Optional[Dict]) -> str:
        return """
        **Understanding Portfolio Risk:**
        
        **Types of Risk:**
        1. **Market Risk**: Overall market movements
        2. **Sector Risk**: Industry-specific issues
        3. **Company Risk**: Individual stock problems
        
        **Risk Metrics:**
        - **Volatility**: How much prices fluctuate (higher = riskier)
        - **Sharpe Ratio**: Return per unit of risk (higher is better)
        - **Max Drawdown**: Worst loss from peak
        
        **Diversification:**
        - Don't put all eggs in one basket!
        - Spread across sectors
        - Mix of large/mid/small cap
        - Different asset classes
        
        **Rule of Thumb:**
        - Diversified portfolio: 10-20 stocks across 5+ sectors
        - Don't let one stock be >10% of portfolio
        - Rebalance periodically
        """
    
    def _general_help(self, message: str) -> str:
        return f"""
        I'm here to help you learn about stock analysis and trading!
        
        I can help with:
        - Explaining technical indicators (RSI, MACD, Moving Averages)
        - Interpreting backtest results
        - Understanding portfolio risk
        - Trading strategies and concepts
        
        **What would you like to know?**
        
        Try asking:
        - "Explain RSI"
        - "What is a good Sharpe ratio?"
        - "How to read backtest results?"
        - "Explain diversification"
        
        {self.disclaimer}
        """
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history."""
        return self.conversation_history[-limit:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

