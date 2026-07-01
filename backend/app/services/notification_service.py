"""
Notification service layer

This module contains business logic for notification operations.
"""

from typing import List, Optional
from app.repositories.notification_repository import NotificationRepository
from app.integrations.smtp_integration import smtp_integration
from app.core.logging import log


class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    async def create_notification(
        self,
        recipient_id: str,
        title: str,
        message: str,
        notification_type: str,
        metadata: Optional[dict] = None
    ) -> str:
        """Create a notification."""
        notification_id = await self.notification_repo.create_notification(
            recipient_id=recipient_id,
            title=title,
            message=message,
            notification_type=notification_type,
            metadata=metadata or {}
        )
        
        log.info(f"Created notification: {notification_id}")
        return notification_id

    async def send_email_notification(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        html: bool = True
    ) -> bool:
        """Send an email notification."""
        try:
            await smtp_integration.send_email(
                to_email=recipient_email,
                subject=subject,
                body=body,
                html=html
            )
            log.info(f"Sent email to {recipient_email}")
            return True
        except Exception as e:
            log.error(f"Failed to send email: {e}")
            return False

    async def get_user_notifications(
        self,
        recipient_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[dict]:
        """Get notifications for a user."""
        if unread_only:
            return await self.notification_repo.get_unread(recipient_id, limit)
        return await self.notification_repo.get_by_recipient(recipient_id, limit)

    async def mark_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        return await self.notification_repo.mark_as_read(notification_id)

    async def mark_all_as_read(self, recipient_id: str) -> bool:
        """Mark all notifications as read for a user."""
        return await self.notification_repo.mark_all_as_read(recipient_id)


notification_service = NotificationService()
