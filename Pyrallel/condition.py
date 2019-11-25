"""
    a
"""


class ConditionHandler:
    """
        a
    """

    def __init__(self, conditions):
        """
            conditions={}
        """
        self.__condition_to_thread__ = {}
        self.__condition_names__ = []
        for condition_name in conditions:
            setattr(self, condition_name, conditions[condition_name])
            self.__condition_to_thread__[condition_name] = []
            self.__condition_names__.append(condition_name)

    def __register_thread__(self, condition_name, thread_object):
        self.__condition_to_thread__[condition_name].append(thread_object)

    def __change_condition__(self, condition_name, new_condition):
        if getattr(self, condition_name) == new_condition:
            return None
        if new_condition:
            print("\nnew thread!!! ", condition_name)
            print(self.__condition_to_thread__[condition_name])
            #新しいthreadを作成 & 起動
            setattr(self, condition_name, new_condition)
            for each_thread in self.__condition_to_thread__[condition_name]:
                print(each_thread.__threadable_function__)
                each_thread.__activate__()
        setattr(self, condition_name, new_condition)

    def __start__(self):
        print("in start")
        print(self.__condition_to_thread__)
        for condition_name in self.__condition_names__:
            if not getattr(self, condition_name):
                continue
            for each_thread in self.__condition_to_thread__[condition_name]:
                each_thread.__activate__()

    def __destory__(self):
        for condition_name in self.__condition_names__:
            print("destory", condition_name)
            setattr(self, condition_name, False)
            del(self.__condition_to_thread__[condition_name])
        print("destory id : ", id(self))
        self.__show_values__()

    def __show_values__(self):
        print("\n---condition show---")
        print("this id is ", id(self))
        for condition_name in self.__condition_names__:
            print(condition_name, " : ", getattr(self, condition_name))
        print("---condition show---\n")
