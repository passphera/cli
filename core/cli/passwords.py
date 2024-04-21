from typing import Annotated, Optional

import typer
from rich.prompt import Prompt

from passphera_core import PasswordGenerator

from core.helpers import interface
# from core.helpers.logger import Logger


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
    # logger = Logger()
    # logger.log_info("New password generated successfully")
    if context != '':
        # TODO: save the generated password to the history
        typer.echo(f"password will be saved using this context '{context}'")
        # logger.log_info(f"New passwords saved using this context {context}")


@app.command()
def update() -> None:
    typer.echo("Updating passwords...")


@app.command()
def delete() -> None:
    typer.echo("Deleting passwords...")


if __name__ == "__main__":
    app()
