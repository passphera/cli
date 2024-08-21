import json
import os
from datetime import datetime


__history__: list[dict[str, str]] = []
__file__: str | None = None


def configure(path: str) -> None:
    global __file__
    __file__ = os.path.join(path)
    load_history()


def load_history() -> None:
    global __history__
    if __file__ and os.path.exists(__file__):
        with open(__file__, "r") as f:
            try:
                __history__ = json.load(f)
            except json.JSONDecodeError:
                __history__ = []
    else:
        __history__ = []


def save_history() -> None:
    if __file__:
        with open(__file__, "w") as f:
            json.dump(__history__, f, indent=4)


def add_to_history(password: str, text: str, key: str, context: str) -> None:
    entry = {
        "context": context,
        "text": text,
        "key": key,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    existing_entry = get_password(context)
    if existing_entry is not None:
        update_password(entry)
    else:
        __history__.append(entry)
    save_history()


def get_password(context: str) -> dict[str, str] | None:
    for entry in __history__:
        if entry['context'] == context:
            return entry
    return None


def update_password(password: dict[str, str]) -> None:
    for entry in __history__:
        if entry["context"] == password["context"]:
            entry["text"] = password['text']
            entry["key"] = password["key"]
            entry["password"] = password["password"]
    save_history()


def remove_password(context: str) -> bool:
    for entry in __history__:
        if entry['context'] == context:
            __history__.remove(entry)
            save_history()
            return True
    return False


def clear_history() -> None:
    __history__.clear()
    save_history()
