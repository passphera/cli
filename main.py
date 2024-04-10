from typing import Annotated, Optional

import typer

from core import passwords, config, history


__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(typer.style(f"Version {__version__}", fg=typer.colors.GREEN, bold=True))
        raise typer.Exit()


app = typer.Typer(rich_markup_mode="rich")
app.add_typer(passwords.app)
app.add_typer(config.app)
app.add_typer(history.app)


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
