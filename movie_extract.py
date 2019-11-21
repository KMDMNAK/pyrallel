"""
    this script aim at extracting image frames from video by parallel.
"""

import cv2
from pyrallel.__init__ import Framework

APP = Framework(
    states={
        "frames": [],
        "time_indexes":[]
    },
    conditions={
        "read_and_write": True,
        "for_loop":True
    }
)

@APP.thread("for_loop","time_indexes")
def execute_time(states):
    @APP.prolife

@APP.condition_changer("")

@APP.prolife("read_and_write",limit=10)
def read_and_write_frame(states):
    pass

VIDEO_PATH = ""
CAPTURE = cv2.VideoCapture(VIDEO_PATH)
