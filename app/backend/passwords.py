from app.backend import vault
from app.core.config import generator


def generate_password(text: str, context: str = '') -> str:
    if vault.get_password(context):
        raise Exception("Password already exists")
    password = generator.generate_password(text)
    if context != '':
        vault.add_to_db(text, context, password)
    return password


def update_password(context: str, text: str) -> str:
    if not vault.get_password(context):
        raise Exception("Password don't exist")
    password = generator.generate_password(text)
    vault.update_password(text, context, password)
    return password


def delete_password(context: str) -> dict[str, str]:
    password: dict[str, str] | None = vault.get_password(context)
    if not vault.delete_password(context):
        raise Exception("Password don't exist")
    return password
