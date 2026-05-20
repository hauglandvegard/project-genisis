import logging
import logging.config
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.errors import GenesisError
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


def _main_with_mocked_logging() -> ExitStack:
    stack = ExitStack()
    stack.enter_context(patch("src.main.cleanup_old_logs"))
    stack.enter_context(patch("src.main.make_logging_config"))
    stack.enter_context(patch("logging.config.dictConfig"))
    stack.enter_context(patch("src.main.LOGS_DIR"))
    return stack


def test_main_handles_genesis_error_from_get_user_info(capsys: MagicMock) -> None:
    from src.main import main

    with _main_with_mocked_logging():
        with patch("src.core.github.get_user_info", side_effect=GenesisError("gh auth failed")):
            main()

    assert "gh auth failed" in capsys.readouterr().out


def test_main_handles_genesis_error_from_get_template_owner_info(capsys: MagicMock) -> None:
    from src.main import main

    with _main_with_mocked_logging():
        with patch("src.core.github.get_user_info"):
            with patch(
                "src.core.github.get_template_owner_info",
                side_effect=GenesisError("owner fetch failed"),
            ):
                main()

    assert "owner fetch failed" in capsys.readouterr().out


def test_main_handles_genesis_error_from_list_templates(capsys: MagicMock) -> None:
    from src.main import main

    with _main_with_mocked_logging():
        with patch("src.core.github.get_user_info"):
            with patch("src.core.github.get_template_owner_info"):
                with patch(
                    "src.core.github.list_templates",
                    side_effect=GenesisError("network error"),
                ):
                    main()

    assert "network error" in capsys.readouterr().out
