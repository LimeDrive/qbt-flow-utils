"""Logging utilities for qbt_flow_utils."""
import logging
import sys
from typing import Union

from loguru import logger

from qbt_flow_utils.settings import settings


class InterceptHandler(logging.Handler):
    """Intercept loguru messages and pass
    them to the standard logging module.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def configure_logging() -> None:  # pragma: no cover
    """Configures logging."""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    # set logs output, level and format
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level.value,
    )
