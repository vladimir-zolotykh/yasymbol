#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType
from instance import signature, _empty
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class Method:
    def __init__(self, name, func) -> None:
        self.methods = {}
        self._name = name
        self.register(func)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return MethodType(self, instance)

    def register(self, func):
        sig = signature(func)
        typ = tuple()
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is _empty:
                raise TypeError(f"{name!r} all parms must have annotation")
            if parm.default is not _empty:
                self.methods[typ] = func
            typ = typ + (typ, parm.annotation)
        self.methods[typ] = func

    def __call__(self, *args, **kwargs):
        typ = (type(a) for a in args[1:])
        return self.methods[typ](*args, **kwargs)


class MultiDict(dict):
    def __setitem__(self, key, val) -> None:
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
            return
        mm = self.setdefault(key, Method())
        mm.register(val)
        super().__setitem__(key, mm)


class EvalMeta(type):
    def __prepare__(mcls, cls, bases, ns):
        return MultiDict()


class Evaluator(metaclass=EvalMeta):
    def eval(self, n: Num) -> float:
        return float(n.val)

    def eval(self, n: Plus) -> float:  # noqa: F811
        return self.eval(n.left) + self.eval(n.right)

    def eval(self, n: Minus) -> float:  # noqa: F811
        return self.eval(n.left) - self.eval(n.right)

    def eval(self, n: Mul) -> float:  # noqa: F811
        return self.eval(n.left) * self.eval(n.right)

    def eval(self, n: Div) -> float:  # noqa: F811
        return self.eval(n.left) / self.eval(n.right)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: Node = Parser().parse(sexpr)
    assert Evaluator().eval(n) == eval(sexpr)
