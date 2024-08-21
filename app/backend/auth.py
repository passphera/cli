import requests

from app.backend import logger
from app.core import config, settings


def signup(email: str, username: str, password: str) -> None:
    if settings.get_key(settings.__auth__, settings.__access_token__):
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
    logger.log_info("registered new user in the app server")


def login(email: str, password: str) -> None:
    if settings.get_key(settings.__auth__, settings.__access_token__):
        raise Exception("Already logged in")
    data = {
        "username": email,
        "password": password,
    }
    response = requests.post(f"{config.ENDPOINT}/auth/login", data=data)
    if response.status_code != 200:
        raise Exception("Invalid credentials")
    print(response.json())
    settings.set_key(settings.__auth__, settings.__access_token__, response.json()['access_token'])
    logger.log_info(f"logged in with user email {email}")


def logout() -> None:
    if not settings.get_key(settings.__auth__, settings.__access_token__):
        raise Exception("Already logged out")
    settings.delete_key(settings.__auth__, settings.__access_token__)
    logger.log_info("logged out user")
