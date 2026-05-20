import logging
import logging.config

from src.config import DEFAULT_DEST, LOGS_DIR
from src.core import cli, github, scaffold
from src.core.errors import GenesisError
from src.logging_config import cleanup_old_logs, make_logging_config


def main() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    cleanup_old_logs(LOGS_DIR, keep=5)
    logging.config.dictConfig(make_logging_config(LOGS_DIR))
    log = logging.getLogger(__name__)

    try:
        user = github.get_user_info()
        template_owner = github.get_template_owner_info()
        templates = github.list_templates()
        config = cli.prompt(templates, DEFAULT_DEST)
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    try:
        log.info("Scaffolding %s from template %s", config.project_name, config.template)
        project_dir = scaffold.scaffold(
            config.template, config.project_name, config.dest, user.name
        )

        log.info("Creating GitHub repo")
        github.create_and_push(
            config.project_name, project_dir, config.public, config.template, user, template_owner
        )
    except GenesisError as e:
        print(f"\nError: {e}")
        return

    print(f"\nDone! {config.project_name} → {project_dir}")


if __name__ == "__main__":
    main()
