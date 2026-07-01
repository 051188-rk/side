from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class MessageRepository(BaseRepository):
    def __init__(self):
        super().__init__("messages")

    async def create_message(
        self,
        channel: str,
        direction: str,
        content: str,
        customer_id: Optional[str] = None,
        external_message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "channel": channel,
            "direction": direction,
            "content": content,
            "customer_id": customer_id,
            "external_message_id": external_message_id,
            "metadata": metadata or {},
            "read": False,
        }
        return await self.create(data)

    async def get_by_channel(self, channel: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "channel", "op": "==", "value": channel}], limit=limit)

    async def get_by_customer(self, customer_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "customer_id", "op": "==", "value": customer_id}], limit=limit)

    async def get_by_direction(self, direction: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "direction", "op": "==", "value": direction}], limit=limit)

    async def get_unread(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "read", "op": "==", "value": False}], limit=limit)

    async def mark_as_read(self, message_id: str) -> bool:
        return await self.update(message_id, {"read": True})

    async def get_by_external_id(self, external_message_id: str, channel: str) -> Optional[Dict[str, Any]]:
        results = await self.query([
            {"field": "external_message_id", "op": "==", "value": external_message_id},
            {"field": "channel", "op": "==", "value": channel}
        ], limit=1)
        return results[0] if results else None
