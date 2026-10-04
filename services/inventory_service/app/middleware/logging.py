import logging
import time
from fastapi import Request


logger = logging.getLogger("inventory_service")


async def logging_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    logger.info(
        "Request started | method=%s path=%s request_id=%s",
        request.method,
        request.url.path,
        request_id,
    )

    try:
        response = await call_next(request)

        process_time = (
            time.perf_counter() - start_time
        )

        logger.info(
            "Request completed | method=%s path=%s "
            "status_code=%s process_time=%.4fs "
            "request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
            request_id,
        )

        return response

    except Exception:
        process_time = (
            time.perf_counter() - start_time
        )

        logger.exception(
            "Request failed | method=%s path=%s "
            "process_time=%.4fs request_id=%s",
            request.method,
            request.url.path,
            process_time,
            request_id,
        )

        raise