import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from cookiecutter.main import cookiecutter

from src.config import COOKIECUTTER_TEMPLATES, TEMPLATES_REPO
from src.core.errors import GenesisError

log = logging.getLogger(__name__)


def scaffold(template: str, project_name: str, dest: Path, author: str) -> Path:
    if template in COOKIECUTTER_TEMPLATES:
        return _cookiecutter(template, project_name, dest, author)
    return _degit(template, project_name, dest)


def _cookiecutter(template: str, project_name: str, dest: Path, author: str) -> Path:
    log.debug(f"Scaffolding {project_name} with cookiecutter from {TEMPLATES_REPO}/{template}")

    cache_dir = Path.home() / ".cookiecutters" / TEMPLATES_REPO.split("/")[-1]
    shutil.rmtree(cache_dir, ignore_errors=True)

    try:
        cookiecutter(
            f"gh:{TEMPLATES_REPO}",
            directory=template,
            no_input=True,
            extra_context={
                "project_name": project_name,
                "author_name": author,
                "year": str(datetime.now().year),
            },
            output_dir=str(dest),
        )
    except Exception as e:
        raise GenesisError(f"Failed to scaffold with cookiecutter: {e}") from e

    return dest / project_name


def _degit(template: str, project_name: str, dest: Path) -> Path:
    target = dest / project_name

    cmd = ["npx", "degit", f"{TEMPLATES_REPO}/{template}", str(target)]

    log.debug(f"Scaffolding {project_name} with degit by running command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to scaffold with degit: {e.stderr.strip()}") from e

    return target
