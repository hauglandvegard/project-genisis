import argparse
import logging
import logging.config
import os
import subprocess

from src.config import DEFAULT_DEST, LOGS_DIR
from src.core import cli, github, scaffold
from src.core.errors import GenesisError
from src.logging_config import cleanup_old_logs, make_logging_config


def main() -> None:
    parser = argparse.ArgumentParser(prog="genesis", description="Initialize a new project.")
    parser.add_argument("--no-push", action="store_true", help="Scaffold locally, skip GitHub.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List available templates.")
    args = parser.parse_args()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    cleanup_old_logs(LOGS_DIR, keep=5)
    logging.config.dictConfig(make_logging_config(LOGS_DIR))
    log = logging.getLogger(__name__)

    try:
        if args.command == "list":
            templates = github.list_templates()
            for t in templates:
                print(t)
            return

        user = github.get_user_info()
        template_owner = github.get_template_owner_info()
        templates = github.list_templates()
        config = cli.prompt(templates, DEFAULT_DEST, no_push=args.no_push)
    except GenesisError as e:
        print(f"\nError: {e}")
        return
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    project_dir = config.dest / config.project_name
    if project_dir.exists():
        print(f"\nError: {project_dir} already exists.")
        return

    try:
        log.info("Scaffolding %s from template %s", config.project_name, config.template)
        project_dir = scaffold.scaffold(
            config.template, config.project_name, config.dest, user.name
        )

        if not args.no_push:
            log.info("Creating GitHub repo")
            github.create_and_push(
                config.project_name,
                project_dir,
                config.public,
                config.template,
                user,
                template_owner,
            )
    except GenesisError as e:
        print(f"\nError: {e}")
        return

    print(f"\nDone! {config.project_name} → {project_dir}")
    if not args.no_push:
        print(f"      https://github.com/{user.login}/{config.project_name}")

    editor = os.environ.get("EDITOR")
    if editor:
        cmd = [editor, str(project_dir)]
        log.debug("Opening %s in %s", project_dir, editor)
        subprocess.run(cmd)


if __name__ == "__main__":
    main()
