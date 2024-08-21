import os
from configparser import ConfigParser


__file__: str | None = None

# sections
__characters_replacements__: str = "Characters Replacements"
__encryption_method__: str = "Encryption Method"
__history__: str = "History"
__auth__: str = "Authentication"

# keys
__algorithm__: str = "primary-algorithm"
__shift__: str = "shift-amount"
__multiplier__: str = "multiplier-amount"
__key__: str = "key"
__encrypted__: str = "encrypted"
__access_token__: str = "access-token"


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
    save_settings()


def delete_key(section: str, key: str) -> None:
    __config.remove_option(section, key)
    save_settings()


def delete_section(section: str) -> None:
    __config.remove_section(section)
    save_settings()


def get_settings(section: str) -> dict[str, str]:
    items = {}
    if __config.has_section(section):
        for key, value in __config.items(section):
            items[key] = value
    return items
