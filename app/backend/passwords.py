from app.backend import vault
from app.core.config import generator


def generate_password(text: str, context: str = '') -> str:
    password = generator.generate_password(text)
    if context != '':
        vault.add_to_db(text, context, password)
    return password


def update_password(context: str, text: str) -> str:
    password = generator.generate_password(text)
    vault.update_password(text, context, password)
    return password


def delete_password(context: str) -> dict[str, str]:
    password: dict[str, str] | None = vault.get_password(context)
    print(password)
    if not vault.delete_password(context):
        raise Exception
    return password
