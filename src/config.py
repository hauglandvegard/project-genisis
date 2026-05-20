from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.resolve()
ENV_FILE = ROOT_DIR / ".env"
LOGS_DIR = ROOT_DIR / "logs"

GITHUB_USERNAME = "hauglandvegard"
TEMPLATES_REPO = f"{GITHUB_USERNAME}/genesis-templates"
DEFAULT_DEST = Path.home() / "Code"
AUTHOR_NAME = "Vegard Haugland"
GITHUB_EMAIL = "66406501+hauglandvegard@users.noreply.github.com"

COOKIECUTTER_TEMPLATES = {"python", "python-flask", "python-django"}

load_dotenv(ENV_FILE)
