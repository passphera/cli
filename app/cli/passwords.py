from typing import Annotated, Optional

import typer

from app.core import functions


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def passwords_callback(ctx: typer.Context) -> None:
    """Manage passwords: create, update, or delete passwords."""


@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text",
                                          prompt="Enter the text to encrypt",
                                          show_default=False,
                                          help="Text to encrypt.")],
        context: Annotated[Optional[str], typer.Option("-c", "--context",
                                                       help="Context to save the password.")] = ''
) -> None:
    """Generate new password (and optionally save it)"""
    if not context:
        context = typer.prompt("Enter a context if you want to save the password", default="", show_default=False)
    functions.generate_password(text, context)


@app.command()
def update(
        context: Annotated[str, typer.Argument(show_default=False, help="Context of password to update.")],
        text: Annotated[str, typer.Option("-t", "--text",
                                          show_default=False,
                                          help="Text to encrypt (optional).")] = '',
) -> None:
    """Update a saved password"""
    functions.update_password(context, text)


@app.command()
def delete(context: Annotated[str, typer.Argument(show_default=False, help="Context of password to update.")],) -> None:
    """Delete a saved password"""
    functions.delete_password(context)


if __name__ == "__main__":
    app()
