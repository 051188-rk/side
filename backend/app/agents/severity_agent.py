from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.core.logging import log


class SeverityAgent(BaseAgent):
    def __init__(self):
        super().__init__("severity_agent")
        self.severity_levels = ["Low", "Medium", "High", "Critical"]

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        category = input_data.get("category", "")
        
        if not content:
            raise ValueError("Content is required")
        
        system_prompt = f"""You are a severity assessment expert. Assess the severity of the feedback based on:
- Impact on users
- Urgency of the issue
- Potential business impact
- Number of affected users (if mentioned)

Severity levels: {', '.join(self.severity_levels)}

Respond with a JSON object containing:
- severity: the selected severity level
- confidence: a float between 0 and 1 indicating confidence
- reasoning: a brief explanation for the severity assessment
- impact_factors: a list of factors that influenced the decision"""

        prompt = f"""Assess the severity of this feedback:
Category: {category}
Content: {content}"""
        
        schema = {
            "type": "object",
            "properties": {
                "severity": {"type": "string", "enum": self.severity_levels},
                "confidence": {"type": "number"},
                "reasoning": {"type": "string"},
                "impact_factors": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["severity", "confidence", "reasoning", "impact_factors"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        log.info(f"Assessed severity for feedback: {feedback_id} as {result['severity']}")
        
        return {
            "severity": result["severity"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
            "impact_factors": result["impact_factors"],
        }

    async def get_severity_score(self, severity: str) -> float:
        severity_scores = {
            "Low": 0.25,
            "Medium": 0.5,
            "High": 0.75,
            "Critical": 1.0,
        }
        return severity_scores.get(severity, 0.5)
