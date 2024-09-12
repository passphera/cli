from typing import Annotated

import typer

from app.core import functions
from app.core.app_loops import settings_loop


app = typer.Typer(rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def settings_callback(ctx: typer.Context) -> None:
    """
    Manage configurations, configure the ciphering settings (shift amount, characters replacements, etc...)
    """
    if ctx.invoked_subcommand is None:
        while True:
            settings_loop()


@app.command()
def algorithm(
        algorithm_name: Annotated[str, typer.Argument(help="Primary algorithm name")],
) -> None:
    """Change ciphering primary algorithm setting"""
    functions.change_algorithm(algorithm_name)


@app.command()
def reset_algorithm() -> None:
    """Reset ciphering primary algorithm setting to default"""
    functions.reset_algorithm()


@app.command()
def shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift setting"""
    functions.change_shift(amount)


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift setting to default value"""
    functions.reset_shift()


@app.command()
def multiplier(
        value: Annotated[int, typer.Argument(help="The value to multiply by")],
) -> None:
    """Change ciphering multiplier setting"""
    functions.change_multiplier(value)


@app.command()
def reset_multiplier() -> None:
    """Reset ciphering multiplier setting to default value"""
    functions.reset_multiplier()


@app.command()
def key(
        key: Annotated[str, typer.Argument(help="The key to use in encryption")]
) -> None:
    """Change ciphering key setting"""
    functions.change_key(key)


@app.command()
def reset_key() -> None:
    """Reset ciphering key setting to default value"""
    functions.reset_key()



@app.command()
def replace_character(
        character: Annotated[str, typer.Argument(help="Character to be replaced (should be one character)")],
        replacement: Annotated[str, typer.Argument(help="The replacement string (should not contain spaces)")],
) -> None:
    """Replace character with a replacement string"""
    functions.replace_character(character, replacement)


@app.command()
def reset_replacement(
        character: Annotated[str, typer.Argument(help="Character to reset it")]
) -> None:
    """reset a character's replacement"""
    functions.reset_replacement(character)


@app.command()
def show_replacements() -> None:
    """Show all character's replacement strings"""
    functions.show_replacements()


if __name__ == "__main__":
    app()
