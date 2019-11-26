import threading
import time


class Option:
    def __init__(self):
        self.while_interval = 0.01
        self.prolife_limit = 100


class ThreadBase:
    """
        ProlifeとThreadにおける,conditionとの接続部分
    """

    def __init__(self, threadable_function, conditions, condition_name, states, willchange_state_names, option=None):
        """
        print("in threadbase")
        print(threadable_function, conditions, condition_name,
              states, willchange_state_names, option)
        """
        self.__conditions__ = conditions
        self.__condition_name__ = condition_name
        self.__willchange_state_names__ = willchange_state_names
        self.__states__ = states
        self.__threadable_function__ = threadable_function
        self.__thread__ = None
        self.__running__ = False  # スレッドが終了しているかどうかの判定
        print("option is ", option)
        if option is not None:
            for option_name in option:
                setattr(self, option_name, option[option_name])
                print("set ", option_name)
        if not getattr(self, "while_interval", None):
            setattr(self, "while_interval", 0.1)
        print("thread's condition id is ", id(self.__conditions__))

    def __updated_states__(self):
        self.__states__.__accept_state_updated__(
            self.__willchange_state_names__)

    def __threading__(self):
        while getattr(self.__conditions__, self.__condition_name__, None):
            #print(self.__condition_name__, "is starting")
            #print("in threading, condition is ", getattr(self.__conditions__, self.__condition_name__))
            self.__threadable_function__(self.__states__)
            self.__updated_states__()
            if getattr(self, "while_interval", None):
                time.sleep(getattr(self, "while_interval"))

            # self.__states__.__show_values__()
            # self.__conditions__.__show_values__()
        print("\n\n now {0} 's thread is ended\n\n".format(
            self.__condition_name__))
        self.__running__ = False

    def __activate__(self):
        if not self.__running__:
            self.__running__ = True
            print("\n\n now {0} 's thread is activated!\n\n".format(
                self.__condition_name__))
            t = threading.Thread(target=self.__threading__)
            t.start()
            self.__thread__ = t
        return None

    def __destroy__(self):
        pass


class ProlifeThread(ThreadBase):
    """
        a
    """

    def __init__(self, threadable_function, conditions, condition_name, states, willchange_state_names, option=None):
        super().__init__(threadable_function, conditions,
                         condition_name, states, willchange_state_names, option)
        self.__active_threads__ = []
        self.__thread_running__ = 0  # amount of  runnning threads
        self.__threadable_function__ = self.__create_threadable_function__(
            threadable_function)
        self.__end_flag__ = False

    def __other_condition__(self):
        prolife_limit = getattr(self, "prolife_limit")
        if prolife_limit is None:
            return True
        if prolife_limit > self.__thread_running__:
            return True
        return False

    # 複製する関数
    def __create_threadable_function__(self, threadable_function):
        def __prolife_template__(self):
            threadable_function(self.__states__)
            self.__updated_states__()
            # 終了判定
            self.__thread_running__ -= 1
            # 増殖threadが終了した場合,end flagを立てて,
            self.__end_flag__ = True
            return None
        return __prolife_template__

    def __threading__(self):
        __test_count__ = 0
        while getattr(self.__conditions__, self.__condition_name__):
            """print(self.__condition_name__, getattr(
                self.__conditions__, self.__condition_name__))
            """
            while not self.__other_condition__():
                while not self.__end_flag__:
                    time.sleep(getattr(self, "while_interval"))
                if self.__end_flag__:
                    self.__end_flag__ = False
            self.__thread_running__ += 1
            t = threading.Thread(
                target=self.__threadable_function__, args=(
                    self,)
            )
            t.start()
            self.__active_threads__.append(t)
            # self.__active_threads__.append(t)
            if getattr(self, "while_interval"):
                time.sleep(getattr(self, "while_interval"))
            __test_count__ += 1
        self.__running__ = False
        return None


class LoopThread(ThreadBase):
    """
        - threadの生成
        - 停止の判定
    """

    def __init__(self, threadable_function, conditions, condition_name, states, willchange_state_names, option=None):
        super().__init__(threadable_function, conditions,
                         condition_name, states, willchange_state_names, option=None)
