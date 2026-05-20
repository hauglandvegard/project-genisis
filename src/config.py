from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.resolve()

ENV_FILE = ROOT_DIR / ".env"
LOGS_DIR = ROOT_DIR / "logs"

load_dotenv(ENV_FILE)
