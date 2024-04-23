import logging


__logger__ = None


def configure(path):
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
            print(f"Error configuring logger: {e}")


def get_instance():
    if __logger__ is None:
        raise RuntimeError("Logger not configured. Call configure() first.")
    return __logger__


def log_info(message):
    get_instance().info(message)


def log_warning(message):
    get_instance().warning(message)


def log_error(message):
    get_instance().error(message)
