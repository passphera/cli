import requests

from app.backend import auth
from app.core import config, constants, settings


def get_shift() -> int:
    return config.generator.shift


def change_shift(amount: int) -> None:
    if auth.is_authenticated():
        data = {
            'shift': amount
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = amount
    settings.set_key(constants.ENCRYPTION_METHOD, constants.SHIFT, str(amount))


def reset_shift() -> None:
    if auth.is_authenticated():
        data = {
            'shift': constants.DEFAULT_SHIFT
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = constants.DEFAULT_SHIFT
    settings.set_key(constants.ENCRYPTION_METHOD, constants.SHIFT, constants.DEFAULT_SHIFT)


def get_multiplier() -> int:
    return config.generator.multiplier


def change_multiplier(value: int) -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': value
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.multiplier = value
    settings.set_key(constants.ENCRYPTION_METHOD, constants.MULTIPLIER, str(value))


def reset_multiplier() -> None:
    if auth.is_authenticated():
        data = {
            'multiplier': constants.DEFAULT_MULTIPLIER
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.shift = constants.DEFAULT_MULTIPLIER
    settings.set_key(constants.ENCRYPTION_METHOD, constants.MULTIPLIER, constants.DEFAULT_MULTIPLIER)


def get_key() -> str:
    return config.generator.key


def change_key(key: str) -> None:
    if auth.is_authenticated():
        data = {
            'key': key
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = key
    settings.set_key(constants.ENCRYPTION_METHOD, constants.KEY, key)


def reset_key() -> None:
    if auth.is_authenticated():
        data = {
            'key': constants.DEFAULT_KEY
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.key = constants.DEFAULT_KEY
    settings.set_key(constants.ENCRYPTION_METHOD, constants.KEY, constants.DEFAULT_KEY)


def get_prefix() -> str:
    return config.generator.prefix


def change_prefix(prefix: str) -> None:
    if auth.is_authenticated():
        data = {
            'prefix': prefix
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = prefix
    settings.set_key(constants.ENCRYPTION_METHOD, constants.PREFIX, prefix)


def reset_prefix() -> None:
    if auth.is_authenticated():
        data = {
            'prefix': constants.DEFAULT_PREFIX
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.prefix = constants.DEFAULT_PREFIX
    settings.set_key(constants.ENCRYPTION_METHOD, constants.PREFIX, constants.DEFAULT_PREFIX)


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
    settings.set_key(constants.ENCRYPTION_METHOD, constants.POSTFIX, postfix)


def reset_postfix() -> None:
    if auth.is_authenticated():
        data = {
            'postfix': constants.DEFAULT_POSTFIX
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.postfix = constants.DEFAULT_POSTFIX
    settings.set_key(constants.ENCRYPTION_METHOD, constants.POSTFIX, constants.DEFAULT_POSTFIX)


def get_algorithm() -> str:
    return config.generator.algorithm


def change_algorithm(algorithm_name: str) -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': algorithm_name
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = algorithm_name
    settings.set_key(constants.ENCRYPTION_METHOD, constants.ALGORITHM, algorithm_name)


def reset_algorithm() -> None:
    if auth.is_authenticated():
        data = {
            'algorithm': constants.DEFAULT_ALGORITHM
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator",
            json=data,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.algorithm = constants.DEFAULT_ALGORITHM
    settings.set_key(constants.ENCRYPTION_METHOD, constants.ALGORITHM, constants.DEFAULT_ALGORITHM)


def get_characters_replacements() -> dict[str, str]:
    if auth.is_authenticated():
        response = requests.get(f"{constants.ENDPOINT}/generator/", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['characters_replacements']
    return settings.get_settings(constants.CHARACTERS_REPLACEMENTS)


def replace_character(character: str, replacement: str) -> None:
    if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
        raise ValueError
    if auth.is_authenticated():
        params = {
            'character': character,
            'replacement': replacement,
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator/replace-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.replace_character(character, replacement)
    settings.set_key(constants.CHARACTERS_REPLACEMENTS, character, replacement)


def reset_replacement(character: str) -> None:
    if auth.is_authenticated():
        params = {
            'character': character,
        }
        response = requests.put(
            f"{constants.ENDPOINT}/generator/reset-character",
            params=params,
            headers=auth.get_auth_header()
        )
        if response.status_code != 200:
            raise Exception(response.text)
    config.generator.reset_character(character)
    settings.set_key(constants.CHARACTERS_REPLACEMENTS, character, character)


def sync() -> None:
    if not auth.is_authenticated():
        raise Exception('You should login first')
    try:
        response = requests.get(f"{constants.ENDPOINT}/generator", headers=auth.get_auth_header())
        if response.status_code != 200:
            raise Exception(response.text)
        shift = str(response.json()['shift'])
        multiplier = str(response.json()['multiplier'])
        key = str(response.json()['key'])
        prefix = str(response.json()['prefix'])
        postfix = str(response.json()['postfix'])
        algorithm = str(response.json()['algorithm'])
        config.generator.shift = int(shift)
        settings.set_key(constants.ENCRYPTION_METHOD, constants.SHIFT, shift)
        config.generator.multiplier = int(multiplier)
        settings.set_key(constants.ENCRYPTION_METHOD, constants.MULTIPLIER, multiplier)
        config.generator.key = key
        settings.set_key(constants.ENCRYPTION_METHOD, constants.KEY, key)
        config.generator.prefix = prefix
        settings.set_key(constants.ENCRYPTION_METHOD, constants.PREFIX, prefix)
        config.generator.postfix = postfix
        settings.set_key(constants.ENCRYPTION_METHOD, constants.POSTFIX, postfix)
        config.generator.algorithm = algorithm
        settings.set_key(constants.ENCRYPTION_METHOD, constants.ALGORITHM, algorithm)
        for character in response.json()['characters_replacements']:
            replacement = response.json()['characters_replacements'][character]
            config.generator.replace_character(character, replacement)
            settings.set_key(constants.CHARACTERS_REPLACEMENTS, character, replacement)
    except requests.RequestException as e:
        raise Exception(f'Error fetching server settings: {str(e)}')
