import typer

from core.cli import history, passwords, settings
from core.helpers import app_loops, config


app: typer.Typer = typer.Typer(rich_markup_mode="rich")
app.add_typer(passwords.app, name="passwords")
app.add_typer(settings.app, name="settings")
app.add_typer(history.app, name="history")


@app.callback(invoke_without_command=True)
def app_callback(ctx: typer.Context,
                 version: bool = typer.Option(None, "--version", "-v", is_eager=True,
                                              callback=config.version_callback, help="Show version and exit")) -> None:
    """
    passphera-cli - Strong passwords generator cli tool to keep track of all your passwords.
    """
    if ctx.invoked_subcommand is None:
        while True:
            app_loops.main_loop()


def main() -> None:
    config.init_configurations()
    app()


if __name__ == "__main__":
    print("You should run the entry point of the app instead.")
