from typing import Annotated

import typer

from app.backend import settings
from app.core import interface, logger
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
        algorithm_name: Annotated[str, typer.Argument(help="Primary algorithm name")],
) -> None:
    """Change ciphering primary algorithm setting"""
    try:
        settings.change_algorithm(algorithm_name)
        interface.display_message(f"Primary Algorithm has been changed to {algorithm_name}")
        logger.log_info(f"Primary Algorithm has been changed to {algorithm_name}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change primary algorithm to {algorithm_name}")


@app.command()
def reset_algorithm() -> None:
    """Reset ciphering primary algorithm setting to default"""
    settings.reset_algorithm()
    interface.display_message("Primary Algorithm has been changed to default")
    logger.log_info("Primary Algorithm has been changed to default")


@app.command()
def shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift setting"""
    try:
        settings.change_shift(amount)
        interface.display_message(f"Shift has been changed to {amount}")
        logger.log_info(f"Shift has been changed to {amount}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change shift to {amount}")


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
    try:
        settings.change_multiplier(value)
        interface.display_message(f"Multiplier has been changed to {value}")
        logger.log_info(f"Multiplier has been changed to {value}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change multiplier to {value}")


@app.command()
def reset_mul() -> None:
    """Reset ciphering multiplier setting to default value"""
    settings.reset_multiplier()
    interface.display_message("Multiplier has been changed to default")
    logger.log_info("Multiplier has been changed to default")


@app.command()
def key(
        new_key: Annotated[str, typer.Argument(help="The key to use in encryption")]
) -> None:
    """Change ciphering key setting"""
    try:
        settings.change_cipher_key(new_key)
        interface.display_message(f"Multiplier has been changed to {new_key}")
        logger.log_info(f"Changed key to {new_key}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change key to {new_key}")


@app.command()
def reset_key() -> None:
    """Reset ciphering key setting to default value"""
    settings.reset_cipher_key()
    interface.display_message("Key has been changed to default")
    logger.log_info("Key has been changed to default")



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
    except Exception as e:
        interface.display_error(f"{e}")


@app.command()
def reset_rep(
        character: Annotated[str, typer.Argument(help="Character to reset it")]
) -> None:
    """reset a character's replacement"""
    try:
        settings.reset_replacement(character)
        interface.display_message(f"Character {character}'s replacement has been removed")
        logger.log_info(f"Character {character}'s replacement has been removed")
    except Exception as e:
        interface.display_error(f"{e}")


@app.command()
def show_rep(
        character: Annotated[str, typer.Argument(help="Character to reset it")]
) -> None:
    """Show a specific character's replacement string"""
    replacement: str | None = settings.show_character_replacement(character)
    if replacement is not None:
        interface.display_character_replacement(character, replacement)
    else:
        interface.display_error("There is no replacement for this character")


@app.command()
def all_reps() -> None:
    """Show all character's replacement strings"""
    replacements: dict[str, str] = settings.show_all_characters_replacements()
    interface.display_character_replacements(replacements)


if __name__ == "__main__":
    app()
