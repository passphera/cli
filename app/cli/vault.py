from typing import Annotated

import typer

from app.backend import vault
from app.core import logger
from app.core.decorators import handle_exception_decorator
from app.core.functions import copy_to_clipboard, handle_error
from app.core.interface import Interface, Messages

app = typer.Typer(rich_markup_mode="rich")


@handle_exception_decorator("")
@app.callback()
def vault_callback() -> None:
    """Access vault: get password or passwords, clear vault, sync vault data with cloud."""


@handle_exception_decorator("failed to get password")
@app.command()
def get(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to get.")]) -> None:
    """Get saved password"""
    try:
        password: dict[str, str] = vault.get_password(context)
        if password is None:
            raise ValueError
        Interface.display_password(password)
        copy_to_clipboard(password['password'])
    except ValueError:
        Interface.display_message(Messages.context_error(context), title='Error')


@handle_exception_decorator("failed to get passwords")
@app.command()
def get_all() -> None:
    """Get all saved passwords"""
    Interface.display_passwords(vault.get_passwords())


@handle_exception_decorator("failed to clear database")
@app.command()
def clear() -> None:
    """Clear history from all saved passwords"""
    vault.clear_db()
    Interface.display_message(Messages.HISTORY_CLEARED, title="Vault")
    logger.log_info("database cleared")


@handle_exception_decorator("failed to sync vault")
@app.command()
def sync() -> None:
    """Sync down from a shared database"""
    local, server = vault.sync()
    Interface.display_message(Messages.sync_vault(local, server))
    logger.log_info("database synced")


if __name__ == "__main__":
    app()
