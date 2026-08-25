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
            return decorate

        return func

    @wraps(func)
    def wrapper(num):
        try:
            res = dir[num](num)
        except KeyError:
            res = iswhat(num)
        return res

    wrapper.register = register
    return wrapper


@parmdispatch
def iswhat(num):
    print(f"{num} is something else")


@iswhat.register(2, 4, 6)
def _(num):
    print(f"{num} is even")


@iswhat.register(1, 5)
def _(num):
    print(f"{num} is odd")


if __name__ == "__main__":
    iswhat(1)
    iswhat(4)
    iswhat(100)
