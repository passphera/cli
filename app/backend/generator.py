from uuid import UUID

import requests

from passphera_core.application.generator import Generator, GetGeneratorUseCase
from passphera_core.application.generator import (
    GetPropertiesUseCase,
    SetPropertyUseCase,
    ResetPropertyUseCase,
    SetCharacterReplacementUseCase,
    ResetCharacterReplacementUseCase
)

from app.core import constants
from app.core.dependencies import auth
from app.core.repositories import TinyDBGeneratorRepository
from app.core.decorators import require_authenticated, handle_exception_decorator


@handle_exception_decorator("failed to show generator settings")
def show_properties() -> dict:
    return GetPropertiesUseCase(TinyDBGeneratorRepository())()


@handle_exception_decorator("failed to set a new value to property")
def set_property(prop: str, value: str) -> Generator:
    return SetPropertyUseCase(TinyDBGeneratorRepository())(prop, value)


@handle_exception_decorator("failed to reset property to its default value")
def reset_property(prop: str) -> Generator:
    return ResetPropertyUseCase(TinyDBGeneratorRepository())(prop)


@handle_exception_decorator("failed to change character replacement")
def set_character_replacement(character: str, replacement: str) -> Generator:
    return SetCharacterReplacementUseCase(TinyDBGeneratorRepository())(character, replacement)


@handle_exception_decorator("failed to reset character replacement")
def reset_character_replacement(character: str) -> Generator:
    return ResetCharacterReplacementUseCase(TinyDBGeneratorRepository())(character)


# @handle_exception_decorator("failed to sync generator")
@require_authenticated
def sync_generator(way: str) -> None:
    if way not in ["up", "down"]:
        raise ValueError("Invalid way. Use 'up' or 'down'.")
    endpoint = f"{constants.ENDPOINT}/generator/sync-{way}"
    try:
        if way == "down":
            response = requests.post(endpoint, headers=auth.get_auth_header())
        else:
            generator: Generator = GetGeneratorUseCase(TinyDBGeneratorRepository())()
            payload = {
                "shift": generator.shift,
                "multiplier": generator.multiplier,
                "key": generator.key,
                "algorithm": generator.algorithm,
                "prefix": generator.prefix,
                "postfix": generator.postfix,
                "characters_replacements": generator.characters_replacements,
            }
            response = requests.put(endpoint, headers=auth.get_auth_header(), json=payload)
        response.raise_for_status()
        data = response.json()
        generator = data.get("generator")
        del generator["user_id"]
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to sync generator ({way}): {e}") from e
    if way == "down":
        generator_repository = TinyDBGeneratorRepository()

        for prop, value in generator.items():
            if prop == "characters_replacements":
                for character, replacement in value.items():
                    SetCharacterReplacementUseCase(generator_repository)(character, replacement)
            else:
                SetPropertyUseCase(generator_repository)(prop, value)
