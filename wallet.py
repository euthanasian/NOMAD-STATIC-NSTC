import hashlib
import os


class Wallet:
    def __init__(self, name):
        self.name = name

        # простой “ключ” (не идеальная криптография, но для системы ок)
        self.private_key = hashlib.sha256(os.urandom(32)).hexdigest()
        self.address = hashlib.sha256(self.private_key.encode()).hexdigest()

    def sign(self, data):
        return hashlib.sha256((str(data) + self.private_key).encode()).hexdigest()

    def info(self):
        return {
            "name": self.name,
            "address": self.address
        }