import typer

from core.helpers.app_loops import history_loop


app = typer.Typer()


@app.callback(invoke_without_command=True)
def history(ctx: typer.Context):
    """
    Access history

    get password or passwords, save/load history data to a backup, hash passwords on history.
    """
    if ctx.invoked_subcommand is None:
        history_loop()


@app.command()
def get():
    """Get a saved password from history"""


@app.command()
def show_all():
    """Show all saved passwords"""


@app.command()
def clear():
    """Clear history from all saved passwords"""


@app.command()
def save_backup():
    """Save backup history"""


@app.command()
def load_backup():
    """Load history from a saved backup"""


@app.command()
def encrypt():
    """Encrypt passwords on history"""


@app.command()
def decrypt():
    """Decrypt passwords on history"""


if __name__ == "__main__":
    app()
