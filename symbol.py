#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re


class Symbol:
    _instances = {}

    def __new__(cls, name, pat):
        if name not in cls._instances:
            sym = cls._instances[name] = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            # print(f"Initializing {cls.__name__}({name})")
        return cls._instances[name]

    @classmethod
    def masterpat(cls):
        return "|".join(
            f"(?P<{name}>{sym.pat})" for name, sym in cls._instances.items()
        )
        return cls._instances


for name, pat in (
    ("NAME", r"[A-Za-z_]\w*"),
    ("NUM", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WS", r"\s+"),
):
    Symbol(name, pat)


class Token:
    def __init__(self, sym: Symbol, val: float | str | None):
        self.sym = sym
        self.val = val

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.sym == other.sym and self.val == other.val
        elif isinstance(other, str):
            return self.sym.name == other
        else:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self.sym}, {self.val!r})"


def iter_tokens(sexpr: str, masterpat=Symbol.masterpat()) -> Iterator[Token]:
    for tok in re.find_iter(masterpat, sexpr):
        if tok.lastgroup == Symbol("WS"):
            continue
        yield Token(Symbol(tok.lastgroup, tok.group(0)))


if __name__ == "__main__":
    for tok in iter_tokens(""):
        print(tok)
