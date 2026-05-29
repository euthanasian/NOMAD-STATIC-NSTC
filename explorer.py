from flask import Flask, jsonify
import requests

app = Flask(__name__)

NODE = "http://127.0.0.1:5000"


@app.route("/")
def home():
    chain = requests.get(NODE + "/chain").json()
    supply = requests.get(NODE + "/supply").json()

    return {
        "blocks": len(chain),
        "latest_block": chain[-1] if chain else None,
        "supply": supply
    }


@app.route("/blocks")
def blocks():
    return jsonify(requests.get(NODE + "/chain").json())


@app.route("/supply")
def supply():
    return jsonify(requests.get(NODE + "/supply").json())


if __name__ == "__main__":
    app.run(port=8000)
