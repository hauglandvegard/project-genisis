import json
import logging
import subprocess
from pathlib import Path
from typing import cast

from src.config import AUTHOR_NAME, GITHUB_EMAIL, GITHUB_USERNAME, TEMPLATES_REPO

log = logging.getLogger(__name__)


def list_templates() -> list[str]:
    cmd = [
        "gh",
        "api",
        f"/repos/{TEMPLATES_REPO}/contents",
        "--jq",
        '[.[] | select(.type=="dir") | .name]',
    ]

    log.debug(f"Listing Genisis templates from Github by running command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return cast(list[str], json.loads(result.stdout))


def create_and_push(name: str, dest: Path, public: bool, template: str) -> None:
    _git_init_and_commit(dest, template)

    visibility = "public" if public else "private"
    cmd = [
        "gh",
        "repo",
        "create",
        f"{GITHUB_USERNAME}/{name}",
        f"--{visibility}",
        "--source",
        str(dest),
        "--remote",
        "origin",
        "--push",
    ]

    log.debug(f"Creating Github repo by running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def _git_init_and_commit(dest: Path, template: str) -> None:
    log.debug(f"Initializing git repo in {dest}")
    template_url = f"https://github.com/{TEMPLATES_REPO}/tree/main/{template}"
    subprocess.run(["git", "-C", str(dest), "init"], check=True)
    subprocess.run(["git", "-C", str(dest), "add", "-A"], check=True)
    message = (
        f"Initial commit.\n\n"
        f"Template from {template_url}\n\n"
        f"Co-Authored-By: {AUTHOR_NAME} <{GITHUB_EMAIL}>"
    )
    subprocess.run(
        ["git", "-C", str(dest), "commit", "-m", message],
        check=True,
    )
