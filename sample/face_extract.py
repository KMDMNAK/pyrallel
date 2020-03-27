import time
import cv2
from Pyrallel.application import Framework
import os

VIDEO_PATH = "hirose1.mp4"
ORIGINAL_IMAGE_PATH = "img/hirose1/"

folder_path = "img/hirose1_face/"
extension = ".jpg"
face_cascade = cv2.CascadeClassifier(
    "C:\\Users\\gale\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")


APP = Framework(
    states={
        "original_folder_path": ORIGINAL_IMAGE_PATH,
        "file_names": os.listdir(ORIGINAL_IMAGE_PATH),
        "images": []  # [(target_frame_index,frame),...],

    },
    conditions={
        "read": True,
        "detect_and_write": True
    }
)


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


@APP.prolife("read", "images", "file_names")
def read_image(states):
    if not states.file_names:
        return None
    filename = states.file_names.pop(0)
    color_img = cv2.imread(states.original_folder_path+filename)
    states.images.append([filename, color_img])


@APP.change_condition("read", "file_names", "images")
def change_read(states):
    if not states.file_names:
        return None
    if len(states.images) > 10:
        return False
    return True


@APP.prolife("detect_and_write", "images",option={"prolife_limit":30})
def detect_and_write_face(states):
    if not states.images:
        return None
    name, image = states.images.pop(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    areas = list(map(lambda each_face: each_face[2]*each_face[3], faces))
    x, y, w, h = faces[areas.index(max(areas))]
    #img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    x1, x2, y1, y2 = correct_size(gray, x, y, w, h)
    cv2.imwrite(folder_path+str(name)+extension, image[y1:y2, x1:x2])

@APP.change_condition("detect_and_write", "images")
def change_daw(states):
    if len(states.images)==0:
        return False
    return True

if __name__ == "__main__":
    APP.run()