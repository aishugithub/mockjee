"""
Trap checks, JEE Main 2026 Session 2, 6 Apr Shift 1 (pyq/2026/06Apr_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from math import comb

from trap_checks.common import Matrix, Rational, sqrt


def checks():
    c = {}
    c[(8, 3)] = lambda: (Rational(comb(28, 14), comb(26, 13)), Rational(27, 7))     # ratio inverted
    c[(9, 3)] = lambda: (Rational(2500 - 100, 20 * 20) / (Rational(2500 + 100, 2 * 20) - 25 - 36), Rational(3, 2))   # mean : variance

    def q12_2():
        fp, fq = Matrix([0, 6]), Matrix([9, 12])
        return fp.dot(fq) / (fp.norm() * fq.norm()), Rational(4, 5)           # cos α given instead of sin α
    c[(12, 2)] = q12_2
    c[(26, 3)] = lambda: (round((0.02 / 97.42 + 0.05 / 8.35 + 0.02 / 20.20) * 100, 2), 0.72)   # d's error counted once
    c[(32, 3)] = lambda: (2 + Rational(3 - 1, 2), 3)                         # mv²/R = N − mg: v² = 2gR, h = 2R + R
    c[(36, 1)] = lambda: (Rational(3, 4) / Rational(1, 4), 3)                # I_B/I_A
    c[(37, 2)] = lambda: (5 * Rational(1, 4), Rational(5, 4))                # T/4 (A to the mean position) instead of T/8
    c[(41, 2)] = lambda: ((1 / (Rational(2, 5) - Rational(1, 4)) * Rational(7, 5)) / 4, Rational(7, 3))   # m = v/u, refractive indices left out
    c[(43, 2)] = lambda: ((1 - Rational(4, 10)) / (1 - Rational(2, 10)), Rational(3, 4))   # V at 4 mA over V at 2 mA
    c[(44, 1)] = lambda: ((Rational(3, 16) / Rational(5, 36)), Rational(27, 20))   # ratio inverted
    c[(57, 3)] = lambda: ((round(1 * 0.082 * 400 / 10, 3), round(0.2 * 1 * 0.082 * 400 / 10, 3)), (3.28, 0.656))   # A’s pressure, not B’s
    c[(73, 5)] = lambda: (round(4.7 / 94 * 100), 5)                          # 60% completion ignored
    return c
