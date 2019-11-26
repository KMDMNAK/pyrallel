"""
    this script aim at extracting image frames from video by parallel.
"""

import cv2
from Pyrallel.application import Framework

VIDEO_PATH = "sample.mp4"
folder_path = "img/"
extension = ".jpg"
capture = cv2.VideoCapture(VIDEO_PATH)
fps = capture.get(cv2.CAP_PROP_FPS)


def make_frame_indexes(fps, time_indexes):
    frame_indexes = []
    for start_index, end_index in time_indexes:
        frame_indexes.extend(
            list(range(int(start_index * fps), int(end_index * fps))))
    return frame_indexes


APP = Framework(
    states={
        # [(1,3),(5,7)]->[FPS*1,FPS*1+1,...,FPS*3,FPS*5,FPS*5+1,...,FPS*7]
        "frame_indexes": make_frame_indexes(fps, [(1, 2)]),
        "capture": capture,
        "frames": []  # [(target_frame_index,frame),...]
    },
    conditions={
        "read": True,
        "write": True
    }
)


@APP.loop("read", "frames", "frame_indexes")
def read_frame(states):
    capture_frame_index = int(states.capture.get(
        cv2.CAP_PROP_POS_FRAMES
    ))  # 現在のフレーム位置の取得
    target_frame_index = int(states.frame_indexes.pop(0))
    if capture_frame_index != target_frame_index:
        states.capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame_index)
    ret, frame = states.capture.read()
    states.frames.append((target_frame_index, frame))
    print("frame in read", len(states.frames))
    print(target_frame_index)



@APP.prolife("write", "frames")
def read_and_write_frame(states):
    if not states.frames:
        return None
    index, frame = states.frames.pop(0)
    print("in write",index)
    cv2.imwrite(folder_path + str(index) + extension, frame)
    return None


@APP.change_condition("read", "frames", "capture")
def change_read(states):
    if len(states.frames) > 100:
        return False
    if not states.capture.isOpened():
        return False
    return True


@APP.change_condition("write", "frames")
def change_write(states):
    if not states.frames:
        return False
    return True


if __name__ == "__main__":
    APP.run()
