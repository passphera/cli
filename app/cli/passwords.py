from typing import Annotated, Optional

import typer

from app.backend import vault, passwords
from app.core import logger
from app.core.decorators import handle_exception_decorator
from app.core.functions import copy_to_clipboard
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@handle_exception_decorator("")
@app.callback()
def passwords_callback() -> None:
    """Manage passwords: create, update, or delete passwords."""


@handle_exception_decorator("failed to generate password")
@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text",
                                          prompt="Enter the text to encrypt",
                                          show_default=False,
                                          help="Text to encrypt.")],
        context: Annotated[Optional[str], typer.Option("-c", "--context",
                                                       help="Context to save the password.")] = ''
) -> None:
    """Generate a new password (and optionally save it)"""
    if not context:
        context = typer.prompt("Enter a context if you want to save the password", default="", show_default=False)
    password: str = passwords.generate_password(text, context)
    Interface.display_password(password, text, context)
    copy_to_clipboard(password)
    logger.log_info("new password generated")
    if context != '':
        logger.log_info(f"new passwords saved using context '{context}'")


@handle_exception_decorator("failed to update password")
@app.command()
def update(
        context: Annotated[str, typer.Argument(show_default=False, help="Context of password to update.")],
        text: Annotated[str, typer.Option("-t", "--text",
                                          show_default=False,
                                          help="Text to encrypt (optional).")] = '',
) -> None:
    """Update a saved password"""
    db_password: dict[str, str] | None = vault.get_password(context)
    if db_password is None:
        raise ValueError(f"entered unsaved password context '{context}'")
    if not text:
        text: str = typer.prompt("Enter text to encrypt (optional)", default=db_password['text'])
    password = passwords.update_password(context, text)
    Interface.display_password(password, text, context)
    copy_to_clipboard(password)
    logger.log_info("saved password was updated")


@handle_exception_decorator("failed to delete password")
@app.command()
def delete(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to update.")],) -> None:
    """Delete a saved password"""
    entry: dict[str, str] = passwords.delete_password(context)
    Interface.display_message(Messages.PASSWORD_REMOVED)
    Interface.display_password(entry['password'], entry['text'], entry['context'])
    logger.log_warning("saved password was deleted")


if __name__ == "__main__":
    app()
