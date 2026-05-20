from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.scaffold import scaffold


@patch("src.core.scaffold._cookiecutter")
def test_scaffold_dispatches_python_to_cookiecutter(mock_cc: MagicMock) -> None:
    scaffold("python", "proj", Path("/tmp"), "Author")
    mock_cc.assert_called_once_with("python", "proj", Path("/tmp"), "Author")


@patch("src.core.scaffold._cookiecutter")
def test_scaffold_dispatches_python_variant_to_cookiecutter(mock_cc: MagicMock) -> None:
    scaffold("python-flask", "proj", Path("/tmp"), "Author")
    mock_cc.assert_called_once_with("python-flask", "proj", Path("/tmp"), "Author")


@patch("src.core.scaffold._degit")
def test_scaffold_dispatches_go_to_degit(mock_degit: MagicMock) -> None:
    scaffold("go", "proj", Path("/tmp"), "Author")
    mock_degit.assert_called_once_with("go", "proj", Path("/tmp"))


@patch("src.core.scaffold._degit")
def test_scaffold_dispatches_react_to_degit(mock_degit: MagicMock) -> None:
    scaffold("react", "proj", Path("/tmp"), "Author")
    mock_degit.assert_called_once_with("react", "proj", Path("/tmp"))


@patch("src.core.scaffold.cookiecutter")
def test_cookiecutter_passes_extra_context(mock_cc: MagicMock) -> None:
    from src.core.scaffold import _cookiecutter

    mock_cc.return_value = None
    _cookiecutter("python", "my-project", Path("/tmp"), "Vegard")

    _, kwargs = mock_cc.call_args
    assert kwargs["extra_context"]["project_name"] == "my-project"
    assert kwargs["extra_context"]["author_name"] == "Vegard"
    assert kwargs["no_input"] is True
    assert kwargs["directory"] == "python"


@patch("src.core.scaffold.subprocess.run")
def test_degit_calls_npx_degit(mock_run: MagicMock) -> None:
    from src.core.scaffold import _degit

    _degit("go", "my-project", Path("/tmp"))
    cmd = mock_run.call_args[0][0]
    assert cmd[:2] == ["npx", "degit"]
    assert "go" in cmd[2]
    assert str(Path("/tmp") / "my-project") == cmd[3]
