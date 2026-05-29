from flask import Flask, request, jsonify

app = Flask(__name__)

# order book
order_book = {
    "buy": [],
    "sell": []
}

price = 1.0


# =====================
# PLACE ORDER
# =====================
@app.route("/order", methods=["POST"])
def order():
    data = request.json

    side = data["side"]  # buy / sell
    amount = data["amount"]
    price_level = data["price"]

    order_book[side].append({
        "amount": amount,
        "price": price_level
    })

    match_orders()

    return {"status": "order placed"}


# =====================
# MATCH ENGINE
# =====================
def match_orders():
    global price

    buys = sorted(order_book["buy"], key=lambda x: -x["price"])
    sells = sorted(order_book["sell"], key=lambda x: x["price"])

    new_buys = []
    new_sells = []

    i = j = 0

    while i < len(buys) and j < len(sells):
        buy = buys[i]
        sell = sells[j]

        if buy["price"] >= sell["price"]:
            trade = min(buy["amount"], sell["amount"])

            price = (buy["price"] + sell["price"]) / 2

            buy["amount"] -= trade
            sell["amount"] -= trade

            if buy["amount"] > 0:
                new_buys.append(buy)
            if sell["amount"] > 0:
                new_sells.append(sell)

            i += 1
            j += 1
        else:
            break

    order_book["buy"] = new_buys + buys[i:]
    order_book["sell"] = new_sells + sells[j:]


# =====================
# ORDER BOOK
# =====================
@app.route("/book")
def book():
    return {
        "buy": order_book["buy"],
        "sell": order_book["sell"],
        "price": price
    }


# =====================
# START
# =====================
if __name__ == "__main__":
    app.run(port=7000, debug=True)
