#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable, get_args
from types import MethodType
from inspect import signature, _empty
from node import Node, Num, BinOp, Plus, Minus, Mul, Div
from parser import Parser


class MultiMethod:
    def __init__(self) -> None:
        self.methods: dict[tuple[type, ...], Callable] = {}

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
            if args := get_args(parm.annotation):
                for utyp in args:
                    self.methods[typ + (utyp,)] = func
            else:
                typ = typ + (parm.annotation,)

        self.methods[typ] = func

    def __call__(self, *args, **kwargs):
        typ = tuple(type(a) for a in args[1:])
        try:
            return self.methods[typ](*args, **kwargs)
        except KeyError:
            for ktyp, func in self.methods.items():
                if issubclass(typ[0], ktyp[0]):  # issubclass(Plus, BinOp)
                    return func(*args, **kwargs)


class MultiDict(dict):
    def __setitem__(self, key, val) -> None:
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
            return
        mm = self.setdefault(key, MultiMethod())
        mm.register(val)
        super().__setitem__(key, mm)


class EvalMeta(type):
    @classmethod
    def __prepare__(mcls, cls, bases, /, **ns):
        return MultiDict()


class Evaluator1(metaclass=EvalMeta):
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


class Evaluator2(metaclass=EvalMeta):
    def eval(self, n: Num) -> float:
        return float(n)

    def eval(self, n: BinOp) -> float:  # noqa: F811
        return float(n)


class Evaluator3(metaclass=EvalMeta):
    def eval(self, n: Num | BinOp) -> float:
        return float(n)


class Evaluator4(metaclass=EvalMeta):
    def eval(self, n: Num | Plus | Minus | Mul | Div) -> float:
        return float(n)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: Node = Parser().parse(sexpr)
    assert Evaluator1().eval(n) == eval(sexpr)
    assert Evaluator2().eval(n) == eval(sexpr)
    assert Evaluator3().eval(n) == eval(sexpr)
    assert Evaluator4().eval(n) == eval(sexpr)
