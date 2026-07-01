from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class TicketUpdateRepository(BaseRepository):
    def __init__(self):
        super().__init__("ticket_updates")

    async def create_update(
        self,
        ticket_id: str,
        author_id: str,
        content: str,
        update_type: str = "comment"
    ) -> str:
        data = {
            "ticket_id": ticket_id,
            "author_id": author_id,
            "content": content,
            "update_type": update_type,
        }
        return await self.create(data)

    async def get_by_ticket(self, ticket_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "ticket_id", "op": "==", "value": ticket_id}], limit=limit, order_by="created_at")

    async def get_by_author(self, author_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "author_id", "op": "==", "value": author_id}], limit=limit)

    async def get_by_type(self, update_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "update_type", "op": "==", "value": update_type}], limit=limit)
