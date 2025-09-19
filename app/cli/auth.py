from typing import Annotated

import typer

from app.backend import auth
from app.core import logger
from app.core.decorators import handle_exception_decorator
from app.core.interface import Interface

app = typer.Typer(rich_markup_mode="rich")


@handle_exception_decorator("")
@app.callback()
def auth_callback() -> None:
    """Manage authentication: signup, login, logout."""


@handle_exception_decorator("failed to login")
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
    """Login to the app server with email and password"""
    auth.login(email, password)
    Interface.display_message("logged in successfully", title='Authentication', style='success')
    logger.log_info(f"logged in with user email {email}")


@handle_exception_decorator("failed to logout")
@app.command()
def logout() -> None:
    """Logout from the app server"""
    auth.logout()
    Interface.display_message("logged out successfully", title='Authentication', style='success')
    logger.log_info("user logged out")


@handle_exception_decorator("failed to signup")
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
    """Register a new user on the app server"""
    auth.signup(email, username, password)
    Interface.display_message("user registered successfully", title='Authentication', style='success')
    logger.log_info("registered new user in the app server")


@handle_exception_decorator("failed to get user")
@app.command()
def whoami() -> None:
    """Get user credentials"""
    Interface.display_user_info(auth.get_auth_user())


if __name__ == "__main__":
    app()
