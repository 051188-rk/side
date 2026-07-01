from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.core.logging import log


class ResponseDraftAgent(BaseAgent):
    def __init__(self):
        super().__init__("response_draft_agent")

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        channel = input_data.get("channel", "email")
        ticket_title = input_data.get("ticket_title", "")
        resolution = input_data.get("resolution", "")
        
        if not content:
            raise ValueError("Content is required")
        
        system_prompt = f"""You are a customer response expert. Draft a professional, empathetic response to the feedback.
The response will be sent via {channel}.

Guidelines:
- Be empathetic and understanding
- Acknowledge the issue
- Explain what's being done
- Set clear expectations
- Be professional but friendly
- Keep it concise but complete

Respond with a JSON object containing:
- draft_response: the drafted response
- tone: the tone of the response (e.g., "professional", "empathetic", "formal")
- suggested_actions: a list of suggested follow-up actions
- approval_required: whether the response requires approval before sending"""

        prompt = f"""Draft a response to this feedback:
Ticket: {ticket_title}
Resolution: {resolution}
Original feedback: {content}"""
        
        schema = {
            "type": "object",
            "properties": {
                "draft_response": {"type": "string"},
                "tone": {"type": "string"},
                "suggested_actions": {"type": "array", "items": {"type": "string"}},
                "approval_required": {"type": "boolean"}
            },
            "required": ["draft_response", "tone", "suggested_actions", "approval_required"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        log.info(f"Drafted response for feedback {feedback_id} / ticket {ticket_id}")
        
        return {
            "draft_response": result["draft_response"],
            "tone": result["tone"],
            "suggested_actions": result["suggested_actions"],
            "approval_required": result["approval_required"],
            "channel": channel,
        }

    async def draft_email_response(
        self,
        feedback_content: str,
        resolution: str,
        customer_name: Optional[str] = None
    ) -> Dict[str, Any]:
        return await self.execute({
            "content": feedback_content,
            "channel": "email",
            "ticket_title": "Your Feedback",
            "resolution": resolution,
            "customer_name": customer_name,
        })

    async def draft_discord_response(
        self,
        feedback_content: str,
        resolution: str
    ) -> Dict[str, Any]:
        return await self.execute({
            "content": feedback_content,
            "channel": "discord",
            "ticket_title": "Your Feedback",
            "resolution": resolution,
        })

    async def draft_github_response(
        self,
        feedback_content: str,
        resolution: str,
        issue_number: Optional[int] = None
    ) -> Dict[str, Any]:
        return await self.execute({
            "content": feedback_content,
            "channel": "github",
            "ticket_title": f"Issue #{issue_number}" if issue_number else "Your Feedback",
            "resolution": resolution,
        })
