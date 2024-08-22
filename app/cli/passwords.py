from typing import Annotated, Optional

import typer
from rich.prompt import Prompt

from app.backend import history, passwords
from app.core import interface, logger
from app.core.app_loops import passwords_loop


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def passwords_callback(ctx: typer.Context) -> None:
    """
    Manage passwords, create, update, or delete passwords.
    """
    if ctx.invoked_subcommand is None:
        while True:
            passwords_loop()


@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text", prompt="Enter the text to encrypt")],
        key: Annotated[Optional[str], typer.Option("-k", "--key")] = '',
        context: Annotated[Optional[str], typer.Option("-c", "--context")] = ''
) -> None:
    """Generate new password (and optionally save it)"""
    try:
        if not key:
            key = Prompt.ask("Enter the key (leave blank for default)", show_default=False)
        if not context:
            context = Prompt.ask("Enter a context if you want to save the password")
        password: str = passwords.generate_password(text, key)
        interface.display_password(password, text, key, context)
        interface.copy_to_clipboard(password)
        logger.log_info("new password generated successfully")
        if context != '':
            history.add_to_history(password, text, key, context)
            logger.log_info(f"new passwords saved using this context '{context}'")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


@app.command()
def update(
        context: Annotated[str, typer.Argument(help="The context of the password you want to update",
                                               show_default=False)],
        text: Annotated[str, typer.Option("-t", "--text",
                                          help="The text to encrypt [old one if blank]")] = '',
        key: Annotated[Optional[str], typer.Option("-k", "--key",
                                                   help="The key to use on encryption [old one if blank]")] = '',
) -> None:
    """Update a saved password"""
    entry: dict[str, str] | None = history.get_password(context)
    if entry is not None:
        if not text:
            text = typer.prompt("Enter the text to encrypt (leave blank for old one)", default=entry['text'])
        if not key:
            key = typer.prompt("Enter the key (leave blank for default)", default=entry['key'])
        password = passwords.update_password(text, key, context)
        interface.display_password(password, text, key, context)
        interface.copy_to_clipboard(password)
        logger.log_info(f"password updated successfully and saved on history")
        return
    interface.display_context_error_message(context)
    logger.log_error(f"entered unsaved password context {context}")


@app.command()
def delete(context: Annotated[str, typer.Argument(help="The context you want to update the password for")],) -> None:
    """Delete a saved password"""
    try:
        entry = passwords.delete_password(context)
        interface.display_password_removed_message()
        interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
        logger.log_warning("saved password was removed")
    except Exception as e:
        interface.display_context_error_message(context)
        logger.log_error(f"entered unsaved password context '{context}'")


if __name__ == "__main__":
    app()
