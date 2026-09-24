
import logging
import sys

from app.core.config import config


def setup_logger() -> logging.Logger:

    logger = logging.getLogger(
        "littihub.order"
    )

    if logger.handlers:
        return logger

    log_level = getattr(
        logging,
        config.LOG_LEVEL.upper(),
        logging.INFO,
    )

    logger.setLevel(
        log_level
    )

    handler = logging.StreamHandler(
        sys.stdout
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    handler.setFormatter(
        formatter
    )

    logger.addHandler(
        handler
    )

    logger.propagate = False

    return logger


logger = setup_logger()

