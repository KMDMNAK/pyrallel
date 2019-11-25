"""
    this script aim at extracting image frames from video by parallel.
"""

import cv2
from pyrallel.application import Framework

VIDEO_PATH = "sample.mp4"
folder_path = "/img/"
extension = ".jpg"

APP = Framework(
    states={
        # [(1,3),(5,7)]->[FPS*1,FPS*1+1,...,FPS*3,FPS*5,FPS*5+1,...,FPS*7]
        "frame_indexes": [],
        "capture": cv2.VideoCapture(VIDEO_PATH)
    },
    conditions={
        "read_and_write": True
    }
)


@APP.prolife("read_and_write", "capture", "frame_indexes", options={"limit": 100})
def read_and_write_frame(states):
    capture_frame_index = int(states.capture.get(
        cv2.CAP_PROP_POS_FRAMES
    ))  # 現在のフレーム位置の取得
    target_frame_index = int(states.frame_indexes.pop())
    if capture_frame_index != target_frame_index:
        states.capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame_index)
    ret, frame = states.capture.read()
    cv2.imwrite(folder_path + capture_frame_index + extension, frame)
    return None


@APP.change_condition("read_and_write","capture")
def change_read_and_write(states):
    if states.capture.isOpened():
        return True
    return False
