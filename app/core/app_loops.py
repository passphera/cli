import typer

from app.backend import auth
from app.core import interface, functions


def main_loop() -> None:
    choice = interface.display_main_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            authentication_loop()
        case 2:
            passwords_loop()
        case 3:
            settings_loop()
        case 4:
            history_loop()
        case 4:
            authentication_loop()


def authentication_loop() -> None:
    choice = interface.display_auth_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
        case 2:
            if auth.is_authenticated():
                interface.display_error("You are already logged in")
                return
            email: str = typer.prompt("Enter your email")
            password: str = typer.prompt("Enter your password", hide_input=True)
            functions.login(email, password)
        case 3:
            if not auth.is_authenticated():
                interface.display_error("You are not logged in")
                return
            functions.logout()
        case 4:
            if auth.is_authenticated():
                interface.display_error("You should logout first")
                return
            email: str = typer.prompt("Enter your email")
            username: str = typer.prompt("Enter your username")
            password: str = typer.prompt("Enter your password", hide_input=True)
            functions.signup(email, username, password)
        case 5:
            functions.whoami()


def passwords_loop() -> None:
    choice = interface.display_passwords_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
        case 2:
            text: str = typer.prompt("Enter the text to encrypt")
            context: str | None = typer.prompt("Enter the context if you want to save the password",
                                               default='', show_default=False)
            functions.generate_password(text, context)
        case 3:
            context: str = typer.prompt("Enter the context of the password you want to update")
            functions.update_password(context)
        case 4:
            context: str = typer.prompt("Enter the context of the password you want to update")
            functions.delete_password(context)


def settings_loop() -> None:
    choice = interface.display_settings_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
        case 2:
            algorithm: str = typer.prompt("Enter the algorithm name")
            functions.change_algorithm(algorithm)
        case 3:
            functions.reset_algorithm()
        case 4:
            amount: int = int(typer.prompt("Enter the shift amount"))
            functions.change_shift(amount)
        case 5:
            functions.reset_shift()
        case 6:
            value: int = int(typer.prompt("Enter the value to multiply by"))
            functions.change_multiplier(value)
        case 7:
            functions.reset_multiplier()
        case 8:
            key: str = typer.prompt("Enter the new key")
            functions.change_key(key)
        case 9:
            functions.reset_key()
        case 10:
            character: str = typer.prompt("Enter the character to replace")
            replacement: str = typer.prompt("Enter the new replacement")
            functions.replace_character(character, replacement)
        case 11:
            character: str = typer.prompt("Enter the character to remove it's replacement")
            functions.reset_replacement(character)
        case 12:
            functions.get_replacements()


def history_loop() -> None:
    choice = interface.display_history_menu()
    match choice:
        case 0:
            raise typer.Exit()
        case 1:
            main_loop()
        case 2:
            context: str = typer.prompt("Enter the context to get it's password")
            functions.get_password(context)
        case 3:
            functions.get_all_passwords()
        case 4:
            functions.clear_database()
        case 5:
            functions.sync()
