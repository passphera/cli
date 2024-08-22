import requests

from app.core import config, settings


def is_authenticated() -> bool:
    return settings.get_key(settings.__auth__, settings.__access_token__) is not None


def signup(email: str, username: str, password: str) -> None:
    if is_authenticated():
        raise Exception("Cannot create new user while logged in")
    data = {
        "email": email,
        "username": username,
        "password": password,
        "re_password": password,
    }
    response = requests.post(f"{config.ENDPOINT}/auth/sign-up", json=data)
    if response.status_code == 400:
        if response.json().get("detail") == "Email already registered":
            raise Exception("Email already registered")
        elif response.json().get("detail") == "Username already registered":
            raise Exception("Username already registered")


def login(email: str, password: str) -> None:
    if is_authenticated():
        raise Exception("Already logged in")
    data = {
        "username": email,
        "password": password,
    }
    response = requests.post(f"{config.ENDPOINT}/auth/login", data=data)
    if response.status_code != 200:
        raise Exception("Invalid credentials")
    settings.set_key(settings.__auth__, settings.__access_token__, response.json()['access_token'])


def logout() -> None:
    if not is_authenticated():
        raise Exception("Already logged out")
    settings.delete_key(settings.__auth__, settings.__access_token__)


def get_auth_header() -> dict[str, str]:
    if not is_authenticated():
        raise Exception("Not logged in")
    return {'Authorization': f'Bearer {settings.get_key(settings.__auth__, settings.__access_token__)}'}
