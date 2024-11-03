import os
from configparser import ConfigParser


FILE: str | None = None


__config: ConfigParser = ConfigParser()


def configure(path: str) -> None:
    global FILE
    FILE = os.path.join(path)
    load_settings()


def load_settings() -> None:
    if FILE and os.path.exists(FILE):
        __config.read(FILE)


def save_settings() -> None:
    with open(FILE, 'w') as configfile:
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


def set_section(section: str) -> None:
    if not __config.has_section(section):
        __config.add_section(section)


def delete_section(section: str) -> None:
    __config.remove_section(section)
    save_settings()


def get_settings(section: str) -> dict[str, str]:
    items = {}
    if __config.has_section(section):
        for key, value in __config.items(section):
            items[key] = value
    return items
