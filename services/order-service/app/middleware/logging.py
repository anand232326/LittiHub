
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
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
            "request_started | "
            "method=%s | "
            "path=%s | "
            "request_id=%s",
            request.method,
            request.url.path,
            request_id,
        )

        try:
            response = await call_next(request)

        except Exception:
            duration = (
                time.perf_counter() - start_time
            )

            logger.exception(
                "request_failed | "
                "method=%s | "
                "path=%s | "
                "request_id=%s | "
                "duration=%.4fs",
                request.method,
                request.url.path,
                request_id,
                duration,
            )

            raise

        duration = (
            time.perf_counter() - start_time
        )

        logger.info(
            "request_completed | "
            "method=%s | "
            "path=%s | "
            "status_code=%s | "
            "request_id=%s | "
            "duration=%.4fs",
            request.method,
            request.url.path,
            response.status_code,
            request_id,
            duration,
        )

        return response

