```python
from flask import Flask, request, jsonify
import requests
import threading
import time
import os

from blockchain import Blockchain

app = Flask(__name__)

# =========================
# BLOCKCHAIN
# =========================

node = Blockchain()

# =========================
# PEERS
# =========================

peers = set()

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return jsonify({
        "status": "NSTC NODE RUNNING",
        "chain_length": len(node.chain),
        "mempool_size": len(node.mempool),
        "peers": list(peers)
    })

# =========================
# BLOCKCHAIN
# =========================

@app.route("/chain")
def chain():
    return jsonify(node.to_list())

# =========================
# MEMPOOL
# =========================

@app.route("/mempool")
def mempool():
    return jsonify(node.mempool)

# =========================
# BALANCE
# =========================

@app.route("/balance/<address>")
def balance(address):
    return jsonify({
        "address": address,
        "balance": node.get_balance(address)
    })

# =========================
# TRANSACTION
# =========================

@app.route("/tx", methods=["POST"])
def tx():

    data = request.json

    sender = data["sender"]
    receiver = data["receiver"]
    amount = data["amount"]

    tx_data = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }

    node.mempool.append(tx_data)

    broadcast_transaction(tx_data)

    return jsonify({
        "status": "transaction added",
        "tx": tx_data
    })

# =========================
# RECEIVE TX
# =========================

@app.route("/receive_tx", methods=["POST"])
def receive_tx():

    tx_data = request.json

    if tx_data not in node.mempool:
        node.mempool.append(tx_data)

    return jsonify({
        "status": "received"
    })

# =========================
# MINE
# =========================

@app.route("/mine", methods=["POST"])
def mine():

    data = request.json
    miner = data["miner"]

    block = node.mine_block(miner)

    broadcast_block(block)

    return jsonify({
        "status": "block mined",
        "block": block
    })

# =========================
# RECEIVE BLOCK
# =========================

@app.route("/receive_block", methods=["POST"])
def receive_block():

    block = request.json

    node.receive_block(block)

    return jsonify({
        "status": "block received"
    })

# =========================
# REGISTER PEER
# =========================

@app.route("/register", methods=["POST"])
def register():

    peer = request.json["peer"]

    peers.add(peer)

    return jsonify({
        "status": "peer added",
        "peers": list(peers)
    })

# =========================
# GET PEERS
# =========================

@app.route("/peers")
def get_peers():

    return jsonify({
        "peers": list(peers)
    })

# =========================
# BROADCAST TX
# =========================

def broadcast_transaction(tx_data):

    for peer in peers:

        try:
            requests.post(
                peer + "/receive_tx",
                json=tx_data,
                timeout=2
            )

        except:
            pass

# =========================
# BROADCAST BLOCK
# =========================

def broadcast_block(block):

    for peer in peers:

        try:
            requests.post(
                peer + "/receive_block",
                json=block,
                timeout=2
            )

        except:
            pass

# =========================
# AUTO SYNC
# =========================

def auto_sync():

    while True:

        time.sleep(15)

        best_chain = node.to_list()

        for peer in peers:

            try:

                r = requests.get(peer + "/chain", timeout=3)

                chain = r.json()

                if len(chain) > len(best_chain):
                    best_chain = chain

            except:
                pass

        node.replace_chain(best_chain)

# =========================
# START
# =========================

if __name__ == "__main__":

    threading.Thread(
        target=auto_sync,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
```
