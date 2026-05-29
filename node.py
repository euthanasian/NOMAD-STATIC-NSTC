from flask import Flask, request, jsonify
import sys
import requests
from blockchain import Blockchain

app = Flask(__name__)

node = Blockchain()
peers = set()


# =====================
# HOME
# =====================
@app.route("/")
def home():
    return {
        "status": "NSTC NODE RUNNING",
        "chain_length": len(node.chain),
        "mempool": len(node.mempool),
        "peers": list(peers)
    }


# =====================
# CHAIN
# =====================
@app.route("/chain")
def chain():
    return jsonify(node.to_list())


# =====================
# REGISTER PEER
# =====================
@app.route("/register", methods=["POST"])
def register():
    peer = request.json["peer"]
    peers.add(peer)
    return {"ok": True, "peers": list(peers)}


# =====================
# PEERS
# =====================
@app.route("/peers")
def get_peers():
    return {"peers": list(peers)}


# =====================
# TX (MONET TRANSACTIONS)
# =====================
@app.route("/tx", methods=["POST"])
def tx():
    data = request.json

    tx_data = {
        "from": data["from"],
        "to": data["to"],
        "amount": data["amount"]
    }

    node.add_tx(tx_data)

    return {
        "status": "tx_added"
    }


# =====================
# MINE (BLOCK + REWARD + BALANCE)
# =====================
@app.route("/mine", methods=["POST"])
def mine():
    miner = request.json["miner"]

    success = node.mine(miner)

    return {
        "status": "mined" if success else "empty_mempool",
        "miner_balance": node.get_balance(miner)
    }


# =====================
# BALANCE CHECK (НОВАЯ ФИЧА)
# =====================
@app.route("/balance/<address>")
def balance(address):
    return {
        "address": address,
        "balance": node.get_balance(address)
    }


# =====================
# SUPPLY INFO
# =====================
@app.route("/supply")
def supply():
    return {
        "max_supply": node.max_supply,
        "mined": node.mined,
        "remaining": node.max_supply - node.mined
    }


# =====================
# BROADCAST (упрощённо)
# =====================
def broadcast_tx(tx):
    for p in list(peers):
        try:
            requests.post(p + "/tx", json=tx, timeout=2)
        except:
            pass


# =====================
# START
# =====================
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    app.run(host="127.0.0.1", port=port, debug=True)