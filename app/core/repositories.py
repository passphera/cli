from uuid import uuid4

from tinydb import TinyDB, Query

from passphera_core.entities import Generator, Password
from passphera_core.interfaces import GeneratorRepository, VaultRepository

from app.core import constants


class TinyDBContext:
    def __init__(self, path: str):
        self.db = TinyDB(path)
        self.generator_table = self.db.table("generator")
        self.vault_table = self.db.table("vault")


_db_context: TinyDBContext


def configure(path: str) -> None:
    global _db_context
    _db_context = TinyDBContext(path)


def get_db_context() -> TinyDBContext:
    if _db_context is None:
        raise RuntimeError("Database not configured. Call configure(path) first.")
    return _db_context


class TinyDBGeneratorRepository(GeneratorRepository):
    def __init__(self):
        self.ctx = get_db_context()

    def save(self, generator: Generator) -> None:
        self.ctx.generator_table.upsert(
            self._to_dict(generator),
            Query().id == generator.id
        )

    def get(self) -> Generator:
        data = self.ctx.generator_table.all()
        if not data:
            generator: Generator = Generator(
                id=uuid4(),
                shift=int(constants.DEFAULT_SHIFT),
                multiplier=int(constants.DEFAULT_MULTIPLIER),
                key=constants.DEFAULT_KEY,
                algorithm=constants.DEFAULT_ALGORITHM,
                prefix=constants.DEFAULT_PREFIX,
                postfix=constants.DEFAULT_POSTFIX,
            )
            self.save(generator)
            return generator
        return self._from_dict(data[0])

    def update(self, generator: Generator) -> None:
        self.save(generator)

    def _to_dict(self, generator: Generator) -> dict:
        return {
            "id": str(generator.id),
            "created_at": str(generator.created_at),
            "updated_at": str(generator.updated_at),
            "shift": generator.shift,
            "multiplier": generator.multiplier,
            "key": generator.key,
            "algorithm": generator.algorithm,
            "prefix": generator.prefix,
            "postfix": generator.postfix,
            "characters_replacements": generator.characters_replacements,
        }

    def _from_dict(self, data: dict) -> Generator:
        return Generator(
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            shift=data.get("shift"),
            multiplier=data.get("multiplier"),
            key=data.get("key"),
            algorithm=data.get("algorithm"),
            prefix=data.get("prefix"),
            postfix=data.get("postfix"),
            characters_replacements=data.get("characters_replacements", {}),
        )


class TinyDBVaultRepository(VaultRepository):
    def __init__(self):
        self.ctx = get_db_context()

    def save(self, password: Password) -> None:
        self.ctx.vault_table.upsert(
            self._to_dict(password),
            Query().context == password.context
        )

    def get(self, context: str) -> Password:
        data = self.ctx.vault_table.get(Query().context == context)
        return self._from_dict(data) if data else None

    def update(self, password: Password) -> None:
        self.save(password)

    def delete(self, password: Password) -> None:
        self.ctx.vault_table.remove(Query().context == password.context)

    def list(self) -> list[Password]:
        return [self._from_dict(password) for password in self.ctx.vault_table.all()]

    def flush(self) -> None:
        self.ctx.vault_table.truncate()

    def _to_dict(self, password: Password) -> dict:
        return {
            "id": password.id,
            "created_at": password.created_at,
            "updated_at": password.updated_at,
            "context": password.context,
            "text": password.text,
            "password": password.password,
            "salt": password.salt,
        }

    def _from_dict(self, data: dict) -> Password:
        return Password(
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            context=data.get("context"),
            text=data.get("text"),
            password=data.get("password"),
            salt=data.get("salt"),
        )
