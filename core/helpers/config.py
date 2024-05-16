import os
import platform
from datetime import datetime as dt

import typer

from passphera_core import PasswordGenerator

from core.backend import history, logger, settings

__version__: str = '0.9.0'
__author__: str = 'Fathi Abdelmalek'
__email__: str = 'passphera@gmail.com'
__url__: str = 'https://github.com/passphera/cli'
__status__: str = 'Development'
__copyright__: str = 'Copyright 2024, Fathi Abdelmalek'


__xdg_cache_home__: str = os.environ.get("XDG_CACHE_HOME")
__xdg_config_home__: str = os.environ.get("XDG_CONFIG_HOME")
__xdg_data_home__: str = os.environ.get("XDG_DATA_HOME")
__paths__: dict[str, dict[str, str]] = {
        "Windows": {
            "cache": os.path.expanduser(os.path.join("~", ".passgen")),
            "config": os.path.expanduser(os.path.join("~", ".passgen")),
            "data": os.path.expanduser(os.path.join("~", ".passgen")),
        },
        "Darwin": {
            "cache": os.path.expanduser(os.path.join("~", "Library", "Caches", "passgen")),
            "config": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passgen")),
            "data": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passgen")),
        },
        "Linux": {
            "cache": os.path.expandvars(os.path.join("$XDG_CACHE_HOME", "passgen")),
            "config": os.path.expandvars(os.path.join("$XDG_CONFIG_HOME", "passgen")),
            "data": os.path.expandvars(os.path.join("$XDG_DATA_HOME", "passgen")),
        }
    }

__default_algorithm__: str = "playfair"
__default_shift__: str = "3"
__default_multiplier__: str = "3"
__default_encrypted__: str = "false"


def setup_xdg_variables() -> None:
    if __xdg_cache_home__ is None:
        os.environ["XDG_CACHE_HOME"] = os.path.expanduser("~/.cache")
    if __xdg_config_home__ is None:
        os.environ["XDG_CONFIG_HOME"] = os.path.expanduser("~/.config")
    if __xdg_data_home__ is None:
        os.environ["XDG_DATA_HOME"] = os.path.expanduser("~/.local/share")


def setup_paths(platform_name) -> dict[str, str]:
    if platform_name not in __paths__:
        raise Exception("Unsupported platform")
    return __paths__[platform_name]


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
    if not settings.get_key(settings.__encryption_method__, settings.__algorithm__):
        settings.set_key(settings.__encryption_method__, settings.__algorithm__, __default_algorithm__)
    if not settings.get_key(settings.__encryption_method__, settings.__shift__):
        settings.set_key(settings.__encryption_method__, settings.__shift__, __default_shift__)
    if not settings.get_key(settings.__encryption_method__, settings.__multiplier__):
        settings.set_key(settings.__encryption_method__, settings.__multiplier__, __default_multiplier__)
    if not settings.get_key(settings.__history__, settings.__encrypted__):
        settings.set_key(settings.__history__, settings.__encrypted__, __default_encrypted__)


def _init_generator() -> None:
    generator.algorithm = settings.get_key(settings.__encryption_method__, key=settings.__algorithm__)
    generator.shift = int(settings.get_key(settings.__encryption_method__, key=settings.__shift__))
    generator.multiplier = int(settings.get_key(settings.__encryption_method__, key=settings.__multiplier__))
    for key, value in settings.get_settings(settings.__characters_replacements__).items():
        generator.replace_character(key, value)


def init_configurations() -> None:
    _init_files()
    _init_settings()
    _init_generator()
