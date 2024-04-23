import typer


app = typer.Typer()


@app.callback(invoke_without_command=False)
def history():
    """
    Access history.

    get password or passwords, save/load history data to a backup, hash passwords on history.
    """
    pass


@app.command()
def get():
    pass


@app.command()
def show_all():
    pass


@app.command()
def clear():
    pass


@app.command()
def save_backup():
    pass


@app.command()
def load_backup():
    pass


@app.command()
def encrypt():
    pass


@app.command()
def decrypt():
    pass


if __name__ == "__main__":
    app()
