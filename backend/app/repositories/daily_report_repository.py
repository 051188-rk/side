from typing import Optional, List, Dict, Any
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.core.logging import log
from app.utils.date_utils import get_start_of_day, get_end_of_day, utc_now


class DailyReportRepository(BaseRepository):
    def __init__(self):
        super().__init__("daily_reports")

    async def create_report(
        self,
        report_date: datetime,
        report_type: str,
        data: Dict[str, Any],
        organization_id: Optional[str] = None
    ) -> str:
        daily_report_data = {
            "report_date": self._serialize_datetime(get_start_of_day(report_date)),
            "report_type": report_type,
            "data": data,
            "organization_id": organization_id,
        }
        return await self.create(daily_report_data)

    async def get_by_date(self, report_date: datetime, report_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        start = get_start_of_day(report_date)
        end = get_end_of_day(report_date)
        
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("report_date", ">=", self._serialize_datetime(start))
        query = query.where("report_date", "<=", self._serialize_datetime(end))
        
        if report_type:
            query = query.where("report_type", "==", report_type)
        
        query = query.limit(1)
        docs = query.get()
        results = [self._doc_to_dict(doc) for doc in docs]
        return results[0] if results else None

    async def get_by_type(self, report_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "report_type", "op": "==", "value": report_type}], limit=limit, order_by="report_date")

    async def get_by_organization(self, organization_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "organization_id", "op": "==", "value": organization_id}], limit=limit, order_by="report_date")

    async def get_recent_reports(self, limit: int = 30) -> List[Dict[str, Any]]:
        return await self.list_all(limit=limit, order_by="report_date")

    async def get_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        report_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("report_date", ">=", self._serialize_datetime(get_start_of_day(start_date)))
        query = query.where("report_date", "<=", self._serialize_datetime(get_end_of_day(end_date)))
        
        if report_type:
            query = query.where("report_type", "==", report_type)
        
        query = query.order_by("report_date", direction=Query.DESCENDING)
        query = query.limit(limit)
        docs = query.get()
        return [self._doc_to_dict(doc) for doc in docs]
