#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import operator


class Node:
    def __init__(self, val):
        self.val = val


class Num(Node):
    def __init__(self, val: float):
        assert isinstance(val, float)
        super().__init__(val)

    def eval(self) -> float:
        return self.val

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.val == other.val
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val})"


class BinOp(Node):
    node_map = {}

    def __init__(self, left: Node, right: Node):
        super().__init__(None)
        self.left = left
        self.right = right

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BinOp.node_map = BinOp.get_node_map()

    @staticmethod
    def get_node_map():
        return {sub: sub.__map__ for sub in BinOp.__subclasses__()}

    def eval(self) -> float:
        op = BinOp.node_map[type(self)][1]
        return getattr(operator, op)(self.left.eval(), self.right.eval())

    def __eq__(self, o) -> bool:
        if isinstance(o, type(self)):
            return self.left == o.left and self.right == o.right
        else:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"


def make_binop(op: str, left, right) -> BinOp:
    for cls, tup in BinOp.node_map.items():
        if tup[0] == op:
            return cls(left, right)


class Plus(BinOp):
    __map__ = ("+", "add")


class Minus(BinOp):
    __map__ = ("-", "sub")


class Mul(BinOp):
    __map__ = ("*", "mul")


class Div(BinOp):
    __map__ = ("/", "truediv")
