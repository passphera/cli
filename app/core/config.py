import os
import platform
from datetime import datetime as dt

import requests

from passphera_core import PasswordGenerator

from app.backend import auth, vault
from app.core import constants, logger, settings
from app.core.interface import Interface, Messages


__name__: str = 'passphera'
__version__: str = '2.0.0'
__author__: str = 'Fathi Abdelmalek'
__author_email__: str = 'passphera@gmail.com'
__url__: str = 'https://passphera-site.onrender.com'
__license__: str = 'Apache-2.0'
__copyright__: str = 'Copyright 2024, Fathi Abdelmalek'
__description__: str = 'Strong passwords generator and manager'


generator: PasswordGenerator = PasswordGenerator()


def setup_xdg_variables() -> None:
    xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_cache_home is None:
        xdg_cache_home = os.path.expanduser("~/.cache")
        os.environ["XDG_CACHE_HOME"] = xdg_cache_home
    if xdg_config_home is None:
        xdg_config_home = os.path.expanduser("~/.config")
        os.environ["XDG_CONFIG_HOME"] = xdg_config_home
    if xdg_data_home is None:
        xdg_data_home = os.path.expanduser("~/.local/share")
        os.environ["XDG_DATA_HOME"] = xdg_data_home


def setup_paths(platform_name) -> dict[str, str]:
    paths: dict[str, dict[str, str]] = {
        "Linux": {
            "cache": os.path.join(os.path.expandvars("$XDG_CACHE_HOME"), "passphera", "cli"),
            "config": os.path.join(os.path.expandvars("$XDG_CONFIG_HOME"), "passphera", "cli"),
            "data": os.path.join(os.path.expandvars("$XDG_DATA_HOME"), "passphera", "cli"),
        },
        "Windows": {
            "cache": os.path.expanduser(os.path.join("~", ".passphera", "cli")),
            "config": os.path.expanduser(os.path.join("~", ".passphera", "cli")),
            "data": os.path.expanduser(os.path.join("~", ".passphera", "cli")),
        },
        "Darwin": {
            "cache": os.path.expanduser(os.path.join("~", "Library", "Caches", "passphera", "cli")),
            "config": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passphera", "cli")),
            "data": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passphera", "cli")),
        },
    }
    if platform_name not in paths:
        raise Exception("Unsupported platform")
    return paths[platform_name]


def create_dirs(paths: dict[str, str]) -> None:
    for path in paths.values():
        if not os.path.exists(path):
            os.makedirs(path)


def init_configurations() -> None:
    try:
        platform_name = platform.system()
        if platform_name == 'Linux':
            setup_xdg_variables()
        paths = setup_paths(platform_name)
        create_dirs(paths)

        vault.configure(os.path.join(paths['data'], ".vault"))
        logger.configure(os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log"))
        settings.configure(os.path.join(paths['config'], "config.ini"))

        settings.set_section(constants.ENCRYPTION_METHOD)
        settings.set_section(constants.CHARACTERS_REPLACEMENTS)
        settings.set_section(constants.AUTH)

        generator.algorithm = settings.get_key(constants.ENCRYPTION_METHOD, constants.ALGORITHM, constants.DEFAULT_ALGORITHM)
        generator.shift = int(settings.get_key(constants.ENCRYPTION_METHOD, constants.SHIFT, constants.DEFAULT_SHIFT))
        generator.multiplier = int(settings.get_key(constants.ENCRYPTION_METHOD, constants.MULTIPLIER, constants.DEFAULT_MULTIPLIER))
        generator.key = settings.get_key(constants.ENCRYPTION_METHOD, constants.KEY, constants.DEFAULT_KEY)
        generator.prefix = settings.get_key(constants.ENCRYPTION_METHOD, constants.PREFIX, constants.DEFAULT_PREFIX)
        generator.postfix = settings.get_key(constants.ENCRYPTION_METHOD, constants.POSTFIX, constants.DEFAULT_POSTFIX)
        for key, value in settings.get_settings(constants.CHARACTERS_REPLACEMENTS).items():
            generator.replace_character(key, value)

        settings.set_key(constants.ENCRYPTION_METHOD, constants.ALGORITHM, generator.algorithm)
        settings.set_key(constants.ENCRYPTION_METHOD, constants.SHIFT, str(generator.shift))
        settings.set_key(constants.ENCRYPTION_METHOD, constants.MULTIPLIER, str(generator.multiplier))
        settings.set_key(constants.ENCRYPTION_METHOD, constants.KEY, generator.key)
        for key, value in generator.characters_replacements.items():
            settings.set_key(constants.CHARACTERS_REPLACEMENTS, key, value)
        settings.save_settings()
    except Exception as e:
        Interface.display_message(str(Messages.error(str(e))), title='error', style='error')
