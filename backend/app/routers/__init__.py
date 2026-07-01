from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.organizations import router as organizations_router
from app.routers.feedback import router as feedback_router
from app.routers.tickets import router as tickets_router
from app.routers.webhooks import router as webhooks_router
from app.routers.agents import router as agents_router
from app.routers.integrations import router as integrations_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "health_router",
    "auth_router",
    "users_router",
    "organizations_router",
    "feedback_router",
    "tickets_router",
    "webhooks_router",
    "agents_router",
    "integrations_router",
    "dashboard_router",
]
