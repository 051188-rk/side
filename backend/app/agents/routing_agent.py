from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.core.logging import log


class RoutingAgent(BaseAgent):
    def __init__(self):
        super().__init__("routing_agent")
        self.available_agents = [
            "feedback_collector",
            "feedback_cleaner",
            "classification",
            "severity",
            "sentiment",
            "duplicate_detection",
            "ticket_generation",
            "priority",
            "memory",
            "insight",
            "response_draft",
            "search",
            "fetch",
        ]

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        task_type = input_data.get("task_type", "process_feedback")
        content = input_data.get("content", "")
        context = input_data.get("context", {})
        
        if task_type == "process_feedback":
            workflow = await self._determine_feedback_workflow(content, context)
        elif task_type == "generate_insights":
            workflow = await self._determine_insight_workflow(context)
        elif task_type == "search_context":
            workflow = await self._determine_search_workflow(content, context)
        else:
            workflow = await self._determine_custom_workflow(task_type, context)
        
        log.info(f"Routing agent determined workflow: {workflow}")
        
        return {
            "task_type": task_type,
            "workflow": workflow,
            "agents_to_execute": workflow["agents"],
            "execution_order": workflow["order"],
        }

    async def _determine_feedback_workflow(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = f"""You are a workflow routing expert. Determine which agents should execute for processing feedback.

Available agents: {', '.join(self.available_agents)}

Standard feedback processing workflow:
1. feedback_cleaner - clean and normalize the feedback
2. classification - categorize the feedback
3. sentiment - analyze emotional tone
4. severity - assess severity level
5. duplicate_detection - check for duplicates
6. memory - store in long-term memory
7. ticket_generation - create a ticket if needed
8. priority - calculate priority score

Conditional routing:
- If category is "Bug" or "Security": include severity and priority
- If duplicate found: skip ticket_generation, link to existing ticket
- If sentiment is "Angry" or "Urgent": include response_draft
- If category is "Question": include search and fetch agents

Respond with a JSON object containing:
- agents: list of agents to execute
- order: execution order (list of agent names)
- reasoning: explanation for the workflow"""

        prompt = f"Determine the workflow for this feedback:\n\n{content[:1000]}"
        
        schema = {
            "type": "object",
            "properties": {
                "agents": {"type": "array", "items": {"type": "string"}},
                "order": {"type": "array", "items": {"type": "string"}},
                "reasoning": {"type": "string"}
            },
            "required": ["agents", "order", "reasoning"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        return {
            "agents": result["agents"],
            "order": result["order"],
            "reasoning": result["reasoning"],
        }

    async def _determine_insight_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        insight_type = context.get("insight_type", "daily_summary")
        
        if insight_type == "daily_summary":
            return {
                "agents": ["insight"],
                "order": ["insight"],
                "reasoning": "Daily summary only requires insight agent",
            }
        elif insight_type == "weekly_summary":
            return {
                "agents": ["insight", "memory"],
                "order": ["memory", "insight"],
                "reasoning": "Weekly summary benefits from historical context",
            }
        elif insight_type == "trending_issues":
            return {
                "agents": ["memory", "insight"],
                "order": ["memory", "insight"],
                "reasoning": "Trending analysis requires historical data",
            }
        else:
            return {
                "agents": ["insight"],
                "order": ["insight"],
                "reasoning": "Standard insight generation",
            }

    async def _determine_search_workflow(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        search_type = context.get("search_type", "general")
        
        if search_type == "with_context":
            return {
                "agents": ["search", "fetch"],
                "order": ["search", "fetch"],
                "reasoning": "Search first, then fetch relevant content",
            }
        elif search_type == "semantic":
            return {
                "agents": ["search"],
                "order": ["search"],
                "reasoning": "Semantic search only",
            }
        else:
            return {
                "agents": ["search"],
                "order": ["search"],
                "reasoning": "Standard search",
            }

    async def _determine_custom_workflow(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "agents": ["insight"],
            "order": ["insight"],
            "reasoning": f"Custom task {task_type} using insight agent",
        }

    async def should_execute_agent(
        self,
        agent_name: str,
        context: Dict[str, Any]
    ) -> bool:
        conditions = {
            "duplicate_detection": context.get("check_duplicates", True),
            "ticket_generation": context.get("create_ticket", True),
            "response_draft": context.get("draft_response", False),
            "search": context.get("needs_search", False),
            "fetch": context.get("needs_fetch", False),
        }
        
        return conditions.get(agent_name, True)

    async def get_next_agent(
        self,
        current_agent: str,
        workflow: Dict[str, Any]
    ) -> Optional[str]:
        order = workflow.get("order", [])
        
        try:
            current_index = order.index(current_agent)
            if current_index + 1 < len(order):
                return order[current_index + 1]
        except ValueError:
            pass
        
        return None
