from typing import Optional, List, Dict, Any
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.core.logging import log
from app.utils.date_utils import get_start_of_day, get_end_of_day, utc_now


class AnalyticsRepository(BaseRepository):
    def __init__(self):
        super().__init__("analytics")

    async def create_analytics(
        self,
        metric_name: str,
        metric_value: float,
        dimensions: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ) -> str:
        data = {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "dimensions": dimensions or {},
            "timestamp": self._serialize_datetime(timestamp or utc_now()),
        }
        return await self.create(data)

    async def get_by_metric(self, metric_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "metric_name", "op": "==", "value": metric_name}], limit=limit)

    async def get_by_date_range(
        self,
        metric_name: str,
        start_date: datetime,
        end_date: datetime,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("metric_name", "==", metric_name)
        query = query.where("timestamp", ">=", self._serialize_datetime(start_date))
        query = query.where("timestamp", "<=", self._serialize_datetime(end_date))
        query = query.order_by("timestamp", direction=Query.DESCENDING)
        query = query.limit(limit)
        docs = query.get()
        return [self._doc_to_dict(doc) for doc in docs]

    async def get_today_metrics(self, metric_name: str) -> List[Dict[str, Any]]:
        today = utc_now()
        start = get_start_of_day(today)
        end = get_end_of_day(today)
        return await self.get_by_date_range(metric_name, start, end)

    async def aggregate_metric(
        self,
        metric_name: str,
        start_date: datetime,
        end_date: datetime,
        aggregation: str = "sum"
    ) -> float:
        metrics = await self.get_by_date_range(metric_name, start_date, end_date, limit=1000)
        values = [m.get("metric_value", 0) for m in metrics]
        
        if aggregation == "sum":
            return sum(values)
        elif aggregation == "avg":
            return sum(values) / len(values) if values else 0
        elif aggregation == "max":
            return max(values) if values else 0
        elif aggregation == "min":
            return min(values) if values else 0
        elif aggregation == "count":
            return len(values)
        return 0
