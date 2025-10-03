from typing import Annotated, Optional

import typer

from app.backend import vault
from app.core import functions, logger
from app.core.functions import copy_to_clipboard
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def vault_callback() -> None:
    """Access vault: get password or passwords, clear vault, sync vault data with cloud."""


@app.command(name="add")
def add_password(
        text: Annotated[str, typer.Option("-t", "--text",
                                          prompt="Enter the text to encrypt",
                                          show_default=False,
                                          help="Text to encrypt.")],
        context: Annotated[Optional[str], typer.Option("-c", "--context",
                                                       help="Context to save the password.")] = ''
) -> None:
    """Generate a new password and optionally save it to the vault"""
    if not context:
        context = typer.prompt("Enter a context if you want to save the password", default="", show_default=False)
    password: dict[str, str] = vault.add_password(context, text)
    Interface.display_password(password.get("password"), text, context)
    functions.copy_to_clipboard(password.get("password"))
    logger.log_info("new password generated")
    if context != '':
        logger.log_info(f"new passwords saved using context '{context}'")


@app.command(name="get")
def get_password(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to get.")]) -> None:
    """Get saved password from the vault"""
    try:
        password: dict[str, str] = vault.get_password(context)
        if password is None:
            raise ValueError
        Interface.display_password(password)
        copy_to_clipboard(password['password'])
    except ValueError:
        Interface.display_message(Messages.context_error(context), title='Error')


@app.command(name="update")
def update_password(
        context: Annotated[str, typer.Argument(show_default=False, help="Context of password to update.")],
        text: Annotated[str, typer.Option("-t", "--text",
                                          prompt="Enter the text to encrypt",
                                          show_default=False,
                                          help="Text to encrypt.")],
) -> None:
    """Update password in the vault"""
    if not text:
        text = typer.prompt("Enter the text to encrypt", show_default=False)
    password: dict[str, str] = vault.update_password(context, text)
    Interface.display_password(password.get("password"), text, context)
    functions.copy_to_clipboard(password.get("password"))
    logger.log_info(f"password updated using context '{context}'")


@app.command(name="delete")
def delete_password(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to delete.")]) -> None:
    """Delete saved password from the vault"""
    vault.delete_password(context)
    Interface.display_message(Messages.password_deleted(context), title="Vault")
    logger.log_info(f"password deleted using context '{context}'")


@app.command(name="list")
def list_passwords() -> None:
    """Get all saved passwords from the vault"""
    Interface.display_passwords(vault.list_passwords())

@app.command(name="flush")
def flush_vault() -> None:
    """Flush the vault (delete all passwords)"""
    vault.flush_vault()
    Interface.display_message(Messages.HISTORY_CLEARED, title="Vault")
    logger.log_info("database cleared")


@app.command(name="sync")
def sync_vault() -> None:
    """Sync down from the cloud"""
    _, updated_local, updated_server = vault.sync_vault()
    Interface.display_message(Messages.sync_vault(updated_local, updated_server))
    logger.log_info("vault synced")


if __name__ == "__main__":
    app()
