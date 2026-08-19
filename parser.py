#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import builtins
from functools import wraps

# import inspect
from node import Node, Num, Plus, Minus, Mul, Div
from symbol import Symbol, Token, iter_tokens


def next(iterable: Iterator[Token], default: Token | None) -> Token | None:
    res = builtins.next(iterable, default)
    # caller = inspect.currentframe().f_back
    # print(f"*** {caller.f_code.co_name}->next->{res}")
    return res


def show(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        depth = getattr(self, "_depth", 0)
        print("    " * depth, f"{func.__name__}")
        # print(f"{func.__name__}")
        setattr(self, "_depth", depth + 1)
        res = func(*args, **kwargs)
        setattr(self, "_depth", depth)
        return res

    return wrapper


class Parser:
    def __init__(self):
        pass

    def parse(self, sexpr) -> Node:
        self.tokens: Iterator[Token] = iter_tokens(sexpr)
        self.tok: Token = self._advance()
        return self.expr()

    @show
    def expr(self) -> Node:
        res = self.term()
        while (op := self.tok) and op.sym in ("PLUS", "MINUS"):
            self._consume()
            right = self.term()
            res = Plus(res, right) if op == "PLUS" else Minus(res, right)
        return res

    @show
    def term(self) -> Node:
        res = self.factor()
        while (op := self.tok) and op.sym in ("MUL", "DIV"):
            self._consume()
            right = self.factor()
            res = Mul(res, right) if op == "MUL" else Div(res, right)
        return res

    @show
    def factor(self) -> Node:
        if self.tok.sym == "LPAREN":
            self._consume()
            res = self.expr()
            self._expect("RPAREN")
        else:
            res = Num(self.tok.val)
            self._consume
        return res

    def _advance(self) -> Token:
        self.tok = next(self.tokens, None)
        return self.tok

    def _consume(self) -> None:
        self.tok = next(self.tokens, None)

    def _expect(self, expected: Symbol) -> None:
        if self.tok.sym != expected:
            raise SyntaxError(f"{expected!r} expected, got {self.tok.sym!r}")
        self.tok = next(self.tokens, None)


if __name__ == "__main__":
    n: Node = Parser().parse("2 + (3 * 4) + 5")
    n: Node = Parser().parse("2")
    n: Node = Parser().parse("2 + 3")
    print(n)
