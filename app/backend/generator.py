from typing import Literal

import requests

from passphera_core.application.generator import Generator
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
from core.decorators import require_authenticated


def show_properties() -> dict:
    return GetPropertiesUseCase(TinyDBGeneratorRepository())()


def set_property(prop: str, value: str) -> Generator:
    return SetPropertyUseCase(TinyDBGeneratorRepository())(prop, value)


def reset_property(prop: str) -> Generator:
    return ResetPropertyUseCase(TinyDBGeneratorRepository())(prop)


def set_character_replacement(character: str, replacement: str) -> Generator:
    return SetCharacterReplacementUseCase(TinyDBGeneratorRepository())(character, replacement)


def reset_character_replacement(character: str) -> Generator:
    return ResetCharacterReplacementUseCase(TinyDBGeneratorRepository())(character)


@require_authenticated
def sync(way: Literal["up", "down"]) -> None:
    endpoint = f"{constants.ENDPOINT}/generator/sync_{way}"
    try:
        response = requests.post(endpoint, headers=auth.get_auth_header())
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to sync generator ({way}): {e}") from e
    if way == "down":
        generator_repository = TinyDBGeneratorRepository()

        for prop, value in data.items():
            if prop == "characters_replacements":
                for character, replacement in value.items():
                    SetCharacterReplacementUseCase(generator_repository)(character, replacement)
            else:
                SetPropertyUseCase(generator_repository)(prop, value)
