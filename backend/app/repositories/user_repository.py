from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")

    async def create_user(
        self,
        email: str,
        display_name: str,
        role: str = "user",
        organization_id: Optional[str] = None,
        firebase_uid: Optional[str] = None
    ) -> str:
        data = {
            "email": email,
            "display_name": display_name,
            "role": role,
            "organization_id": organization_id,
            "firebase_uid": firebase_uid,
            "is_active": True,
            "email_verified": False,
        }
        return await self.create(data)

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        results = await self.query([{"field": "email", "op": "==", "value": email}], limit=1)
        return results[0] if results else None

    async def get_by_firebase_uid(self, firebase_uid: str) -> Optional[Dict[str, Any]]:
        results = await self.query([{"field": "firebase_uid", "op": "==", "value": firebase_uid}], limit=1)
        return results[0] if results else None

    async def get_by_organization(self, organization_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "organization_id", "op": "==", "value": organization_id}], limit=limit)

    async def get_by_role(self, role: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "role", "op": "==", "value": role}], limit=limit)

    async def update_role(self, user_id: str, role: str) -> bool:
        return await self.update(user_id, {"role": role})

    async def deactivate_user(self, user_id: str) -> bool:
        return await self.update(user_id, {"is_active": False})

    async def activate_user(self, user_id: str) -> bool:
        return await self.update(user_id, {"is_active": True})

    async def verify_email(self, user_id: str) -> bool:
        return await self.update(user_id, {"email_verified": True})
