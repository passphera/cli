import typer

from core.backend import interface


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
