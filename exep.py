
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
        print(self.__funcs__)
        for func in self.__funcs__:
            t = threading.Thread(target=func, args=(self.states,))
            t.start()
        time.sleep(2)
        print(self.states.a)
        self.states.a = 1000

    def dec(self, func):
        print(func)
        self.__funcs__.append(func)
        print(self.__funcs__)
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


class C:
    """
        property x,yを監視
    """

    def __init__(self):
        self._x = []
        self._y = 0

    @property
    def x(self):
        return self._x

    @x.getter
    def x(self):
        print("get", self._x)
        return self._x

    @x.setter
    def x(self, value):
        self._x.append(value)
        print("set", self._x)

    @property
    def y(self):
        return self._y


class D:
    def __init__(self):
        pass

    def execute(self, states):
        def thread(states):
            while states.isRunning:
                print("runnning!!")
                time.sleep(1)
            print("end")
        t = threading.Thread(target=thread, args=(states,))
        t.start()


class D_cond:
    def __init__(self):
        self.isRunning = True

    def changer(self):

        while True:
            time.sleep(3)
            self.isRunning = not self.isRunning


if __name__ == "__main__":
    """
        state自体を渡せば,引数をreactiveに渡せる.
    setattr(AC.states, "a", 532545)
    AC.execute()
    """
    d = D()
    d_c = D_cond()
    d.execute(d_c)
    d_c.changer()
