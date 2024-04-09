from typing import Annotated, Optional

import typer


__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(typer.style(f"Version {__version__}", fg=typer.colors.GREEN, bold=True))
        raise typer.Exit()


def main(
        username: Annotated[str, typer.Option(
            "--username",
            "-n",
            prompt=True)],
        password: Annotated[str, typer.Option(
            "--password",
            "-p",
            prompt=True,
            confirmation_prompt=True,
            hide_input=True)],
        version: Annotated[
            Optional[bool], typer.Option(
                "--version",
                "-v",
                callback=version_callback,
                is_eager=True)] = None,
) -> None:
    if username is None or password is None:
        typer.echo("Please provide both username and password")
        raise typer.Exit(code=1)
    if username != "admin" or password != "admin":
        typer.echo("Incorrect username or password")
        raise typer.Exit(code=1)
    typer.echo("Logging in...")


if __name__ == '__main__':
    typer.run(main)
