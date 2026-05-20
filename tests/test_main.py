import logging
import logging.config
from pathlib import Path

from src.logging_config import cleanup_old_logs, make_logging_config


def test_cleanup_old_logs_removes_excess(tmp_path: Path) -> None:
    for i in range(7):
        (tmp_path / f"run_{i:02d}.log").touch()
    cleanup_old_logs(tmp_path, keep=5)
    assert len(list(tmp_path.iterdir())) == 4  # keep-1 before new run


def test_cleanup_old_logs_noop_when_under_limit(tmp_path: Path) -> None:
    for i in range(3):
        (tmp_path / f"run_{i:02d}.log").touch()
    cleanup_old_logs(tmp_path, keep=5)
    assert len(list(tmp_path.iterdir())) == 3


def test_make_logging_config_returns_valid_config(tmp_path: Path) -> None:
    config = make_logging_config(tmp_path)
    assert config["version"] == 1
    assert "console" in config["handlers"]
    assert "file" in config["handlers"]
    logging.config.dictConfig(config)  # must not raise
