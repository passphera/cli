import random

import pyperclip
from rich import print


def _display_menu(m, r):
    print(m)
    while True:
        try:
            choice = int(input("Select and option: "))
            if choice in r:
                return choice
            print(f"[yellow]Invalid choice. Please select from 0 to {len(r) - 1}.")
        except ValueError:
            print(f"[red]Invalid input. Please enter a number.")


def display_main_menu():
    m = """1. Manage Passwords
2. Manage Configurations
3. Manage History
0. Exit"""
    r = [0, 1, 2, 3]
    return _display_menu(m, r)


def display_passwords_menu():
    m = """1.  Back
2.  Generate new password
3.  Update saved password on history
4.  Remove saved password from history
0.  Exit"""
    r = [0, 1, 2, 3, 4]
    return _display_menu(m, r)


def display_settings_menu():
    m = """1.  Back
2.  Change the shift of the encryption
3.  Reset the shift to its default value
4.  Replace an alphabet character with a set of custom characters
5.  Reset an alphabet character replacement to it's default
6.  Show a specific character replacement
7.  Show all characters replacements
0.  Exit"""
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return _display_menu(m, r)


def display_history_menu():
    m = """1.  Back
2.  Retrieve saved password from history
3.  Show all saved passwords
4.  Clear history
5.  Back up history into backup file
6.  Load history from a back up from backup file
7.  Encrypt passwords on history file
8.  Decrypt passwords on history file
0.  Exit"""
    r = [0, 1, 2, 3, 4, 5, 6]
    return _display_menu(m, r)


def display_password(text, key, password, context=None):
    if context is not None:
        print(f"The context is:             [bold]{context}")
    print(f"The Text is:                [bold]{text}")
    print(f"The Key is:                 [bold]{key}")
    print(f"The Password is:            [bold magenta]{password}")


def display_character_replacement(character, replacement):
    print(f"{character} => {replacement}")


def display_password_removed_message():
    print(f"[red]This password was removed from memory, if you want to restore it, regenerate it.")


def display_context_error_message(context):
    print(f"[red]There is no password saved with this context '{context}'")


def display_replacement_error_message(replacement):
    print(f"[red]'[bold]{replacement}[/bold]' is not a valid replacement, you should chose another replacement[/red]\n"
          f"Allowed special characters: [green]'!', '@', '$', '^', '-', '_', '=', '+', ',', '.', '/', ':'[/green]\n"
          f"Disallowed special characters: [red]'`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', ''', "
          f"'\"', '|', '\'[/red]")


def get_text():
    text = str(input("Enter plain text: "))
    return text


def get_text_to_update():
    text = str(input("Enter plain text (or press Enter to skip): "))
    return text if text else None


def get_key(none: bool = False):
    key = str(input("Enter the key (or press Enter to skip): "))
    return key if key else None if none else ''.join(
        random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(4, 6)))


def get_shift():
    shift = str(input("Enter the shift number (between 1 and 25 or press Enter for default value): "))
    return shift if shift in range(1, 26) else 5


def get_context_to_save():
    context = str(input("Enter the context if you want to save the password in history (or press Enter to skip): "))
    return context if context else None


def get_context_to_load():
    return str(input("Enter the context of the saved password: "))


def get_character():
    return str(input("Which character ? "))


def replace_character():
    return str(input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))


def reset_character():
    return str(input("Enter the character you want to reset it ot it's default: "))[0]


def copy_to_clipboard(password):
    try:
        pyperclip.copy(password)
        print(f"[blue]Your password has been copied to your clipboard. Just paste it")
    except pyperclip.PyperclipException:
        print(f"[red]Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip)")
