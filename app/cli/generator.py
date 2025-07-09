from typing import Annotated

import typer

from passphera_core import InvalidAlgorithmException

from app.backend import generator
from app.core import logger
from app.core.decorators import handle_exception_decorator
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@handle_exception_decorator("")
@app.callback()
def generator_callback() -> None:
    """Manage generator: configure the ciphering settings (shift amount, character replacements, etc...)"""


@handle_exception_decorator("failed to get algorithm")
@app.command()
def get_algorithm() -> None:
    """Show ciphering primary algorithm"""
    Interface.display_message(f"Algorithm: {generator.get_algorithm()}", title="Generator Settings")


@handle_exception_decorator("failed to change primary algorithm")
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


@handle_exception_decorator("failed to reset primary algorithm")
@app.command()
def reset_algorithm() -> None:
    """Reset ciphering primary algorithm to default"""
    generator.reset_algorithm()
    Interface.display_message("Primary Algorithm has been changed to default", title="Generator Settings")
    logger.log_info("primary Algorithm has been reset")


@handle_exception_decorator("failed to get shift")
@app.command()
def get_shift() -> None:
    """Show ciphering shift amount"""
    Interface.display_message(f"Shift amount: {generator.get_shift()}", title="Generator Settings")


@handle_exception_decorator("failed to change shift")
@app.command()
def set_shift(
        amount: Annotated[int, typer.Argument(show_default=False, help="Amount to shift to.")],
) -> None:
    """Change ciphering shift amount"""
    generator.set_shift(amount)
    Interface.display_message(f"Shift has been changed to {amount}", title="Generator Settings")
    logger.log_info(f"shift changed to {amount}")


@handle_exception_decorator("failed to reset shift")
@app.command()
def reset_shift() -> None:
    """Reset ciphering shift amount to default value"""
    generator.reset_shift()
    Interface.display_message("Shift has been changed to default", title="Generator Settings")
    logger.log_info("shift has been reset")


@handle_exception_decorator("failed to get multiplier")
@app.command()
def get_multiplier() -> None:
    """Show ciphering multiplier value"""
    Interface.display_message(f"Multiplier value: {generator.get_multiplier()}", title="Generator Settings")


@handle_exception_decorator("failed to change multiplier")
@app.command()
def set_multiplier(
        value: Annotated[int, typer.Argument(show_default=False, help="Value to multiply by.")],
) -> None:
    """Change ciphering multiplier value"""
    generator.set_multiplier(value)
    Interface.display_message(f"Multiplier has been changed to {value}", title="Generator Settings")
    logger.log_info(f"multiplier changed to {value}")


@handle_exception_decorator("failed to reset multiplier")
@app.command()
def reset_multiplier() -> None:
    """Reset ciphering multiplier value to default value"""
    generator.reset_multiplier()
    Interface.display_message("Multiplier has been changed to default", title="Generator Settings")
    logger.log_info("multiplier has been reset")


@handle_exception_decorator("failed to get key")
@app.command()
def get_key() -> None:
    """Show ciphering key"""
    Interface.display_message(f"Key: {generator.get_key()}", title="Generator Settings")


@handle_exception_decorator("failed to change key")
@app.command()
def set_key(
        key: Annotated[str, typer.Argument(show_default=False, help="Key to use in encryption.")]
) -> None:
    """Change ciphering key"""
    generator.set_key(key)
    Interface.display_message(f"Key has been changed to {key}", title="Generator Settings")
    logger.log_info(f"key changed to {key}")


@handle_exception_decorator("failed to reset key")
@app.command()
def reset_key() -> None:
    """Reset ciphering key to default value"""
    generator.reset_key()
    Interface.display_message("Key has been changed to default", title="Generator Settings")
    logger.log_info("key has been reset")


@handle_exception_decorator("failed to get prefix")
@app.command()
def get_prefix() -> None:
    """Show ciphering prefix"""
    Interface.display_message(f"Prefix: {generator.get_prefix()}", title="Generator Settings")


@handle_exception_decorator("failed to change prefix")
@app.command()
def set_prefix(
        prefix: Annotated[str, typer.Argument(show_default=False, help="Text prefix.")],
) -> None:
    """Change ciphering prefix"""
    generator.set_prefix(prefix)
    Interface.display_message(f"Prefix has been changed to {prefix}", title="Generator Settings")
    logger.log_info(f"prefix changed to {prefix}")


@handle_exception_decorator("failed to reset prefix")
@app.command()
def reset_prefix() -> None:
    """Reset ciphering prefix to default"""
    generator.reset_prefix()
    Interface.display_message("Prefix has been changed to default", title="Generator Settings")
    logger.log_info("prefix has been reset")


@handle_exception_decorator("failed to get postfix")
@app.command()
def get_postfix() -> None:
    """Show ciphering postfix"""
    Interface.display_message(f"Postfix: {generator.get_postfix()}", title="Generator Settings")


@handle_exception_decorator("failed to change postfix")
@app.command()
def set_postfix(
        postfix: Annotated[str, typer.Argument(show_default=False, help="Text postfix.")],
) -> None:
    """Change ciphering postfix"""
    generator.set_postfix(postfix)
    Interface.display_message(f"Postfix has been changed to {postfix}", title="Generator Settings")
    logger.log_info(f"postfix changed to {postfix}")


@handle_exception_decorator("failed to reset postfix")
@app.command()
def reset_postfix() -> None:
    """Reset ciphering postfix to default"""
    generator.reset_postfix()
    Interface.display_message("Postfix has been reset", title="Generator Settings")
    logger.log_info("postfix has been reset")


@handle_exception_decorator("failed to get replacements")
@app.command()
def get_replacements() -> None:
    """Show all characters replacement strings"""
    replacements: dict[str, str] = generator.get_replacements()
    Interface.display_character_replacements(replacements)


@handle_exception_decorator("failed to change character replacement")
@app.command()
def set_replacement(
        character: Annotated[str, typer.Argument(show_default=False,
                                                 help="Character to be replaced (one character).")],
        replacement: Annotated[str, typer.Argument(show_default=False,
                                                   help="The replacement string (without spaces).")],
) -> None:
    """Replace character with a replacement string"""
    try:
        generator.set_replacement(character, replacement)
        Interface.display_message(f"Character '{character}' has been replaced with '{replacement}'", title="Generator Settings")
        logger.log_info(f"replace character '{character}' with '{replacement}'")
    except ValueError:
        Interface.display_message(Messages.INVALID_REPLACEMENT, style='bold red', title="Error")
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")


@handle_exception_decorator("failed to reset character replacement")
@app.command()
def reset_replacement(
        character: Annotated[str, typer.Argument(help="Character to reset it.")]
) -> None:
    """Reset a character's replacement"""
    generator.reset_replacement(character)
    Interface.display_message(f"Character {character}'s replacement has been removed", title="Generator Settings")
    logger.log_info(f"removed replacement for character {character}")


@handle_exception_decorator("failed to sync generator")
@app.command()
def sync() -> None:
    """Sync local settings with cloud settings id logged in"""
    generator.sync()
    Interface.display_message(Messages.SETTINGS_SYNCED, title="Generator Settings")
    logger.log_info("generator synced")


if __name__ == "__main__":
    app()
