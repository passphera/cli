from typing import Any

import pyperclip
from typer.rich_utils import Console, Panel, Table


console: Console = Console()


def _display_panel(message: Any, title: str = None) -> None:
    console.print(Panel(message, title=title, title_align="left", style="bold cyan", border_style="green"))


def display_user_info(user: dict[str, str]) -> None:
    info = f"""Username: {user.get('username')}
Email: {user.get('email')}"""
    _display_panel(info, "User Information")


def display_password(password: dict[str, str] | str, text: str = '', context: str = '') -> None:
    table: Table = Table("context", "text", "password", show_header=True, header_style="bold magenta",
                         border_style="blue")
    if type(password) is dict:
        table.add_row(password['context'], password['text'], password['password'])
        _display_panel(table)
    else:
        table.add_row(context, text, password)
        _display_panel(table)


def display_passwords(passwords: list[dict[str, str]]):
    table: Table = Table("context", "text", "password", show_header=True, header_style="bold magenta",
                         border_style="blue")
    for password in passwords:
        table.add_row(password['context'], password['text'], password['password'])
    _display_panel(table)


def display_character_replacement(character: str, replacement: str) -> None:
    _display_panel(f"{character} => {replacement}")


def display_character_replacements(replacements: dict[str, str]) -> None:
    table: Table = Table("character", "replacement", show_header=True, header_style="bold magenta",
                         border_style="blue")
    for character, replacement in replacements.items():
        table.add_row(character, replacement)
    _display_panel(table)


def display_password_removed_message() -> None:
    console.print("[orange]This password was removed from memory, if you want to restore it, regenerate it.")


def display_clear_history_message() -> None:
    console.print("[yellow]The history has been cleared, if you want to restore it, you should have a backup, "
                  "or regenerate it.")

def display_sync_settings_message() -> None:
    console.print("Settings synced successfully, now all settings are matching the cloud settings.")


def display_sync_vault_message(local: int, server: int) -> None:
    console.print(f"Database synced successfully\n{local} local has synced\n{server} server has synced")


def display_context_error_message(context: str) -> None:
    console.print(f"[red]There is no password saved with this context '{context}'")


def display_replacement_error_message(replacement: str) -> None:
    console.print(f"[red]'[bold]{replacement}[/bold]' is not a valid replacement, you should chose another "
                  f"replacement[/red]\nAllowed special characters: [green]'!', '@', '$', '^', '-', '_', '=', '+', ',', "
                  f"'.', '/', ':'[/green]\nDisallowed special characters: [red]'`', '~', '#', '%', '&', '*', '(', ')',"
                  f" '<', '>', '?', ';', ''', '\"', '|', '\\'[/red]")


def display_error(error: str) -> None:
    _display_panel(f"[red]There is an error: {error}")


def display_message(message: str) -> None:
    _display_panel(message)


def get_text() -> str:
    return str(console.input("Enter plain text: "))


def get_text_to_update() -> str:
    return str(console.input("Enter plain text (or press Enter to skip): "))


def get_key() -> str:
    return str(console.input("Enter the key (or press Enter to skip): "))


def get_shift() -> str:
    return str(console.input("Enter the shift number (between 1 and 25 or press Enter for default value): "))


def get_context_to_save() -> str:
    return str(console.input("Enter a context if you want to save the password in history (or press Enter to skip): "))


def get_context_to_load() -> str:
    return str(console.input("Enter the context of the saved password: "))


def get_character() -> str:
    return str(console.input("Which character ? "))


def replace_character() -> (str, str):
    return str(console.input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))


def reset_character() -> str:
    return str(console.input("Enter the character you want to reset it ot it's default: "))[0]


def copy_to_clipboard(password) -> None:
    try:
        pyperclip.copy(password)
        console.print("[bold blue]Your password has been copied to your clipboard. Just paste it")
    except pyperclip.PyperclipException:
        console.print("[bold red]Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip)")
