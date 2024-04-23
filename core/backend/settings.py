import os
from configparser import ConfigParser


__file__ = None
__characters_replacements__ = "Characters Replacements"
__encryption_method__ = "Encryption Method"
__history__ = "History"

__config__ = ConfigParser()


def configure(path):
    global __file__
    __file__ = os.path.join(path)
    load_settings()


def load_settings():
    if __file__ and os.path.exists(__file__):
        __config__.read(__file__)


def save_settings():
    with open(__file__, 'w') as configfile:
        __config__.write(configfile)


def get_key(section, key, default=None):
    return __config__.get(section, key, fallback=default)


def set_key(section, key, value):
    if not __config__.has_section(section):
        __config__.add_section(section)
    __config__.set(section, key, value)


def delete_key(section, key):
    __config__.remove_option(section, key)


def delete_section(section):
    __config__.remove_section(section)


def get_settings(section):
    items = {}
    if __config__.has_section(section):
        for key, value in __config__.items(section):
            items[key] = value
    return items
