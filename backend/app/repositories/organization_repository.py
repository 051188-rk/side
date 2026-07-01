from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class OrganizationRepository(BaseRepository):
    def __init__(self):
        super().__init__("organizations")

    async def create_organization(
        self,
        name: str,
        slug: str,
        plan: str = "free",
        settings: Optional[Dict[str, Any]] = None
    ) -> str:
        data = {
            "name": name,
            "slug": slug,
            "plan": plan,
            "settings": settings or {},
            "is_active": True,
            "member_count": 1,
        }
        return await self.create(data)

    async def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        results = await self.query([{"field": "slug", "op": "==", "value": slug}], limit=1)
        return results[0] if results else None

    async def get_by_plan(self, plan: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "plan", "op": "==", "value": plan}], limit=limit)

    async def update_settings(self, org_id: str, settings: Dict[str, Any]) -> bool:
        return await self.update(org_id, {"settings": settings})

    async def increment_member_count(self, org_id: str) -> bool:
        org = await self.get_by_id(org_id)
        if org:
            current_count = org.get("member_count", 0)
            return await self.update(org_id, {"member_count": current_count + 1})
        return False

    async def decrement_member_count(self, org_id: str) -> bool:
        org = await self.get_by_id(org_id)
        if org:
            current_count = org.get("member_count", 0)
            return await self.update(org_id, {"member_count": max(0, current_count - 1)})
        return False
