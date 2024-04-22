from typing import Annotated, Optional

import typer
from rich.prompt import Prompt

from passphera_core import PasswordGenerator

from core.helpers import interface
from core.helpers.history import History
from core.helpers.logger import Logger


app = typer.Typer()


@app.callback(invoke_without_command=False)
def passwords(ctx: typer.Context) -> None:
    """
    Manage passwords.

    create, update, or delete passwords.
    """
    typer.echo("Here when we create, update and delete passwords")


@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text", prompt="Enter the text to encrypt")],
        key: Annotated[Optional[str], typer.Option("-k", "--key")] = '',
        context: Annotated[Optional[str], typer.Option("-c", "--context")] = '',
) -> None:
    if text == '':
        typer.echo("Text can't be empty")
        return
    if not key:
        key = Prompt.ask("Enter a key [or leave blank for default]")
    if not context:
        context = Prompt.ask("Enter a context if you want to save the password")
    p = PasswordGenerator(text=text)
    if key != '':
        p.key_str = key
    else:
        key = p.key_str
    password = p.generate_password()
    interface.display_password(text, key, password)
    interface.copy_to_clipboard(password)
    Logger.log_info("new password generated successfully")
    if context != '':
        History.add_to_history(text, key, password, context)
        Logger.log_info(f"new passwords saved using this context '{context}'")


@app.command()
def update(
        context: Annotated[str, typer.Argument(help="The context you want to update the password for")],
        text: Annotated[str, typer.Option("-t", "--text", prompt="Enter the text to encrypt")],
        key: Annotated[Optional[str], typer.Option("-k", "--key")] = '',
) -> None:
    entry = History.get_password(context)
    if text == '':
        text = entry['text']
    if not key:
        key = Prompt.ask("Enter a key [or leave blank for default]")
    if key == '':
        key = entry['key']
    if entry:
        p = PasswordGenerator(text=text, key_str=key)
        password = p.generate_password()
        interface.display_password(text, key, password)
        interface.copy_to_clipboard(password)
        History.update_password(context, text, key, password)
        Logger.log_info(f"password updated successfully")
        Logger.log_info(f"password saved on history")
        return
    interface.display_context_error_message(context)
    Logger.log_error(f"entered unsaved password context {context}")


@app.command()
def delete(context: Annotated[str, typer.Argument(help="The context you want to update the password for")],) -> None:
    entry = History.get_password(context)
    if History.remove_password(context):
        interface.display_password_removed_message()
        interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
        Logger.log_warning("saved password was removed")
    else:
        interface.display_context_error_message(context)
        Logger.log_error(f"entered unsaved password context '{context}'")


if __name__ == "__main__":
    app()
