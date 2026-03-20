import json, hashlib

class Blockchain:
    def __init__(self):
        self.chain = []
        self.prev_hash = "0"

    def add_block(self, tx):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": tx["timestamp"],
            "transaction": tx,
            "previous_hash": self.prev_hash
        }

        block["hash"] = hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()
        ).hexdigest()

        self.chain.append(block)
        self.prev_hash = block["hash"]

    def save(self, filename="blockchain.json"):
        with open(filename, "w") as f:
            json.dump(self.chain, f, indent=2)

    def load(self, filename="blockchain.json"):
        import os
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.chain = json.load(f)
                if self.chain:
                    self.prev_hash = self.chain[-1]["hash"]
        else:
            self.chain = []
            self.prev_hash = "0"