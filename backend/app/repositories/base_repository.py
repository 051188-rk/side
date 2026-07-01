from typing import Optional, List, Dict, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from datetime import datetime
from app.repositories.firebase_client import firebase_client
from app.core.logging import log
from app.utils.date_utils import utc_now, format_datetime, to_utc

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.db = firebase_client.db

    def _doc_to_dict(self, doc) -> Dict[str, Any]:
        if not doc.exists:
            return {}
        data = doc.to_dict()
        if data:
            data["id"] = doc.id
        return data or {}

    def _serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        if dt is None:
            return None
        return format_datetime(dt)

    def _deserialize_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        if dt_str is None:
            return None
        return to_utc(datetime.fromisoformat(dt_str))

    async def create(self, data: Dict[str, Any]) -> str:
        try:
            doc_ref = self.db.collection(self.collection_name).document()
            data["created_at"] = self._serialize_datetime(utc_now())
            data["updated_at"] = self._serialize_datetime(utc_now())
            doc_ref.set(data)
            log.info(f"Created document in {self.collection_name}: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            log.error(f"Error creating document in {self.collection_name}: {e}")
            raise

    async def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc = doc_ref.get()
            return self._doc_to_dict(doc)
        except Exception as e:
            log.error(f"Error getting document {doc_id} from {self.collection_name}: {e}")
            raise

    async def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            data["updated_at"] = self._serialize_datetime(utc_now())
            doc_ref.update(data)
            log.info(f"Updated document {doc_id} in {self.collection_name}")
            return True
        except Exception as e:
            log.error(f"Error updating document {doc_id} in {self.collection_name}: {e}")
            raise

    async def delete(self, doc_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.delete()
            log.info(f"Deleted document {doc_id} from {self.collection_name}")
            return True
        except Exception as e:
            log.error(f"Error deleting document {doc_id} from {self.collection_name}: {e}")
            raise

    async def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[str] = None,
        direction: str = "DESC"
    ) -> List[Dict[str, Any]]:
        try:
            query = self.db.collection(self.collection_name)
            
            if order_by:
                from firebase_admin.firestore import Query
                direction_enum = Query.DESCENDING if direction.upper() == "DESC" else Query.ASCENDING
                query = query.order_by(order_by, direction=direction_enum)
            
            query = query.limit(limit).offset(offset)
            docs = query.get()
            
            results = [self._doc_to_dict(doc) for doc in docs]
            log.info(f"Listed {len(results)} documents from {self.collection_name}")
            return results
        except Exception as e:
            log.error(f"Error listing documents from {self.collection_name}: {e}")
            raise

    async def query(
        self,
        filters: List[Dict[str, Any]],
        limit: int = 100,
        order_by: Optional[str] = None,
        direction: str = "DESC"
    ) -> List[Dict[str, Any]]:
        try:
            query = self.db.collection(self.collection_name)
            
            for filter_dict in filters:
                field = filter_dict.get("field")
                op = filter_dict.get("op", "==")
                value = filter_dict.get("value")
                query = query.where(field, op, value)
            
            if order_by:
                from firebase_admin.firestore import Query
                direction_enum = Query.DESCENDING if direction.upper() == "DESC" else Query.ASCENDING
                query = query.order_by(order_by, direction=direction_enum)
            
            query = query.limit(limit)
            docs = query.get()
            
            results = [self._doc_to_dict(doc) for doc in docs]
            log.info(f"Queried {len(results)} documents from {self.collection_name}")
            return results
        except Exception as e:
            log.error(f"Error querying documents from {self.collection_name}: {e}")
            raise

    async def count(self) -> int:
        try:
            docs = self.db.collection(self.collection_name).get()
            return len(docs)
        except Exception as e:
            log.error(f"Error counting documents in {self.collection_name}: {e}")
            raise

    async def exists(self, doc_id: str) -> bool:
        try:
            doc = await self.get_by_id(doc_id)
            return doc is not None and bool(doc)
        except Exception:
            return False
