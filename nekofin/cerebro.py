import pandas as pd
import types

BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"


class Cerebro:
    def __init__(self, cash=100000, commision=0.001, strategy=None):
        self.data = []
        self.cash = cash
        self.commision = commision
        self.asset = 0
        self.log = []
        self.strategy = strategy

    def feedData(self, data):
        self.data = data

    def runBackTest(self, start=0, end=None, verbal=False):

        if end is None:
            end = len(self.data) - 1
        for i in range(start, end):
            if verbal:
                print(i)
            self.next(i)

    def next(self, i):
        pass

    def buy(self, i, size=1):
        self.cash -= self.data.iloc[i + 1]["Open"] * size * (1 + self.commision)
        self.asset += size
        self.log.append(
            {
                "action": BUY,
                "price": self.data.iloc[i]["Close"],
                "size": size,
                "time": self.data.index[i],
                "asset": self.asset,
                "cash": self.cash,
                "value": self.getValue(i),
            }
        )

    def sell(self, i, size=1):
        self.cash += self.data.iloc[i + 1]["Open"] * size * (1 - self.commision)
        self.asset -= size
        self.log.append(
            {
                "action": SELL,
                "price": self.data.iloc[i]["Close"],
                "size": size,
                "time": self.data.index[i],
                "asset": self.asset,
                "cash": self.cash,
                "value": self.getValue(i),
            }
        )

    def hold(self, i):
        self.log.append(
            {
                "action": HOLD,
                "price": self.data.iloc[i]["Close"],
                "size": 0,
                "time": self.data.index[i],
                "asset": self.asset,
                "cash": self.cash,
                "value": self.getValue(i),
            }
        )

    def addStrategy(self, strategy):
        self.next = types.MethodType(strategy, self)

    def getValue(self, i=0):
        return self.cash + self.asset * self.data.iloc[i]["Close"]

    def getLog():
        pass


def runBackTest(data, strategy, cash=100000, commision=0.001):
    cash = 100000
    asset = 0
    log = [(cash, asset, "FIRST", data.iloc[0]["Close"])]

    for i in range(len(data)):
        action = strategy(data, i, cash)
        if not action:
            pass
        if action["type"] == BUY:
            cash -= action["size"] * action["price"] * (1 + commision)
            asset += action["size"]
            log.append((cash, asset, BUY, data.iloc[i]["Close"]))

        elif action["type"] == "sell":
            cash += action["size"] * action["price"] * (1 - commision)
            asset -= action["size"]
            log.append((cash, asset, SELL, data.iloc[i]["Close"]))

        else:
            log.append((cash, asset, HOLD, data.iloc[i]["Close"]))
    return log


# interface fucntion strategy
def demo_strategy(data, i, cash):
    if i < 100:
        return buy(data, i)
    elif i >= len(data) - 100:
        return sell(data, i)
    else:
        return hold(data, i)


def buy(data, i, size=1):
    return {"type": BUY, "size": size, "price": data.iloc[i]["Close"]}


def sell(data, i, size=1):
    return {"type": SELL, "size": size, "price": data.iloc[i]["Close"]}


def hold(data, i):
    return {"type": HOLD}