from typing import Annotated

import typer

from passphera_core import InvalidAlgorithmException

from app.backend import generator
from app.core import logger
from app.core.functions import handle_error
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def generator_callback() -> None:
    """Manage generator: configure the ciphering settings (shift amount, characters replacements, etc...)"""


@app.command()
def get_algorithm() -> None:
    """Show ciphering primary algorithm"""
    try:
        Interface.display_message(f"Algorithm: {generator.get_algorithm()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get algorithm: {e}")


@app.command()
def set_algorithm(
        algorithm: Annotated[str, typer.Argument(show_default=False, help="Primary algorithm name.")],
) -> None:
    """Change ciphering primary algorithm"""
    try:
        generator.set_algorithm(algorithm)
        Interface.display_message(f"Primary Algorithm has been changed to {algorithm}", title="Generator Settings")
        logger.log_info(f"primary algorithm changed to {algorithm}")
    except InvalidAlgorithmException as e:
        Interface.display_message(str(Messages.error("Invalid algorithm name")), title='error', style='error')
        logger.log_error(f"failed to change primary algorithm to {algorithm}: {e}")
    except Exception as e:
        handle_error(f"failed to change primary algorithm to {algorithm}: {e}")


@app.command()
def reset_algorithm() -> None:
    """Reset ciphering primary algorithm to default"""
    try:
        generator.reset_algorithm()
        Interface.display_message("Primary Algorithm has been changed to default", title="Generator Settings")
        logger.log_info("primary Algorithm has been reset")
    except Exception as e:
        handle_error(f"failed to reset primary algorithm: {e}")


@app.command()
def get_shift() -> None:
    """Show ciphering shift amount"""
    try:
        Interface.display_message(f"Shift amount: {generator.get_shift()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get shift: {e}")


