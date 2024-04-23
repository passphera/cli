import typer

from core.backend import interface


def main_loop() -> None:
    while True:
        main_choice = interface.display_main_menu()
        match main_choice:
            case 0:
                raise typer.Exit()
            case 1:
                interface.display_passwords_menu()
            case 2:
                interface.display_settings_menu()
            case 3:
                interface.display_history_menu()
