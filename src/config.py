from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
LOGS_DIR = ROOT_DIR / "logs"
RESOURCES_DIR = ROOT_DIR / "resources"
CLAUDE_RESOURCES = RESOURCES_DIR / "claude"

TEMPLATES_REPO = "hauglandvegard/genesis-templates"
DEFAULT_DEST = Path.home() / "Code"

COOKIECUTTER_TEMPLATES = {"python"}
