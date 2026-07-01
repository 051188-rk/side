from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class ActivityLogRepository(BaseRepository):
    def __init__(self):
        super().__init__("activity_logs")

    async def create_log(
        self,
        action: str,
        entity_type: str,
        entity_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user_id,
            "metadata": metadata or {},
        }
        return await self.create(data)

    async def get_by_entity(self, entity_type: str, entity_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([
            {"field": "entity_type", "op": "==", "value": entity_type},
            {"field": "entity_id", "op": "==", "value": entity_id}
        ], limit=limit, order_by="created_at")

    async def get_by_user(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "user_id", "op": "==", "value": user_id}], limit=limit, order_by="created_at")

    async def get_by_action(self, action: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "action", "op": "==", "value": action}], limit=limit)

    async def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.list_all(limit=limit, order_by="created_at")
