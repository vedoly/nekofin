import pandas as pd
import types

ASSERT_BUY = "ASSERT_BUY"
ASSERT_SELL = "ASSERT_SELL"
BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"


class Cerebro:
    def __init__(self, data, cash=100000, commission=0.001, strategy=None, enable_log = False):
        self.data = data
        self.cash = cash
        self.commision = commision
        self.asset = 0
        self.log = []
        self.strategy = strategy
        self.close = self.data.Close.to_list()
        self.open = self.data.Open.to_list()
        self.enable_log = enable_log

    def feedData(self, data):
        self.data = data

    def runBackTest(self, start=0, end=None, verbal=False):

        if end is None:
            end = len(self.data) - 1
        for i in range(start, end):
            if self.enable_log:
                print(self.cash, self.asset)
            assert self.cash >= 0
            assert self.asset >= 0
            if verbal and self.enable_log:
                print(i)
            self.next(i)
    
    def customize(self, i):
        pass
       
    def next(self, i):
        pass

    def assert_buy(self, i, size = 1):
        return self.cash >= self.open[i + 1] * size * (1 + self.commision)
    
    def buy(self, i, size=1):
        self.cash -= self.open[i + 1] * size * (1 + self.commision)
        self.asset += size
        self.log.append(
            {
                "action": BUY,
                "price": self.close[i],
                "size": size,
                "time": self.data.index[i],
                "asset": self.asset,
                "cash": self.cash,
                "value": self.getValue(i),
            }
        )
        
    def assert_sell(self, i, size=1):
        return self.asset >= size

    def sell(self, i, size=1):
        self.cash += self.open[i + 1] * size * (1 - self.commision)
        self.asset -= size
        self.log.append(
            {
                "action": SELL,
                "price": self.close[i],
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
                "price": self.close[i],
                "size": 0,
                "time": self.data.index[i],
                "asset": self.asset,
                "cash": self.cash,
                "value": self.getValue(i),
            }
        )

    def setConfig(self):
        pass
        
    def addStrategy(self, strategy, params = { }, setConfig = None):
        # TODO: convert params as bt params
        self.p = params
        if setConfig is not None:
            self.setConfig = types.MethodType(setConfig, self)
            self.setConfig()
        self.next = types.MethodType(strategy, self)

    def getValue(self, i=0):
        return self.cash + self.asset * self.close[i]

    def getLog():
        pass


def runBackTest(data, strategy, cash=100000, commision=0.001):
    cash = 100000
    asset = 0
    log = [(cash, asset, "FIRST", self.close[0])]

    for i in range(len(data)):
        action = strategy(data, i, cash)
        if not action:
            pass
        if action["type"] == BUY:
            cash -= action["size"] * action["price"] * (1 + commision)
            asset += action["size"]
            log.append((cash, asset, BUY, self.close[i]))
        
        elif action["type"] == ASSERT_BUY:
            return cash >= action["size"] * action["price"] * (1 + commision)

        elif action["type"] == SELL:
            cash += action["size"] * action["price"] * (1 - commision)
            asset -= action["size"]
            log.append((cash, asset, SELL, self.close[i]))
            
        elif action["type"] == ASSERT_SELL:
            return asset >= action["size"]

        else:
            log.append((cash, asset, HOLD, self.close[i]))
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
    return {"type": BUY, "size": size, "price": self.close[i]}


def sell(data, i, size=1):
    return {"type": SELL, "size": size, "price": self.close[i]}


def hold(data, i):
    return {"type": HOLD}
