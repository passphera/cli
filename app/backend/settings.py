import requests

from app.backend import auth
from app.core import config, settings


def get_shift() -> int:
    return config.generator.shift


def change_shift(amount: int) -> None:
    if auth.is_authenticated():
        data = {
            'shift': amount
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = amount
    settings.set_key(settings.__encryption_method__, settings.__shift__, str(amount))


def reset_shift() -> None:
    if auth.is_authenticated():
        data = {
            'shift': config.DEFAULT_SHIFT
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = config.DEFAULT_SHIFT
    settings.set_key(settings.__encryption_method__, settings.__shift__, config.DEFAULT_SHIFT)


def get_multiplier() -> int:
    return config.generator.multiplier


def change_multiplier(value: int) -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': value
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.multiplier = value
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, str(value))


def reset_multiplier() -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': config.DEFAULT_MULTIPLIER
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = config.DEFAULT_MULTIPLIER
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, config.DEFAULT_MULTIPLIER)


def get_key() -> str:
    return config.generator.key


def change_key(key: str) -> None:
    if auth.is_authenticated():
        data = {
            'key': key
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = key
    settings.set_key(settings.__encryption_method__, settings.__key__, key)


def reset_key() -> None:
    if auth.is_authenticated():
        data = {
            'key': config.DEFAULT_KEY
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = config.DEFAULT_KEY
    settings.set_key(settings.__encryption_method__, settings.__key__, config.DEFAULT_KEY)


def get_prefix() -> str:
    return config.generator.prefix


def change_prefix(prefix: str) -> None:
    if auth.is_authenticated():
        data = {
            'prefix': prefix
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = prefix
    settings.set_key(settings.__encryption_method__, settings.__prefix__, prefix)


def reset_prefix() -> None:
    if auth.is_authenticated():
        data = {
            'prefix': config.DEFAULT_PREFIX
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = config.DEFAULT_PREFIX
    settings.set_key(settings.__encryption_method__, settings.__prefix__, config.DEFAULT_PREFIX)


def get_postfix() -> str:
    return config.generator.postfix


def change_postfix(postfix: str) -> None:
    if auth.is_authenticated():
        data = {
            'postfix': postfix
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.postfix = postfix
    settings.set_key(settings.__encryption_method__, settings.__postfix__, postfix)


def reset_postfix() -> None:
    if auth.is_authenticated():
        data = {
            'postfix': config.DEFAULT_POSTFIX
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.postfix = config.DEFAULT_POSTFIX
    settings.set_key(settings.__encryption_method__, settings.__postfix__, config.DEFAULT_POSTFIX)


def get_algorithm() -> str:
    return config.generator.algorithm


def change_algorithm(algorithm_name: str) -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': algorithm_name
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = algorithm_name
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, algorithm_name)


def reset_algorithm() -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': config.DEFAULT_ALGORITHM
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = config.DEFAULT_ALGORITHM
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, config.DEFAULT_ALGORITHM)


def get_characters_replacements() -> dict[str, str]:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/generators/", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['characters_replacements']
    return settings.get_settings(settings.__characters_replacements__)


def replace_character(character: str, replacement: str) -> None:
    if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
        raise ValueError
    if auth.is_authenticated():
        params = {
            'character': character,
            'replacement': replacement,
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators/replace-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.replace_character(character, replacement)
    settings.set_key(settings.__characters_replacements__, character, replacement)


def reset_replacement(character: str) -> None:
    if auth.is_authenticated():
        params = {
            'character': character,
        }
        response = requests.patch(
            f"{config.ENDPOINT}/generators/reset-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.reset_character(character)
    settings.set_key(settings.__characters_replacements__, character, character)
