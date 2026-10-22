"""
Trap checks, JEE Main 2026 Session 2, 6 Apr Shift 2 (pyq/2026/06Apr_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from math import comb

from trap_checks.common import Rational


def checks():
    c = {}
    c[(7, 4)] = lambda: (comb(9, 4) * 10 * 9, 11340)                         # all 10 floors allowed (1st and 2nd not excluded)
    c[(26, 2)] = lambda: (1 * 2, 2)                                          # error in d reported as the error in V (power 3 ignored)
    c[(38, 4)] = lambda: (round(2e-7 * 30 / 0.04 * 1e6) - round(2e-7 * 30 / 0.04 * 1e6), 0)   # the two wires' fields subtracted (as for parallel currents)
    c[(38, 3)] = lambda: (round(2e-7 * 30 / 0.04 * 1e6), 150)                # one wire only
    c[(41, 3)] = lambda: (round(4 * 7.2 - 2 * 1.1, 6), 26.6)                 # 1.1 MeV used per deuteron instead of per nucleon
    return c
