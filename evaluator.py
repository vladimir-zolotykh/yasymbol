#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatchmethod
from node import Node, Num, BinOp
from parser import Parser


class Evaluator1:
    def eval(self, n: Node) -> float:
        return n.eval()


class Evaluator2:
    @singledispatchmethod
    def eval(self, n) -> float:
        raise NotImplementedError(f"Found no eval metod for {type(n).__name__}")

    @eval.register(Num)
    def _(self, n: Num) -> float:
        return n.eval()

    @eval.register(BinOp)
    def _(self, n: BinOp) -> float:
        return n.eval()


if __name__ == "__main__":
    print(Evaluator1().eval(Parser().parse("2 + (3 * 4) + 5")))
    print(Evaluator2().eval(Parser().parse("2 + (3 * 4) + 5")))
