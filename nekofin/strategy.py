import pandas as pd
import ccxt
import pymongo
import pandas as pd

BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"


def runBackTest(data, strategy, cash=100000, commision=0.001):
    cash = 100000
    asset = 0
    log = [(cash, asset, "FIRST", data.iloc[0]["Close"])]

    for i in range(len(data)):
        action = strategy(data, i, cash)

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
