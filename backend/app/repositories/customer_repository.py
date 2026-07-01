from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__("customers")

    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        source: Optional[str] = None,
        external_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "email": email,
            "name": name,
            "source": source,
            "external_id": external_id,
            "metadata": metadata or {},
            "tier": "standard",
            "feedback_count": 0,
            "is_active": True,
        }
        return await self.create(data)

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        results = await self.query([{"field": "email", "op": "==", "value": email}], limit=1)
        return results[0] if results else None

    async def get_by_external_id(self, external_id: str, source: str) -> Optional[Dict[str, Any]]:
        results = await self.query([
            {"field": "external_id", "op": "==", "value": external_id},
            {"field": "source", "op": "==", "value": source}
        ], limit=1)
        return results[0] if results else None

    async def get_by_source(self, source: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "source", "op": "==", "value": source}], limit=limit)

    async def get_by_tier(self, tier: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "tier", "op": "==", "value": tier}], limit=limit)

    async def update_tier(self, customer_id: str, tier: str) -> bool:
        return await self.update(customer_id, {"tier": tier})

    async def increment_feedback_count(self, customer_id: str) -> bool:
        customer = await self.get_by_id(customer_id)
        if customer:
            current_count = customer.get("feedback_count", 0)
            return await self.update(customer_id, {"feedback_count": current_count + 1})
        return False

    async def deactivate_customer(self, customer_id: str) -> bool:
        return await self.update(customer_id, {"is_active": False})
