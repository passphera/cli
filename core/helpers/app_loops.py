import typer

from core.helpers import interface, functions


def main_loop() -> None:
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
    choice = interface.display_settings_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
        case 2:
            functions.change_algorithm()
        case 3:
            functions.reset_algorithm()
        case 4:
            functions.change_shift()
        case 5:
            functions.reset_shift()
        case 6:
            functions.change_multiplier()
        case 7:
            functions.reset_multiplier()
        case 8:
            functions.replace_character()
        case 9:
            functions.reset_replacement()
        case 10:
            functions.show_replacement()
        case 11:
            functions.show_all_replacements()


def history_loop() -> None:
    choice = interface.display_history_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
