from datetime import datetime, UTC

import requests
from tinydb import TinyDB, Query

from app.backend import auth
from app.core import config

db: TinyDB
Password: Query = Query()


def configure(path: str) -> None:
    global db
    db = TinyDB(path)
    db.default_table_name = 'passwords'


def add_to_db(text: str, context: str, password: str) -> None:
    data = {
        'context': context,
        'text': text,
    }
    if auth.is_authenticated():
        response = requests.post(f'{config.ENDPOINT}/passwords', json=data, headers=auth.get_auth_header())
        if response.status_code != 201:
            raise Exception(response.text)
        data['created_at'] = response.json().get('created_at')
        data['updated_at'] = response.json().get('updated_at')
    else:
        data['created_at'] = datetime.now(UTC).strftime(config.TIME_FORMAT)
        data['updated_at'] = datetime.now(UTC).strftime(config.TIME_FORMAT)
    data['password'] = password
    db.insert(data)


def get_password(context: str) -> dict[str, str] | None:
    password: dict[str, str]
    if auth.is_authenticated():
        response = requests.get(f'{config.ENDPOINT}/passwords/{context}', headers=auth.get_auth_header())
        if response.status_code == 200:
            return response.json()
    result = db.search(Password.context == context)
    if result:
        return dict(result[0])


def get_passwords() -> list[dict[str, str]]:
    all_passwords: dict[str, dict[str, str]] = {}
    if auth.is_authenticated():
        response = requests.get(f'{config.ENDPOINT}/passwords', headers=auth.get_auth_header())
        if response.status_code == 200:
            for password in response.json():
                all_passwords[password['context']] = password
    local_passwords = db.all()
    if local_passwords:
        for password in local_passwords:
            if password['context'] not in all_passwords:
                all_passwords[password['context']] = password
    return list(all_passwords.values())


def update_password(text: str, context: str, password: str) -> None:
    if auth.is_authenticated():
        data = {
            'text': text
        }
        response = requests.put(f'{config.ENDPOINT}/passwords/{context}',
                                  json=data,
                                  headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
    db.update({
        'text': text,
        'updated_at': datetime.now(UTC).strftime(config.TIME_FORMAT),
        'password': password,
    }, Password.context == context)


def delete_password(context: str) -> bool:
    if auth.is_authenticated():
        response = requests.delete(f'{config.ENDPOINT}/passwords/{context}', headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    db.remove(Password.context == context)
    return True


def clear_db() -> None:
    if auth.is_authenticated():
        response = requests.delete(f'{config.ENDPOINT}/passwords', headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    db.truncate()


def sync() -> (int, int):
    if not auth.is_authenticated():
        raise Exception('You should login first')
    local_passwords = db.all()
    try:
        response = requests.get(f'{config.ENDPOINT}/passwords', headers=auth.get_auth_header())
        if response.status_code != 200:
            raise requests.RequestException(response.text)
        server_passwords = response.json()
    except requests.RequestException as e:
        raise Exception(f'Error fetching server passwords: {str(e)}')
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
    local_updated = datetime.strptime(local_password['updated_at'], config.TIME_FORMAT)
    server_updated = datetime.strptime(server_password['updated_at'], config.TIME_FORMAT)
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
        'password': password['password'],
    }
    response = requests.put(f'{config.ENDPOINT}/passwords/{password['context']}', json=data,
                              headers=auth.get_auth_header())
    if response.status_code != 200:
        raise Exception(response.text)


def _update_local_password(password: dict) -> None:
    db.update({
        'text': password['text'],
        'updated_at': password['updated_at'],
        'password': password['password'],
    }, Password.context == password['context'])


def _create_server_password(password: dict) -> None:
    data = {
        'context': password['context'],
        'text': password['text'],
    }
    response = requests.post(f'{config.ENDPOINT}/passwords', json=data, headers=auth.get_auth_header())
    if response.status_code != 201:
        raise Exception(response.text)


def _create_local_password(password: dict) -> None:
    db.insert(password)
