"""
    this module is wrapper of cv2's video handling
    capture=cv2.VideoCapture("C.mp4")
"""
import cv2
import asyncio
import threading

loop = asyncio.get_event_loop()


class Error(Exception):
    """
        error class
    """

    def __init__(self, message: str):
        print(message)


class ExtractImages:
    """
        this class is to get images from video

        ex)
        EI=ExtranctImages("a.mp4")
        frames=EI.extract_images([(0,10),(11,20)])
        EI.imwrite_frames(frames,"img/")
    """

    def __init__(self, video_path):
        self.capture = cv2.VideoCapture(video_path)
        self.checking_index = -1
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.all_frames_list = None

    def extract_images_by_time(self, start_time_index, end_time_index, mod):
        """
            mod:int , 中抜き
            returns : list
        """
        frames_list = []
        start_index_of_images = int(start_time_index*self.fps)
        end_index_of_images = int(end_time_index*self.fps)+1
        mod_count = 0
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, start_index_of_images)
        self.checking_index = start_index_of_images-1
        while self.capture.isOpened():
            self.checking_index += 1
            ret, frame = self.capture.read()
            if (self.checking_index >= start_index_of_images &
                    self.checking_index < end_index_of_images):
                frames_list.append(frame)
            if self.checking_index >= end_index_of_images:
                break
            mod_count += 1
        return frames_list

    def extract_images_by_time_thread(self, start_time_index, end_time_index, mod, all_frames_list_index, all_frames_list):
        """
            mod:int , 中抜き
            returns : list
        """

        start_time_index, end_time_index = end_time_index
        print(start_time_index, end_time_index, mod, all_frames_list_index)
        frames_list = []
        start_index_of_images = int(start_time_index*self.fps)
        end_index_of_images = int(end_time_index*self.fps)+1
        mod_count = 0
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, start_index_of_images)
        self.checking_index = start_index_of_images-1
        while self.capture.isOpened():
            self.checking_index += 1
            ret, frame = self.capture.read()
            if (self.checking_index >= start_index_of_images &
                    self.checking_index < end_index_of_images):
                frames_list.append(frame)
            if self.checking_index >= end_index_of_images:
                break
            mod_count += 1
        all_frames_list[all_frames_list_index] = frames_list

    def extract_images(self, time_indexes, mod=3):
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

    def extract_images_thread(self, time_indexes, mod=3):
        """
            each pairs of time indexes do not duplicate time range
        """
        # sort time
        time_indexes = sorted(time_indexes, key=lambda x: x[0])
        # whether is it valid time indexes
        print(time_indexes)
        mod = 3
        all_frames_list = [None for i in range(len(time_indexes))]
        threads = []
        i = 0
        for start_time_index, end_time_index in enumerate(time_indexes):
            t = threading.Thread(target=self.extract_images_by_time_thread, args=(
                start_time_index, end_time_index, mod, i, all_frames_list))
            threads.append(t)
            t.start()
            i += 1
        for each_thread in threads:
            print("join")
            each_thread.join()
        frames_list = []
        for each_frames in all_frames_list:
            frames_list.extend(each_frames)
        return frames_list

    def imwrite_frames(self, frames_list, folder_path, frame_names=None, extension=".jpg"):
        """
            write images to specific folder

            frame_names doesn't contain folder path and extension name
            folder_path end with "/"
        """
        if frame_names:
            if len(frame_names) != len(frames_list):
                raise Error("mismatch frame and name length")
            for name, frame in zip(frame_names, frames_list):
                cv2.imwrite(folder_path+name+extension, frame)
            return None

        # frame_names == None
        for (i, frame) in enumerate(frames_list):
            path = folder_path+str(i)+extension
            cv2.imwrite(path, frame)

    def imwrite(self, i, frame, folder_path, extension):
        path = folder_path+str(i)+extension
        cv2.imwrite(path, frame)

    def imwrite_frames_thread(self, frames_list, folder_path, frame_names=None, extension=".jpg"):
        """
            write images to specific folder

            frame_names doesn't contain folder path and extension name
            folder_path end with "/"
        """
        if frame_names:
            if len(frame_names) != len(frames_list):
                raise Error("mismatch frame and name length")
            for name, frame in zip(frame_names, frames_list):
                cv2.imwrite(folder_path+name+extension)
            return None
        threads = []
        # frame_names == None
        for (i, frame) in enumerate(frames_list):
            t = threading.Thread(target=self.imwrite, args=(
                i, frame, folder_path, extension)
            )
            threads.append(t)
            t.start()
        for each_thread in threads:
            each_thread.join()


class AsyncExtractImages:
    """
        this class is to get images from video

        ex)
        EI=ExtranctImages("a.mp4")
        frames=EI.extract_images([(0,10),(11,20)])
        EI.imwrite_frames(frames,"img/")
    """

    def __init__(self, video_path, output_folder_path, extension=".jpg"):
        self.output_folder_path = output_folder_path
        self.video_path = video_path
        self.fps = None
        self.joinning = True
        self.frame_info_queue = []
        self.extension = extension

    def extract_images_by_time_thread(self, start_time_index, end_time_index, mod):
        """
            mod:int , 中抜き
            returns : list
        """
        capture = cv2.VideoCapture(self.video_path)
        if self.fps is None:
            self.fps = capture.get(cv2.CAP_PROP_FPS)
        start_time_index, end_time_index = end_time_index
        print(start_time_index, end_time_index, mod)
        start_index_of_images = int(start_time_index*self.fps)
        end_index_of_images = int(end_time_index*self.fps)+1
        capture.set(cv2.CAP_PROP_POS_FRAMES, start_index_of_images)
        checking_index = start_index_of_images-1
        while capture.isOpened():
            ret, frame = capture.read()
            if (checking_index >= start_index_of_images &
                    checking_index < end_index_of_images):
                self.frame_info_queue.append(frame)
            if checking_index >= end_index_of_images:
                break

    def extract_images_thread(self, time_indexes, mod=3):
        """
            each pairs of time indexes do not duplicate time range
        """
        # sort time
        time_indexes = sorted(time_indexes, key=lambda x: x[0])
        # whether is it valid time indexes
        print(time_indexes)
        mod = 3
        threads = []
        i = 0
        for start_time_index, end_time_index in enumerate(time_indexes):
            t = threading.Thread(target=self.extract_images_by_time_thread, args=(
                start_time_index, end_time_index, mod, i))
            threads.append(t)
            t.start()
            i += 1
        for each_thread in threads:
            print("join")
            each_thread.join()
        return None

    def imwrite(self, frame, count):
        path = self.output_folder_path+str(count)+self.extension
        cv2.imwrite(path, frame)

    def imwrite_event(self):
        count = 0
        while self.joinning:
            if len(self.frame_info_queue) == 0:
                continue
            self.imwrite(self.frame_info_queue.pop(), count)
            count += 1
