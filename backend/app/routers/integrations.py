from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.integration import IntegrationResponse, IntegrationCreate, IntegrationUpdate
from app.schemas.common import SuccessResponse
from app.repositories.integration_repository import IntegrationRepository
from app.core.security import get_current_user, require_admin
from app.core.logging import log

router = APIRouter()
integration_repo = IntegrationRepository()


@router.post("/", response_model=IntegrationResponse)
async def create_integration(
    integration_data: IntegrationCreate,
    current_user: dict = Depends(get_current_user)
):
    integration_id = await integration_repo.create_integration(
        integration_type=integration_data.integration_type,
        organization_id=integration_data.organization_id,
        config=integration_data.config,
        is_active=integration_data.is_active
    )
    integration = await integration_repo.get_by_id(integration_id)
    return integration


@router.get("/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    integration_id: str,
    current_user: dict = Depends(get_current_user)
):
    integration = await integration_repo.get_by_id(integration_id)
    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
    return integration


@router.put("/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: str,
    updates: IntegrationUpdate,
    current_user: dict = Depends(get_current_user)
):
    await integration_repo.update(integration_id, updates.dict(exclude_unset=True))
    integration = await integration_repo.get_by_id(integration_id)
    return integration


@router.post("/{integration_id}/activate", response_model=SuccessResponse)
async def activate_integration(
    integration_id: str,
    current_user: dict = Depends(get_current_user)
):
    await integration_repo.activate(integration_id)
    return SuccessResponse(success=True, message="Integration activated")


@router.post("/{integration_id}/deactivate", response_model=SuccessResponse)
async def deactivate_integration(
    integration_id: str,
    current_user: dict = Depends(get_current_user)
):
    await integration_repo.deactivate(integration_id)
    return SuccessResponse(success=True, message="Integration deactivated")


@router.get("/", response_model=list)
async def list_integrations(
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    integrations = await integration_repo.list_all(limit=limit)
    return integrations
