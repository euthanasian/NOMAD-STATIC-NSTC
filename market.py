class Market:
    def __init__(self):
        self.price = 1.0
        self.order_book = {"buy": [], "sell": []}

    def place_order(self, side, amount, price):
        self.order_book[side].append((amount, price))
        self.match()

    def match(self):
        buys = sorted(self.order_book["buy"], key=lambda x: -x[1])
        sells = sorted(self.order_book["sell"], key=lambda x: x[1])

        new_buys = []
        new_sells = []

        i = j = 0

        while i < len(buys) and j < len(sells):
            buy_amt, buy_price = buys[i]
            sell_amt, sell_price = sells[j]

            if buy_price >= sell_price:
                traded = min(buy_amt, sell_amt)
                self.price = (buy_price + sell_price) / 2

                buy_amt -= traded
                sell_amt -= traded

                if buy_amt > 0:
                    new_buys.append((buy_amt, buy_price))
                if sell_amt > 0:
                    new_sells.append((sell_amt, sell_price))

                i += 1
                j += 1
            else:
                break

        self.order_book["buy"] = new_buys + buys[i:]
        self.order_book["sell"] = new_sells + sells[j:]
