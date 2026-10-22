"""
Trap checks, JEE Main 2026 Session 2, 5 Apr Shift 2 (pyq/2026/05Apr_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational


def checks():
    c = {}
    c[(2, 3)] = lambda: ((-5)**2 + (-2)**2, 29)                              # |z2|² only (z2 = −5 − 2i)
    c[(27, 2)] = lambda: (10 / 5, 2)                                         # R itself, not its error
    c[(29, 2)] = lambda: ((Rational(1, 2) * 20 * 5, Rational(1, 2) * 20 * 5 - Rational(1, 2) * 20 * 5), (50, 0))   # distance = one triangle; displacement 50 − 50
    c[(29, 4)] = lambda: ((2 * Rational(1, 2) * 20 * 5, Rational(100, 40)), (100, Rational(5, 2)))   # average speed as velocity
    c[(30, 3)] = lambda: (Rational(16, 4), 4)                                # total angle in 4 s over θ1
    c[(30, 4)] = lambda: (Rational(4, 12), Rational(1, 3))                   # θ1/θ2
    c[(32, 1)] = lambda: (Rational(1, 1) / (1 + 1), Rational(1, 2))          # mgh/(1 + h/R) with h = R, not 2R
    c[(37, 2)] = lambda: (Rational(2, 8) * 6, Rational(3, 2))                # voltage across the 6 Ω
    c[(43, 1)] = lambda: (1 + 0.2, 1.20)                                     # λ taken to rise by the same 20%
    c[(57, 4)] = lambda: (1 / Rational(4, 59) * Rational(1, 10), Rational(59, 40))   # the fraction 4/5.9 inverted
    c[(71, 19)] = lambda: (3 + 4 + 5 + 4 + 3, 19)                            # d4 and d7 taken as high spin
    c[(75, 640)] = lambda: (240 * Rational(4, 1) / Rational(3, 2), 640)      # t½ taken as ∝ 1/[A]0
    return c
