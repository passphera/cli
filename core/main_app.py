import os
import platform
from datetime import datetime as dt
from typing import Annotated, Optional

import typer

from core.backend import history as b_history, logger as b_logger, settings as b_settings
from core.cli import history as cli_history, passwords as cli_passwords, settings as cli_settings
from core.helpers import config
from core.helpers.app_loops import main_loop


app = typer.Typer(rich_markup_mode="rich")
app.add_typer(cli_passwords.app)
app.add_typer(cli_settings.app)
app.add_typer(cli_history.app)


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
    if platform_name == 'Linux':
        config.setup_xdg_variables()
    paths = config.setup_paths(platform_name)
    config.create_dirs(paths)

    b_history.configure(os.path.join(paths['data'], "history.json"))
    b_logger.configure(os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log"))
    b_settings.configure(os.path.join(paths['config'], "config.ini"))

    for key, value in b_settings.get_settings(b_settings.__characters_replacements__).items():
        config.generator.replace_character(key, value)

    app()


if __name__ == "__main__":
    print("You should run the entry point of the app instead.")
