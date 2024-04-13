from typing import Annotated

import typer

from passphera_core import PasswordGenerator


app = typer.Typer()


@app.callback(invoke_without_command=True)
def passwords(ctx: typer.Context) -> None:
    """
    Manage passwords.

    create, update, or delete passwords.
    """
    typer.echo("Here when we create, update and delete passwords")


@app.command()
def generate(
        text: Annotated[str, typer.Option("-t", "--text", prompt=True)],
) -> None:
    typer.echo("Generating passwords...")
    p = PasswordGenerator(text)
    typer.echo(f"text : {p.text}")
    typer.echo(f"shift : {p.shift}")
    typer.echo(f"multiplier : {p.multiplier}")
    typer.echo(f"key shift : {p.key_str}")
    typer.echo(f"key iter : {p.key_iter}")
    typer.echo(f"main algorithm : {p.algorithm}")
    typer.echo(f"raw password : {p.generate_raw_password()}")
    typer.echo(f"password : {p.generate_password()}")


@app.command()
def update() -> None:
    typer.echo("Updating passwords...")


@app.command()
def delete() -> None:
    typer.echo("Deleting passwords...")


if __name__ == "__main__":
    app()
