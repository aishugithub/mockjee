"""Shared helpers for the per-shift trap checks (see tools/verify_traps.py)."""
from fractions import Fraction
from itertools import product

from sympy import Matrix, Rational, Symbol, expand, limit, log, nsimplify, pi, simplify, sin, solve, sqrt, symbols, cos

x = Symbol('x')
