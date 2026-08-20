#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    def __init__(self, val):
        self.val = val


class Num(Node):
    def __init__(self, val: float):
        super().__init__(val)

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.val == other.val
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val})"


class BinOp(Node):
    def __init__(self, left: Node, right: Node):
        op = {"Plus": "+", "Minus": "-", "Mul": "*", "Div": "/"}[type(self).__name__]
        super().__init__(op)
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return (
                super().__eq__(other)
                and self.left == other.left  # noqa: W503
                and self.right == other.right  # noqa: W503
            )
        else:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"


class Plus(BinOp):
    pass


class Minus(BinOp):
    pass


class Mul(BinOp):
    pass


class Div(BinOp):
    pass
