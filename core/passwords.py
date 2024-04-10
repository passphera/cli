import typer


app = typer.Typer()


@app.callback()
def passwords():
    """
    Manage passwords.

    create, update, or delete passwords.
    """
    typer.echo("Here when we create, update and delete passwords")


@app.command()
def generate():
    typer.echo("Generating passwords...")


@app.command()
def update():
    typer.echo("Updating passwords...")


@app.command()
def delete():
    typer.echo("Deleting passwords...")


if __name__ == "__main__":
    app()
