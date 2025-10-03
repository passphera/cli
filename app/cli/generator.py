from typing import Annotated

import typer

from app.backend import generator
from app.core import logger
from app.core.interface import Interface, Messages


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def generator_callback() -> None:
    """Manage generator: configure the ciphering settings (shift amount, character replacements, etc...)"""


@app.command(name="show")
def show_properties() -> None:
    """Show generator settings"""
    Interface.display_generator_settings(generator.show_properties())


@app.command(name="set")
def set_property(
        prop: Annotated[str, typer.Argument(show_default=False, help="Property to edit (shit, multiplier, key, algorithm, prefix, postfix).")],
        value: Annotated[str, typer.Argument(show_default=False, help="The value for the property")],
):
    """Set a new value to a property"""
    generator.set_property(prop, value)
    message = f"Property '{prop}' has been set to '{value}'"
    Interface.display_message(message, title="Generator Settings")
    logger.log_info(message)


@app.command(name="reset")
def reset_property(
        prop: Annotated[str, typer.Argument(show_default=False, help="Property to edit (shit, multiplier, key, algorithm, prefix, postfix).")]
):
    """Reset a property to its default value"""
    generator.reset_property(prop)
    message = f"Property '{prop}' has been reset to its default value"
    Interface.display_message(message, title="Generator Settings")
    logger.log_info(message)


@app.command(name="set-replacement")
def set_character_replacement(
        character: Annotated[str, typer.Argument(show_default=False,
                                                 help="Character to be replaced (one character).")],
        replacement: Annotated[str, typer.Argument(show_default=False,
                                                   help="The replacement string (without spaces).")],
) -> None:
    """Replace a character with a replacement string"""
    generator.set_character_replacement(character, replacement)
    Interface.display_message(f"Character '{character}' has been replaced with '{replacement}'", title="Generator Settings")
    logger.log_info(f"replace character '{character}' with '{replacement}'")


@app.command(name="reset-replacement")
def reset_character_replacement(
        character: Annotated[str, typer.Argument(help="Character to reset it.")]
) -> None:
    """Reset a character's replacement"""
    generator.reset_character_replacement(character)
    Interface.display_message(f"Character {character}'s replacement has been removed", title="Generator Settings")
    logger.log_info(f"removed replacement for character {character}")


@app.command(name="sync")
def sync_generator(
        way: Annotated[str, typer.Argument(help="Direction of sync: 'up' (local → cloud) or 'down' (cloud → local)")]
) -> None:
    """Sync local settings with cloud settings id logged in"""
    generator.sync_generator(way)
    Interface.display_message(Messages.SETTINGS_SYNCED, title="Generator Settings")
    logger.log_info(f"generator synced {way}")


if __name__ == "__main__":
    app()
