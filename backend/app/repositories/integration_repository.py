from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.core.logging import log


class IntegrationRepository(BaseRepository):
    def __init__(self):
        super().__init__("integrations")

    async def create_integration(
        self,
        integration_type: str,
        organization_id: str,
        config: Dict[str, Any],
        is_active: bool = True
    ) -> str:
        data = {
            "integration_type": integration_type,
            "organization_id": organization_id,
            "config": config,
            "is_active": is_active,
            "status": "connected",
        }
        return await self.create(data)

    async def get_by_type(self, integration_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "integration_type", "op": "==", "value": integration_type}], limit=limit)

    async def get_by_organization(self, organization_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "organization_id", "op": "==", "value": organization_id}], limit=limit)

    async def get_active(self, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.query([{"field": "is_active", "op": "==", "value": True}], limit=limit)

    async def update_config(self, integration_id: str, config: Dict[str, Any]) -> bool:
        return await self.update(integration_id, {"config": config})

    async def activate(self, integration_id: str) -> bool:
        return await self.update(integration_id, {"is_active": True, "status": "connected"})

    async def deactivate(self, integration_id: str) -> bool:
        return await self.update(integration_id, {"is_active": False, "status": "disconnected"})

    async def update_status(self, integration_id: str, status: str) -> bool:
        return await self.update(integration_id, {"status": status})
