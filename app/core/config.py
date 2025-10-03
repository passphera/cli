import os
import platform
from datetime import datetime as dt

from app.core import constants, logger, repositories, settings
from app.core.interface import Interface, Messages


def setup_xdg_variables() -> None:
    os.environ.setdefault("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    os.environ.setdefault("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    os.environ.setdefault("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))


def setup_paths(platform_name: str) -> dict[str, str]:
    paths: dict[str, dict[str, str]] = {
        "Linux": {
            "cache": os.path.join(os.path.expandvars("$XDG_CACHE_HOME"), "passphera"),
            "config": os.path.join(os.path.expandvars("$XDG_CONFIG_HOME"), "passphera"),
            "data": os.path.join(os.path.expandvars("$XDG_DATA_HOME"), "passphera"),
        },
        "Windows": {
            "cache": os.path.expanduser(os.path.join("~", ".passphera")),
            "config": os.path.expanduser(os.path.join("~", ".passphera")),
            "data": os.path.expanduser(os.path.join("~", ".passphera")),
        },
        "Darwin": {
            "cache": os.path.expanduser(os.path.join("~", "Library", "Caches", "passphera")),
            "config": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passphera")),
            "data": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passphera")),
        },
    }
    if platform_name not in paths:
        raise RuntimeError(f"Unsupported platform: {platform_name}")
    return paths[platform_name]

def create_dirs(paths: dict[str, str]) -> None:
    for path in paths.values():
        os.makedirs(path, exist_ok=True)


def init_configurations() -> None:
    try:
        platform_name = platform.system()
        if platform_name == "Linux":
            setup_xdg_variables()
        paths = setup_paths(platform_name)
        create_dirs(paths)

        repositories.configure(os.path.join(paths["data"], ".vault"))
        logger.configure(os.path.join(paths["cache"], f"log_{dt.now().strftime('%Y-%m-%d')}.log"))
        settings.configure(os.path.join(paths["config"], "config.ini"))

        settings.set_section(constants.AUTH)
        settings.save_settings()
    except Exception as e:
        if os.environ.get("PASSPHERA_DEBUG"):
            raise
        Interface.display_message(str(Messages.error(str(e))), title="error", style="error")
