from typing import Annotated

import typer

from core.backend import history
from core.helpers import interface
from core.helpers.app_loops import history_loop


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def history_callback(ctx: typer.Context) -> None:
    """
    Access history, get password or passwords, save/load history data to a backup, hash passwords on history.
    """
    if ctx.invoked_subcommand is None:
        history_loop()


@app.command()
def get(context: Annotated[str, typer.Argument(help="The context you want to get")]) -> None:
    """Get a saved password from history"""
    password: dict[str, str] = history.get_password(context)
    if password is not None:
        interface.display_password(password)
    else:
        interface.display_context_error_message(context)
    interface.copy_to_clipboard(password['password'])


@app.command()
def show_all() -> None:
    """Show all saved passwords"""
    interface.display_passwords(history.__history__)


@app.command()
def clear() -> None:
    """Clear history from all saved passwords"""
    history.clear_history()
    interface.display_clear_history_message()


@app.command()
def save_backup() -> None:
    """Save backup history"""


@app.command()
def load_backup() -> None:
    """Load history from a saved backup"""


@app.command()
def encrypt() -> None:
    """Encrypt passwords on history"""


@app.command()
def decrypt() -> None:
    """Decrypt passwords on history"""


if __name__ == "__main__":
    app()
