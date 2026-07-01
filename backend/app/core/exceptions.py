from typing import Optional, Any
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class BaseException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "An error occurred",
        details: Optional[dict] = None
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundException(BaseException):
    def __init__(self, message: str = "Resource not found", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            details=details
        )


class BadRequestException(BaseException):
    def __init__(self, message: str = "Bad request", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details
        )


class UnauthorizedException(BaseException):
    def __init__(self, message: str = "Unauthorized", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            details=details
        )


class ForbiddenException(BaseException):
    def __init__(self, message: str = "Forbidden", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            details=details
        )


class ConflictException(BaseException):
    def __init__(self, message: str = "Conflict", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            details=details
        )


class RateLimitException(BaseException):
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            details=details
        )


class ExternalServiceException(BaseException):
    def __init__(self, service: str, message: str = "External service error", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=f"{service}: {message}",
            details=details
        )


class LLMException(BaseException):
    def __init__(self, provider: str, message: str = "LLM provider error", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"{provider} LLM error: {message}",
            details=details
        )


class ValidationException(BaseException):
    def __init__(self, message: str = "Validation error", details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            details=details
        )


async def base_exception_handler(request: Any, exc: BaseException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "status_code": exc.status_code,
            }
        },
    )


async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "status_code": exc.status_code,
            }
        },
    )


async def general_exception_handler(request: Any, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        },
    )
