import typer


app = typer.Typer()


@app.callback(invoke_without_command=False)
def config():
    """
    Manage configurations.

    configure the ciphering settings (shift amount, multiplier amount, characters replacements, etc...)
    """
    typer.echo("Here when we configure the application")


@app.command()
def shift():
    pass


@app.command()
def reset_shift():
    pass


@app.command()
def replace():
    pass


@app.command()
def reset_rep():
    pass


@app.command()
def char_rep():
    pass


@app.command()
def all_reps():
    pass


if __name__ == "__main__":
    app()
