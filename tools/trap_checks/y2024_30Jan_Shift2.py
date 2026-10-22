"""
Trap checks, JEE Main 2024 Session 1, 30 Jan Shift 2 (pyq/2024/30Jan_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, sqrt


def checks():
    c = {}
    c[(9, 2)] = lambda: ((4 + 3)**2 * (4 - 2)**3, 392)                       # M = f(4) alone, m not subtracted
    c[(11, 4)] = lambda: (Rational(3 + 2, 3 - 2), 5)                          # sign slip: tan α = +5 tan β
    c[(15, 1)] = lambda: (9 * (1 + Rational(2**2, 4)), 18)                    # x² alone, y² not added to OP²
    c[(18, 2)] = lambda: (2**2 - 1**2, 3)                                     # cross term sign: 4 − 1 instead of 4 + 1
    c[(20, 4)] = lambda: (Rational(3, 3 + 7), Rational(3, 10))                 # P(white | A) given instead of P(A | white)
    c[(35, 1)] = lambda: (Rational(1, 10) * 1 * 10 * sqrt(3) / 2 * 10, 5 * sqrt(3))   # μmg sin 60° used instead of cos 60°
    c[(35, 4)] = lambda: (Rational(1, 10) * 1 * 10 * 10, 10)                  # μmg on the incline taken without cos 60°
    c[(41, 1)] = lambda: (1 / Rational(1, 2), 2)                              # only halved (R/2), not put in parallel (R/4)
    c[(43, 4)] = lambda: (round((Rational(1, 2) * 1) / 100 * 1000, 6), 5)     # time from 0 to peak (T/4) in ms
    c[(44, 2)] = lambda: (round(2 * 6.48e5 / 3e8 * 1e3, 2), 4.32)             # 2E/c (perfect reflection) instead of E/c
    c[(45, 2)] = lambda: (Rational(1, 2) * 1, Rational(1, 2))                 # stopped after polaroid A (cos²45° step missed)
    c[(49, 4)] = lambda: (15 - Rational(3, 10) - Rational(7, 10), 14)         # supply minus diode drops given as V_L
    c[(21, 1024)] = lambda: (2 ** (4 + 6), 1024)                             # all symmetric relations: 2^(n + n(n−1)/2)
    c[(52, 192)] = lambda: (Rational(1, 2) * 6 * 8**2, 192)                   # final KE given instead of the loss
    c[(57, 10)] = lambda: (Rational(40, 4), 10)                               # one side only
    c[(58, 50)] = lambda: (round(2300 * 5 / 230), 50)                         # efficiency 90% ignored
    c[(60, 4)] = lambda: (2 * sqrt(Rational(4, 1)), 4)                         # g at the surface used: T = 2π√(4/π²) = 4 s
    c[(83, 200)] = lambda: (300 * 2 // 3, 200)                                # V_s/V_a = 2 read the other way round
    c[(85, 8)] = lambda: (round((3 - 2.75) / 30 * 1000), 8)                   # rate of N2O5 loss, not doubled for NO2
    return c
