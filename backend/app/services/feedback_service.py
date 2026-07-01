"""
Feedback service layer

This module contains business logic for feedback operations.
"""

from typing import List, Optional, Dict, Any
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.customer_repository import CustomerRepository
from app.graphs.feedback_graph import feedback_graph
from app.core.logging import log


class FeedbackService:
    def __init__(self):
        self.feedback_repo = FeedbackRepository()
        self.customer_repo = CustomerRepository()

    async def create_feedback(
        self,
        source: str,
        content: str,
        customer_email: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create new feedback and optionally process it."""
        # Get or create customer
        customer_id = None
        if customer_email:
            customer = await self.customer_repo.get_by_email(customer_email)
            if customer:
                customer_id = customer["id"]
        
        # Create feedback
        feedback_id = await self.feedback_repo.create_feedback(
            source=source,
            content=content,
            customer_id=customer_id,
            metadata=metadata or {}
        )
        
        log.info(f"Created feedback: {feedback_id}")
        return feedback_id

    async def process_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """Process feedback through the AI agent graph."""
        feedback = await self.feedback_repo.get_by_id(feedback_id)
        if not feedback:
            raise ValueError(f"Feedback not found: {feedback_id}")
        
        result = await feedback_graph.process(
            content=feedback["content"],
            context={"feedback_id": feedback_id}
        )
        
        # Update feedback with processing results
        await self.feedback_repo.mark_processed(feedback_id, result.get("ticket_id"))
        
        log.info(f"Processed feedback: {feedback_id}")
        return result

    async def get_feedback_by_customer(self, customer_email: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all feedback from a customer."""
        customer = await self.customer_repo.get_by_email(customer_email)
        if not customer:
            return []
        
        return await self.feedback_repo.get_by_customer(customer["id"], limit)

    async def get_unprocessed_feedback(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get feedback that hasn't been processed yet."""
        return await self.feedback_repo.get_unprocessed(limit)


feedback_service = FeedbackService()
