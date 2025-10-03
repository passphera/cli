import requests

from app.core import constants, settings
from app.core.decorators import handle_exception_decorator, require_authenticated, require_unauthenticated
from app.core.dependencies import auth


@handle_exception_decorator("failed to login")
@require_unauthenticated
def login(email: str, password: str) -> None:
    data = {
        "username": email,
        "password": password,
    }
    response = requests.post(f"{constants.ENDPOINT}/auth/login", data=data)
    response.raise_for_status()
    settings.set_key(constants.AUTH, constants.ACCESS_TOKEN, response.json()['access_token'])


@handle_exception_decorator("failed to logout")
@require_authenticated
def logout() -> None:
    settings.delete_key(constants.AUTH, constants.ACCESS_TOKEN)


@handle_exception_decorator("failed to signup")
@require_unauthenticated
def signup(email: str, username: str, password: str) -> None:
    data = {
        "email": email,
        "username": username,
        "password": password,
        "re_password": password,
    }
    response = requests.post(f"{constants.ENDPOINT}/auth/sign-up", json=data)
    response.raise_for_status()


@handle_exception_decorator("failed to get user")
@require_authenticated
def get_auth_user() -> dict[str, str]:
    response = requests.get(f"{constants.ENDPOINT}/auth/users/me", headers=auth.get_auth_header())
    response.raise_for_status()
    return response.json()['user']
