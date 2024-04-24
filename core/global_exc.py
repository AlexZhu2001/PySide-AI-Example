import sys
from typing import Callable


class ExceptHooks:
    hook_functions = []

    @classmethod
    def register(cls, func: Callable) -> int:
        cls.hook_functions.append(func)
        return len(cls.hook_functions) - 1

    @classmethod
    def deregister(cls, id):
        if 0 <= id <= len(cls.hook_functions):
            del cls.hook_functions[id]

    @classmethod
    def except_hook(cls, ttype, tvalue, ttraceback):
        for f in cls.hook_functions:
            f(ttype, tvalue, ttraceback)


def init_except(default=True):
    default_hook = sys.excepthook
    sys.excepthook = ExceptHooks.except_hook
    if default:
        ExceptHooks.register(default_hook)
