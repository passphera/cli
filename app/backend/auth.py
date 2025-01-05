import requests

from app.core import constants, settings


def validate_token() -> bool:
    token = settings.get_key(constants.AUTH, constants.ACCESS_TOKEN)
    if not token:
        return False
    params = {
        "token": token,
    }
    try:
        response = requests.get(f"{constants.ENDPOINT}/auth/validate", params=params)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def is_authenticated() -> bool:
    if validate_token():
        return settings.get_key(constants.AUTH, constants.ACCESS_TOKEN) is not None
    settings.delete_key(constants.AUTH, constants.ACCESS_TOKEN)
    return False


def get_auth_header() -> dict[str, str]:
    if not is_authenticated():
        raise Exception("Not logged in")
    return {
        'accept': 'application/json',
        'Authorization': f'Bearer {settings.get_key(constants.AUTH, constants.ACCESS_TOKEN)}',
    }


def get_auth_user() -> dict[str, str]:
    if not is_authenticated():
        raise Exception("Not logged in")
    user = requests.get(f"{constants.ENDPOINT}/auth/users/me", headers=get_auth_header())
    return user.json()


def login(email: str, password: str) -> None:
    if is_authenticated():
        raise Exception("Already logged in")
    data = {
        "username": email,
        "password": password,
    }
    response = requests.post(f"{constants.ENDPOINT}/auth/login", data=data)
    if response.status_code != 200:
        raise Exception("Invalid credentials")
    settings.set_key(constants.AUTH, constants.ACCESS_TOKEN, response.json()['access_token'])


def logout() -> None:
    if not is_authenticated():
        raise Exception("Already logged out")
    settings.delete_key(constants.AUTH, constants.ACCESS_TOKEN)


def signup(email: str, username: str, password: str) -> None:
    if is_authenticated():
        raise Exception("Cannot create new user while logged in")
    data = {
        "email": email,
        "username": username,
        "password": password,
        "re_password": password,
    }
    response = requests.post(f"{constants.ENDPOINT}/auth/sign-up", json=data)
    if response.status_code == 400:
        if response.json().get("detail") == "Email already registered":
            raise Exception("Email already registered")
        elif response.json().get("detail") == "Username already registered":
            raise Exception("Username already registered")
