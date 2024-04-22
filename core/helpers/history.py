import json
import os
from datetime import datetime


class History:
    _history = []
    _file = None

    @classmethod
    def configure(cls, path):
        cls._file = os.path.join(path)
        cls.load_history()

    @classmethod
    def load_history(cls):
        if cls._file and os.path.exists(cls._file):
            with open(cls._file, "r") as f:
                try:
                    cls._history = json.load(f)
                except json.JSONDecodeError:
                    cls._history = []
        else:
            cls._history = []

    @classmethod
    def save_history(cls):
        if cls._file:
            with open(cls._file, "w") as f:
                json.dump(cls._history, f, indent=4)

    @classmethod
    def add_to_history(cls, text, key, password, context):
        entry = {
            "text": text,
            "context": context,
            "key": key,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        existing_entry = cls.get_password(context)
        if existing_entry:
            cls._history[existing_entry] = entry
        else:
            cls._history.append(entry)
        cls.save_history()

    @classmethod
    def get_password(cls, context):
        for entry in cls._history:
            if entry['context'] == context:
                return entry
        return None

    @classmethod
    def update_password(cls, context, text, key, password):
        for entry in cls._history:
            if entry['context'] == context:
                entry['text'] = text
                entry['key'] = key
                entry['password'] = password
        cls.save_history()

    @classmethod
    def remove_password(cls, context):
        for entry in cls._history:
            if entry['context'] == context:
                cls._history.remove(entry)
                cls.save_history()
                return True
        return False

    @classmethod
    def clear_history(cls):
        cls._history.clear()
        cls.save_history()
