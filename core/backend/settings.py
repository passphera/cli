import os
from configparser import ConfigParser

from core.backend import logger
from core.helpers import config


__file__: str | None = None
__characters_replacements__: str = "Characters Replacements"
__encryption_method__: str = "Encryption Method"
__history__: str = "History"

__algorithm__: str = "primary-algorithm"
__shift__: str = "shift-amount"
__multiplier__: str = "multiplier-amount"
__encrypted__: str = "encrypted"


__config: ConfigParser = ConfigParser()


def configure(path: str) -> None:
    global __file__
    __file__ = os.path.join(path)
    load_settings()


def load_settings() -> None:
    if __file__ and os.path.exists(__file__):
        __config.read(__file__)


def save_settings() -> None:
    with open(__file__, 'w') as configfile:
        __config.write(configfile)


def get_key(section: str, key: str, default: str = None) -> str | None:
    return __config.get(section, key, fallback=default)


def set_key(section: str, key: str, value: str) -> None:
    if not __config.has_section(section):
        __config.add_section(section)
    __config.set(section, key, value)


def delete_key(section: str, key: str) -> None:
    __config.remove_option(section, key)


def delete_section(section: str) -> None:
    __config.remove_section(section)


def get_settings(section: str) -> dict[str, str]:
    items = {}
    if __config.has_section(section):
        for key, value in __config.items(section):
            items[key] = value
    return items


def set_setting(section: str, key: str, value: str) -> None:
    set_key(section, key, value)
    save_settings()


def change_algorithm(name: str) -> None:
    config.generator.algorithm = name
    set_setting(__encryption_method__, __algorithm__, name)
    logger.log_info(f"Primary algorithm changed to {name}")


def reset_algorithm() -> None:
    config.generator.algorithm = config.__default_algorithm__
    set_setting(__encryption_method__, __algorithm__, config.__default_algorithm__)
    logger.log_info(f"Primary algorithm reset to it's default")


def change_shift(amount: int) -> None:
    config.generator.shift = amount
    set_setting(__encryption_method__, __shift__, str(amount))
    logger.log_info(f"Changed ciphering shift to {amount}")


def reset_shift() -> None:
    config.generator.shift = config.__default_shift__
    set_setting(__encryption_method__, __shift__, config.__default_shift__)
    logger.log_info(f"Reset ciphering shift settings to default value")


def change_multiplier(value: int) -> None:
    config.generator.multiplier = value
    set_setting(__encryption_method__, __multiplier__, str(value))
    logger.log_info(f"Changed ciphering multiplier to {value}")


def reset_multiplier() -> None:
    config.generator.shift = config.__default_multiplier__
    set_setting(__encryption_method__, __multiplier__, config.__default_multiplier__)
    logger.log_info(f"Reset ciphering multiplier settings to default value (3)")


def replace_character(character: str, replacement: str) -> None:
    if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
        raise ValueError
    config.generator.replace_character(character, replacement)
    set_setting(__characters_replacements__, character, replacement)
    logger.log_info(f"Replaced {character} with {replacement}")


def reset_replacement(character: str) -> None:
    config.generator.reset_character(character)
    set_setting(__characters_replacements__, character, character)
    logger.log_info(f"reset character {character} to its default")
