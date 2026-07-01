from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.repositories.ticket_repository import TicketRepository
from app.core.logging import log


class TicketGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ticket_generation_agent")
        self.ticket_repo = TicketRepository()

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        category = input_data.get("category", "")
        severity = input_data.get("severity", "")
        sentiment = input_data.get("sentiment", "")
        
        if not content:
            raise ValueError("Content is required")
        
        system_prompt = """You are a ticket generation expert. Generate a comprehensive ticket from the feedback.

Respond with a JSON object containing:
- title: a concise, descriptive title (max 100 characters)
- summary: a brief summary of the issue (max 200 characters)
- description: a detailed description of the issue
- affected_feature: the feature or component affected
- suggested_owner: the suggested owner/team (e.g., "frontend", "backend", "devops")
- reproduction_steps: a list of steps to reproduce the issue (if applicable)
- labels: a list of relevant labels
- priority: suggested priority based on severity"""

        prompt = f"""Generate a ticket from this feedback:
Category: {category}
Severity: {severity}
Sentiment: {sentiment}
Content: {content}"""
        
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "description": {"type": "string"},
                "affected_feature": {"type": "string"},
                "suggested_owner": {"type": "string"},
                "reproduction_steps": {"type": "array", "items": {"type": "string"}},
                "labels": {"type": "array", "items": {"type": "string"}},
                "priority": {"type": "string"}
            },
            "required": ["title", "summary", "description", "affected_feature", "suggested_owner"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        ticket_id = await self.ticket_repo.create_ticket(
            title=result["title"],
            description=result["description"],
            category=category,
            severity=severity,
            priority_score=0.5,
            suggested_owner=result["suggested_owner"],
            labels=result.get("labels", []),
            affected_feature=result.get("affected_feature"),
            reproduction_steps=result.get("reproduction_steps", []),
            organization_id=input_data.get("organization_id")
        )
        
        log.info(f"Generated ticket {ticket_id} from feedback {feedback_id}")
        
        return {
            "ticket_id": ticket_id,
            "title": result["title"],
            "summary": result["summary"],
            "description": result["description"],
            "affected_feature": result.get("affected_feature"),
            "suggested_owner": result["suggested_owner"],
            "reproduction_steps": result.get("reproduction_steps", []),
            "labels": result.get("labels", []),
        }
