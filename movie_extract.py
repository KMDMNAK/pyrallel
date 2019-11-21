"""
    this script aim at extracting image frames from video by parallel.
"""

import cv2
from pyrallel.__init__ import Framework

APP = Framework(
    states={
        "frames": []
    },
    conditions={
        "read_and_write": True
    }
)


@APP.thread("read_and_write", "frames")
def execute_frame(states):
    pass

@APP.clone_thread(limit=10)
def read_and_write_frame(states):
    pass

VIDEO_PATH = ""
CAPTURE = cv2.VideoCapture(VIDEO_PATH)
