import os
import platform
from datetime import datetime as dt
from typing import Annotated, Optional

import typer

from core.backend import history as b_history, logger as b_logger, settings as b_settings
from core.cli import history, passwords, settings
from core.helpers import config
from core.helpers.app_loops import main_loop


app = typer.Typer(rich_markup_mode="rich")
app.add_typer(passwords.app)
app.add_typer(settings.app)
app.add_typer(history.app)


@app.callback(invoke_without_command=True)
def app_callback(
        ctx: typer.Context,
        version: Annotated[
            Optional[bool], typer.Option(
                "--version",
                "-v",
                callback=config.version_callback,
                help="Show version and exit",
                is_eager=True)] = None,
) -> None:
    """
    passphera-cli - Strong passwords generator cli tool to keep track of all your passwords.
    """
    if ctx.invoked_subcommand is None:
        main_loop()


def main():
    platform_name = platform.system()
    paths = config.setup_paths(platform_name)
    if platform_name == 'Linux':
        config.setup_xdg_variables()
    config.create_dirs(paths)

    history_file_path = os.path.join(paths['data'], "history.json")
    log_file_path = os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log")
    settings_file_path = os.path.join(paths['config'], "config.ini")

    b_history.configure(history_file_path)
    b_logger.configure(log_file_path)
    b_settings.configure(settings_file_path)

    for key, value in b_settings.get_settings(b_settings.__characters_replacements__).items():
        config.generator.replace_character(key, value)

    app()


if __name__ == "__main__":
    print("You should run the entry point of the app instead.")
