from typing import Any

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console: Console = Console()


def _display_panel(message: Any, title: str = None) -> None:
    console.print(Panel(message, title=title, title_align="left", style="bold cyan", border_style="green"))


def _display_menu(prompt: str, choices: list[int], title: str) -> int:
    _display_panel(prompt, title)
    while True:
        try:
            choice = int(console.input("Select an option: "))
            if choice in choices:
                return choice
            console.print(f"[yellow]Invalid choice. Please select from 0 to {len(choices) - 1}.")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.")


def display_main_menu() -> int:
    prompt = """1. Authentication
2. Passwords
3. Settings
4. Database
0. Exit"""
    choices = [0, 1, 2, 3, 4]
    return _display_menu(prompt, choices, "passphera CLI Main Menu")


def display_auth_menu() -> int:
    prompt = """1. Back
2. Login with email and password
3. Logout
4. Register new user
5. My information
0. Exit"""
    choices = [0, 1, 2, 3, 4, 5]
    return _display_menu(prompt, choices, "passphera CLI Authentication Menu")


def display_passwords_menu() -> int:
    prompt = """1.  Back
2.  Generate new password
3.  Update saved password
4.  Delete saved password
0.  Exit"""
    choices = [0, 1, 2, 3, 4]
    return _display_menu(prompt, choices, "passphera CLI Passwords Menu")


def display_settings_menu() -> int:
    prompt = """1.  Back
2.  Change cipher algorithm
3.  Reset cipher algorithm to default value
4.  Change cipher shift
5.  Reset cipher shift to default value
6.  Change cipher multiplier
7.  Reset cipher multiplier to default value
8.  Change cipher key
9.  Reset cipher key to default value
10. Replace an alphabet character with a set of custom characters
11. Reset an alphabet character replacement to default value
12. Show characters replacements
0.  Exit"""
    choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    return _display_menu(prompt, choices, "passphera CLI Settings Menu")


def display_history_menu() -> int:
    prompt = """1.  Back
2.  Get saved password
3.  Show all saved passwords
4.  Clear database
5.  Sync with shared database
0.  Exit"""
    choices = [0, 1, 2, 3, 4, 5]
    return _display_menu(prompt, choices, "passphera CLI History Menu")


def display_user_info(user: dict[str, str]) -> None:
    info = f"""Username: {user.get('username')}
Email: {user.get('email')}
ID: {user.get('id')}"""
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
    table: Table = Table("text", "password", "context", show_header=True, header_style="bold magenta",
                         border_style="blue")
    for password in passwords:
        table.add_row(password['text'], password['password'], password['context'])
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
    console.print("[orange]The history has been cleared, if you want to restore it, you should have a backup, "
                  "or regenerate it.")


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
