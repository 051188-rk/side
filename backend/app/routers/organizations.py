from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.organization import OrganizationResponse, OrganizationCreate, OrganizationUpdate
from app.schemas.common import SuccessResponse
from app.repositories.organization_repository import OrganizationRepository
from app.core.security import get_current_user, require_admin
from app.core.logging import log

router = APIRouter()
org_repo = OrganizationRepository()


@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: dict = Depends(get_current_user)
):
    org_id = await org_repo.create_organization(
        name=org_data.name,
        slug=org_data.slug,
        plan=org_data.plan,
        settings=org_data.settings
    )
    org = await org_repo.get_by_id(org_id)
    return org


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: str,
    current_user: dict = Depends(get_current_user)
):
    org = await org_repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    updates: OrganizationUpdate,
    current_user: dict = Depends(get_current_user)
):
    await org_repo.update(org_id, updates.dict(exclude_unset=True))
    org = await org_repo.get_by_id(org_id)
    return org


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    limit: int = 100,
    current_user: dict = Depends(require_admin())
):
    orgs = await org_repo.list_all(limit=limit)
    return orgs
