from pathlib import Path
from unittest.mock import MagicMock, patch

from src.config import AUTHOR_NAME, GITHUB_EMAIL, TEMPLATES_REPO
from src.core.github import _git_init_and_commit, create_and_push, list_templates


@patch("src.core.github.subprocess.run")
def test_list_templates_returns_parsed_json(mock_run: MagicMock) -> None:
    mock_run.return_value.stdout = '["python", "go"]'
    result = list_templates()
    assert result == ["python", "go"]


@patch("src.core.github.subprocess.run")
def test_list_templates_calls_gh_api(mock_run: MagicMock) -> None:
    mock_run.return_value.stdout = "[]"
    list_templates()
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == "gh"
    assert f"/repos/{TEMPLATES_REPO}/contents" in cmd


@patch("src.core.github.subprocess.run")
def test_git_init_and_commit_runs_three_git_commands(mock_run: MagicMock) -> None:
    _git_init_and_commit(Path("/tmp/test"), "python")
    assert mock_run.call_count == 3
    commands = [c[0][0] for c in mock_run.call_args_list]
    assert all(cmd[0] == "git" for cmd in commands)


@patch("src.core.github.subprocess.run")
def test_git_init_and_commit_message_contains_template_url(mock_run: MagicMock) -> None:
    _git_init_and_commit(Path("/tmp/test"), "python")
    commit_call = mock_run.call_args_list[2]
    message = commit_call[0][0][-1]
    assert "https://github.com/hauglandvegard/genesis-templates/tree/main/python" in message


@patch("src.core.github.subprocess.run")
def test_git_init_and_commit_message_contains_co_author(mock_run: MagicMock) -> None:
    _git_init_and_commit(Path("/tmp/test"), "python")
    commit_call = mock_run.call_args_list[2]
    message = commit_call[0][0][-1]
    assert f"Co-Authored-By: {AUTHOR_NAME} <{GITHUB_EMAIL}>" in message


@patch("src.core.github._git_init_and_commit")
@patch("src.core.github.subprocess.run")
def test_create_and_push_public(mock_run: MagicMock, mock_init: MagicMock) -> None:
    create_and_push("my-project", Path("/tmp/my-project"), public=True, template="python")
    cmd = mock_run.call_args[0][0]
    assert "--public" in cmd


@patch("src.core.github._git_init_and_commit")
@patch("src.core.github.subprocess.run")
def test_create_and_push_private(mock_run: MagicMock, mock_init: MagicMock) -> None:
    create_and_push("my-project", Path("/tmp/my-project"), public=False, template="python")
    cmd = mock_run.call_args[0][0]
    assert "--private" in cmd


@patch("src.core.github._git_init_and_commit")
@patch("src.core.github.subprocess.run")
def test_create_and_push_calls_git_init_first(mock_run: MagicMock, mock_init: MagicMock) -> None:
    create_and_push("my-project", Path("/tmp/my-project"), public=True, template="python")
    mock_init.assert_called_once_with(Path("/tmp/my-project"), "python")
