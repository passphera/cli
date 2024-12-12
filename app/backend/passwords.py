import base64

from app.backend import vault
from app.core.config import generator
from app.core.security import generate_salt, derive_key, encrypt_password


def generate_password(text: str, context: str = '') -> str:
    if vault.get_password(context):
        raise Exception("Password already exists")
    generated_password = generator.generate_password(text)
    salt: bytes = generate_salt()
    encryption_key = derive_key(generated_password, salt)
    encrypted_password = encrypt_password(generated_password, encryption_key)
    if context != '':
        vault.add_to_db(text, context, encrypted_password, salt)
    return generated_password


def update_password(context: str, text: str) -> str:
    db_password = vault.get_password(context)
    if not db_password:
        raise Exception("Password don't exist")
    generated_password = generator.generate_password(text)
    encryption_key = derive_key(generated_password, base64.b16decode(db_password['salt']))
    encrypted_password = encrypt_password(generated_password, encryption_key)
    vault.update_password(text, context, encrypted_password)
    return generated_password


def delete_password(context: str) -> dict[str, str]:
    password: dict[str, str] | None = vault.get_password(context)
    if not vault.delete_password(context):
        raise Exception("Password don't exist")
    return password
