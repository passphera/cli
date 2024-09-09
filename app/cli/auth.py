from typing import Annotated

import typer

from app.backend import auth
from app.core import interface, logger
from app.core.app_loops import authentication_loop

app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def auth_callback(ctx: typer.Context) -> None:
    """Manage authentication (signup, login, logout)"""
    if ctx.invoked_subcommand is None:
        while True:
            authentication_loop()


@app.command()
def signup(
        email: Annotated[str, typer.Option("-e", "--email", prompt=True)],
        username: Annotated[str, typer.Option("-n", "--username", prompt=True)],
        password: Annotated[str, typer.Option("-p",
                                              "--password",
                                              prompt=True,
                                              hide_input=True,
                                              confirmation_prompt=True
                                              )],
) -> None:
    """Register new user on the app server"""
    try:
        auth.signup(email, username, password)
        interface.display_message("user registered successfully")
        logger.log_info("registered new user in the app server")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


@app.command()
def login(
        email: Annotated[str, typer.Option("-e", "--email", prompt=True)],
        password: Annotated[str, typer.Option("-p", "--password", prompt=True, hide_input=True)],
) -> None:
    """Login to the app server"""
    try:
        auth.login(email, password)
        interface.display_message("logged in successfully")
        logger.log_info(f"logged in with user email {email}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


@app.command()
def logout() -> None:
    """Logout from the app server"""
    try:
        auth.logout()
        interface.display_message("logged out successfully")
        logger.log_info("user logged out")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


@app.command()
def whoami() -> None:
    """Get user credentials"""
    try:
        user = auth.get_auth_user()
        header = auth.get_auth_header()
        print(header)
        print(user)
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


if __name__ == "__main__":
    app()
