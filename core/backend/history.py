import json
import os
from datetime import datetime


__history__ = []
__file__ = None


def configure(path):
    global __file__
    __file__ = os.path.join(path)
    load_history()


def load_history():
    global __history__
    if __file__ and os.path.exists(__file__):
        with open(__file__, "r") as f:
            try:
                __history__ = json.load(f)
            except json.JSONDecodeError:
                __history__ = []
    else:
        __history__ = []


def save_history():
    if __file__:
        with open(__file__, "w") as f:
            json.dump(__history__, f, indent=4)


def add_to_history(text, key, password, context):
    entry = {
        "text": text,
        "context": context,
        "key": key,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    existing_entry = get_password(context)
    if existing_entry:
        __history__[existing_entry] = entry
    else:
        __history__.append(entry)
    save_history()


def get_password(context):
    for entry in __history__:
        if entry['context'] == context:
            return entry
    return None


def update_password(context, text, key, password):
    for entry in __history__:
        if entry['context'] == context:
            entry['text'] = text
            entry['key'] = key
            entry['password'] = password
    save_history()


def remove_password(context):
    for entry in __history__:
        if entry['context'] == context:
            __history__.remove(entry)
            save_history()
            return True
    return False


def clear_history():
    __history__.clear()
    save_history()
