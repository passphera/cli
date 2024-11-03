from typing import Annotated

import typer

from app.backend import vault
from app.core import logger
from app.core.functions import copy_to_clipboard, handle_error
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def vault_callback() -> None:
    """Access vault: get password or passwords, clear vault, sync vault data with cloud."""


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
    except Exception as e:
        handle_error(f"failed to get password: {e}")


@app.command()
def get_all() -> None:
    """Get all saved passwords"""
    try:
        Interface.display_passwords(vault.get_passwords())
    except Exception as e:
        handle_error(f"failed to get passwords: {e}")


@app.command()
def clear() -> None:
    """Clear history from all saved passwords"""
    try:
        vault.clear_db()
        Interface.display_message(Messages.HISTORY_CLEARED, title="Vault")
        logger.log_info("database cleared")
    except Exception as e:
        handle_error(f"failed to clear database: {e}")


@app.command()
def sync() -> None:
    """Sync with shared database"""
    try:
        local, server = vault.sync()
        Interface.display_message(Messages.sync_vault(local, server))
        logger.log_info("database synced")
    except Exception as e:
        handle_error(f"failed to sync vault: {e}")


if __name__ == "__main__":
    app()
