import logging
import subprocess
from datetime import datetime
from pathlib import Path

from cookiecutter.main import cookiecutter

from src.config import TEMPLATES_REPO

log = logging.getLogger(__name__)


def scaffold(template: str, project_name: str, dest: Path, author: str) -> Path:
    if template.startswith("python"):
        return _cookiecutter(template, project_name, dest, author)
    return _degit(template, project_name, dest)


def _cookiecutter(template: str, project_name: str, dest: Path, author: str) -> Path:
    log.debug(f"Scaffolding {project_name} with cookiecutter from {TEMPLATES_REPO}/{template}")

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

    return dest / project_name


def _degit(template: str, project_name: str, dest: Path) -> Path:
    target = dest / project_name

    cmd = ["npx", "degit", f"{TEMPLATES_REPO}/{template}", str(target)]

    log.debug(f"Scaffolding {project_name} with degit by running command: {' '.join(cmd)}")

    subprocess.run(cmd, check=True)

    return target
