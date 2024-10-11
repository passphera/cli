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
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = amount
    settings.set_key(settings.ENCRYPTION_METHOD, settings.SHIFT, str(amount))


def reset_shift() -> None:
    if auth.is_authenticated():
        data = {
            'shift': config.DEFAULT_SHIFT
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = config.DEFAULT_SHIFT
    settings.set_key(settings.ENCRYPTION_METHOD, settings.SHIFT, config.DEFAULT_SHIFT)


def get_multiplier() -> int:
    return config.generator.multiplier


def change_multiplier(value: int) -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': value
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.multiplier = value
    settings.set_key(settings.ENCRYPTION_METHOD, settings.MULTIPLIER, str(value))


def reset_multiplier() -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': config.DEFAULT_MULTIPLIER
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = config.DEFAULT_MULTIPLIER
    settings.set_key(settings.ENCRYPTION_METHOD, settings.MULTIPLIER, config.DEFAULT_MULTIPLIER)


def get_key() -> str:
    return config.generator.key


def change_key(key: str) -> None:
    if auth.is_authenticated():
        data = {
            'key': key
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = key
    settings.set_key(settings.ENCRYPTION_METHOD, settings.KEY, key)


def reset_key() -> None:
    if auth.is_authenticated():
        data = {
            'key': config.DEFAULT_KEY
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = config.DEFAULT_KEY
    settings.set_key(settings.ENCRYPTION_METHOD, settings.KEY, config.DEFAULT_KEY)


def get_prefix() -> str:
    return config.generator.prefix


def change_prefix(prefix: str) -> None:
    if auth.is_authenticated():
        data = {
            'prefix': prefix
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = prefix
    settings.set_key(settings.ENCRYPTION_METHOD, settings.PREFIX, prefix)


def reset_prefix() -> None:
    if auth.is_authenticated():
        data = {
            'prefix': config.DEFAULT_PREFIX
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = config.DEFAULT_PREFIX
    settings.set_key(settings.ENCRYPTION_METHOD, settings.PREFIX, config.DEFAULT_PREFIX)


def get_postfix() -> str:
    return config.generator.postfix


def change_postfix(postfix: str) -> None:
    if auth.is_authenticated():
        data = {
            'postfix': postfix
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.postfix = postfix
    settings.set_key(settings.ENCRYPTION_METHOD, settings.POSTFIX, postfix)


def reset_postfix() -> None:
    if auth.is_authenticated():
        data = {
            'postfix': config.DEFAULT_POSTFIX
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.postfix = config.DEFAULT_POSTFIX
    settings.set_key(settings.ENCRYPTION_METHOD, settings.POSTFIX, config.DEFAULT_POSTFIX)


def get_algorithm() -> str:
    return config.generator.algorithm


def change_algorithm(algorithm_name: str) -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': algorithm_name
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = algorithm_name
    settings.set_key(settings.ENCRYPTION_METHOD, settings.ALGORITHM, algorithm_name)


def reset_algorithm() -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': config.DEFAULT_ALGORITHM
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = config.DEFAULT_ALGORITHM
    settings.set_key(settings.ENCRYPTION_METHOD, settings.ALGORITHM, config.DEFAULT_ALGORITHM)


def get_characters_replacements() -> dict[str, str]:
    if auth.is_authenticated():
        response = requests.get(f"{config.ENDPOINT}/generator/", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['characters_replacements']
    return settings.get_settings(settings.CHARACTERS_REPLACEMENTS)


def replace_character(character: str, replacement: str) -> None:
    if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
        raise ValueError
    if auth.is_authenticated():
        params = {
            'character': character,
            'replacement': replacement,
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator/replace-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.replace_character(character, replacement)
    settings.set_key(settings.CHARACTERS_REPLACEMENTS, character, replacement)


def reset_replacement(character: str) -> None:
    if auth.is_authenticated():
        params = {
            'character': character,
        }
        response = requests.put(
            f"{config.ENDPOINT}/generator/reset-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.reset_character(character)
    settings.set_key(settings.CHARACTERS_REPLACEMENTS, character, character)


def sync() -> None:
    if not auth.is_authenticated():
        raise Exception('You should login first')
    try:
        response = requests.get(f"{config.ENDPOINT}/generator", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        shift = str(response.json()['shift'])
        multiplier = str(response.json()['multiplier'])
        key = str(response.json()['key'])
        prefix = str(response.json()['prefix'])
        postfix = str(response.json()['postfix'])
        algorithm = str(response.json()['algorithm'])
        config.generator.shift = int(shift)
        settings.set_key(settings.ENCRYPTION_METHOD, settings.SHIFT, shift)
        config.generator.multiplier = int(multiplier)
        settings.set_key(settings.ENCRYPTION_METHOD, settings.MULTIPLIER, multiplier)
        config.generator.key = key
        settings.set_key(settings.ENCRYPTION_METHOD, settings.KEY, key)
        config.generator.prefix = prefix
        settings.set_key(settings.ENCRYPTION_METHOD, settings.PREFIX, prefix)
        config.generator.postfix = postfix
        settings.set_key(settings.ENCRYPTION_METHOD, settings.POSTFIX, postfix)
        config.generator.algorithm = algorithm
        settings.set_key(settings.ENCRYPTION_METHOD, settings.ALGORITHM, algorithm)
        for character in response.json()['characters_replacements']:
            replacement = response.json()['characters_replacements'][character]
            config.generator.replace_character(character, replacement)
            settings.set_key(settings.CHARACTERS_REPLACEMENTS, character, replacement)
    except requests.RequestException as e:
        raise Exception(f'Error fetching server settings: {str(e)}')
