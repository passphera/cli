from typing import Annotated, Optional

import typer


__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(typer.style(f"Version {__version__}", fg=typer.colors.GREEN, bold=True))
        raise typer.Exit()


app = typer.Typer(rich_markup_mode="rich")


@app.command()
def passwords():
    """
    Manage passwords.

    create, update, or delete passwords.
    """
    typer.echo("Here when we create, update and delete passwords")


@app.command()
def config():
    """
    Manage configurations.

    configure the ciphering settings (shift amount, multiplier amount, characters replacements, etc...)
    """
    typer.echo("Here when we configure the application")


@app.command()
def history():
    """
    Access history.

    get password or passwords, save/load history data to a backup, hash passwords on history.
    """
    typer.echo("Here when we access the history")


@app.callback(invoke_without_command=True)
def main(
        ctx: typer.Context,
        version: Annotated[
            Optional[bool], typer.Option(
                "--version",
                "-v",
                callback=version_callback,
                is_eager=True)] = None,):
    """
    Strong passwords generator cli tool to keep track of all your passwords.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Please specify a subcommand")
    else:
        typer.echo(f"Running {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
