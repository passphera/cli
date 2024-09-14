import os
import pickle

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from tinydb.storages import Storage


class EncryptedStorage(Storage):
    def __init__(self, filename: str):
        self.filename = filename
        self.key = get_random_bytes(16)

    def pad(self, s: bytes) -> bytes:
        return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

    def unpad(self, s: bytes) -> bytes:
        # Remove padding
        return s.rstrip(b'\0')

    def encrypt(self, data: bytes) -> bytes:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(self.pad(data))

    def decrypt(self, data: bytes) -> bytes:
        iv = data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(data[AES.block_size:]))

    def read(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'rb') as f:
            encrypted_data = f.read()
            try:
                decrypted_data = self.decrypt(encrypted_data)
                return pickle.loads(decrypted_data)
            except (EOFError, pickle.UnpicklingError):
                return {}

    def write(self, data: dict) -> None:
        with open(self.filename, 'wb') as f:
            serialized_data = pickle.dumps(data)
            encrypted_data = self.encrypt(serialized_data)
            f.write(encrypted_data)

    def close(self):
        pass
