import logging
import sys


class SafeFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:

        if not hasattr(record, "request_id"):
            record.request_id = "-"

        if not hasattr(record, "method"):
            record.method = "-"

        if not hasattr(record, "path"):
            record.path = "-"

        if not hasattr(record, "status_code"):
            record.status_code = "-"

        if not hasattr(record, "duration"):
            record.duration = "-"

        return super().format(record)


# 1. Create module-level logger instance
logger = logging.getLogger("littihub")


def setup_logging():

    formatter = SafeFormatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s | "
        "request_id=%(request_id)s | "
        "method=%(method)s | "
        "path=%(path)s | "
        "status_code=%(status_code)s | "
        "duration=%(duration)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False


# 2. Automatically configure logging on module import
setup_logging()