from typing import Annotated

import typer
from passphera_core import InvalidAlgorithmException

from core.backend import logger, settings
from core.helpers import interface
from core.helpers.app_loops import settings_loop


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def settings_callback(ctx: typer.Context) -> None:
    """
    Manage configurations, configure the ciphering settings (shift amount, characters replacements, etc...)
    """
    if ctx.invoked_subcommand is None:
        while True:
            settings_loop()


@app.command()
def algorithm(
        name: Annotated[str, typer.Argument(help="Primary algorithm name")],
) -> None:
    """Change ciphering primary algorithm setting"""
    try:
        settings.change_algorithm(name)
        interface.display_message(f"Primary Algorithm has been changed to {name}")
        logger.log_info(f"Primary Algorithm has been changed to {name}")
    except InvalidAlgorithmException:
        interface.display_error(f"Invalid algorithm name: {name}")
        logger.log_error(f"Failed to change primary algorithm to {name}")


@app.command()
def reset_algo() -> None:
    """Reset ciphering primary algorithm setting to default"""
    settings.reset_algorithm()
    interface.display_message("Primary Algorithm has been changed to default")
    logger.log_info("Primary Algorithm has been changed to default")


@app.command()
def shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift setting"""
    settings.change_shift(amount)
    interface.display_message(f"Shift has been changed to {amount}")
    logger.log_info(f"Shift has been changed to {amount}")


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift setting to default value"""
    settings.reset_shift()
    interface.display_message("Shift has been changed to default")
    logger.log_info("Shift has been changed to default")


@app.command()
def multiplier(
        value: Annotated[int, typer.Argument(help="The value to multiply by")],
) -> None:
    """Change ciphering multiplier setting"""
    settings.change_multiplier(value)
    interface.display_message(f"Multiplier has been changed to {value}")
    logger.log_info(f"Multiplier has been changed to {value}")


@app.command()
def reset_mul() -> None:
    """Reset ciphering multiplier setting to default value"""
    settings.reset_multiplier()
    interface.display_message("Multiplier has been changed to default")
    logger.log_info("Multiplier has been changed to default")


@app.command()
def replace_char(
        character: Annotated[str, typer.Argument(help="Character to be replaced (should be one character)")],
        replacement: Annotated[str, typer.Argument(help="The replacement string (should not contain spaces)")],
) -> None:
    """Replace character with a replacement string"""
    try:
        settings.replace_character(character, replacement)
        interface.display_message(f"Character {character} has been replaced with {replacement}")
        logger.log_info(f"Character {character} has been replaced with {replacement}")
    except ValueError:
        interface.display_replacement_error_message(replacement)
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")


@app.command()
def reset_rep(
        character: Annotated[str, typer.Argument(help="Character to reset it")]
) -> None:
    """reset a character's replacement"""
    settings.reset_replacement(character)
    interface.display_message(f"Character {character}'s replacement has been removed")
    logger.log_info(f"Character {character}'s replacement has been removed")


@app.command()
def show_rep(
        character: Annotated[str, typer.Argument(help="Character to reset it")]
) -> None:
    """Show a specific character's replacement string"""
    replacement: str | None = settings.get_key(settings.__characters_replacements__, character)
    if replacement is not None:
        interface.display_character_replacement(character, replacement)
    else:
        interface.display_error("There is no replacement for this character")


@app.command()
def all_reps() -> None:
    """Show all character's replacement strings"""
    replacements: dict[str, str] = settings.get_settings(settings.__characters_replacements__)
    interface.display_character_replacements(replacements)


if __name__ == "__main__":
    app()
