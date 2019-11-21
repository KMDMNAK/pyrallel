"""
Task:
A -> checkValue? B : C

"""

import time
import threading
import logging

# ログの出力名を設定（1）
logger = logging.getLogger('LoggingTest')

# ログレベルの設定（2）
logger.setLevel(10)

# ログのコンソール出力の設定（3）
logger.addHandler(logging.StreamHandler())

# ログのファイル出力先を設定（4）
logger.addHandler(logging.FileHandler('debug.log', mode="w"))


class States:
    def __init__(self, states):
        """
            states={"count":0,"stock":[]}
        """
        self.state_names = []
        for state_name in states.keys():
            setattr(self, state_name, states[state_name])
            self.state_names.append(state_name)


class Framework:
    def __init__(self, states, conditions, loop_interval=None):
        self.states = States(states)
        self.__conditions__ = {"__event_watcher__": True}
        self.__conditions__.update(conditions)
        self.__condition_trigger_functions__ = {}
        # not recommended set to None
        self.__while_interval__ = loop_interval

        for condition_name in self.__conditions__.keys():
            self.__condition_trigger_functions__[condition_name] = []

        self.__state_change_condition__ = {}
        for state_name in self.states.state_names:
            self.__state_change_condition__[state_name] = []

        self.__state_change_queue__ = []
        self.__active_threads__ = []

    def thread(self, condition_name, *state_names):
        """
            decolate for threadable function.

            if condition is True ,
            create a thread of threadable function
            ,or keep going the threading untill it's True

        """
        def decolator_wrapper(threadable_function):
            self.__condition_trigger_functions__[condition_name].append(
                [threadable_function, *state_names]
            )
            return threadable_function
        return decolator_wrapper

    def condition_changer(self, condition_name, *state_names):
        """
            decolate for functions that change condition
        """
        def decolator_wrapper(threadable_function):
            for state_name in state_names:
                self.__state_change_condition__[state_name].append(
                    (condition_name, threadable_function, state_names))
            return threadable_function
        return decolator_wrapper

    def set_states(self, new_state):
        changed_keys = []
        for key in new_state.keys():
            value = new_state[key]
            if value is getattr(self.states, key):
                continue

            setattr(self.states, key, value)
            changed_keys.append(key)
        self.__dispatch_states_change__(changed_keys)
        return None

    def add_active_thread(self, thread):
        """
            activeなthreadをstockする.
            TODO 重複するthreadの処理
        """
        self.__active_threads__.append(thread)
        return None

    def run(self, runnning_time=None):

        print(self.__condition_trigger_functions__)
        print(self.__state_change_condition__)

        t = self.__create_thread__(
            "__event_watcher__",
            self.__change_conditions_thread__
        )
        self.add_active_thread(t)
        for condition_name in self.__conditions__:
            self.__create_or_throught_threads__(condition_name)

        while True:
            try:
                if runnning_time:
                    logger.log(10, "in running time")
                    time.sleep(runnning_time)
                    logger.log(10, "end runnning_time")
            except KeyboardInterrupt:
                break
            time.sleep(1)
        self.release_threads()

    def release_threads(self):
        """
            stop all threads
        """
        for condition_name in self.__conditions__:
            self.__conditions__[condition_name] = False

    def __create_or_throught_threads__(self, condition_name):
        """
            FOR LOOP FUNCTION
            Returs
            None
        """
        condition = self.__conditions__.get(condition_name)

        if condition is None:
            raise BaseException("given condition doesn't exist")

        if not condition:
            return None

        for threadable_function, *args in self.__condition_trigger_functions__[condition_name]:
            print("create or throught args")
            print(args)
            t = self.__create_thread__(
                condition_name, threadable_function, *args
            )
        return None

    def __create_thread__(self, condition_name, threadable_function, *state_names):
        """
            threadable functionに対してconditionに基づくthreadを生成する.
        """

        def __threading__(self):
            while self.__conditions__[condition_name]:
                new_states = threadable_function(self.states)
                if not new_states:
                    continue
                self.set_states(new_states)
                if self.__while_interval__:
                    print("thread is sleeping")
                    time.sleep(self.__while_interval__)

        t = threading.Thread(
            target=__threading__,
            args=(self,)
        )
        t.start()
        self.add_active_thread(t)
        return t

    def __dispatch_states_change__(self, keys):
        """
            変更されたstateの名前をキューに保存
        """
        for key in keys:
            self.__state_change_queue__.append(key)
        return None

    def __change_conditions_thread__(self, states):
        if not self.__state_change_queue__:
            return None
        queue, self.__state_change_queue__ = self.__state_change_queue__, []
        for changed_state_name in queue:
            for condition_name, changer, all_args_states in self.__state_change_condition__[changed_state_name]:
                self.__change_state_handler__(
                    condition_name,
                    changer,
                    all_args_states
                )
        print("active threads: ", self.__active_threads__)
        return None

    def __change_state_handler__(self, condition_name, changer, all_args_states):
        """
            this function is for FOR LOOP
        """
        new_condition = changer(self.states)
        if self.__conditions__[condition_name] == new_condition:
            return None
        logger.log(10, "condition changed : {0} to {1}".format(
            condition_name, new_condition))
        self.__conditions__[condition_name] = new_condition
        self.__create_or_throught_threads__(condition_name)