@app.command()
def set_shift(
        amount: Annotated[int, typer.Argument(show_default=False, help="Amount to shift to.")],
) -> None:
    """Change ciphering shift amount"""
    try:
        generator.set_shift(amount)
        Interface.display_message(f"Shift has been changed to {amount}", title="Generator Settings")
        logger.log_info(f"shift changed to {amount}")
    except Exception as e:
        handle_error(f"failed to change shift to {amount}: {e}")


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift amount to default value"""
    try:
        generator.reset_shift()
        Interface.display_message("Shift has been changed to default", title="Generator Settings")
        logger.log_info("shift has been reset")
    except Exception as e:
        handle_error(f"failed to reset shift: {e}")


@app.command()
def get_multiplier() -> None:
    """Show ciphering multiplier value"""
    try:
        Interface.display_message(f"Multiplier value: {generator.get_multiplier()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get multiplier: {e}")


@app.command()
def set_multiplier(
        value: Annotated[int, typer.Argument(show_default=False, help="Value to multiply by.")],
) -> None:
    """Change ciphering multiplier value"""
    try:
        generator.set_multiplier(value)
        Interface.display_message(f"Multiplier has been changed to {value}", title="Generator Settings")
        logger.log_info(f"multiplier changed to {value}")
    except Exception as e:
        handle_error(f"failed to change multiplier to {value}: {e}")


@app.command()
def reset_multiplier() -> None:
    """Reset ciphering multiplier value to default value"""
    try:
        generator.reset_multiplier()
        Interface.display_message("Multiplier has been changed to default", title="Generator Settings")
        logger.log_info("multiplier has been reset")
    except Exception as e:
        handle_error(f"failed to reset multiplier: {e}")


@app.command()
def get_key() -> None:
    """Show ciphering key"""
    try:
        Interface.display_message(f"Key: {generator.get_key()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get key: {e}")


@app.command()
def set_key(
        key: Annotated[str, typer.Argument(show_default=False, help="Key to use in encryption.")]
) -> None:
    """Change ciphering key"""
    try:
        generator.set_key(key)
        Interface.display_message(f"Key has been changed to {key}", title="Generator Settings")
        logger.log_info(f"key changed to {key}")
    except Exception as e:
        handle_error(f"failed to change key to {key}: {e}")


@app.command()
def reset_key() -> None:
    """Reset ciphering key to default value"""
    try:
        generator.reset_key()
        Interface.display_message("Key has been changed to default", title="Generator Settings")
        logger.log_info("key has been reset")
    except Exception as e:
        handle_error(f"failed to reset key: {e}")


@app.command()
def get_prefix() -> None:
    """Show ciphering prefix"""
    try:
        Interface.display_message(f"Prefix: {generator.get_prefix()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get prefix: {e}")


@app.command()
def set_prefix(
        prefix: Annotated[str, typer.Argument(show_default=False, help="Text prefix.")],
) -> None:
    """Change ciphering prefix"""
    try:
        generator.set_prefix(prefix)
        Interface.display_message(f"Prefix has been changed to {prefix}", title="Generator Settings")
        logger.log_info(f"prefix changed to {prefix}")
    except Exception as e:
        handle_error(f"failed to change prefix to {prefix}: {e}")


@app.command()
def reset_prefix() -> None:
    """Reset ciphering prefix to default"""
    try:
        generator.reset_prefix()
        Interface.display_message("Prefix has been changed to default", title="Generator Settings")
        logger.log_info("prefix has been reset")
    except Exception as e:
        handle_error(f"failed to reset prefix: {e}")


@app.command()
def get_postfix() -> None:
    """Show ciphering postfix"""
    try:
        Interface.display_message(f"Postfix: {generator.get_postfix()}", title="Generator Settings")
    except Exception as e:
        handle_error(f"failed to get postfix: {e}")


@app.command()
def set_postfix(
        postfix: Annotated[str, typer.Argument(show_default=False, help="Text postfix.")],
) -> None:
    """Change ciphering postfix"""
    try:
        generator.set_postfix(postfix)
        Interface.display_message(f"Postfix has been changed to {postfix}", title="Generator Settings")
        logger.log_info(f"postfix changed to {postfix}")
    except Exception as e:
        handle_error(f"failed to change postfix to {postfix}: {e}")


@app.command()
def reset_postfix() -> None:
    """Reset ciphering postfix to default"""
    try:
        generator.reset_postfix()
        Interface.display_message("Postfix has been reset", title="Generator Settings")
        logger.log_info("postfix has been reset")
    except Exception as e:
        handle_error(f"failed to reset postfix: {e}")


@app.command()
def get_replacements() -> None:
    """Show all character's replacement strings"""
    try:
        replacements: dict[str, str] = generator.get_characters_replacements()
        Interface.display_character_replacements(replacements)
    except Exception as e:
        handle_error(f"failed to get replacements: {e}")


@app.command()
def set_character(
        character: Annotated[str, typer.Argument(show_default=False,
                                                 help="Character to be replaced (one character).")],
        replacement: Annotated[str, typer.Argument(show_default=False,
                                                   help="The replacement string (without spaces).")],
) -> None:
    """Replace character with a replacement string"""
    try:
        generator.set_character(character, replacement)
        Interface.display_message(f"Character '{character}' has been replaced with '{replacement}'", title="Generator Settings")
        logger.log_info(f"replace character '{character}' with '{replacement}'")
    except ValueError:
        Interface.display_message(Messages.INVALID_REPLACEMENT, style='bold red', title="Error")
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")
    except Exception as e:
        handle_error(f"failed to change character '{character}' with {replacement}: {e}")


@app.command()
def reset_replacement(
        character: Annotated[str, typer.Argument(help="Character to reset it.")]
) -> None:
    """Reset a character's replacement"""
    try:
        generator.reset_replacement(character)
        Interface.display_message(f"Character {character}'s replacement has been removed", title="Generator Settings")
        logger.log_info(f"removed replacement for character {character}")
    except Exception as e:
        handle_error(f"failed to reset character {character} replacement: {e}")


@app.command()
def sync() -> None:
    """Sync local settings with cloud settings id logged in"""
    try:
        generator.sync()
        Interface.display_message(Messages.SETTINGS_SYNCED, title="Generator Settings")
        logger.log_info("generator synced")
    except Exception as e:
        handle_error(f"failed to sync generator: {e}")


if __name__ == "__main__":
    app()
