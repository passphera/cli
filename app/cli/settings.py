from typing import Annotated

import typer

from app.core import functions


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def settings_callback(ctx: typer.Context) -> None:
    """Manage configurations, configure the ciphering settings (shift amount, characters replacements, etc...)"""


@app.command()
def get_shift() -> None:
    """Show ciphering shift amount"""
    functions.get_shift()


@app.command()
def change_shift(
        amount: Annotated[int, typer.Argument(help="The amount to shift to")],
) -> None:
    """Change ciphering shift amount"""
    functions.change_shift(amount)


@app.command()
def reset_shift() -> None:
    """Reset ciphering shift amount to default value"""
    functions.reset_shift()


@app.command()
def get_multiplier() -> None:
    """Show ciphering multiplier value"""
    functions.get_multiplier()


@app.command()
def change_multiplier(
        value: Annotated[int, typer.Argument(help="The value to multiply by")],
) -> None:
    """Change ciphering multiplier value"""
    functions.change_multiplier(value)


@app.command()
def reset_multiplier() -> None:
    """Reset ciphering multiplier value to default value"""
    functions.reset_multiplier()


@app.command()
def get_key() -> None:
    """Show ciphering key"""
    functions.get_key()


@app.command()
def change_key(
        key: Annotated[str, typer.Argument(help="The key to use in encryption")]
) -> None:
    """Change ciphering key"""
    functions.change_key(key)


@app.command()
def reset_key() -> None:
    """Reset ciphering key to default value"""
    functions.reset_key()


@app.command()
def get_prefix() -> None:
    """Show ciphering prefix"""
    functions.get_prefix()


@app.command()
def change_prefix(
        prefix: Annotated[str, typer.Argument(help="Text prefix")],
) -> None:
    """Change ciphering prefix"""
    functions.change_prefix(prefix)


@app.command()
def reset_prefix() -> None:
    """Reset ciphering prefix to default"""
    functions.reset_prefix()


@app.command()
def get_postfix() -> None:
    """Show ciphering postfix"""
    functions.get_postfix()


@app.command()
def change_postfix(
        postfix: Annotated[str, typer.Argument(help="Text postfix")],
) -> None:
    """Change ciphering postfix"""
    functions.change_postfix(postfix)


@app.command()
def reset_postfix() -> None:
    """Reset ciphering postfix to default"""
    functions.reset_postfix()


@app.command()
def get_algorithm() -> None:
    """Show ciphering primary algorithm"""
    functions.get_algorithm()


@app.command()
def change_algorithm(
        algorithm_name: Annotated[str, typer.Argument(help="Primary algorithm name")],
) -> None:
    """Change ciphering primary algorithm"""
    functions.change_algorithm(algorithm_name)


@app.command()
def reset_algorithm() -> None:
    """Reset ciphering primary algorithm to default"""
    functions.reset_algorithm()


@app.command()
def get_replacements() -> None:
    """Show all character's replacement strings"""
    functions.get_replacements()


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
    """Reset a character's replacement"""
    functions.reset_replacement(character)


@app.command()
def sync() -> None:
    """Sync local settings with cloud settings id logged in"""
    functions.sync_settings()


if __name__ == "__main__":
    app()
