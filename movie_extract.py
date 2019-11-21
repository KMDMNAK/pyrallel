import cv2
from pyrallel.__init__ import Framework

app = Framework(
    states={
        "frames":[]
    },
    conditions={
        "read":True
    }
)

@app.thread("read","frames")
def read_frame(states):
    pass