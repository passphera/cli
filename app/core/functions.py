import typer

from passphera_core import InvalidAlgorithmException

from app.backend import auth, vault, settings, passwords
from app.core import interface, logger


# auth
def login(email: str, password: str) -> None:
    try:
        auth.login(email, password)
        interface.display_message("logged in successfully")
        logger.log_info(f"logged in with user email {email}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def logout() -> None:
    try:
        auth.logout()
        interface.display_message("logged out successfully")
        logger.log_info("user logged out")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def signup(email: str, username: str, password: str) -> None:
    try:
        auth.signup(email, username, password)
        interface.display_message("user registered successfully")
        logger.log_info("registered new user in the app server")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def whoami() -> None:
    try:
        interface.display_user_info(auth.get_auth_user())
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


# settings
def get_algorithm() -> None:
    try:
        interface.display_message(f"Algorithm: {settings.get_algorithm()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_algorithm(algorithm: str) -> None:
    try:
        settings.change_algorithm(algorithm)
        interface.display_message(f"Primary Algorithm has been changed to {algorithm}")
        logger.log_info(f"Primary Algorithm has been changed to {algorithm}")
    except InvalidAlgorithmException:
        interface.display_error("Invalid algorithm name")
        logger.log_error(f"Failed to change primary algorithm to {algorithm}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change primary algorithm to {algorithm}")


def reset_algorithm() -> None:
    try:
        settings.reset_algorithm()
        interface.display_message("Primary Algorithm has been changed to default")
        logger.log_info("Primary Algorithm has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset algorithm to default")


def get_shift() -> None:
    try:
        interface.display_message(f"Shift amount: {settings.get_shift()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_shift(amount: int) -> None:
    try:
        settings.change_shift(amount)
        interface.display_message(f"Shift has been changed to {amount}")
        logger.log_info(f"Shift has been changed to {amount}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change shift to {amount}")


def reset_shift() -> None:
    try:
        settings.reset_shift()
        interface.display_message("Shift has been changed to default")
        logger.log_info("Shift has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset shift to default")


def get_multiplier() -> None:
    try:
        interface.display_message(f"Multiplier value: {settings.get_multiplier()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_multiplier(value: int) -> None:
    try:
        settings.change_multiplier(value)
        interface.display_message(f"Multiplier has been changed to {value}")
        logger.log_info(f"Multiplier has been changed to {value}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change multiplier to {value}")


def reset_multiplier() -> None:
    try:
        settings.reset_multiplier()
        interface.display_message("Multiplier has been changed to default")
        logger.log_info("Multiplier has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset multiplier to default")


def get_key() -> None:
    try:
        interface.display_message(f"Key: {settings.get_key()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_key(key: str) -> None:
    try:
        settings.change_key(key)
        interface.display_message(f"Key has been changed to {key}")
        logger.log_info(f"Changed key to {key}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change key to {key}")


def reset_key() -> None:
    try:
        settings.reset_key()
        interface.display_message("Key has been changed to default")
        logger.log_info("Key has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset key to default")


def get_prefix() -> None:
    try:
        interface.display_message(f"Prefix: {settings.get_prefix()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_prefix(prefix: str) -> None:
    try:
        settings.change_prefix(prefix)
        interface.display_message(f"Prefix has been changed to {prefix}")
        logger.log_info(f"Changed prefix to {prefix}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change prefix to {prefix}")


def reset_prefix() -> None:
    try:
        settings.reset_prefix()
        interface.display_message("Prefix has been changed to default")
        logger.log_info("Prefix has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset prefix to default")


def get_postfix() -> None:
    try:
        interface.display_message(f"Postfix: {settings.get_postfix()}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def change_postfix(postfix: str) -> None:
    try:
        settings.change_postfix(postfix)
        interface.display_message(f"Postfix has been changed to {postfix}")
        logger.log_info(f"Changed postfix to {postfix}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change postfix to {postfix}")


def reset_postfix() -> None:
    try:
        settings.reset_postfix()
        interface.display_message("Postfix has been changed to default")
        logger.log_info("Postfix has been changed to default")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error("Failed to reset postfix to default")


def get_replacements() -> None:
    try:
        replacements: dict[str, str] = settings.get_characters_replacements()
        interface.display_character_replacements(replacements)
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def replace_character(character: str, replacement: str) -> None:
    try:
        settings.replace_character(character, replacement)
        interface.display_message(f"Character {character} has been replaced with {replacement}")
        logger.log_info(f"Character {character} has been replaced with {replacement}")
    except ValueError:
        interface.display_replacement_error_message(replacement)
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to change character '{character}' replacement to {replacement}")


def reset_replacement(character: str) -> None:
    try:
        settings.reset_replacement(character)
        interface.display_message(f"Character {character}'s replacement has been removed")
        logger.log_info(f"Character {character}'s replacement has been removed")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"Failed to reset character '{character}' replacement to default")


# passwords
def generate_password(text: str, context: str = '') -> None:
    try:
        password: str = passwords.generate_password(text, context)
        interface.display_password(password, text, context)
        interface.copy_to_clipboard(password)
        logger.log_info("new password generated successfully")
        if context != '':
            logger.log_info(f"new passwords saved using this context '{context}'")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def update_password(context: str, text: str | None = None) -> None:
    try:
        db_password: dict[str, str] | None = vault.get_password(context)
        if db_password is None:
            raise ValueError(f"entered unsaved password context {context}")
        if not text:
            text: str = typer.prompt("Enter the text to encrypt (leave blank for old one)",
                                     default=db_password['text'])
        password = passwords.update_password(context, text)
        interface.display_password(password, text, context)
        interface.copy_to_clipboard(password)
        logger.log_info("password updated successfully")
    except ValueError as e:
        interface.display_context_error_message(context)
        logger.log_error(f"{e}")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def delete_password(context: str) -> None:
    try:
        entry: dict[str, str] = passwords.delete_password(context)
        interface.display_password_removed_message()
        interface.display_password(entry['context'], entry['text'], entry['password'])
        logger.log_warning("saved password was removed from database")
    except ValueError as e:
        interface.display_context_error_message(context)
        logger.log_error(f"entered unsaved password context '{context}'")
        logger.log_error(f"{e}")


# vault
def get_password(context: str) -> None:
    try:
        password: dict[str, str] = vault.get_password(context)
        if password is None:
            raise ValueError
        interface.display_password(password)
        interface.copy_to_clipboard(password['password'])
    except ValueError:
        interface.display_context_error_message(context)


def get_all_passwords() -> None:
    try:
        interface.display_passwords(vault.get_passwords())
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def clear_database() -> None:
    try:
        vault.clear_db()
        interface.display_clear_history_message()
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")


def sync() -> None:
    try:
        local, server = vault.sync()
        interface.display_sync_message(local, server)
        logger.log_info("Database synced successfully")
    except Exception as e:
        interface.display_error(f"{e}")
        logger.log_error(f"{e}")
