from core.backend import history, logger
from core.helpers import interface
from core.helpers.config import generator


def generate_password(text: str, key: str = '', context: str = '') -> None:
    generator.text = text
    if key != '':
        generator.key_str = key
    else:
        key = generator.key_str
    password = generator.generate_password()
    interface.display_password(password, text, key, context)
    interface.copy_to_clipboard(password)
    logger.log_info("new password generated successfully")
    if context != '':
        history.add_to_history(password, text, key, context)
        logger.log_info(f"new passwords saved using this context '{context}'")


def update_password(text: str, key: str, context: str) -> None:
    generator.text = text
    generator.key_str = key
    password = generator.generate_password()
    interface.display_password(password, text, key, context)
    interface.copy_to_clipboard(password)
    history.add_to_history(password, text, key, context)
    logger.log_info(f"password updated successfully")
    logger.log_info(f"password saved on history")


def delete_password(context: str) -> None:
    entry: dict[str, str] | None = history.get_password(context)
    if history.remove_password(context):
        interface.display_password_removed_message()
        interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
        logger.log_warning("saved password was removed")
    else:
        interface.display_context_error_message(context)
        logger.log_error(f"entered unsaved password context '{context}'")
