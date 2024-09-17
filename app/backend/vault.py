from datetime import datetime, UTC

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
        "context": context
    }
    if auth.is_authenticated():
        response = requests.post(f"{config.ENDPOINT}/passwords", json=data, headers=auth.get_auth_header())
        if response.status_code != 201:
            raise Exception(response.text)
        data['password'] = response.json().get("password")
    else:
        data['password'] = password
    data['created_at'] = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
    data['updated_at'] = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
    db.insert(data)


def get_password(context: str) -> dict[str, str]:
    password: dict[str, str]
    try:
        if auth.is_authenticated():
            response = requests.get(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
            if response.status_code != 200:
                raise ValueError
            return response.json()
    except ValueError:
        result = db.search(Password.context == context)
        if not result:
            raise ValueError
        return dict(result[0])


def get_passwords() -> list[dict[str, str]]:
    all_passwords: list[dict[str, str]] = []
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/passwords", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        all_passwords.extend(response.json())
    result = db.all()
    if result:
        all_passwords.extend(result)
    return all_passwords


def update_password(text: str, context: str, password: str) -> None:
    if auth.is_authenticated():
        data = {
            "text": text
        }
        response = requests.patch(f"{config.ENDPOINT}/passwords/{context}",
                                  json=data,
                                  headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
    db.update({
        "text": text,
        "password": password,
        "updated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
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


def sync() -> (int, int):
    if not auth.is_authenticated():
        raise Exception("You should login first")
    local_passwords = db.all()
    try:
        response = requests.get(f"{config.ENDPOINT}/passwords", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        server_passwords = response.json()
    except requests.RequestException as e:
        raise Exception(f"Error fetching server passwords: {str(e)}")
    updated_local = 0
    updated_server = 0
    for local_password in local_passwords:
        server_password = next((p for p in server_passwords if p['context'] == local_password['context']), None)
        if server_password:
            updated_local, updated_server = _update_password(local_password,
                                                             server_password,
                                                             updated_local,
                                                             updated_server)
        else:
            _create_server_password(local_password)
            updated_server += 1
    local_contexts = {p['context'] for p in local_passwords}
    for server_password in server_passwords:
        if server_password['context'] not in local_contexts:
            _create_local_password(server_password)
            updated_local += 1
    return updated_local, updated_server


def _update_password(local_password, server_password, updated_local, updated_server) -> (int, int):
    local_updated = datetime.strptime(local_password['updated_at'], "%Y-%m-%d %H:%M:%S")
    server_updated = datetime.strptime(server_password['updated_at'], "%Y-%m-%d %H:%M:%S")
    if local_updated < server_updated:
        _update_local_password(server_password)
        updated_local += 1
    elif local_updated > server_updated:
        _update_server_password(local_password)
        updated_server += 1
    return updated_local, updated_server


def _update_server_password(password: dict) -> None:
    data = {
        'text': password['text'],
        "password": password['password']
    }
    response = requests.patch(f"{config.ENDPOINT}/passwords/{password['context']}", json=data,
                              headers=auth.get_auth_header())
    if response.status_code != 200:
        raise Exception(response.text)


def _update_local_password(password: dict) -> None:
    db.update({
        "text": password['text'],
        "password": password['password']
    }, Password.context == password['context'])


def _create_server_password(password: dict) -> None:
    data = {
        "text": password['text'],
        "context": password['context'],
    }
    response = requests.post(f"{config.ENDPOINT}/passwords", json=data, headers=auth.get_auth_header())
    if response.status_code != 201:
        raise Exception(response.text)


def _create_local_password(password: dict) -> None:
    db.insert(password)
