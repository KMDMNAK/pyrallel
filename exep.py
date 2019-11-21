
import threading
import time
import random


class states:
    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, random.random())


class A:
    def __init__(self):
        self.__funcs__ = []
        self.states = states("a")

    def execute(self):
        for func in self.__funcs__:
            t = threading.Thread(target=func, args=(self.states,))
            t.start()
        time.sleep(2)
        print(self.states.a)
        self.states.a = 1000

    def dec(self, func):
        self.__funcs__.append(func)
        return func


AC = A()


@AC.dec
def test(states):
    time.sleep(5)
    print(states.a)


class B:
    def __init__(self):
        setattr(self, "a", 10)
        setattr(self, "b", getattr(self, "a"))
        
    def get(self):
        print(self.a)
        print(self.b)

        self.a = 0
        print(self.a)
        print(self.b)


if __name__ == "__main__":
    AC = A()
    setattr(AC.states,"a",532545)
    AC.execute()
    
