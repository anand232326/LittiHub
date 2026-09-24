
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.logger import logger


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:

    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    logger.warning(
        "application_error | "
        "method=%s | "
        "path=%s | "
        "status_code=%s | "
        "request_id=%s | "
        "message=%s",
        request.method,
        request.url.path,
        exc.status_code,
        request_id,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "details": exc.details,
            "request_id": request_id,
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    logger.exception(
        "unhandled_exception | "
        "method=%s | "
        "path=%s | "
        "request_id=%s",
        request.method,
        request.url.path,
        request_id,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "details": None,
            "request_id": request_id,
        },
    )

