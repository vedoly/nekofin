import pandas as pd
import ccxt
import pymongo
import pandas as pd


def createMockData(arr, open_price, hl_ration=1.1):
    data = {"Close": [float(e) for e in arr], "Open": [float(open_price)] + arr[0:-1]}
    data["High"] = [
        max(data["Close"][i], data["Open"][i]) * hl_ration
        for i in range(len(data["Close"]))
    ]
    data["Low"] = [
        min(data["Close"][i], data["Open"][i]) / hl_ration
        for i in range(len(data["Close"]))
    ]
    data["Time"] = [
        pd.Timestamp(year=2000, month=1, day=1, hour=0) + pd.DateOffset(minutes=i)
        for i in range(len(data["Close"]))
    ]
    data["Volume"] = 1000000
    return pd.DataFrame(data).set_index("Time")


# connect to mongoDB
def connect_mongo(mongo_key):
    try:
        conn = pymongo.MongoClient(mongo_key)

        db = conn.get_database("dataleak")
        return db
    except Exception as e:
        print("[ERROR] %s" % e)
        return None


# open dataleak table with symbol
def open_table(db, table_name, symbol):
    try:
        table = db.get_collection(table_name)
        if symbol:
            table = table.find({"symbol": symbol})
        # table = table.find({'symbol':symbol})
        return table
    except Exception as e:
        print("[ERROR] %s" % e)
        return None


# convert table to pandas dataFrame
def table_to_df(table):
    try:
        df = pd.DataFrame(list(table))
        return df
    except Exception as e:
        print("[ERROR] %s" % e)
        return None


# list unique symbol of collection
def list_unique_symbol(table):
    try:
        symbols = table.distinct("symbol")
        return symbols
    except Exception as e:
        print("[ERROR] %s" % e)
        return None


# df = table_to_df(open_table(connect_mongo(),"histories",'BTC/USDT'))
