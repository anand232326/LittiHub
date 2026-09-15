
import time

from fastapi import Request

from app.core.logger import logger


async def logging_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    )

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.info(
        "%s %s | status=%s | "
        "request_id=%s | duration=%.4fs",
        request.method,
        request.url.path,
        response.status_code,
        request_id,
        process_time,
    )

    return response

