import typer

from app.cli import passwords, generator, vault, auth
from app.core import config, functions

app: typer.Typer = typer.Typer(rich_markup_mode="rich", no_args_is_help=True,
                               context_settings={"help_option_names": ["-h", "--help"]},
                               add_completion=False)
app.add_typer(passwords.app, name="passwords", no_args_is_help=True)
app.add_typer(generator.app, name="generator", no_args_is_help=True)
app.add_typer(vault.app, name="vault", no_args_is_help=True)
app.add_typer(auth.app, name="auth", no_args_is_help=True)


@app.callback()
def app_callback(
        ctx: typer.Context,
        version: bool = typer.Option(None, "--version", "-v",
                                     is_eager=True, callback=functions.version_callback, help="Show version and exit")
) -> None:
    """passphera-cli - Strong passwords generator and manager."""


def main() -> None:
    config.init_configurations()
    app()


if __name__ == "__main__":
    main()
