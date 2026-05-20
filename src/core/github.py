import json
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from src.config import TEMPLATES_REPO
from src.core.errors import GenesisError

log = logging.getLogger(__name__)


@dataclass
class UserInfo:
    name: str
    login: str
    email: str


def get_user_info() -> UserInfo:
    cmd = ["gh", "api", "user", "--jq", "{name: .name, login: .login, id: .id}"]
    log.debug("Fetching authenticated user info from GitHub")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to fetch user info: {e.stderr.strip()}") from e
    data = json.loads(result.stdout)
    return UserInfo(
        name=data["name"],
        login=data["login"],
        email=f"{data['id']}+{data['login']}@users.noreply.github.com",
    )


def get_template_owner_info() -> UserInfo:
    owner = TEMPLATES_REPO.split("/")[0]
    cmd = ["gh", "api", f"users/{owner}", "--jq", "{name: .name, login: .login, id: .id}"]
    log.debug(f"Fetching template owner info for {owner}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to fetch template owner info: {e.stderr.strip()}") from e
    data = json.loads(result.stdout)
    return UserInfo(
        name=data["name"],
        login=data["login"],
        email=f"{data['id']}+{data['login']}@users.noreply.github.com",
    )


def list_templates() -> list[str]:
    cmd = [
        "gh",
        "api",
        f"/repos/{TEMPLATES_REPO}/contents",
        "--jq",
        '[.[] | select(.type=="dir") | .name]',
    ]

    log.debug(f"Listing Genesis templates from Github by running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise GenesisError(f"Failed to fetch templates: {e.stderr.strip()}") from e
    return cast(list[str], json.loads(result.stdout))


def create_and_push(
    name: str, dest: Path, public: bool, template: str, user: UserInfo, template_owner: UserInfo
) -> None:
    _git_init_and_commit(dest, template, template_owner)

    visibility = "public" if public else "private"
    cmd = [
        "gh",
        "repo",
        "create",
        f"{user.login}/{name}",
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


def _git_init_and_commit(dest: Path, template: str, user: UserInfo) -> None:
    log.debug(f"Initializing git repo in {dest}")
    template_url = f"https://github.com/{TEMPLATES_REPO}/tree/main/{template}"

    message = (
        f"Initial commit.\n\n"
        f"Template from {template_url}\n\n"
        f"Co-Authored-By: {user.name} <{user.email}>"
    )

    cmd1 = ["git", "-C", str(dest), "init"], "Failed to initialize git repo"
    cmd2 = ["git", "-C", str(dest), "add", "-A"], "Failed to add files to git repo"
    cmd3 = ["git", "-C", str(dest), "commit", "-m", message], "Failed to commit to git repo"

    for cmd, err in [cmd1, cmd2, cmd3]:
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise GenesisError(f"{err}: {e.stderr.strip()}") from e
