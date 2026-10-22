"""
Trap checks, JEE Main 2024 Session 1, 31 Jan Shift 2 (pyq/2024/31Jan_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, sqrt


def checks():
    c = {}
    c[(9, 1)] = lambda: (0 + 1, 1)                                            # lim f(5x)/f(x) = 1 given, the −1 forgotten (answer 0 + 1)
    c[(19, 2)] = lambda: (Rational(1, 3)**2 * Rational(2, 3), Rational(2, 27))   # one order (TTH) only, C(3,2) = 3 forgotten
    c[(36, 1)] = lambda: (sqrt(Rational(1, 144)), Rational(1, 12))            # v ∝ √M, the radius ignored
    c[(37, 4)] = lambda: (2**2, 4)                                            # v ∝ r² (same density) instead of same mass
    c[(39, 1)] = lambda: (8 * Rational(3, 2) + 6 * Rational(3, 2), 21)        # O2 taken as monatomic (3/2 RT per mole)
    c[(40, 4)] = lambda: (1 / Rational(1, 5)**2, 25)                          # dielectric constant ignored
    c[(40, 1)] = lambda: (1 / Rational(5) * 1, Rational(1, 5))                 # F/K only, distance change to r/5 ignored
    c[(57, 36)] = lambda: ((2 + 4)**2, 36)                                    # perpendicular fields added as numbers: 2 + 4 = 6 mT
    return c
