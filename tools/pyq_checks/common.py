"""Shared helpers for the per-shift answer checks (see tools/verify_pyq_solutions.py)."""
import math
from fractions import Fraction
from itertools import product

from sympy import (Matrix, Rational, Symbol, cos, diff, exp, expand, integrate, limit, log, nsimplify,
                   pi, simplify, sin, solve, sqrt, symbols, tan, factor)

x = Symbol('x')


def opt(value, options):
    """1-based position of value among the options (exact comparison after simplify; floats within 1e-9)."""
    same = lambda o: abs(value - o) < 1e-9 if isinstance(value, float) else simplify(value - o) == 0
    hits = [i for i, o in enumerate(options, 1) if same(o)]
    assert len(hits) == 1, (value, options)
    return hits[0]


def nearest(value, options):
    """1-based position of the option closest to a computed float (for rounded numeric options)."""
    return min(range(1, len(options) + 1), key=lambda i: abs(float(options[i - 1]) - float(value)))
