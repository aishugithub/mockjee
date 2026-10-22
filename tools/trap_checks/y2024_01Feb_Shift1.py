"""
Trap checks, JEE Main 2024 Session 1, 1 Feb Shift 1 (pyq/2024/01Feb_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational


def checks():
    c = {}
    c[(3, 4)] = lambda: (3 * 9**2, 243)                                       # det X = det A·(det C)², one det A (from A^T) forgotten
    c[(6, 2)] = lambda: (Rational((3 - 2) + (3 - 4) + (3 - 6), 3), -1)        # d = −2 kept (it makes a − 1 = 0 in the GP)
    c[(34, 1)] = lambda: (400 / (Rational(1, 2) * Rational(1, 2)), 1600)      # ω² given, square root not taken
    c[(42, 4)] = lambda: (100 / Rational(5, 1000) + 50, 20050)                # G added instead of subtracted
    c[(45, 1)] = lambda: (round(6e-7 * 0.2 / 1e-5 * 1000, 6), 12)             # half width λf/a instead of 2λf/a
    vel = lambda m, lam: 1 / (m * lam)                                        # λ = h/mv  =>  v ∝ 1/(mλ)
    c[(46, 1)] = lambda: (vel(4, 2) / vel(1, 1), Rational(1, 8))              # ratio v_α : v_p written the wrong way round
    c[(46, 2)] = lambda: (vel(1, 1) / vel(4, 1), 4)                           # masses used, wavelength ratio 2 ignored
    c[(49, 4)] = lambda: (Rational(10 * 5, 11), Rational(50, 11))             # one Vernier division (50/11) given instead of MSD − VSD
    c[(50, 2)] = lambda: (round(10 + 0.05 / 0.35 * 100 + 0.2 / 15 * 100, 1), 25.6)   # radius error counted once (ρ ∝ r²)
    c[(53, 96000)] = lambda: (round(0.5 * 1 * (70**2 - 50**2) * 80), 96000)   # lift force given; not divided by g
    c[(57, 12)] = lambda: (72 // 6, 12)                                       # one side only
    c[(81, 25)] = lambda: (50 // 2, 25)                                       # (NH4)3PO4 taken as limiting (PbCl2 is: 72/3 = 24)
    return c
