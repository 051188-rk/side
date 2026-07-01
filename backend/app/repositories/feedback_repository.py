from typing import Optional, List, Dict, Any
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.core.logging import log
from app.utils.date_utils import utc_now, get_start_of_day, get_end_of_day


class FeedbackRepository(BaseRepository):
    def __init__(self):
        super().__init__("feedback")

    async def create_feedback(
        self,
        source: str,
        content: str,
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "source": source,
            "content": content,
            "customer_id": customer_id,
            "metadata": metadata or {},
            "status": "pending",
            "processed": False,
            "ticket_id": None,
            "duplicate_cluster_id": None,
        }
        return await self.create(data)

    async def get_by_source(self, source: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "source", "op": "==", "value": source}], limit=limit)

    async def get_by_customer(self, customer_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "customer_id", "op": "==", "value": customer_id}], limit=limit)

    async def get_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "status", "op": "==", "value": status}], limit=limit)

    async def get_unprocessed(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "processed", "op": "==", "value": False}], limit=limit)

    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("created_at", ">=", self._serialize_datetime(start_date))
        query = query.where("created_at", "<=", self._serialize_datetime(end_date))
        query = query.order_by("created_at", direction=Query.DESCENDING)
        query = query.limit(limit)
        docs = query.get()
        return [self._doc_to_dict(doc) for doc in docs]

    async def mark_processed(self, feedback_id: str, ticket_id: Optional[str] = None) -> bool:
        update_data = {"processed": True, "status": "processed"}
        if ticket_id:
            update_data["ticket_id"] = ticket_id
        return await self.update(feedback_id, update_data)

    async def link_to_ticket(self, feedback_id: str, ticket_id: str) -> bool:
        return await self.update(feedback_id, {"ticket_id": ticket_id})

    async def link_to_duplicate_cluster(self, feedback_id: str, cluster_id: str) -> bool:
        return await self.update(feedback_id, {"duplicate_cluster_id": cluster_id})
