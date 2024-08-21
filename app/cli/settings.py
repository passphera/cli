from typing import Annotated

import typer
from passphera_core import InvalidAlgorithmException

from app.backend import logger
from app.core import config, interface, settings
from app.core.app_loops import settings_loop


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
        config.generator.algorithm = name
        settings.set_key(settings.__encryption_method__, settings.__algorithm__, name)
        interface.display_message(f"Primary Algorithm has been changed to {name}")
        logger.log_info(f"Primary Algorithm has been changed to {name}")
    except InvalidAlgorithmException:
        interface.display_error(f"Invalid algorithm name: {name}")
        logger.log_error(f"Failed to change primary algorithm to {name}")


@app.command()
def reset_algo() -> None:
    """Reset ciphering primary algorithm setting to default"""
    config.generator.algorithm = config.__default_algorithm__
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, config.__default_algorithm__)
    interface.display_message("Primary Algorithm has been changed to default")
    logger.log_info("Primary Algorithm has been changed to default")


@app.command()
def shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift setting"""
    config.generator.shift = amount
    settings.set_key(settings.__encryption_method__, settings.__shift__, str(amount))
    interface.display_message(f"Shift has been changed to {amount}")
    logger.log_info(f"Shift has been changed to {amount}")


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift setting to default value"""
    config.generator.shift = config.__default_shift__
    settings.set_key(settings.__encryption_method__, settings.__shift__, config.__default_shift__)
    interface.display_message("Shift has been changed to default")
    logger.log_info("Shift has been changed to default")


@app.command()
def multiplier(
        value: Annotated[int, typer.Argument(help="The value to multiply by")],
) -> None:
    """Change ciphering multiplier setting"""
    config.generator.multiplier = value
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, str(value))
    interface.display_message(f"Multiplier has been changed to {value}")
    logger.log_info(f"Multiplier has been changed to {value}")


@app.command()
def reset_mul() -> None:
    """Reset ciphering multiplier setting to default value"""
    config.generator.shift = config.__default_multiplier__
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, config.__default_multiplier__)
    interface.display_message("Multiplier has been changed to default")
    logger.log_info("Multiplier has been changed to default")


@app.command()
def key(
        new_key: Annotated[str, typer.Argument(help="The key to use in encryption")]
) -> None:
    """Change ciphering key setting"""
    config.generator.key = new_key
    settings.set_key(settings.__encryption_method__, settings.__key__, new_key)
    interface.display_message(f"Multiplier has been changed to {new_key}")
    logger.log_info(f"Changed key to {new_key}")


@app.command()
def reset_key() -> None:
    """Reset ciphering key setting to default value"""
    config.generator.key = config.__default_key__
    settings.set_key(settings.__encryption_method__, settings.__key__, config.__default_key__)
    interface.display_message("Key has been changed to default")
    logger.log_info("Key has been changed to default")



@app.command()
def replace_char(
        character: Annotated[str, typer.Argument(help="Character to be replaced (should be one character)")],
        replacement: Annotated[str, typer.Argument(help="The replacement string (should not contain spaces)")],
) -> None:
    """Replace character with a replacement string"""
    try:
        if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
            raise ValueError
        config.generator.replace_character(character, replacement)
        settings.set_key(settings.__characters_replacements__, character, replacement)
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
    config.generator.reset_character(character)
    settings.set_key(settings.__characters_replacements__, character, character)
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
