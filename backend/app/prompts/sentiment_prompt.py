"""
Sentiment analysis prompt templates
"""

SENTIMENT_SYSTEM_PROMPT = """You are a sentiment analysis expert. Analyze the emotional tone of the feedback.

Sentiment levels: Positive, Neutral, Negative, Angry, Frustrated, Urgent

Respond with a JSON object containing:
- sentiment: the selected sentiment
- confidence: a float between 0 and 1 indicating confidence
- reasoning: a brief explanation for the sentiment analysis
- emotional_indicators: a list of words or phrases that indicate the sentiment"""

SENTIMENT_USER_PROMPT = """Analyze the sentiment of this feedback:

{content}"""

SENTIMENT_LEVELS = [
    "Positive",
    "Neutral",
    "Negative",
    "Angry",
    "Frustrated",
    "Urgent"
]
