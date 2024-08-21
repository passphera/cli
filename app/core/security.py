from app.backend import settings


def is_authenticated() -> bool:
    return settings.get_key(settings.__auth__, settings.__access_token__) is not None


def store_access_token(access_token: str | None) -> None:
    settings.set_key(settings.__auth__, settings.__access_token__, access_token)


def destroy_access_token() -> None:
    settings.delete_key(settings.__auth__, settings.__access_token__)


def with_header() -> dict:
    return {'Authorization': f'Bearer {settings.get_key(settings.__auth__, settings.__access_token__)}'}
