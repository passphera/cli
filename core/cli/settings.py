from typing import Annotated

import typer

from core.backend import interface, logger, settings as b_settings
from core.helpers.config import generator


app = typer.Typer()


@app.callback(invoke_without_command=False)
def settings():
    """
    Manage configurations.

    configure the ciphering settings (shift amount, multiplier amount, characters replacements, etc...)
    """
    pass


@app.command()
def shift():
    pass


@app.command()
def reset_shift():
    pass


@app.command()
def replace(
        character: Annotated[str, typer.Argument(help="Character to be replaced (should be one character)")],
        replacement: Annotated[str, typer.Argument(help="The replacement string (should not contain spaces)")],
) -> None:
    try:
        if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
            raise ValueError
        generator.replace_character(character, replacement)
        b_settings.set_key(b_settings.__characters_replacements__, character, replacement)
        b_settings.save_settings()
        logger.log_info(f"Replaced {character} with {replacement}")
    except ValueError:
        interface.display_replacement_error_message(replacement)
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")


@app.command()
def reset_rep(
    character: Annotated[str, typer.Argument(help="Character to reset it")]
):
    generator.reset_character(character)
    b_settings.delete_key(b_settings.__characters_replacements__, character)
    b_settings.save_settings()
    logger.log_info(f"reset character {character} to its default")


@app.command()
def char_rep():
    pass


@app.command()
def all_reps():
    pass


if __name__ == "__main__":
    app()
