import requests

from app.backend import auth, history
from app.core import config
from app.core.config import generator


def generate_password(text: str, key: str = '', context: str = '') -> str:
    generator.text = text
    if key != '':
        generator.key = key
    if auth.is_authenticated() and context != '':
        data = {
            "text": text,
            "context": context,
        }
        response = requests.post(f"{config.ENDPOINT}/passwords", json=data, headers=auth.get_auth_header())
        if response.status_code != 201:
            raise Exception(response.text)
        return response.json()['password']
    return generator.generate_password()


def update_password(text: str, key: str, context: str) -> str:
    generator.text = text
    generator.key_str = key
    password = generator.generate_password()
    history.add_to_history(password, text, key, context)
    return password


def delete_password(context: str) -> dict[str, str]:
    entry: dict[str, str] | None = history.get_password(context)
    if not history.remove_password(context):
        raise Exception
    return entry
