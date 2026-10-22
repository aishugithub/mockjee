"""
Trap checks, JEE Main 2024 Session 1, 27 Jan Shift 1 (pyq/2024/27Jan_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, log, sqrt


def checks():
    c = {}
    # Q7: common terms 9, 24, 39, ... must be ≤ 124 (25th term of the first AP) and ≤ 111 (37th term of the second)
    c[(7, 3)] = lambda: (len([t for t in range(9, 125, 15)]), 8)              # 111 limit of the second AP ignored

    def trisect():
        return (Rational(4, 3) / Rational(10, 3), Rational(8, 3) / Rational(5, 3))   # slopes of L1, L2
    c[(15, 1)] = lambda: (trisect()[0], Rational(2, 5))                       # slope of one line given
    c[(15, 2)] = lambda: (trisect()[1], Rational(8, 5))                       # slope of the other line given
    c[(20, 4)] = lambda: (sqrt(Rational(50**2 - 1100, 10) - 5**2), sqrt(115))   # Σa² = 2500 − 1100 (factor 2 on Σ a_k a_j dropped)
    c[(36, 2)] = lambda: (Rational(1, 2) ** 2, Rational(1, 4))                # g ∝ R² instead of 1/R²
    c[(36, 4)] = lambda: (1 / Rational(1, 2), 2)                              # g ∝ 1/R instead of 1/R²
    c[(41, 1)] = lambda: (1 / (5 * (1 / Rational(1))), Rational(1, 5))        # each piece taken as R (not R/5), five in parallel
    c[(44, 2)] = lambda: (round(8.85e-12 * 3e8 * 200**2, 1), 106.2)           # I = cε0E0² (the ½ dropped)
    c[(44, 3)] = lambda: (round(0.25 * 8.85e-12 * 3e8 * 200**2, 1), 26.6)     # I = cε0E0²/4
    c[(47, 1)] = lambda: (Rational(3, 4) ** 2, Rational(9, 16))               # r ∝ n², ratio inverted: (3/4)² instead of (4/3)²
    c[(47, 3)] = lambda: (Rational(4, 1) / 3, Rational(4, 3))                  # r ∝ n instead of n²
    c[(57, 0)] = lambda: (round(2e-7 * 10 / 0.025 * 1e6) - round(2e-7 * 10 / 0.025 * 1e6), 0)   # the two fields subtracted
    c[(57, 80)] = lambda: (round(2e-7 * 10 / 0.025 * 1e6), 80)                # one wire only
    c[(81, 32)] = lambda: (Rational(44, 22) * 16, 32)                          # mole ratio inverted: 44/22 instead of 22/44
    c[(82, 32)] = lambda: (2 + 6 + 10 + 14, 32)                               # spin condition ignored: all electrons in n = 4
    c[(84, 3034)] = lambda: (round(float(3 * 8.314 * 300 * log(Rational(45, 30)))), 3034)   # reversible formula nRT ln(V2/V1)
    c[(86, 54)] = lambda: (round(5.6 / 22.4 * 2 * 108), 54)                   # 2 electrons per O2 (as for H2) instead of 4
    return c
