import logging
import time

from fastapi import Request


logger = logging.getLogger("littihub.request")


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.info(
        "request_started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": round(duration, 4),
        },
    )

    return response