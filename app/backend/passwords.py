import requests

from app.backend import auth, history
from app.core import config
from app.core.config import generator


def generate_password(text: str, context: str = '') -> str:
    if auth.is_authenticated() and context != '':
        data = {
            "text": text,
            "context": context,
        }
        response = requests.post(f"{config.ENDPOINT}/passwords", json=data, headers=auth.get_auth_header())
        if response.status_code != 201:
            raise Exception(response.text)
        return response.json()['password']
    password = generator.generate_password(text)
    if context != '':
        history.add_to_history(context, text, password)
    return password


def update_password(context: str, text: str) -> str:
    if auth.is_authenticated():
        data = {
            "text": text,
        }
        response = requests.patch(f"{config.ENDPOINT}/passwords/{context}", json=data, headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['password']
    generator.text = text
    password = generator.generate_password(text)
    history.add_to_history(context, text, password)
    return password


def delete_password(context: str) -> dict[str, str]:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/passwords/{context}")
        if response.status_code != 200:
            raise Exception(response.text)
        entry: dict[str, str] = response.json()
        response = requests.delete(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
        return entry
    entry: dict[str, str] | None = history.get_password(context)
    if not history.remove_password(context):
        raise Exception
    return entry
