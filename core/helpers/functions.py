import typer

from core.backend import history, logger, passwords
from core.helpers import interface
from core.helpers.config import generator


def generate_password() -> None:
    text: str = typer.prompt("Enter the text to encrypt")
    key: str | None = typer.prompt("Enter the key (leave blank for default)",
                                   default=generator.key_str, show_default=False)
    context: str | None = typer.prompt("Enter the context if you want to save the password",
                                       default='', show_default=False)
    passwords.generate_password(text, key, context)


def update_password() -> None:
    context: str = typer.prompt("Enter the context of the password you want to update")
    entry: dict[str, str] | None = history.get_password(context)
    if entry is not None:
        text: str = typer.prompt("Enter the text to encrypt (leave blank for old one)",
                                 default=entry['text'])
        key: str = typer.prompt("Enter the key (leave blank for default)", default=entry['key'])
        passwords.update_password(text, key, context)
    interface.display_context_error_message(context)
    logger.log_error(f"entered unsaved password context {context}")


def delete_password() -> None:
    context: str = typer.prompt("Enter the context of the password you want to update")
    passwords.delete_password(context)
