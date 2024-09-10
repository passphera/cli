import json
import os
from datetime import datetime

import requests

from app.backend import auth
from app.core import config


HISTORY: list[dict[str, str]] = []
FILE: str | None = None


def configure(path: str) -> None:
    global FILE
    FILE = os.path.join(path)
    load_history()


def load_history() -> None:
    global HISTORY
    if FILE and os.path.exists(FILE):
        with open(FILE, "r") as f:
            try:
                HISTORY = json.load(f)
            except json.JSONDecodeError:
                HISTORY = []
    else:
        HISTORY = []


def save_history() -> None:
    if FILE:
        with open(FILE, "w") as f:
            json.dump(HISTORY, f, indent=4)


def add_to_history(text: str, context: str, password: str) -> None:
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
    HISTORY.append(data)
    save_history()


def get_password(context: str) -> dict[str, str] | None:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()
    for entry in HISTORY:
        if entry['context'] == context:
            return entry
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
    for entry in HISTORY:
        if entry["context"] == context:
            entry["text"] = text
            entry["password"] = password
            entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_history()


def remove_password(context: str) -> bool:
    if auth.is_authenticated():
        response = requests.delete(f"{config.ENDPOINT}/passwords/{context}", headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    for entry in HISTORY:
        if entry['context'] == context:
            HISTORY.remove(entry)
            save_history()
            return True
    return False


def clear_history() -> None:
    if auth.is_authenticated():
        response = requests.delete(f"{config.ENDPOINT}/passwords", headers=auth.get_auth_header())
        if response.status_code != 204:
            raise Exception(response.text)
    HISTORY.clear()
    save_history()
