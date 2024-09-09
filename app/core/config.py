import os
import platform
from datetime import datetime as dt

import typer

from passphera_core import PasswordGenerator

from app.backend import history
from app.core import settings, logger

__version__: str = '0.14.0'
__author__: str = 'Fathi Abdelmalek'
__email__: str = 'passphera@gmail.com'
__url__: str = 'https://github.com/passphera/cli'
__status__: str = 'Development'
__copyright__: str = 'Copyright 2024, Fathi Abdelmalek'

DEFAULT_SHIFT: str = "3"
DEFAULT_MULTIPLIER: str = "3"
DEFAULT_KEY: str = "hill"
DEFAULT_ALGORITHM: str = "hill"
DEFAULT_ENCRYPTED: str = "false"

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

    history.configure(os.path.join(paths['data'], "history.json"))
    logger.configure(os.path.join(paths['cache'], f"log_{dt.now().strftime('%Y-%m-%d')}.log"))
    settings.configure(os.path.join(paths['config'], "config.ini"))


def _init_settings() -> None:
    if settings.get_key(settings.__encryption_method__, settings.__algorithm__) is None:
        settings.set_key(settings.__encryption_method__, settings.__algorithm__, DEFAULT_ALGORITHM)
    if settings.get_key(settings.__encryption_method__, settings.__shift__) is None:
        settings.set_key(settings.__encryption_method__, settings.__shift__, DEFAULT_SHIFT)
    if settings.get_key(settings.__encryption_method__, settings.__multiplier__) is None:
        settings.set_key(settings.__encryption_method__, settings.__multiplier__, DEFAULT_MULTIPLIER)
    if settings.get_key(settings.__encryption_method__, settings.__key__) is None:
        settings.set_key(settings.__encryption_method__, settings.__key__, DEFAULT_KEY)
    if settings.get_key(settings.__history__, settings.__encrypted__) is None:
        settings.set_key(settings.__history__, settings.__encrypted__, DEFAULT_ENCRYPTED)
    settings.save_settings()


def _init_generator() -> None:
    generator.algorithm = settings.get_key(settings.__encryption_method__, settings.__algorithm__)
    generator.shift = int(settings.get_key(settings.__encryption_method__, settings.__shift__))
    generator.multiplier = int(settings.get_key(settings.__encryption_method__, settings.__multiplier__))
    generator.key = settings.get_key(settings.__encryption_method__, settings.__key__)
    for key, value in settings.get_settings(settings.__characters_replacements__).items():
        generator.replace_character(key, value)


def init_configurations() -> None:
    _init_files()
    _init_settings()
    _init_generator()
