from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserLogin, UserSignup, UserResponse
from app.schemas.common import SuccessResponse
from app.integrations.firebase_integration import firebase_integration
from app.core.security import create_access_token, create_refresh_token, verify_firebase_token
from app.repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganizationRepository
from app.core.logging import log

router = APIRouter()
user_repo = UserRepository()
org_repo = OrganizationRepository()


@router.post("/login", response_model=SuccessResponse)
async def login(credentials: UserLogin):
    if credentials.firebase_token:
        decoded = await verify_firebase_token(credentials.firebase_token)
        user = await user_repo.get_by_firebase_uid(decoded.get("uid"))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        access_token = create_access_token(data={"sub": user["id"], "role": user["role"]})
        refresh_token = create_refresh_token(data={"sub": user["id"]})
        
        return SuccessResponse(
            success=True,
            message="Login successful",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user,
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email/password login not implemented, use Firebase token"
        )


@router.post("/signup", response_model=SuccessResponse)
async def signup(credentials: UserSignup):
    try:
        firebase_user = await firebase_integration.create_user(
            email=credentials.email,
            password=credentials.password,
            display_name=credentials.display_name
        )
        
        org_id = None
        if credentials.organization_name:
            org_id = await org_repo.create_organization(
                name=credentials.organization_name,
                slug=credentials.organization_name.lower().replace(" ", "-")
            )
        
        user_id = await user_repo.create_user(
            email=credentials.email,
            display_name=credentials.display_name,
            firebase_uid=firebase_user["uid"],
            organization_id=org_id
        )
        
        user = await user_repo.get_by_id(user_id)
        
        access_token = create_access_token(data={"sub": user_id, "role": user["role"]})
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        return SuccessResponse(
            success=True,
            message="Signup successful",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user,
            }
        )
    except Exception as e:
        log.error(f"Signup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {str(e)}"
        )


@router.post("/refresh", response_model=SuccessResponse)
async def refresh_token(token: str):
    from app.core.security import decode_token
    
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": user_id, "role": user["role"]})
    
    return SuccessResponse(
        success=True,
        message="Token refreshed",
        data={"access_token": access_token}
    )
