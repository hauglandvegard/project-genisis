import logging
import logging.config

from src.config import LOGS_DIR
from src.logging_config import cleanup_old_logs, make_logging_config


def main() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    cleanup_old_logs(LOGS_DIR, keep=5)
    logging.config.dictConfig(make_logging_config(LOGS_DIR))
    logger = logging.getLogger(__name__)

    logger.info("Application started.")

    # Code

    logger.info("Application finished.")


if __name__ == "__main__":
    main()
