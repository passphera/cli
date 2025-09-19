import os
from configparser import ConfigParser
from typing import Optional


FILE: Optional[str] = None
__config: ConfigParser = ConfigParser()


def configure(path: str) -> None:
    global FILE
    FILE = os.path.join(path)
    load_settings()


def load_settings() -> None:
    if FILE:
        __config.read(FILE)


def save_settings() -> None:
    if not FILE:
        raise RuntimeError("Settings file not configured")
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
    if __config.has_option(section, key):
        __config.remove_option(section, key)
        save_settings()


def set_section(section: str) -> None:
    if not __config.has_section(section):
        __config.add_section(section)
        save_settings()


def delete_section(section: str) -> None:
    if __config.has_section(section):
        __config.remove_section(section)
        save_settings()


def get_settings(section: str) -> dict[str, str]:
    return dict(__config.items(section)) if __config.has_section(section) else {}
