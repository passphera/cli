from typing import Annotated

import typer

from app.core import functions
from app.core.app_loops import history_loop


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def history_callback(ctx: typer.Context) -> None:
    """
    Access history, get password or passwords, save/load history data to a backup, hash passwords on history.
    """
    if ctx.invoked_subcommand is None:
        while True:
            history_loop()


@app.command()
def get(context: Annotated[str, typer.Argument(help="The context to get it's password")]) -> None:
    """Get saved password"""
    functions.get_password(context)


@app.command()
def get_all() -> None:
    """Get all saved passwords"""
    functions.get_all_passwords()


@app.command()
def clear() -> None:
    """Clear history from all saved passwords"""
    functions.clear_database()


@app.command()
def sync() -> None:
    """Sync with shared database"""
    functions.sync()


if __name__ == "__main__":
    app()
