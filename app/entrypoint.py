from app.core import config
from app.cli.main import app


def main() -> None:
    config.init_configurations()
    app()


if __name__ == "__main__":
    main()
