from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.resolve()
ENV_FILE = ROOT_DIR / ".env"
LOGS_DIR = ROOT_DIR / "logs"

TEMPLATES_REPO = "hauglandvegard/genesis-templates"
DEFAULT_DEST = Path.home() / "Code"

COOKIECUTTER_TEMPLATES = {"python", "python-fastapi", "python-flask", "python-django"}

load_dotenv(ENV_FILE)
