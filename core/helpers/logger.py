import logging


class Logger:
    _logger = None

    @classmethod
    def configure(cls, log_file_path):
        if cls._logger is None:
            try:
                cls._logger = logging.getLogger(__name__)
                cls._logger.setLevel(logging.INFO)

                formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(formatter)

                cls._logger.addHandler(file_handler)
            except Exception as e:
                print(f"Error configuring logger: {e}")

    @classmethod
    def get_instance(cls):
        if cls._logger is None:
            raise RuntimeError("Logger not configured. Call configure() first.")
        return cls._logger

    @classmethod
    def log_info(cls, message):
        cls.get_instance().info(message)

    @classmethod
    def log_warning(cls, message):
        cls.get_instance().warning(message)

    @classmethod
    def log_error(cls, message):
        cls.get_instance().error(message)
