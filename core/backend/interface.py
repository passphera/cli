import pyperclip
from rich.console import Console
from rich.panel import Panel


console = Console()


def _display_menu(prompt, choices, title: str):
    console.print(Panel(prompt, title=title, title_align="left", style="bold cyan", border_style="magenta"))
    while True:
        try:
            choice = int(console.input("Select an option: "))
            if choice in choices:
                return choice
            console.print(f"[yellow]Invalid choice. Please select from 0 to {len(choices) - 1}.")
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a number.")


def display_main_menu():
    prompt = """1. Manage Passwords
2. Manage Configurations
3. Manage History
0. Exit"""
    choices = [0, 1, 2, 3]
    return _display_menu(prompt, choices, "passphera CLI Main Menu")


def display_passwords_menu():
    prompt = """1.  Back
2.  Generate new password
3.  Update saved password on history
4.  Remove saved password from history
0.  Exit"""
    choices = [0, 1, 2, 3, 4]
    return _display_menu(prompt, choices, "passphera CLI Passwords Menu")


def display_settings_menu():
    prompt = """1.  Back
2.  Change the shift of the encryption
3.  Reset the shift to its default value
4.  Replace an alphabet character with a set of custom characters
5.  Reset an alphabet character replacement to it's default
6.  Show a specific character replacement
7.  Show all characters replacements
0.  Exit"""
    choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return _display_menu(prompt, choices, "passphera CLI Settings Menu")


def display_history_menu():
    prompt = """1.  Back
2.  Retrieve saved password from history
3.  Show all saved passwords
4.  Clear history
5.  Back up history into backup file
6.  Load history from a back up from backup file
7.  Encrypt passwords on history file
8.  Decrypt passwords on history file
0.  Exit"""
    choices = [0, 1, 2, 3, 4, 5, 6]
    return _display_menu(prompt, choices, "passphera CLI History Menu")


def display_password(text, key, password, context=None):
    if context is not None:
        console.print(f"The context is:             [bold]{context}")
    console.print(f"The Text is:                [bold]{text}")
    console.print(f"The Key is:                 [bold]{key}")
    console.print(f"The Password is:            [bold magenta]{password}")


def display_character_replacement(character, replacement):
    console.print(f"{character} => {replacement}")


def display_password_removed_message():
    console.print("[red]This password was removed from memory, if you want to restore it, regenerate it.")


def display_context_error_message(context):
    console.print(f"[red]There is no password saved with this context '{context}'")


def display_replacement_error_message(replacement):
    console.print(f"[red]'[bold]{replacement}[/bold]' is not a valid replacement, you should chose another "
                  f"replacement[/red]\nAllowed special characters: [green]'!', '@', '$', '^', '-', '_', '=', '+', ',', "
                  f"'.', '/', ':'[/green]\nDisallowed special characters: [red]'`', '~', '#', '%', '&', '*', '(', ')',"
                  f" '<', '>', '?', ';', ''', '\"', '|', '\'[/red]")


def get_text():
    return str(console.input("Enter plain text: "))


def get_text_to_update():
    return str(console.input("Enter plain text (or press Enter to skip): "))


def get_key():
    return str(console.input("Enter the key (or press Enter to skip): "))


def get_shift():
    return str(console.input("Enter the shift number (between 1 and 25 or press Enter for default value): "))


def get_context_to_save():
    return str(console.input("Enter a context if you want to save the password in history (or press Enter to skip): "))


def get_context_to_load():
    return str(console.input("Enter the context of the saved password: "))


def get_character():
    return str(console.input("Which character ? "))


def replace_character():
    return str(console.input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))


def reset_character():
    return str(console.input("Enter the character you want to reset it ot it's default: "))[0]


def copy_to_clipboard(password):
    try:
        pyperclip.copy(password)
        console.print(f"[blue]Your password has been copied to your clipboard. Just paste it")
    except pyperclip.PyperclipException:
        console.print(f"[red]Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip)")
