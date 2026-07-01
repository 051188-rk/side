from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.repositories.ticket_repository import TicketRepository
from app.core.logging import log


class PriorityAgent(BaseAgent):
    def __init__(self):
        super().__init__("priority_agent")
        self.ticket_repo = TicketRepository()

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        severity = input_data.get("severity", "Medium")
        sentiment = input_data.get("sentiment", "Neutral")
        duplicate_count = input_data.get("duplicate_count", 0)
        affected_users = input_data.get("affected_users", 1)
        customer_tier = input_data.get("customer_tier", "standard")
        category = input_data.get("category", "")
        
        system_prompt = f"""You are a priority calculation expert. Calculate a priority score (0.0 to 1.0) based on:
- Severity: {severity}
- Sentiment: {sentiment}
- Duplicate count: {duplicate_count}
- Affected users: {affected_users}
- Customer tier: {customer_tier}
- Category: {category}

Consider:
- Higher severity increases priority
- Negative sentiment increases priority
- More duplicates increase priority
- More affected users increase priority
- Higher customer tier increases priority
- Certain categories (Security, Payment) have higher priority

Respond with a JSON object containing:
- priority_score: a float between 0.0 and 1.0
- priority_level: one of "Low", "Medium", "High", "Critical"
- reasoning: a brief explanation for the priority score
- factors: a breakdown of how each factor contributed"""

        prompt = f"""Calculate priority for this ticket with the following factors:
Severity: {severity}
Sentiment: {sentiment}
Duplicate count: {duplicate_count}
Affected users: {affected_users}
Customer tier: {customer_tier}
Category: {category}"""
        
        schema = {
            "type": "object",
            "properties": {
                "priority_score": {"type": "number"},
                "priority_level": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
                "reasoning": {"type": "string"},
                "factors": {"type": "object"}
            },
            "required": ["priority_score", "priority_level", "reasoning", "factors"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        if ticket_id:
            await self.ticket_repo.update(ticket_id, {
                "priority_score": result["priority_score"]
            })
        
        log.info(f"Calculated priority for ticket {ticket_id}: {result['priority_level']} ({result['priority_score']})")
        
        return {
            "priority_score": result["priority_score"],
            "priority_level": result["priority_level"],
            "reasoning": result["reasoning"],
            "factors": result["factors"],
        }
