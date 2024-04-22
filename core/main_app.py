import os
import platform
from datetime import datetime as dt
from typing import Annotated, Optional

import typer

from core.cli import history, passwords, settings
from core.helpers import config
from core.helpers.history import History
from core.helpers.logger import Logger
from core.helpers.main_loop import main_loop


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
    log_file_path = os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log")
    Logger.configure(log_file_path)
    history_file_path = os.path.join(paths['data'], "history.json")
    History.configure(history_file_path)
    app()


if __name__ == "__main__":
    print("You should run the entry point of the app instead.")
