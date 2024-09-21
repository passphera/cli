import os
import platform
from datetime import datetime as dt

import requests
import typer

from passphera_core import PasswordGenerator

from app.backend import auth, vault
from app.core import interface, logger, settings


__version__: str = '0.20.0'
__author__: str = 'Fathi Abdelmalek'
__email__: str = 'passphera@gmail.com'
__url__: str = 'https://github.com/passphera/cli'
__status__: str = 'Development'
__copyright__: str = 'Copyright 2024, Fathi Abdelmalek'

DEFAULT_SHIFT: str = "3"
DEFAULT_MULTIPLIER: str = "3"
DEFAULT_KEY: str = "hill"
DEFAULT_PREFIX: str = "prefix"
DEFAULT_POSTFIX: str = "postfix"
DEFAULT_ALGORITHM: str = "hill"
TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

ENDPOINT: str = "http://0.0.0.0:8000/api/v1"


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


def version_callback(value: bool) -> None:
    if value:
        print(typer.style(f"Version {__version__}", fg=typer.colors.CYAN, bold=True))
        raise typer.Exit()


generator: PasswordGenerator = PasswordGenerator()


def _init_files() -> None:
    platform_name = platform.system()
    if platform_name == 'Linux':
        setup_xdg_variables()
    paths = setup_paths(platform_name)
    create_dirs(paths)

    vault.configure(os.path.join(paths['data'], ".vault"))
    logger.configure(os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log"))
    settings.configure(os.path.join(paths['config'], "config.ini"))


def _init_generator() -> None:
    if auth.is_authenticated():
        response = requests.get(f"{ENDPOINT}/generator", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        generator.algorithm = response.json().get("algorithm")
        generator.shift = response.json().get("shift")
        generator.multiplier = response.json().get("multiplier")
        generator.key = response.json().get("key")
        generator.prefix = response.json().get("prefix")
        generator.postfix = response.json().get("postfix")
        for key, value in response.json().get('characters_replacements', {}).items():
            generator.replace_character(key, value)
    else:
        generator.algorithm = settings.get_key(settings.__encryption_method__, settings.__algorithm__, DEFAULT_ALGORITHM)
        generator.shift = int(settings.get_key(settings.__encryption_method__, settings.__shift__, DEFAULT_SHIFT))
        generator.multiplier = int(settings.get_key(settings.__encryption_method__, settings.__multiplier__, DEFAULT_MULTIPLIER))
        generator.key = settings.get_key(settings.__encryption_method__, settings.__key__, DEFAULT_KEY)
        generator.prefix = settings.get_key(settings.__encryption_method__, settings.__prefix__, DEFAULT_PREFIX)
        generator.postfix = settings.get_key(settings.__encryption_method__, settings.__postfix__, DEFAULT_POSTFIX)
        for key, value in settings.get_settings(settings.__characters_replacements__).items():
            generator.replace_character(key, value)


def _init_settings() -> None:
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, generator.algorithm)
    settings.set_key(settings.__encryption_method__, settings.__shift__, str(generator.shift))
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, str(generator.multiplier))
    settings.set_key(settings.__encryption_method__, settings.__key__, generator.key)
    for key, value in generator.characters_replacements.items():
        settings.set_key(settings.__characters_replacements__, key, value)
    settings.save_settings()


def init_configurations() -> None:
    try:
        _init_files()
        _init_generator()
        _init_settings()
    except Exception as e:
        interface.display_error(f"{e}")
