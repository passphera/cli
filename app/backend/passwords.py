from app.backend import history
from app.core.config import generator


def generate_password(text: str, context: str = '') -> str:
    password = generator.generate_password(text)
    if context != '':
        history.add_to_history(text, context, password)
    return password


def update_password(context: str, text: str) -> str:
    password = generator.generate_password(text)
    history.update_password(text, context, password)
    return password


def delete_password(context: str) -> dict[str, str]:
    password: dict[str, str] | None = history.get_password(context)
    if not history.remove_password(context):
        raise Exception
    return password
