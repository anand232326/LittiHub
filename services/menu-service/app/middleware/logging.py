import time

from fastapi import Request

from app.core.logger import logger


async def logging_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    logger.info(
        "request_started method=%s path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "request_completed method=%s path=%s status=%s duration=%.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "request_failed method=%s path=%s duration=%.4fs",
            request.method,
            request.url.path,
            duration,
        )

        raise