from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import time
from app.repositories.agent_run_repository import AgentRunRepository
from app.core.logging import log


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.agent_run_repo = AgentRunRepository()

    async def execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        run_id = await self.agent_run_repo.create_agent_run(
            self.name,
            input_data,
            feedback_id,
            ticket_id
        )
        
        start_time = time.time()
        try:
            result = await self._execute(input_data, feedback_id, ticket_id)
            duration_ms = int((time.time() - start_time) * 1000)
            
            await self.agent_run_repo.complete_run(run_id, result, duration_ms)
            log.info(f"Agent {self.name} completed in {duration_ms}ms")
            
            return {
                "success": True,
                "result": result,
                "duration_ms": duration_ms,
            }
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_message = str(e)
            
            await self.agent_run_repo.fail_run(run_id, error_message, duration_ms)
            log.error(f"Agent {self.name} failed: {error_message}")
            
            return {
                "success": False,
                "error": error_message,
                "duration_ms": duration_ms,
            }

    @abstractmethod
    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        pass
