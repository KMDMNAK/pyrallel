"""
Task:
A -> checkValue? B : C

"""

import time
import threading
import logging
from .state import States
from .condition import ConditionHandler as Condition
from .thread import multiplyThread, LoopThread

# ログの出力名を設定（1）
logger = logging.getLogger('LoggingTest')

# ログレベルの設定（2）
logger.setLevel(10)

# ログのコンソール出力の設定（3）
logger.addHandler(logging.StreamHandler())

# ログのファイル出力先を設定（4）
logger.addHandler(logging.FileHandler('debug.log', mode="w"))


class Framework:
    def __init__(self, states, conditions, loop_interval=None):
        self.__conditions__ = Condition(conditions)
        self.__states__ = States(states, self.__conditions__)
        self.__while_interval__ = loop_interval
        self.__threads__ = []

    def loop(self, condition_name, *state_names, option=None):
        """
            decolate for threadable function.

            if condition is True ,
            create a thread of threadable function
            ,or keep going the threading untill it's True

        """
        def decolator_wrapper(threadable_function):
            """
            print("in decolator loop")
            print(threadable_function,
                  self.__conditions__,
                  condition_name,
                  self.__states__,
                  state_names)
            """
            print("in decolate ", condition_name)
            self.__conditions__.__register_thread__(
                condition_name,
                LoopThread(
                    threadable_function=threadable_function,
                    conditions=self.__conditions__,
                    condition_name=condition_name,
                    states=self.__states__,
                    willchange_state_names=state_names,
                    option=option
                )
            )
            return threadable_function
        return decolator_wrapper

    def multiply(self, condition_name, *state_names, option=None):
        def decolator_wrapper(threadable_function):
            print(option)
            self.__conditions__.__register_thread__(
                condition_name,
                multiplyThread(
                    threadable_function,
                    self.__conditions__,
                    condition_name,
                    self.__states__,
                    state_names,
                    option=option
                )
            )
            return threadable_function
        return decolator_wrapper

    def change_condition(self, condition_name, *state_names):
        """

        """
        def decolator_wrapper(changer_function):
            self.__states__.__register_state_to_condition__(
                condition_name,
                changer_function,
                *state_names
            )
            return changer_function
        return decolator_wrapper

    def run(self, runnning_time=None):
        self.__conditions__.__start__()
        try:
            while True:
                if runnning_time:
                    logger.log(10, "in running time")
                    time.sleep(runnning_time)
                    logger.log(10, "end runnning time")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nkey board interrupt\n")

        self.release_threads()

    def release_threads(self):
        """
            stop all threads
        """
        self.__conditions__.__destory__()
