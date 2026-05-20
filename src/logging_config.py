import datetime
import os
from pathlib import Path
from typing import Any


def cleanup_old_logs(log_dir: Path, keep: int = 5) -> None:
    files = sorted(
        [log_dir / f for f in os.listdir(log_dir) if (log_dir / f).is_file()],
        key=os.path.getmtime,
    )
    to_delete = len(files) - (keep - 1)
    if to_delete > 0:
        for f in files[:to_delete]:
            f.unlink()


def make_logging_config(log_dir: Path) -> dict[str, Any]:
    timestamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    log_filename = log_dir / f"run_{timestamp}.log"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",  # noqa: E501
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": str(log_filename),
                "formatter": "detailed",
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
