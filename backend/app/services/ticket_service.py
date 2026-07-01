"""
Ticket service layer

This module contains business logic for ticket operations.
"""

from typing import List, Optional, Dict, Any
from app.repositories.ticket_repository import TicketRepository
from app.repositories.ticket_update_repository import TicketUpdateRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.core.logging import log


class TicketService:
    def __init__(self):
        self.ticket_repo = TicketRepository()
        self.ticket_update_repo = TicketUpdateRepository()
        self.feedback_repo = FeedbackRepository()

    async def create_ticket_from_feedback(
        self,
        feedback_id: str,
        title: str,
        description: str,
        category: str,
        severity: str,
        priority_score: float
    ) -> str:
        """Create a ticket from feedback."""
        feedback = await self.feedback_repo.get_by_id(feedback_id)
        if not feedback:
            raise ValueError(f"Feedback not found: {feedback_id}")
        
        ticket_id = await self.ticket_repo.create_ticket(
            title=title,
            description=description,
            category=category,
            severity=severity,
            priority_score=priority_score,
            organization_id=feedback.get("metadata", {}).get("organization_id")
        )
        
        # Link feedback to ticket
        await self.feedback_repo.link_to_ticket(feedback_id, ticket_id)
        
        log.info(f"Created ticket {ticket_id} from feedback {feedback_id}")
        return ticket_id

    async def assign_ticket(self, ticket_id: str, assignee: str, user_id: str) -> bool:
        """Assign a ticket to a user."""
        await self.ticket_repo.assign_ticket(ticket_id, assignee)
        
        # Log the assignment
        await self.ticket_update_repo.create_update(
            ticket_id=ticket_id,
            author_id=user_id,
            content=f"Assigned to {assignee}",
            update_type="assignment"
        )
        
        log.info(f"Assigned ticket {ticket_id} to {assignee}")
        return True

    async def resolve_ticket(self, ticket_id: str, resolution: str, user_id: str) -> bool:
        """Resolve a ticket."""
        await self.ticket_repo.resolve_ticket(ticket_id, resolution)
        
        # Log the resolution
        await self.ticket_update_repo.create_update(
            ticket_id=ticket_id,
            author_id=user_id,
            content=f"Resolved: {resolution}",
            update_type="resolution"
        )
        
        log.info(f"Resolved ticket {ticket_id}")
        return True

    async def get_ticket_history(self, ticket_id: str) -> List[Dict[str, Any]]:
        """Get the complete history of a ticket."""
        updates = await self.ticket_update_repo.get_by_ticket(ticket_id)
        return updates

    async def get_high_priority_tickets(self, min_score: float = 0.7, limit: int = 50) -> List[Dict[str, Any]]:
        """Get tickets with high priority scores."""
        return await self.ticket_repo.get_high_priority(min_score, limit)


ticket_service = TicketService()
