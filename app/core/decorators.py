from functools import wraps

import typer

import requests

from app.core import constants, settings


def _validate_token() -> bool:
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

def _is_authenticated() -> bool:
    if _validate_token():
        return settings.get_key(constants.AUTH, constants.ACCESS_TOKEN) is not None
    settings.delete_key(constants.AUTH, constants.ACCESS_TOKEN)
    return False


def require_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.core.functions import handle_error
        if not _is_authenticated():
            handle_error("You are not authenticated. Please use 'passphera auth login' to authenticate.")
            raise typer.Exit(code=1)
        return func(*args, **kwargs)
    return wrapper


def require_unauthenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.core.functions import handle_error
        if _is_authenticated():
            handle_error("You are already authenticated. Please use 'passphera auth logout' to logout.")
            raise typer.Exit(code=1)
        return func(*args, **kwargs)
    return wrapper


def handle_exception_decorator(error_message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                from app.core.functions import handle_error
                handle_error(f"{error_message}: {e}")
                raise typer.Exit(code=1)
        return wrapper
    return decorator
