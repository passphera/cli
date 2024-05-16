import typer

from passphera_core import InvalidAlgorithmException

from core.backend import history, logger, settings, passwords
from core.helpers import interface
from core.helpers.config import generator


def generate_password() -> None:
    text: str = typer.prompt("Enter the text to encrypt")
    key: str | None = typer.prompt("Enter the key (leave blank for default)",
                                   default=generator.key_str, show_default=False)
    context: str | None = typer.prompt("Enter the context if you want to save the password",
                                       default='', show_default=False)
    passwords.generate_password(text, key, context)


def update_password() -> None:
    context: str = typer.prompt("Enter the context of the password you want to update")
    entry: dict[str, str] | None = history.get_password(context)
    if entry is not None:
        text: str = typer.prompt("Enter the text to encrypt (leave blank for old one)",
                                 default=entry['text'])
        key: str = typer.prompt("Enter the key (leave blank for default)", default=entry['key'])
        passwords.update_password(text, key, context)
    interface.display_context_error_message(context)
    logger.log_error(f"entered unsaved password context {context}")


def delete_password() -> None:
    context: str = typer.prompt("Enter the context of the password you want to update")
    passwords.delete_password(context)


def change_algorithm() -> None:
    name: str = typer.prompt("Enter the algorithm name")
    try:
        settings.change_algorithm(name)
        interface.display_message(f"Primary Algorithm has been changed to {name}")
        logger.log_info(f"Primary Algorithm has been changed to {name}")
    except InvalidAlgorithmException:
        interface.display_error(f"Invalid algorithm name: {name}")
        logger.log_error(f"Failed to change primary algorithm to {name}")


def reset_algorithm() -> None:
    settings.reset_algorithm()
    interface.display_message("Primary Algorithm has been changed to default")
    logger.log_info("Primary Algorithm has been changed to default")


def change_shift() -> None:
    amount: int = int(typer.prompt("Enter the shift amount"))
    settings.change_shift(amount)
    interface.display_message(f"Shift has been changed to {amount}")
    logger.log_info(f"Shift has been changed to {amount}")


def reset_shift() -> None:
    settings.reset_shift()
    interface.display_message("Shift has been changed to default")
    logger.log_info("Shift has been changed to default")


def change_multiplier() -> None:
    value: int = int(typer.prompt("Enter the value to multiply by"))
    settings.change_multiplier(value)
    interface.display_message(f"Multiplier has been changed to {value}")
    logger.log_info(f"Multiplier has been changed to {value}")


def reset_multiplier() -> None:
    settings.reset_multiplier()
    interface.display_message("Multiplier has been changed to default")
    logger.log_info("Multiplier has been changed to default")


def replace_character() -> None:
    character: str = typer.prompt("Enter the character to replace")
    replacement: str = typer.prompt("Enter the new replacement")
    try:
        settings.replace_character(character, replacement)
        interface.display_message(f"Character {character} has been replaced with {replacement}")
        logger.log_info(f"Character {character} has been replaced with {replacement}")
    except ValueError:
        interface.display_replacement_error_message(replacement)
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")


def reset_replacement() -> None:
    character: str = typer.prompt("Enter the character to remove it's replacement")
    settings.reset_replacement(character)
    interface.display_message(f"Character {character}'s replacement has been removed")
    logger.log_info(f"Character {character}'s replacement has been removed")


def show_replacement() -> None:
    character: str = typer.prompt("Enter the character to show it's replacement")
    replacement: str | None = settings.get_key(settings.__characters_replacements__, character)
    if replacement is not None:
        interface.display_character_replacement(character, replacement)
    else:
        interface.display_error("There is no replacement for this character")


def show_all_replacements() -> None:
    replacements: dict[str, str] = settings.get_settings(settings.__characters_replacements__)
    interface.display_character_replacements(replacements)
