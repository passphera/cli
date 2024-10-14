from typing import Annotated

import typer

from app.core import functions


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def vault_callback(ctx: typer.Context) -> None:
    """Access vault: get password or passwords, clear vault, sync vault data with cloud."""


@app.command()
def get(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to get.")]) -> None:
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
    functions.sync_vault()


if __name__ == "__main__":
    app()
