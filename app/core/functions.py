import typer

from passphera_core import InvalidAlgorithmException

from app.backend import auth, vault, generator, passwords
from app.core import logger
from app.core.interface import Interface, Messages


def _handle_error(message: str) -> None:
    Interface.display_message(str(Messages.error(message)), title='error', style='error')
    logger.log_error(message)


# auth
def login(email: str, password: str) -> None:
    try:
        auth.login(email, password)
        Interface.display_message("logged in successfully", title='login', style='success')
        logger.log_info(f"logged in with user email {email}")
    except Exception as e:
        _handle_error(f"failed to login: {e}")


def logout() -> None:
    try:
        auth.logout()
        Interface.display_message("logged out successfully", title='logout', style='success')
        logger.log_info("user logged out")
    except Exception as e:
        _handle_error(f"failed to logout: {e}")


def signup(email: str, username: str, password: str) -> None:
    try:
        auth.signup(email, username, password)
        Interface.display_message("user registered successfully", title='signup', style='success')
        logger.log_info("registered new user in the app server")
    except Exception as e:
        _handle_error(f"failed to signup: {e}")


def whoami() -> None:
    try:
        Interface.display_user_info(auth.get_auth_user())
    except Exception as e:
        _handle_error(f"failed to get user: {e}")


# generator
def get_algorithm() -> None:
    try:
        Interface.display_message(f"Algorithm: {generator.get_algorithm()}")
    except Exception as e:
        _handle_error(f"failed to get algorithm: {e}")


def change_algorithm(algorithm: str) -> None:
    try:
        generator.change_algorithm(algorithm)
        Interface.display_message(f"Primary Algorithm has been changed to {algorithm}")
        logger.log_info(f"primary algorithm changed to {algorithm}")
    except InvalidAlgorithmException as e:
        Interface.display_message(str(Messages.error("Invalid algorithm name")), title='error', style='error')
        logger.log_error(f"failed to change primary algorithm to {algorithm}: {e}")
    except Exception as e:
        _handle_error(f"failed to change primary algorithm to {algorithm}: {e}")


def reset_algorithm() -> None:
    try:
        generator.reset_algorithm()
        Interface.display_message("Primary Algorithm has been changed to default")
        logger.log_info("primary Algorithm has been reset")
    except Exception as e:
        _handle_error(f"failed to reset primary algorithm: {e}")


def get_shift() -> None:
    try:
        Interface.display_message(f"Shift amount: {generator.get_shift()}")
    except Exception as e:
        _handle_error(f"failed to get shift: {e}")


def change_shift(amount: int) -> None:
    try:
        generator.change_shift(amount)
        Interface.display_message(f"Shift has been changed to {amount}")
        logger.log_info(f"shift changed to {amount}")
    except Exception as e:
        _handle_error(f"failed to change shift to {amount}: {e}")


def reset_shift() -> None:
    try:
        generator.reset_shift()
        Interface.display_message("Shift has been changed to default")
        logger.log_info("shift has been reset")
    except Exception as e:
        _handle_error(f"failed to reset shift: {e}")


def get_multiplier() -> None:
    try:
        Interface.display_message(f"Multiplier value: {generator.get_multiplier()}")
    except Exception as e:
        _handle_error(f"failed to get multiplier: {e}")


def change_multiplier(value: int) -> None:
    try:
        generator.change_multiplier(value)
        Interface.display_message(f"Multiplier has been changed to {value}")
        logger.log_info(f"multiplier changed to {value}")
    except Exception as e:
        _handle_error(f"failed to change multiplier to {value}: {e}")


def reset_multiplier() -> None:
    try:
        generator.reset_multiplier()
        Interface.display_message("Multiplier has been changed to default")
        logger.log_info("multiplier has been reset")
    except Exception as e:
        _handle_error(f"failed to reset multiplier: {e}")


def get_key() -> None:
    try:
        Interface.display_message(f"Key: {generator.get_key()}")
    except Exception as e:
        _handle_error(f"failed to get key: {e}")


def change_key(key: str) -> None:
    try:
        generator.change_key(key)
        Interface.display_message(f"Key has been changed to {key}")
        logger.log_info(f"key changed to {key}")
    except Exception as e:
        _handle_error(f"failed to change key to {key}: {e}")


def reset_key() -> None:
    try:
        generator.reset_key()
        Interface.display_message("Key has been changed to default")
        logger.log_info("key has been reset")
    except Exception as e:
        _handle_error(f"failed to reset key: {e}")


def get_prefix() -> None:
    try:
        Interface.display_message(f"Prefix: {generator.get_prefix()}")
    except Exception as e:
        _handle_error(f"failed to get prefix: {e}")


def change_prefix(prefix: str) -> None:
    try:
        generator.change_prefix(prefix)
        Interface.display_message(f"Prefix has been changed to {prefix}")
        logger.log_info(f"prefix changed to {prefix}")
    except Exception as e:
        _handle_error(f"failed to change prefix to {prefix}: {e}")


