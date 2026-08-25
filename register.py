#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from functools import wraps


def parmdispatch(func):
    dir: dict[int, Callable] = {}

    def register(*values):
        def decorate(func):
            for val in values:
                dir[val] = func
            return func

        return decorate

    @wraps(func)
    def wrapper(num):
        try:
            res = dir[num](num)
        except KeyError:
            res = f"{num} is something else"
        return res

    wrapper.register = register
    return wrapper


@parmdispatch
def iswhat(num):
    return f"{num} is something else"


@iswhat.register(2, 4, 6)
def _(num):
    return f"{num} is even"


@iswhat.register(1, 5)
def _(num):
    return f"{num} is odd"


if __name__ == "__main__":
    print(iswhat(1))
    print(iswhat(4))
    print(iswhat(100))
