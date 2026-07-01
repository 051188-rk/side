from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.core.logging import log


class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("sentiment_agent")
        self.sentiments = ["Positive", "Neutral", "Negative", "Angry", "Frustrated", "Urgent"]

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        if not content:
            raise ValueError("Content is required")
        
        system_prompt = f"""You are a sentiment analysis expert. Analyze the emotional tone of the feedback.

Sentiment levels: {', '.join(self.sentiments)}

Respond with a JSON object containing:
- sentiment: the selected sentiment
- confidence: a float between 0 and 1 indicating confidence
- reasoning: a brief explanation for the sentiment analysis
- emotional_indicators: a list of words or phrases that indicate the sentiment"""

        prompt = f"Analyze the sentiment of this feedback:\n\n{content}"
        
        schema = {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string", "enum": self.sentiments},
                "confidence": {"type": "number"},
                "reasoning": {"type": "string"},
                "emotional_indicators": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["sentiment", "confidence", "reasoning", "emotional_indicators"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        log.info(f"Analyzed sentiment for feedback: {feedback_id} as {result['sentiment']}")
        
        return {
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
            "emotional_indicators": result["emotional_indicators"],
        }

    async def get_sentiment_score(self, sentiment: str) -> float:
        sentiment_scores = {
            "Positive": 1.0,
            "Neutral": 0.5,
            "Negative": 0.0,
            "Angry": -0.5,
            "Frustrated": -0.3,
            "Urgent": 0.7,
        }
        return sentiment_scores.get(sentiment, 0.5)
