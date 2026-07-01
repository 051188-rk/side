from fastapi import APIRouter
from app.schemas.common import HealthResponse
from app.config import settings
from app.utils.date_utils import utc_now

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=utc_now(),
    )


@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    return {"status": "alive"}
