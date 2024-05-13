import os
from configparser import ConfigParser


__file__: str | None = None
__characters_replacements__: str = "Characters Replacements"
__encryption_method__: str = "Encryption Method"
__history__: str = "History"

__config__: ConfigParser = ConfigParser()


def configure(path: str) -> None:
    global __file__
    __file__ = os.path.join(path)
    load_settings()


def load_settings() -> None:
    if __file__ and os.path.exists(__file__):
        __config__.read(__file__)


def save_settings() -> None:
    with open(__file__, 'w') as configfile:
        __config__.write(configfile)


def get_key(section: str, key: str, default: str = None) -> str | None:
    return __config__.get(section, key, fallback=default)


def set_key(section: str, key: str, value: str) -> None:
    if not __config__.has_section(section):
        __config__.add_section(section)
    __config__.set(section, key, value)


def delete_key(section: str, key: str) -> None:
    __config__.remove_option(section, key)


def delete_section(section: str) -> None:
    __config__.remove_section(section)


def get_settings(section: str) -> dict[str, str]:
    items = {}
    if __config__.has_section(section):
        for key, value in __config__.items(section):
            items[key] = value
    return items
