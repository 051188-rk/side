from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import SuccessResponse
from app.repositories.user_repository import UserRepository
from app.core.security import get_current_user, require_admin
from app.core.logging import log

router = APIRouter()
user_repo = UserRepository()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    user = await user_repo.get_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    updates: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    await user_repo.update(current_user["user_id"], updates.dict(exclude_unset=True))
    user = await user_repo.get_by_id(current_user["user_id"])
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_admin())
):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    updates: UserUpdate,
    current_user: dict = Depends(require_admin())
):
    await user_repo.update(user_id, updates.dict(exclude_unset=True))
    user = await user_repo.get_by_id(user_id)
    return user


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_admin())
):
    await user_repo.delete(user_id)
    return SuccessResponse(success=True, message="User deleted successfully")


@router.get("/", response_model=List[UserResponse])
async def list_users(
    limit: int = 100,
    current_user: dict = Depends(require_admin())
):
    users = await user_repo.list_all(limit=limit)
    return users
