"""
    this script aim at extracting image frames from video by parallel.
"""

import cv2
from pyrallel.__init__ import Framework

APP = Framework(
    states={
        "frames": [],
        "time_indexes": []
    },
    conditions={
        "read_and_write": True,
        "for_loop": True
    }
)


@APP.thread("for_loop", "time_indexes")
def execute_time(states):
    pass

@APP.condition_changer("")

@APP.prolife("read_and_write", limit=10)
def read_and_write_frame(states):
    pass


VIDEO_PATH = ""
CAPTURE = cv2.VideoCapture(VIDEO_PATH)


def extract_images(time_indexes, mod=3):
    """
        each pairs of time indexes do not duplicate time range
    """
    # sort time
    time_indexes = sorted(time_indexes, key=lambda x: x[0])
    # whether is it valid time indexes
    print(time_indexes)
    all_frames_list = []
    for start_time_index, end_time_index in time_indexes:
        frames_list = self.extract_images_by_time(
            start_time_index, end_time_index, mod)
        if frames_list == []:
            break
        all_frames_list.extend(frames_list)
    return all_frames_list
