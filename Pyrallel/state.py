
import threading
import time


class States:
    """
        a
    """

    def __init__(self, states, conditions):
        """
            states={"count":0,"stock":[]}
        """
        # {"state_name":[(condition_name,changer1),changer2,...]}
        self.__state_names__ = []
        self.__map_state_to_condition__ = {}
        for state_name in states:
            setattr(self, state_name, states[state_name])
            self.__map_state_to_condition__[state_name] = []
            self.__state_names__.append(state_name)
        self.__conditions__ = conditions

    def __accept_state_updated__(self, changed_state_names):
        for state_name in changed_state_names:
            for condition_name, condition_changer in self.__map_state_to_condition__.get(state_name):
                self.__conditions__.__change_condition__(
                    condition_name,
                    condition_changer(self)
                )
        return None

    def __register_state_to_condition__(self, condition_name, changer_function, *state_names):
        """
            register __map_state_to_condition__
        """
        for state_name in state_names:
            self.__map_state_to_condition__[state_name].append(
                (condition_name, changer_function))
        print(self.__map_state_to_condition__)

    def __show_values__(self):
        print("\n---state show---")
        for name in self.__state_names__:
            print(name, " : ", getattr(self, name))
        print("---state show---\n")
