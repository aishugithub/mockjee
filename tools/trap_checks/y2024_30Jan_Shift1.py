"""
Trap checks, JEE Main 2024 Session 1, 30 Jan Shift 1 (pyq/2024/30Jan_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, log, sqrt


def S(n, a=-8, d=5):
    return Rational(n, 2) * (2 * a + (n - 1) * d)


def checks():
    c = {}
    c[(6, 1)] = lambda: (S(15), 405)                                          # S15 alone, S5 not subtracted
    c[(33, 3)] = lambda: (round(1 * (14 + 9.9), 1), 23.9)                     # mass 100 g used as 1 kg
    c[(41, 2)] = lambda: (round((Rational(80, 60) - 1) / Rational(2, 10**4)), 1667)   # rise ΔT given as the temperature (27 °C not added)
    c[(42, 4)] = lambda: (sqrt(Rational(1, 2)**2 + 0), Rational(1, 2))        # one loop only: μ0I/2a (coefficient of μ0I/a); both loops give √2 × ½
    c[(48, 4)] = lambda: (round((20 - 10) / 200 * 1000), 50)                   # current in the 200 Ω (total) given as the Zener current
    c[(48, 2)] = lambda: (round(10 / 500 * 1000), 20)                         # load current given as the Zener current
    c[(50, 1)] = lambda: (220 * 10 // 100, 22)                                # secondary voltage, divider ignored
    c[(50, 3)] = lambda: (22 * 15 // 22, 15)                                  # voltage across the 15 kΩ instead of the 7 kΩ
    c[(81, 29)] = lambda: (round(0.35 * 82.02), 29)                           # 250 mL taken as 1 L
    c[(84, 5)] = lambda: (round(-log(sqrt(Rational(1, 10**11) / Rational(1, 10)), 10)), 5)   # pOH given as the pH
    return c
