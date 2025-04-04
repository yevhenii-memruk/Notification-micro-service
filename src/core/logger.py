import logging
import sys

from src.core.settings import settings


def configure_logger() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logger = logging.getLogger("notification-service")
    logger.info("Logging configured.")
