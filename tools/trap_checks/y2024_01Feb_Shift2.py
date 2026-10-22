"""
Trap checks, JEE Main 2024 Session 1, 1 Feb Shift 2 (pyq/2024/01Feb_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational


def S(n, a=3, d=8):
    return Rational(n, 2) * (2 * a + (n - 1) * d)


def checks():
    c = {}
    c[(7, 3)] = lambda: (S(15), 885)                                          # S15 alone, S5 not subtracted
    c[(37, 3)] = lambda: (Rational(1000, 1) ** Rational(1, 3), 10)             # ratio inverted: small drops : big drop
    c[(40, 1)] = lambda: (Rational(2, 1) / 3, Rational(2, 3))                  # C2 taken to enclose only its own 3Q (2Q inside not added)
    c[(45, 1)] = lambda: (round(__import__('math').degrees(__import__('math').asin(2 / 4))), 30)   # half-angle θ given, not the spread 2θ
    return c
