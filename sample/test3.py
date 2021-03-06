import random
import time

from Pyrallel.application import Framework

app = Framework(
    states={"count": 0, "stock": []},
    conditions={"start": True, "watch": False},
    loop_interval=0.5
)


@app.multiply("start", "stock", option={"multiply_limit": 10})
def pro(states):
    states.stock.append(random.randint(1, 10))
    time.sleep(random.randint(1, 10))

if __name__ == "__main__":
    app.run()
