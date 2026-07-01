"""
Classification agent prompt templates
"""

CLASSIFICATION_SYSTEM_PROMPT = """You are a feedback classification expert. Classify the given feedback into one of these categories:
Bug, Feature Request, Question, Complaint, Praise, Security, Payment, Account, Other.

Respond with a JSON object containing:
- category: the selected category
- confidence: a float between 0 and 1 indicating confidence
- reasoning: a brief explanation for the classification"""

CLASSIFICATION_USER_PROMPT = """Classify this feedback:

{content}"""

CLASSIFICATION_CATEGORIES = [
    "Bug",
    "Feature Request",
    "Question",
    "Complaint",
    "Praise",
    "Security",
    "Payment",
    "Account",
    "Other"
]
