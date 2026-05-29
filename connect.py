import requests

requests.post("http://127.0.0.1:5000/register", json={
    "peer": "http://127.0.0.1:5001"
})

requests.post("http://127.0.0.1:5001/register", json={
    "peer": "http://127.0.0.1:5000"
})

print("CONNECTED")