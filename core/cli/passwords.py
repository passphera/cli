from typing import Annotated, Optional

import typer
from rich.prompt import Prompt

from core.backend import history, logger
from core.helpers import interface
from core.helpers.app_loops import passwords_loop
from core.helpers.config import generator


app = typer.Typer()


@app.callback(invoke_without_command=True)
def passwords_callback(ctx: typer.Context) -> None:
    """
    Manage passwords, create, update, or delete passwords.
    """
    if ctx.invoked_subcommand is None:
        passwords_loop()


@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text", prompt="Enter the text to encrypt")],
        key: Annotated[Optional[str], typer.Option("-k", "--key")] = '',
        context: Annotated[Optional[str], typer.Option("-c", "--context")] = ''
) -> None:
    """Generate new password (and optionally save it)"""
    if text == '':
        typer.echo("Text can't be empty")
        return
    if not key:
        key = Prompt.ask("Enter a key [or leave blank for default]")
    if not context:
        context = Prompt.ask("Enter a context if you want to save the password")
    generator.text = text
    if key != '':
        generator.key_str = key
    else:
        key = generator.key_str
    password = generator.generate_password()
    if context is None:
        interface.display_password(password, text, key)
    else:
        interface.display_password(password, text, key, context)
    interface.copy_to_clipboard(password)
    logger.log_info("new password generated successfully")
    if context != '':
        history.add_to_history(text, key, password, context)
        logger.log_info(f"new passwords saved using this context '{context}'")


@app.command()
def update(
        context: Annotated[str, typer.Argument(help="The context you want to update the password for")],
        text: Annotated[str, typer.Option("-t", "--text", prompt="Enter the text to encrypt")],
        key: Annotated[Optional[str], typer.Option("-k", "--key")] = '',
) -> None:
    """Update a saved password"""
    entry = history.get_password(context)
    if text == '':
        text = entry['text']
    if not key:
        key = Prompt.ask("Enter a key [or leave blank for default]")
    if key == '':
        key = entry['key']
    if entry:
        generator.text = text
        generator.key_str = key
        password = generator.generate_password()
        interface.display_password(text, key, password)
        interface.copy_to_clipboard(password)
        history.add_to_history(context, text, key, password)
        logger.log_info(f"password updated successfully")
        logger.log_info(f"password saved on history")
        return
    interface.display_context_error_message(context)
    logger.log_error(f"entered unsaved password context {context}")


@app.command()
def delete(context: Annotated[str, typer.Argument(help="The context you want to update the password for")],) -> None:
    """Delete a saved password"""
    entry = history.get_password(context)
    if history.remove_password(context):
        interface.display_password_removed_message()
        interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
        logger.log_warning("saved password was removed")
    else:
        interface.display_context_error_message(context)
        logger.log_error(f"entered unsaved password context '{context}'")


if __name__ == "__main__":
    app()
