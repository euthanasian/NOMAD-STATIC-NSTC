import hashlib
import time


# =====================
# BLOCK
# =====================
class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0

    def hash(self):
        data = f"{self.index}{self.transactions}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty

        while not self.hash().startswith(target):
            self.nonce += 1

        return self.hash()

    def to_dict(self):
        return {
            "index": self.index,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash()
        }


# =====================
# BLOCKCHAIN (UTXO MODEL)
# =====================
class Blockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.difficulty = 3

        self.max_supply = 200_000_000
        self.mined = 0

        self.create_genesis()

    # =====================
    # GENESIS
    # =====================
    def create_genesis(self):
        genesis = Block(0, [], "0")
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    # =====================
    # BALANCE (REAL CRYPTO STYLE)
    # =====================
    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for tx in block.transactions:

                # reward / receive
                if tx.get("to") == address:
                    balance += tx["amount"]

                # spend
                if tx.get("from") == address:
                    balance -= tx["amount"]

        return balance

    # =====================
    # ADD TX (NO VALIDATION SIMPLIFIED)
    # =====================
    def add_tx(self, tx):
        self.mempool.append(tx)

    # =====================
    # MINE BLOCK
    # =====================
    def mine(self, miner):
        if not self.mempool:
            return False

        block_txs = self.mempool.copy()
        self.mempool = []

        reward = 50

        if self.mined + reward > self.max_supply:
            reward = 0

        block_txs.append({
            "from": "SYSTEM",
            "to": miner,
            "amount": reward
        })

        self.mined += reward

        block = Block(len(self.chain), block_txs, self.chain[-1].hash())
        block.mine(self.difficulty)

        self.chain.append(block)

        return True

    # =====================
    # CHAIN EXPORT
    # =====================
    def to_list(self):
        return [b.to_dict() for b in self.chain]

    # =====================
    # REPLACE CHAIN
    # =====================
    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain):
            self.chain = [
                Block(
                    b["index"],
                    b["transactions"],
                    b["previous_hash"],
                    b["timestamp"],
                    b["nonce"]
                )
                for b in new_chain
            ]
            return True
        return False