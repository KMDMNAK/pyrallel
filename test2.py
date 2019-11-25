"""
    this is test for framework
"""

import random
import time

from Pyrallel.application import Framework

app = Framework(
    states={"count": 0, "stock": []},
    conditions={"start": True, "watch": False},
    loop_interval=0.5
)


@app.loop("watch", "stock")
def stock_popper(states):
    if len(states.stock) <= 4:
        return None
    print(states.stock.pop())


@app.loop("start", "stock", "count")
def stock_pusher(states):
    sleep_time = random.randint(1, 3)
    print("sleep time : ", sleep_time)
    time.sleep(sleep_time)
    states.stock.append(sleep_time)
    states.count = states.count + 1
    print(states.stock)


@app.change_condition("watch", "stock")
def watch_changer(states):
    if len(states.stock) >= 3:
        return True
    print("in watch changer : ", states.stock, ",id : ", id(states.stock))
    return False
# not all arguments converted during string formatting

"""
@app.change_condition("start", "count")
def start_changer(states):
    print("in start changer : ", states.count)
    return True
"""

if __name__ == "__main__":
    app.run(runnning_time=100)
    pass
