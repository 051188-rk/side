from typing import Optional, List, Dict, Any
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__("tickets")

    async def create_ticket(
        self,
        title: str,
        description: str,
        category: str,
        severity: str,
        priority_score: float,
        suggested_owner: Optional[str] = None,
        labels: Optional[List[str]] = None,
        affected_feature: Optional[str] = None,
        reproduction_steps: Optional[List[str]] = None,
        related_tickets: Optional[List[str]] = None,
        organization_id: Optional[str] = None
    ) -> str:
        data = {
            "title": title,
            "description": description,
            "category": category,
            "severity": severity,
            "priority_score": priority_score,
            "suggested_owner": suggested_owner,
            "labels": labels or [],
            "affected_feature": affected_feature,
            "reproduction_steps": reproduction_steps or [],
            "related_tickets": related_tickets or [],
            "organization_id": organization_id,
            "status": "open",
            "assignee": None,
            "resolution": None,
            "resolved_at": None,
        }
        return await self.create(data)

    async def get_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "status", "op": "==", "value": status}], limit=limit)

    async def get_by_category(self, category: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "category", "op": "==", "value": category}], limit=limit)

    async def get_by_severity(self, severity: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "severity", "op": "==", "value": severity}], limit=limit)

    async def get_by_organization(self, organization_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "organization_id", "op": "==", "value": organization_id}], limit=limit)

    async def get_by_assignee(self, assignee: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "assignee", "op": "==", "value": assignee}], limit=limit)

    async def get_high_priority(self, min_score: float = 0.7, limit: int = 100) -> List[Dict[str, Any]]:
        from firebase_admin.firestore import Query
        query = self.db.collection(self.collection_name)
        query = query.where("priority_score", ">=", min_score)
        query = query.order_by("priority_score", direction=Query.DESCENDING)
        query = query.limit(limit)
        docs = query.get()
        return [self._doc_to_dict(doc) for doc in docs]

    async def assign_ticket(self, ticket_id: str, assignee: str) -> bool:
        return await self.update(ticket_id, {"assignee": assignee, "status": "assigned"})

    async def update_status(self, ticket_id: str, status: str) -> bool:
        update_data = {"status": status}
        if status == "resolved":
            update_data["resolved_at"] = self._serialize_datetime(utc_now())
        return await self.update(ticket_id, update_data)

    async def resolve_ticket(self, ticket_id: str, resolution: str) -> bool:
        return await self.update(ticket_id, {
            "status": "resolved",
            "resolution": resolution,
            "resolved_at": self._serialize_datetime(utc_now())
        })

    async def close_ticket(self, ticket_id: str) -> bool:
        return await self.update(ticket_id, {"status": "closed"})

    async def reopen_ticket(self, ticket_id: str) -> bool:
        return await self.update(ticket_id, {
            "status": "open",
            "resolution": None,
            "resolved_at": None
        })

    async def add_related_ticket(self, ticket_id: str, related_ticket_id: str) -> bool:
        ticket = await self.get_by_id(ticket_id)
        if ticket:
            related_tickets = ticket.get("related_tickets", [])
            if related_ticket_id not in related_tickets:
                related_tickets.append(related_ticket_id)
                return await self.update(ticket_id, {"related_tickets": related_tickets})
        return False

    async def add_label(self, ticket_id: str, label: str) -> bool:
        ticket = await self.get_by_id(ticket_id)
        if ticket:
            labels = ticket.get("labels", [])
            if label not in labels:
                labels.append(label)
                return await self.update(ticket_id, {"labels": labels})
        return False
