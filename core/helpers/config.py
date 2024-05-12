import os

import typer

from passphera_core import PasswordGenerator

__version__ = '0.5.0'
__author__ = 'Fathi Abdelmalek'
__email__ = 'passphera@gmail.com'
__url__ = 'https://github.com/passphera/cli'
__status__ = 'Development'
__copyright__ = 'Copyright 2024, Fathi Abdelmalek'


__xdg_cache_home__ = os.environ.get("XDG_CACHE_HOME")
__xdg_config_home__ = os.environ.get("XDG_CONFIG_HOME")
__xdg_data_home__ = os.environ.get("XDG_DATA_HOME")
__paths__ = {
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


def setup_xdg_variables():
    if __xdg_cache_home__ is None:
        os.environ["XDG_CACHE_HOME"] = os.path.expanduser("~/.cache")
    if __xdg_config_home__ is None:
        os.environ["XDG_CONFIG_HOME"] = os.path.expanduser("~/.config")
    if __xdg_data_home__ is None:
        os.environ["XDG_DATA_HOME"] = os.path.expanduser("~/.local/share")


def setup_paths(platform_name):
    if platform_name not in __paths__:
        raise Exception("Unsupported platform")
    return __paths__[platform_name]


def create_dirs(paths):
    for path in paths.values():
        if not os.path.exists(path):
            os.makedirs(path)


def version_callback(value: bool):
    if value:
        print(typer.style(f"Version {__version__}", fg=typer.colors.CYAN, bold=True))
        raise typer.Exit()


generator = PasswordGenerator()
