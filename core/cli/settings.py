from typing import Annotated

import typer

from core.backend import interface, logger, settings
from core.helpers.app_loops import settings_loop
from core.helpers.config import generator


app = typer.Typer()


@app.callback(invoke_without_command=True)
def settings(ctx: typer.Context):
    """
    Manage configurations

    configure the ciphering settings (shift amount, multiplier amount, characters replacements, etc...)
    """
    if ctx.invoked_subcommand is None:
        settings_loop()


@app.command()
def shift():
    """Change ciphering shift setting"""
    pass


@app.command()
def reset_shift():
    """Reset ciphering shift setting to default value"""
    pass


@app.command()
def replace(
        character: Annotated[str, typer.Argument(help="Character to be replaced (should be one character)")],
        replacement: Annotated[str, typer.Argument(help="The replacement string (should not contain spaces)")],
) -> None:
    """Replace character with a replacement string"""
    try:
        if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
            raise ValueError
        generator.replace_character(character, replacement)
        settings.set_key(settings.__characters_replacements__, character, replacement)
        settings.save_settings()
        logger.log_info(f"Replaced {character} with {replacement}")
    except ValueError:
        interface.display_replacement_error_message(replacement)
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")


@app.command()
def reset_rep(
    character: Annotated[str, typer.Argument(help="Character to reset it")]
):
    """reset a character's replacement"""
    generator.reset_character(character)
    settings.delete_key(settings.__characters_replacements__, character)
    settings.save_settings()
    logger.log_info(f"reset character {character} to its default")


@app.command()
def char_rep():
    """Show a specific character's replacement string"""
    pass


@app.command()
def all_reps():
    """Show all character's replacement strings"""
    pass


if __name__ == "__main__":
    app()
