import base64
from datetime import datetime, UTC

import requests
from tinydb import TinyDB, Query

from app.backend import auth
from app.core.config import generator
from app.core import constants
from app.core.security import derive_key, decrypt_password


db: TinyDB
Password: Query = Query()


def configure(path: str) -> None:
    global db
    db = TinyDB(path)
    db.default_table_name = 'passwords'


def add_to_db(text: str, context: str, password: str, salt: bytes) -> None:
    data = {
        'context': context,
        'text': text,
        'created_at': datetime.now(UTC).strftime(constants.TIME_FORMAT),
        'updated_at': datetime.now(UTC).strftime(constants.TIME_FORMAT),
        'password': password,
        'salt': base64.b64encode(salt).decode('utf-8'),
    }
    db.insert(data)


def get_password(context: str) -> dict[str, str] | None:
    passwords = db.search(Password.context == context)
    if passwords:
        password: dict[str, str] = passwords[0]
        generated_password = generator.generate_password(password['text'])
        encryption_key = derive_key(generated_password, base64.b64decode(password['salt']))
        decrypted_password = decrypt_password(password['password'], encryption_key)
        decrypted_entry = dict(password)
        decrypted_entry['password'] = decrypted_password
        return decrypted_entry
    return None


def get_passwords() -> list[dict[str, str]]:
    all_passwords: dict[str, dict[str, str]] = {}
    local_passwords = db.all()
    if local_passwords:
        for password in local_passwords:
            if password['context'] not in all_passwords:
                all_passwords[password['context']] = get_password(password['context'])
    return list(all_passwords.values())


def update_password(text: str, context: str, password: str) -> None:
    db.update({
        'text': text,
        'updated_at': datetime.now(UTC).strftime(constants.TIME_FORMAT),
        'password': password,
    }, Password.context == context)


def delete_password(context: str) -> bool:
    removed = db.remove(Password.context == context)
    return len(removed) > 0


def clear_db() -> None:
    db.truncate()


def sync() -> (int, int):
    if not auth.is_authenticated():
        raise Exception('You should login first')
    local_passwords = db.all()
    try:
        response = requests.get(f'{constants.ENDPOINT}/passwords', headers=auth.get_auth_header())
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
    local_updated = datetime.strptime(local_password['updated_at'], constants.TIME_FORMAT)
    server_updated = datetime.strptime(server_password['updated_at'], constants.TIME_FORMAT)
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
    response = requests.put(f'{constants.ENDPOINT}/passwords/{password['context']}', json=data,
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
    response = requests.post(f'{constants.ENDPOINT}/passwords', json=data, headers=auth.get_auth_header())
    if response.status_code != 201:
        raise Exception(response.text)


def _create_local_password(password: dict) -> None:
    db.insert(password)
