from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    return app
