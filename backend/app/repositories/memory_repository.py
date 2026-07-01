from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class MemoryRepository(BaseRepository):
    def __init__(self):
        super().__init__("memory")

    async def create_memory(
        self,
        memory_type: str,
        content: str,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        related_entities: Optional[List[str]] = None
    ) -> str:
        data = {
            "memory_type": memory_type,
            "content": content,
            "embedding": embedding,
            "metadata": metadata or {},
            "related_entities": related_entities or [],
            "access_count": 0,
        }
        return await self.create(data)

    async def get_by_type(self, memory_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "memory_type", "op": "==", "value": memory_type}], limit=limit)

    async def get_by_entity(self, entity_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "related_entities", "op": "array_contains", "value": entity_id}], limit=limit)

    async def search_by_content(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query_ref = self.db.collection(self.collection_name)
        query_ref = query_ref.where("content", ">=", query)
        query_ref = query_ref.where("content", "<=", query + "\uf8ff")
        query_ref = query_ref.limit(limit)
        docs = query_ref.get()
        return [self._doc_to_dict(doc) for doc in docs]

    async def increment_access(self, memory_id: str) -> bool:
        memory = await self.get_by_id(memory_id)
        if memory:
            current_count = memory.get("access_count", 0)
            return await self.update(memory_id, {"access_count": current_count + 1})
        return False

    async def update_embedding(self, memory_id: str, embedding: List[float]) -> bool:
        return await self.update(memory_id, {"embedding": embedding})

    async def add_related_entity(self, memory_id: str, entity_id: str) -> bool:
        memory = await self.get_by_id(memory_id)
        if memory:
            related_entities = memory.get("related_entities", [])
            if entity_id not in related_entities:
                related_entities.append(entity_id)
                return await self.update(memory_id, {"related_entities": related_entities})
        return False
