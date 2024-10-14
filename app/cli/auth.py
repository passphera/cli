from typing import Annotated

import typer

from app.core import functions


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def auth_callback(ctx: typer.Context) -> None:
    """Manage authentication: signup, login, logout."""


@app.command()
def login(
        email: Annotated[str, typer.Option("-e", "--email",
                                           prompt=True, show_default=False,
                                           help="Email address to login."),],
        password: Annotated[str, typer.Option("-p", "--password",
                                              prompt=True, show_default=False,
                                              hide_input=True,
                                              help="Password to login."),],
) -> None:
    """Login to the app server"""
    functions.login(email, password)


@app.command()
def logout() -> None:
    """Logout from the app server"""
    functions.logout()


@app.command()
def signup(
        email: Annotated[str, typer.Option("-e", "--email",
                                           prompt=True, show_default=False,
                                           help="Email address.")],
        username: Annotated[str, typer.Option("-n", "--username",
                                              prompt=True, show_default=False,
                                              help="Username.")],
        password: Annotated[str, typer.Option("-p",
                                              "--password",
                                              prompt=True, show_default=False,
                                              hide_input=True, confirmation_prompt=True,
                                              help="Password."
                                              )],
) -> None:
    """Register new user on the app server"""
    functions.signup(email, username, password)


@app.command()
def whoami() -> None:
    """Get user credentials"""
    functions.whoami()


if __name__ == "__main__":
    app()
