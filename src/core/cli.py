import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import questionary

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

log = logging.getLogger(__name__)


@dataclass
class ProjectConfig:
    template: str
    framework: str | None
    project_name: str
    dest: Path
    public: bool
    include_claude: bool


def prompt(
    templates: list[str],
    default_dest: Path,
    no_push: bool = False,
    get_framework_choices: Callable[[str], list[str]] | None = None,
) -> ProjectConfig:
    template = questionary.select("Language:", choices=templates).ask()
    if template is None:
        raise KeyboardInterrupt

    framework: str | None = None
    if get_framework_choices:
        choices = get_framework_choices(template)
        if len(choices) > 1:
            framework = questionary.select("Framework:", choices=choices).ask()
            if framework is None:
                raise KeyboardInterrupt

    project_name = questionary.text(
        "Project name:",
        validate=lambda v: (
            _SLUG_RE.match(v) is not None
            or "Use lowercase letters, numbers, hyphens only (no leading/trailing hyphens)"
        ),
    ).ask()
    if not project_name:
        raise KeyboardInterrupt

    dest_str = questionary.text("Destination:", default=str(default_dest)).ask()
    if dest_str is None:
        raise KeyboardInterrupt

    if no_push:
        public = False
    else:
        visibility = questionary.select("Visibility:", choices=["public", "private"]).ask()
        if visibility is None:
            raise KeyboardInterrupt
        public = visibility == "public"

    include_claude = questionary.confirm(
        "Include Claude resources (CLAUDE.md, agents, commands)?",
        default=True,
    ).ask()
    if include_claude is None:
        raise KeyboardInterrupt

    config = ProjectConfig(
        template=template,
        framework=framework,
        project_name=project_name,
        dest=Path(dest_str).expanduser(),
        public=public,
        include_claude=include_claude,
    )
    log.debug(f"User selected: {config}")
    return config
