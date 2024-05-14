from typing import Annotated

import typer

from passphera_core import InvalidAlgorithmException

from core.backend import logger, settings
from core.helpers import config, interface
from core.helpers.app_loops import settings_loop
from core.helpers.config import generator


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def settings_callback(ctx: typer.Context) -> None:
    """
    Manage configurations, configure the ciphering settings (shift amount, characters replacements, etc...)
    """
    if ctx.invoked_subcommand is None:
        settings_loop()


@app.command()
def algorithm(
        name: Annotated[str, typer.Argument(help="Primary algorithm name")],
) -> None:
    """Change ciphering primary algorithm setting"""
    try:
        generator.algorithm = name
        settings.set_key(settings.__encryption_method__, settings.__algorithm__, name)
        settings.save_settings()
        logger.log_info(f"Primary algorithm changed to {name}")
    except InvalidAlgorithmException:
        logger.log_error(f"Failed to change primary algorithm to {name}")


@app.command()
def reset_algo() -> None:
    """Reset ciphering primary algorithm setting to default"""
    generator.algorithm = config.__default_algorithm__
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, config.__default_algorithm__)
    settings.save_settings()
    logger.log_info(f"Primary algorithm reset to it's default")


@app.command()
def shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift setting"""
    generator.shift = amount
    settings.set_key(settings.__encryption_method__, settings.__shift__, str(amount))
    settings.save_settings()
    logger.log_info(f"Changed ciphering shift to {amount}")


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift setting to default value"""
    generator.shift = 3
    settings.set_key(settings.__encryption_method__, settings.__shift__, "3")
    settings.save_settings()
    logger.log_info(f"Reset ciphering shift settings to default value (3)")


@app.command()
def multiplier(
        value: Annotated[int, typer.Argument(help="The value to multiply by")],
) -> None:
    """Change ciphering multiplier setting"""
    generator.multiplier = value
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, str(value))
    settings.save_settings()
    logger.log_info(f"Changed ciphering multiplier to {value}")


@app.command()
def reset_mul() -> None:
    """Reset ciphering multiplier setting to default value"""
    generator.shift = 3
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, "3")
    settings.save_settings()
    logger.log_info(f"Reset ciphering multiplier settings to default value (3)")


@app.command()
def replace_char(
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
) -> None:
    """reset a character's replacement"""
    generator.reset_character(character)
    settings.delete_key(settings.__characters_replacements__, character)
    settings.save_settings()
    logger.log_info(f"reset character {character} to its default")


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
