import logging
import re
from dataclasses import dataclass
from pathlib import Path

import questionary

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

log = logging.getLogger(__name__)


@dataclass
class ProjectConfig:
    template: str
    project_name: str
    dest: Path
    public: bool


def prompt(templates: list[str], default_dest: Path, no_push: bool = False) -> ProjectConfig:
    groups = _group_templates(templates)

    language = questionary.select("Language:", choices=list(groups.keys())).ask()
    if language is None:
        raise KeyboardInterrupt

    variants = groups[language]
    if len(variants) == 1:
        template = variants[0]
    else:
        labels = [t.split("-", 1)[1] if "-" in t else "base" for t in variants]
        label = questionary.select("Variant:", choices=labels).ask()
        if label is None:
            raise KeyboardInterrupt
        template = variants[labels.index(label)]

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

    config = ProjectConfig(
        template=template,
        project_name=project_name,
        dest=Path(dest_str).expanduser(),
        public=public,
    )
    log.debug(f"User selected: {config}")
    return config


def _group_templates(templates: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for t in templates:
        lang = t.split("-")[0]
        groups.setdefault(lang, []).append(t)
    return groups
