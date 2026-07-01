from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class DuplicateClusterRepository(BaseRepository):
    def __init__(self):
        super().__init__("duplicate_clusters")

    async def create_cluster(
        self,
        representative_feedback_id: str,
        similarity_threshold: float,
        feedback_ids: List[str],
        title: str,
        description: str
    ) -> str:
        data = {
            "representative_feedback_id": representative_feedback_id,
            "similarity_threshold": similarity_threshold,
            "feedback_ids": feedback_ids,
            "title": title,
            "description": description,
            "ticket_id": None,
            "status": "open",
            "count": len(feedback_ids),
        }
        return await self.create(data)

    async def get_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "status", "op": "==", "value": status}], limit=limit)

    async def get_by_ticket(self, ticket_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "ticket_id", "op": "==", "value": ticket_id}], limit=limit)

    async def get_large_clusters(self, min_count: int = 5, limit: int = 100) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("count", ">=", min_count)
        query = query.order_by("count", direction=Query.DESCENDING)
        query = query.limit(limit)
        docs = query.get()
        return [self._doc_to_dict(doc) for doc in docs]

    async def add_feedback(self, cluster_id: str, feedback_id: str) -> bool:
        cluster = await self.get_by_id(cluster_id)
        if cluster:
            feedback_ids = cluster.get("feedback_ids", [])
            if feedback_id not in feedback_ids:
                feedback_ids.append(feedback_id)
                count = cluster.get("count", 0) + 1
                return await self.update(cluster_id, {"feedback_ids": feedback_ids, "count": count})
        return False

    async def link_to_ticket(self, cluster_id: str, ticket_id: str) -> bool:
        return await self.update(cluster_id, {"ticket_id": ticket_id, "status": "linked"})

    async def close_cluster(self, cluster_id: str) -> bool:
        return await self.update(cluster_id, {"status": "closed"})
