"""
Trap checks, JEE Main 2026 Session 2, 5 Apr Shift 1 (pyq/2026/05Apr_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, sqrt


def checks():
    c = {}
    c[(5, 3)] = lambda: (528 * (Rational(1, 2) - Rational(1, 132)), 260)     # forgot the ½ in the partial fractions
    c[(9, 4)] = lambda: (4 * Rational(12, 5), Rational(48, 5))               # OS × |α| without the ½
    d = lambda: sqrt((3 - (-3))**2 + (4 - (-4))**2)                          # circle centre (3, 4) to vertex (−3, −4)
    c[(10, 1)] = lambda: (d() - 2, 8)                                        # minimum (d − r) instead of maximum
    c[(10, 2)] = lambda: (d(), 10)                                           # distance to the centre, radius not added
    c[(28, 3)] = lambda: (2 * 16 / 6400 * 100, 0.50)                         # above: 2h/R; below: no change counted
    c[(28, 4)] = lambda: (3 * 16 / 6400 * 100, 0.75)                         # 2h/R above plus h/R below, added
    c[(29, 3)] = lambda: (Rational(240, 7) / Rational(400, 7), Rational(3, 5))   # T2/T1 instead of T1/T2
    c[(39, 4)] = lambda: (round(2.4 * 1.2, 6), 2.88)                         # multiplied by μ instead of dividing
    c[(43, 1)] = lambda: (960 / 10 - 40, 56)                                 # upper wire only
    c[(51, 1)] = lambda: (round(2.76 / 276 * 108, 6), 1.08)                  # one Ag per Ag2CO3
    c[(54, 2)] = lambda: (round((10 / 60) / (10 / 60 + 90 / 18), 3), 0.032)  # mole fraction of urea, not water
    return c
