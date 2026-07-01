from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config import settings
from app.core.logging import log
from app.core.exceptions import (
    base_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from app.middleware import (
    setup_cors_middleware,
    setup_rate_limit_middleware,
    RequestIDMiddleware,
    error_handler_middleware,
)
from app.routers import (
    auth,
    users,
    organizations,
    feedback,
    tickets,
    webhooks,
    agents,
    integrations,
    dashboard,
    health,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    log.info(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="SIDE (Signal Desk) - AI-powered Omnichannel Customer Feedback Intelligence Platform",
    lifespan=lifespan,
)

app = setup_cors_middleware(app)
app = setup_rate_limit_middleware(app)
app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(Exception, error_handler_middleware)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(auth.router, prefix=f"{settings.api_v1_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.api_v1_prefix}/users", tags=["Users"])
app.include_router(organizations.router, prefix=f"{settings.api_v1_prefix}/organizations", tags=["Organizations"])
app.include_router(feedback.router, prefix=f"{settings.api_v1_prefix}/feedback", tags=["Feedback"])
app.include_router(tickets.router, prefix=f"{settings.api_v1_prefix}/tickets", tags=["Tickets"])
app.include_router(webhooks.router, prefix=f"{settings.api_v1_prefix}/webhooks", tags=["Webhooks"])
app.include_router(agents.router, prefix=f"{settings.api_v1_prefix}/agents", tags=["Agents"])
app.include_router(integrations.router, prefix=f"{settings.api_v1_prefix}/integrations", tags=["Integrations"])
app.include_router(dashboard.router, prefix=f"{settings.api_v1_prefix}/dashboard", tags=["Dashboard"])


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
