import json
import base64
from hashlib import sha256
from time import time
import os


filename = "data.json"


class Block:
    def __init__(self, name, timestamp=None, data=None):
        self.name = name  # Имя пользователя
        self.timestamp = timestamp or time()
        self.data = data  # Хэш аудиозаписи
        self.prevHash = None
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        hash_obj = sha256()
        hash_obj.update(str(self.prevHash).encode("utf-8"))
        hash_obj.update(str(self.timestamp).encode("utf-8"))
        hash_obj.update(str(self.name).encode("utf-8"))
        hash_obj.update(str(self.data).encode("utf-8"))
        hash_obj.update(str(self.nonce).encode("utf-8"))
        return hash_obj.hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 1
        self.load_from_file(filename)
        if self.chain == []:
            self.chain = [Block("Genesis Block", data="Initial block")]

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, name, audio_hash):
        # Проверка, есть ли уже запись с таким именем
        if self.user_exists(name):
            return

        new_block = Block(name=name, data=audio_hash)
        new_block.prevHash = self.getLastBlock().hash
        new_block.hash = new_block.getHash()
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.save_to_file(filename)

    def user_exists(self, name):
        return any(block.name == name for block in self.chain)

    def save_to_file(self, filename):
        status = False
        data = None
        if os.path.exists(filename):
            with open(filename) as f:
                data = json.load(f)
                if data:
                    status = True
        status = False

        # if status:
        data = [block.__dict__ for block in self.chain]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                for block_data in data:
                    block = Block(
                        block_data["name"], block_data["timestamp"], block_data["data"]
                    )
                    block.prevHash = block_data.get("prevHash", None)
                    block.nonce = block_data.get("nonce", 0)
                    block.hash = block_data.get("hash", None)
                    self.chain.append(block)

            # Убедитесь, что каждый блок ссылается на предыдущий
            for i in range(1, len(self.chain)):
                self.chain[i].prevHash = self.chain[i - 1].hash

    def __repr__(self):
        return json.dumps(
            [
                {
                    "name": item.name,
                    "data": item.data,
                    "timestamp": item.timestamp,
                    "nonce": item.nonce,
                    "hash": item.hash,
                    "prevHash": item.prevHash,
                }
                for item in self.chain
            ],
            indent=4,
        )


# # Пример использования
# if __name__ == "__main__":
#     blockchain = Blockchain()
#     blockchain.addBlock("Alice", "audio_hash_1")
#     blockchain.addBlock("Bob", "audio_hash_2")
#     print(blockchain)
