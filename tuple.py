#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import re
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, ns):
        fields = ns.get("_fields", [])
        for n, fname in enumerate(fields):
            setattr(cls, fname, property(itemgetter(n)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls.__name__} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def test_person():
    bob = Person("Bob", 37, 12000)
    assert (bob.name, bob.age, bob.salary) == ("Bob", 37, 12000)
    assert str(bob) == "('Bob', 37, 12000)"


def test_person_error():
    with pytest.raises(TypeError, match=re.escape("gets exactly 3 arguments")):
        Person("Bob", 37)


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob.name, bob.age, bob.salary)
