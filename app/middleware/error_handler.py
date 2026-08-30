import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException


logger = logging.getLogger("littihub.error")


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.error(
        "application_exception",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": exc.status_code,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
            "request_id": request_id,
        },
    )