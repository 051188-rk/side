from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class AgentRunRepository(BaseRepository):
    def __init__(self):
        super().__init__("agent_runs")

    async def create_agent_run(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> str:
        data = {
            "agent_name": agent_name,
            "input_data": input_data,
            "feedback_id": feedback_id,
            "ticket_id": ticket_id,
            "status": "running",
            "output_data": None,
            "error": None,
            "duration_ms": None,
        }
        return await self.create(data)

    async def get_by_agent(self, agent_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "agent_name", "op": "==", "value": agent_name}], limit=limit)

    async def get_by_feedback(self, feedback_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "feedback_id", "op": "==", "value": feedback_id}], limit=limit)

    async def get_by_ticket(self, ticket_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "ticket_id", "op": "==", "value": ticket_id}], limit=limit)

    async def get_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "status", "op": "==", "value": status}], limit=limit)

    async def complete_run(self, run_id: str, output_data: Dict[str, Any], duration_ms: int) -> bool:
        return await self.update(run_id, {
            "status": "completed",
            "output_data": output_data,
            "duration_ms": duration_ms
        })

    async def fail_run(self, run_id: str, error: str, duration_ms: int) -> bool:
        return await self.update(run_id, {
            "status": "failed",
            "error": error,
            "duration_ms": duration_ms
        })

    async def get_recent_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.list_all(limit=limit, order_by="created_at")
