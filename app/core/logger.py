import logging

from app.core import interface

__logger__: logging.Logger | None = None


def configure(path: str) -> None:
    global __logger__
    if __logger__ is None:
        try:
            __logger__ = logging.getLogger(__name__)
            __logger__.setLevel(logging.INFO)

            formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

            file_handler = logging.FileHandler(path)
            file_handler.setFormatter(formatter)

            __logger__.addHandler(file_handler)
        except Exception as e:
            interface.display_error(f"Error configuring logger: {e}")


def get_instance() -> logging.Logger:
    if __logger__ is None:
        raise RuntimeError("Logger not configured. Call configure() first.")
    return __logger__


def log_info(message: str) -> None:
    get_instance().info(message)


def log_warning(message: str) -> None:
    get_instance().warning(message)


def log_error(message: str) -> None:
    get_instance().error(message)
