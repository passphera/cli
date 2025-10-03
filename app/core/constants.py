from dataclasses import dataclass


@dataclass(frozen=True)
class AppMetadata:
    NAME: str = "passphera"
    VERSION: str = "2.0.0"
    AUTHOR: str = "Fathi Abdelmalek"
    AUTHOR_EMAIL: str = "passphera@imfathi.com"
    URL: str = "https://passphera.imfathi.com"
    LICENSE: str = "Apache-2.0"
    COPYRIGHT: str = "© 2025, Fathi Abdelmalek"
    DESCRIPTION: str = "Strong passwords generator and manager"


APP = AppMetadata()


DEFAULT_SHIFT: str = "3"
DEFAULT_MULTIPLIER: str = "3"
DEFAULT_KEY: str = "hill"
DEFAULT_ALGORITHM: str = "hill"
DEFAULT_PREFIX: str = "prefix"
DEFAULT_POSTFIX: str = "postfix"
TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

ENDPOINT: str = 'https://api.passphera.imfathi.com/api/v2'

AUTH: str = "Authentication"
ENCRYPTION_METHOD: str = "Encryption Method"
CHARACTERS_REPLACEMENTS: str = "Characters Replacements"

ACCESS_TOKEN: str = "access-token"
SHIFT: str = "shift-amount"
MULTIPLIER: str = "multiplier-amount"
KEY: str = "cipher-key"
PREFIX: str = "prefix"
POSTFIX: str = "postfix"
ALGORITHM: str = "primary-algorithm"
