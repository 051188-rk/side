from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__("notifications")

    async def create_notification(
        self,
        recipient_id: str,
        title: str,
        message: str,
        notification_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "recipient_id": recipient_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "metadata": metadata or {},
            "read": False,
            "sent": False,
        }
        return await self.create(data)

    async def get_by_recipient(self, recipient_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "recipient_id", "op": "==", "value": recipient_id}], limit=limit, order_by="created_at")

    async def get_unread(self, recipient_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        results = await self.query([
            {"field": "recipient_id", "op": "==", "value": recipient_id},
            {"field": "read", "op": "==", "value": False}
        ], limit=limit, order_by="created_at")
        return results

    async def get_by_type(self, notification_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "notification_type", "op": "==", "value": notification_type}], limit=limit)

    async def mark_as_read(self, notification_id: str) -> bool:
        return await self.update(notification_id, {"read": True})

    async def mark_as_sent(self, notification_id: str) -> bool:
        return await self.update(notification_id, {"sent": True})

    async def mark_all_as_read(self, recipient_id: str) -> bool:
        notifications = await self.get_unread(recipient_id, limit=1000)
        for notification in notifications:
            await self.mark_as_read(notification["id"])
        return True
