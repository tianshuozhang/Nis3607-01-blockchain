import hashlib

class Block:
    def __init__(self, index, previous_hash, nonce=0,id = -1):
        self.index = index
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.id = id

    def calculate_hash(self):
        value = f"{self.index}{self.id}{self.nonce}".encode()
        return hashlib.sha256(value).hexdigest()