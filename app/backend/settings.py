from passphera_core import InvalidAlgorithmException

from app.core import config, settings


def change_algorithm(algorithm_name: str) -> None:
    try:
        config.generator.algorithm = algorithm_name
        settings.set_key(settings.__encryption_method__, settings.__algorithm__, algorithm_name)
    except InvalidAlgorithmException:
        raise InvalidAlgorithmException(algorithm_name)


def reset_algorithm() -> None:
    config.generator.algorithm = config.__default_algorithm__
    settings.set_key(settings.__encryption_method__, settings.__algorithm__, config.__default_algorithm__)


def change_shift(amount: int) -> None:
    config.generator.shift = amount
    settings.set_key(settings.__encryption_method__, settings.__shift__, str(amount))


def reset_shift() -> None:
    config.generator.shift = config.__default_shift__
    settings.set_key(settings.__encryption_method__, settings.__shift__, config.__default_shift__)


def change_multiplier(value: int) -> None:
    config.generator.multiplier = value
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, str(value))


def reset_multiplier() -> None:
    config.generator.shift = config.__default_multiplier__
    settings.set_key(settings.__encryption_method__, settings.__multiplier__, config.__default_multiplier__)


def change_cipher_key(new_key: str) -> None:
    config.generator.key = new_key
    settings.set_key(settings.__encryption_method__, settings.__key__, new_key)


def reset_cipher_key() -> None:
    config.generator.key = config.__default_key__
    settings.set_key(settings.__encryption_method__, settings.__key__, config.__default_key__)


def replace_character(replacement: str, character: str) -> None:
    if replacement in ['`', '~', '#', '%', '&', '*', '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
        raise ValueError
    config.generator.replace_character(character, replacement)
    settings.set_key(settings.__characters_replacements__, character, replacement)


def reset_replacement(character: str) -> None:
    config.generator.reset_character(character)
    settings.set_key(settings.__characters_replacements__, character, character)


def show_character_replacement(character: str) -> str:
    return settings.get_key(settings.__characters_replacements__, character)


def show_all_characters_replacements() -> dict[str, str]:
    return settings.get_settings(settings.__characters_replacements__)
