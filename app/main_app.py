import typer

from app.cli import passwords, settings, vault, auth
from app.core import config


app: typer.Typer = typer.Typer(rich_markup_mode="rich")
app.add_typer(passwords.app, name="passwords")
app.add_typer(settings.app, name="settings")
app.add_typer(vault.app, name="vault")
app.add_typer(auth.app, name="auth")


@app.callback()
def app_callback(
        ctx: typer.Context,
        version: bool = typer.Option(None, "--version", "-v",
                                     is_eager=True, callback=config.version_callback, help="Show version and exit")
) -> None:
    """passphera-cli - Strong passwords generator cli tool to keep track of all your passwords."""


def main() -> None:
    config.init_configurations()
    app()


if __name__ == "__main__":
    print("You should run the entry point of the app instead.")
