import typer
import pyperclip

from app.core import logger
from app.core.interface import Interface, Messages


def version_callback(value: bool) -> None:
    if value:
        Interface.display_version()
        raise typer.Exit()


def copy_to_clipboard(password: str) -> None:
    try:
        pyperclip.copy(password)
        Interface.display_message(Messages.COPIED_TO_CLIPBOARD)
    except pyperclip.PyperclipException:
        handle_error(str("Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip)"))


def handle_error(error: str) -> None:
    Interface.display_message(Messages.error(error), title="Error")
    logger.log_error(error)
