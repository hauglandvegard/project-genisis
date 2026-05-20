from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.cli import ProjectConfig, _group_templates, prompt


def test_group_templates_single_per_language() -> None:
    result = _group_templates(["python", "go"])
    assert result == {"python": ["python"], "go": ["go"]}


def test_group_templates_multiple_variants() -> None:
    result = _group_templates(["python", "python-flask", "python-django", "go"])
    assert result == {
        "python": ["python", "python-flask", "python-django"],
        "go": ["go"],
    }


def test_group_templates_preserves_order() -> None:
    templates = ["go", "python", "react"]
    result = _group_templates(templates)
    assert list(result.keys()) == ["go", "python", "react"]


@patch("src.core.cli.questionary")
def test_prompt_single_variant_skips_variant_select(mock_q: MagicMock) -> None:
    mock_q.select.return_value.ask.side_effect = ["python", "public"]
    mock_q.text.return_value.ask.side_effect = ["my-project", "/Users/vegard/Code"]

    config = prompt(["python"], Path("/Users/vegard/Code"))

    assert config == ProjectConfig(
        template="python",
        project_name="my-project",
        dest=Path("/Users/vegard/Code"),
        public=True,
    )


@patch("src.core.cli.questionary")
def test_prompt_multiple_variants_shows_variant_select(mock_q: MagicMock) -> None:
    mock_q.select.return_value.ask.side_effect = ["python", "flask", "public"]
    mock_q.text.return_value.ask.side_effect = ["my-project", "/Users/vegard/Code"]

    config = prompt(["python", "python-flask"], Path("/Users/vegard/Code"))

    assert config.template == "python-flask"


@patch("src.core.cli.questionary")
def test_prompt_aborts_on_keyboard_interrupt(mock_q: MagicMock) -> None:
    mock_q.select.return_value.ask.return_value = None

    try:
        prompt(["python"], Path("/Users/vegard/Code"))
        raise AssertionError("Expected KeyboardInterrupt")
    except KeyboardInterrupt:
        pass


@patch("src.core.cli.questionary")
def test_prompt_private_visibility(mock_q: MagicMock) -> None:
    mock_q.select.return_value.ask.side_effect = ["python", "private"]
    mock_q.text.return_value.ask.side_effect = ["my-project", "/Users/vegard/Code"]

    config = prompt(["python"], Path("/Users/vegard/Code"))

    assert config.public is False
