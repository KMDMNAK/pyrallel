"""
    this is test for framework
"""

import random
import time

from __init__ import Framework
app = Framework(
    states={"count": 0, "stock": []},
    conditions={"start": True, "watch": False}
)


@app.thread("watch", "stock")
def stock_popper(stock):
    if len(stock) <= 5:
        return None
    print("in stock popper", ",id : ", id(stock))
    print(stock)
    print(stock.pop(0))
    return {
        "stock": stock.copy()
    }


@app.thread("start", "stock", "count")
def stock_pusher(stock, count):
    new_stock = stock.copy()
    sleep_time = random.randint(1, 3)
    print("sleep time : ", sleep_time)
    time.sleep(sleep_time)
    new_stock.append(sleep_time)
    count = count + 1
    return {
        "stock": new_stock,
        "count": count
    }


@app.condition_changer("watch", "stock")
def watch_changer(stock):
    if len(stock) >= 5:
        return True
    print("in watch changer : ", stock, ",id : ", id(stock))
    return False
# not all arguments converted during string formatting


@app.condition_changer("start", "count")
def start_changer(count):
    print("in start changer : ", count)
    return True


if __name__ == "__main__":
    app.run(runnning_time=100)
