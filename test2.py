"""
    this is test for framework
"""

import random
import time

from __init__2 import Framework

app = Framework(
    states={"count": 0, "stock": []},
    conditions={"start": True, "watch": False}
)


@app.thread("watch", "stock")
def stock_popper(states):
    if len(states.stock) <= 5:
        return None
    print("in stock popper", ",id : ", id(states.stock))
    print(states.stock)
    return {
        "stock": []
    }


@app.thread("start", "stock", "count")
def stock_pusher(states):
    sleep_time = random.randint(1, 3)
    print("sleep time : ", sleep_time)
    time.sleep(sleep_time)
    new_stock = states.stock.copy()
    new_stock.append(sleep_time)
    count = states.count + 1
    return {
        "stock": new_stock,
        "count": count
    }


@app.condition_changer("watch", "stock")
def watch_changer(states):
    if len(states.stock) >= 5:
        return True
    print("in watch changer : ", states.stock, ",id : ", id(states.stock))
    return False
# not all arguments converted during string formatting


@app.condition_changer("start", "count")
def start_changer(states):
    print("in start changer : ", states.count)
    return True


if __name__ == "__main__":
    app.run(runnning_time=100,loop_interval=0.5)