def reset_prefix() -> None:
    try:
        generator.reset_prefix()
        Interface.display_message("Prefix has been changed to default")
        logger.log_info("prefix has been reset")
    except Exception as e:
        _handle_error(f"failed to reset prefix: {e}")


def get_postfix() -> None:
    try:
        Interface.display_message(f"Postfix: {generator.get_postfix()}")
    except Exception as e:
        _handle_error(f"failed to get postfix: {e}")


def change_postfix(postfix: str) -> None:
    try:
        generator.change_postfix(postfix)
        Interface.display_message(f"Postfix has been changed to {postfix}")
        logger.log_info(f"postfix changed to {postfix}")
    except Exception as e:
        _handle_error(f"failed to change postfix to {postfix}: {e}")


def reset_postfix() -> None:
    try:
        generator.reset_postfix()
        Interface.display_message("Postfix has been reset")
        logger.log_info("postfix has been reset")
    except Exception as e:
        _handle_error(f"failed to reset postfix: {e}")


def get_replacements() -> None:
    try:
        replacements: dict[str, str] = generator.get_characters_replacements()
        Interface.display_character_replacements(replacements)
    except Exception as e:
        _handle_error(f"failed to get replacements: {e}")


def replace_character(character: str, replacement: str) -> None:
    try:
        generator.replace_character(character, replacement)
        Interface.display_message(f"Character '{character}' has been replaced with '{replacement}'")
        logger.log_info(f"replace character '{character}' with '{replacement}'")
    except ValueError:
        Interface.display_message(Messages.INVALID_REPLACEMENT, style='bold red')
        logger.log_error(f"failed to replace character '{character}' with '{replacement}'")
    except Exception as e:
        _handle_error(f"failed to change character '{character}' with {replacement}: {e}")


def reset_replacement(character: str) -> None:
    try:
        generator.reset_replacement(character)
        Interface.display_message(f"Character {character}'s replacement has been removed")
        logger.log_info(f"removed replacement for character {character}")
    except Exception as e:
        _handle_error(f"failed to reset character {character} replacement: {e}")


def sync_generator() -> None:
    try:
        generator.sync()
        Interface.display_message(Messages.SETTINGS_SYNCED)
        logger.log_info("generator synced")
    except Exception as e:
        _handle_error(f"failed to sync generator: {e}")


# passwords
def generate_password(text: str, context: str = '') -> None:
    try:
        password: str = passwords.generate_password(text, context)
        Interface.display_password(password, text, context)
        Interface.copy_to_clipboard(password)
        logger.log_info("new password generated")
        if context != '':
            logger.log_info(f"new passwords saved using context '{context}'")
    except Exception as e:
        _handle_error(f"failed to generate password: {e}")


def update_password(context: str, text: str | None = None) -> None:
    try:
        db_password: dict[str, str] | None = vault.get_password(context)
        if db_password is None:
            raise ValueError(f"entered unsaved password context {context}")
        if not text:
            text: str = typer.prompt("Enter text to encrypt (optional)", default=db_password['text'])
        password = passwords.update_password(context, text)
        Interface.display_password(password, text, context)
        Interface.copy_to_clipboard(password)
        logger.log_info("saved password was updated")
    except ValueError as e:
        _handle_error(str(e))
    except Exception as e:
        _handle_error(f"failed to update password: {e}")


def delete_password(context: str) -> None:
    try:
        entry: dict[str, str] = passwords.delete_password(context)
        Interface.display_message(Messages.PASSWORD_REMOVED)
        Interface.display_password(entry['password'], entry['text'], entry['context'])
        logger.log_warning("saved password was deleted")
    except ValueError as e:
        _handle_error(f"failed to delete password: {e}")


# vault
def get_password(context: str) -> None:
    try:
        password: dict[str, str] = vault.get_password(context)
        if password is None:
            raise ValueError
        Interface.display_password(password)
        Interface.copy_to_clipboard(password['password'])
    except ValueError:
        Interface.display_message(str(Messages.context_error(context)), style='error')
    except Exception as e:
        _handle_error(f"failed to get password: {e}")


def get_all_passwords() -> None:
    try:
        Interface.display_passwords(vault.get_passwords())
    except Exception as e:
        _handle_error(f"failed to get passwords: {e}")


def clear_database() -> None:
    try:
        vault.clear_db()
        Interface.display_message(Messages.HISTORY_CLEARED)
        logger.log_info("database cleared")
    except Exception as e:
        _handle_error(f"failed to clear database: {e}")


def sync_vault() -> None:
    try:
        local, server = vault.sync()
        Interface.display_message(str(Messages.sync_vault(local, server)))
        logger.log_info("database synced")
    except Exception as e:
        _handle_error(f"failed to sync vault: {e}")
