from typing import Annotated, Optional

import typer

from passphera_core.entities import Password

from app.backend import vault as b_vault
from app.cli import generator, vault, auth
from app.core import config, functions, logger
from app.core.interface import Interface
from core.decorators import handle_exception_decorator

app: typer.Typer = typer.Typer(rich_markup_mode="rich", no_args_is_help=True,
                               context_settings={"help_option_names": ["-h", "--help"]},
                               add_completion=False)
app.add_typer(generator.app, name="generator", no_args_is_help=True)
app.add_typer(vault.app, name="vault", no_args_is_help=True)
app.add_typer(auth.app, name="auth", no_args_is_help=True)


@handle_exception_decorator("")
@app.callback()
def app_callback(
        ctx: typer.Context,
        version: bool = typer.Option(None, "--version", "-v",
                                     is_eager=True, callback=functions.version_callback, help="Show version and exit")
) -> None:
    """passphera-cli - Strong passwords generator and manager."""


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
    """Alias to `vault add`"""
    if not context:
        context = typer.prompt("Enter a context if you want to save the password", default="", show_default=False)
    password_entity: Password = b_vault.add(context, text)
    password: str = password_entity.password
    Interface.display_password(password, text, context)
    functions.copy_to_clipboard(password)
    logger.log_info("new password generated")
    if context != '':
        logger.log_info(f"new passwords saved using context '{context}'")


def main() -> None:
    config.init_configurations()
    app()


if __name__ == "__main__":
    main()
