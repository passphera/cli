from app.core import constants, settings


class AuthDependency:
    def get_auth_header(self) -> dict[str, str]:
        return {
            'accept': 'application/json',
            'Authorization': f'Bearer {settings.get_key(constants.AUTH, constants.ACCESS_TOKEN)}',
        }


auth = AuthDependency()
