"""
    this script aim at extracting image frames from video by parallel.
    non threading script cost about 1144.56 second,means 19 minutes for get 12066 images.
    this script cost about 212 second , mean 3.5 minutes for get 12066 images
"""

import time
import cv2
from Pyrallel.application import Framework

VIDEO_PATH = "hirose1.mp4"
folder_path = "img/hirose1_face/"
extension = ".jpg"
capture = cv2.VideoCapture(VIDEO_PATH)
fps = capture.get(cv2.CAP_PROP_FPS)
time_indexes = [(6, 40), (47, 226), (234, 272),
                (279, 350), (358, 406), (413, 546)]  # 210秒で終了 12000枚数
face_cascade = cv2.CascadeClassifier(
    "C:\\Users\\gale\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
face_folder_path = "img/hirose1_face/"


def make_frame_indexes(fps, time_indexes, over=None):
    frame_indexes = []
    for start_index, end_index in time_indexes:
        indexes = list(range(int(start_index * fps), int(end_index * fps)+1))
        if over:
            indexes = list(filter(lambda x: x > over, indexes))
        frame_indexes.extend(indexes)
    return frame_indexes


APP = Framework(
    states={
        # [(1,3),(5,7)]->[FPS*1,FPS*1+1,...,FPS*3,FPS*5,FPS*5+1,...,FPS*7]
        "frame_indexes": make_frame_indexes(fps, time_indexes,2701),
        "capture": capture,
        "frames": [],  # [(target_frame_index,frame),...]
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


@APP.change_condition("read", "frames", "capture")
def change_read(states):
    if len(states.frames) > 10:
        return False
    if not states.capture.isOpened():
        return False
    return True


def correct_size(gray, x, y, w, h, percent=3):
    """
        オリジナル画像の大きさに合わせてbboxを拡大
    """
    height, width = gray.shape
    correct_value_x = int(percent*0.005*width)
    correct_value_y = int(percent*0.005*height)

    sub_x1, sub_y1 = x-correct_value_x, y-correct_value_y
    x1 = sub_x1 if sub_x1 > 0 else 0
    y1 = sub_y1 if sub_y1 > 0 else 0

    plus_x2, plus_y2 = x+correct_value_x+w, y+correct_value_y+h
    x2 = plus_x2 if plus_x2 < width else width
    y2 = plus_y2 if plus_y2 < height else height
    return x1, x2, y1, y2


@APP.multiply("write", "frames", option={"multiply_limit": 10})
def detect_and_write_face(states):
    if not states.frames:
        return None
    name, frame = states.frames.pop(0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    areas = list(map(lambda each_face: each_face[2]*each_face[3], faces))
    x, y, w, h = faces[areas.index(max(areas))]
    # img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    x1, x2, y1, y2 = correct_size(gray, x, y, w, h)
    cv2.imwrite(face_folder_path+str(name)+extension, frame[y1:y2, x1:x2])
    return None


@APP.change_condition("write", "frames")
def change_write(states):
    if not states.frames:
        return False
    return True


if __name__ == "__main__":
    s = time.time()
    APP.run()
    print(time.time()-s)
