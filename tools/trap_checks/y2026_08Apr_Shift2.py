"""
Trap checks, JEE Main 2026 Session 2, 8 Apr Shift 2 (pyq/2026/08Apr_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational


def checks():
    c = {}
    c[(31, 3)] = lambda: (10 * 5 * 10 // 1, 500)                             # R = gT1T2 (the ½ dropped)
    c[(34, 1)] = lambda: (Rational(64, 1) ** Rational(1, 3), 4)              # v ∝ r, not r²: ratio of radii 4
    c[(36, 2)] = lambda: (-(Rational(1, 9) - 1) * Rational(3, 2), Rational(4, 3))   # sign lost: ΔU = (PV − P2V2)/(γ − 1)
    return c
