import requests

from passphera_core.application.password import (
    GeneratePasswordUseCase,
    GetPasswordUseCase,
    UpdatePasswordUseCase,
    DeletePasswordUseCase,
    ListPasswordsUseCase,
    FlushPasswordsUseCase,
)
from passphera_core.entities import Password

from app.core import constants
from app.core.decorators import require_authenticated, handle_exception_decorator
from app.core.dependencies import auth
from app.core.repositories import TinyDBVaultRepository, TinyDBGeneratorRepository


# @handle_exception_decorator("failed to save password")
def add_password(context: str, text: str) -> dict[str, str]:
    return (GeneratePasswordUseCase(TinyDBVaultRepository(), TinyDBGeneratorRepository())
            (context=context, text=text).to_dict())


@handle_exception_decorator("failed to get password")
def get_password(context: str) -> dict[str, str]:
    return GetPasswordUseCase(TinyDBVaultRepository())(context=context).to_dict()


@handle_exception_decorator("failed to update password")
def update_password(context: str, text: str) -> dict[str, str]:
    return UpdatePasswordUseCase(TinyDBVaultRepository(), TinyDBGeneratorRepository())(context=context, text=text).to_dict()


@handle_exception_decorator("failed to delete password")
def delete_password(context: str) -> dict[str, str]:
    password: dict[str, str] = get_password(context)
    DeletePasswordUseCase(TinyDBVaultRepository())(context=context)
    return password


@handle_exception_decorator("failed to get passwords")
def list_passwords() -> list[dict[str, str]]:
    passwords: list[Password] = ListPasswordsUseCase(TinyDBVaultRepository())()
    passwords_list: list[dict[str, str]] = []
    for password in passwords:
        passwords_list.append(password.to_dict())
    return passwords_list


@handle_exception_decorator("failed to flush database")
def flush_vault() -> None:
    return FlushPasswordsUseCase(TinyDBVaultRepository())()


@handle_exception_decorator("failed to sync vault")
@require_authenticated
def sync_vault():
    endpoint = f"{constants.ENDPOINT}/vault/sync"
    try:
        response = requests.post(endpoint, headers=auth.get_auth_header())
        response.raise_for_status()
        data = response.json()
        return data['local_passwords_list'], data['updated_local'], data['updated_server']
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to sync vault: {e}") from e
