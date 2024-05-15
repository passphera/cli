import typer

from core.helpers import interface, functions


def main_loop() -> None:
    while True:
        choice = interface.display_main_menu()
        match choice:
            case 0:
                raise typer.Exit()
            case 1:
                passwords_loop()
            case 2:
                settings_loop()
            case 3:
                history_loop()


def passwords_loop() -> None:
    while True:
        choice = interface.display_passwords_menu()
        match choice:
            case 0:
                raise typer.Exit()
            case 1:
                main_loop()
            case 2:
                functions.generate_password()
            case 3:
                functions.update_password()
            case 4:
                functions.delete_password()


def settings_loop() -> None:
    while True:
        choice = interface.display_settings_menu()
        match choice:
            case 0:
                raise typer.Exit()
            case 1:
                main_loop()


def history_loop() -> None:
    while True:
        choice = interface.display_history_menu()
        match choice:
            case 0:
                raise typer.Exit()
            case 1:
                main_loop()
