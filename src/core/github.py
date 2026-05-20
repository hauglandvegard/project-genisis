import json
import logging
import subprocess
from pathlib import Path
from typing import cast

from src.config import AUTHOR_NAME, GITHUB_EMAIL, GITHUB_USERNAME, TEMPLATES_REPO
from src.core.errors import GenesisError

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

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to fetch templates: {e.stderr.strip()}") from e
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

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to create GitHub repo: {e.stderr.strip()}") from e


def _git_init_and_commit(dest: Path, template: str) -> None:
    log.debug(f"Initializing git repo in {dest}")
    template_url = f"https://github.com/{TEMPLATES_REPO}/tree/main/{template}"

    cmd1 = ["git", "-C", str(dest), "init"], "Failed to initilize git repo"
    cmd2 = ["git", "-C", str(dest), "add", "-A"], "Failed to add files to git repo"

    message = (
        f"Initial commit.\n\n"
        f"Template from {template_url}\n\n"
        f"Co-Authored-By: {AUTHOR_NAME} <{GITHUB_EMAIL}>"
    )
    cmd3 = ["git", "-C", str(dest), "commit", "-m", message], "Failed to commit to git repo"

    for cmd, err in [cmd1, cmd2, cmd3]:
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise GenesisError(f"{err}: {e.stderr.strip()}") from e
