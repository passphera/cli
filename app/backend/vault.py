from datetime import datetime

import requests
from tinydb import TinyDB, Query

from app.backend import auth
from app.core import config
from app.core.storage import EncryptedStorage

db: TinyDB
Password: Query = Query()


def configure(path: str) -> None:
    global db
    db = TinyDB(path, storage=EncryptedStorage)
    db.default_table_name = 'passwords'


def add_to_db(text: str, context: str, password: str) -> None:
    data = {
        "text": text,
        "context": context,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if auth.is_authenticated():
        response = requests.post(f"{config.ENDPOINT}/passwords", json=data, headers=auth.get_auth_header())
        if response.status_code != 201:
            raise Exception(response.text)
        data['password'] = response.json().get("password")
    else:
        data['password'] = password
    db.insert(data)


def get_password(context: str) -> dict[str, str] | None:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()
    result = db.search(Password.context == context)
    if result:
        return result[0]
    return None


def get_passwords() -> list[dict[str, str]] | None:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/passwords", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()
    result = db.all()
    if result:
        return result
    return None


def update_password(text: str, context: str, password: str) -> None:
    if auth.is_authenticated():
        data = {
            "text": text,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        response = requests.patch(f"{config.ENDPOINT}/passwords/{context}",
                                  json=data,
                                  headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
    db.update({
        "text": text,
        "password": password,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, Password.context == context)


def remove_password(context: str) -> bool:
    if auth.is_authenticated():
        response = requests.delete(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    db.remove(Password.context == context)
    return True


def clear_db() -> None:
    if auth.is_authenticated():
        response = requests.delete(f"{config.ENDPOINT}/passwords", headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    db.truncate()


def sync() -> None:
    pass
