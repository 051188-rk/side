from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    BaseException,
    base_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from app.core.logging import log


async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except BaseException as e:
        log.error(
            f"BaseException: {e.message}",
            extra={
                "status_code": e.status_code,
                "details": e.details,
                "path": request.url.path,
            }
        )
        return await base_exception_handler(request, e)
    except Exception as e:
        log.error(
            f"Unhandled exception: {str(e)}",
            extra={"path": request.url.path},
            exc_info=True
        )
        return await general_exception_handler(request, e)
