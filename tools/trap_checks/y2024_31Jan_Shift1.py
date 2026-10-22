"""
Trap checks, JEE Main 2024 Session 1, 31 Jan Shift 1 (pyq/2024/31Jan_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Rational, sqrt


def checks():
    c = {}
    c[(1, 1)] = lambda: (Rational(4 * 4 + 3, 6 * 4 - 4), Rational(19, 20))    # g taken as f itself: g∘g∘g = f∘f∘f = f, so f(4)
    c[(3, 1)] = lambda: (2 * 12, 24)                                          # 2f(0) only, f'(0) forgotten
    c[(3, 2)] = lambda: (42 - 2 * 12, 18)                                     # f'(0) only, 2f(0) forgotten (f'(0) = 42 − 24)
    c[(13, 1)] = lambda: (sqrt(2**2 + 4**2), sqrt(20))                        # distance between the centres given as the radius
    c[(13, 4)] = lambda: (sqrt(25 + 4 - 13), 4)                               # radius of the given circle instead of C
    c[(17, 4)] = lambda: (Rational(45 + 4 * 3, 153), Rational(57, 153))       # E(x²) given instead of the variance
    c[(43, 3)] = lambda: (22 / (Rational(22, 7) * Rational(1, 10**4) * 2000), 35)   # ΔB not divided by the 2 s
    c[(44, 3)] = lambda: (round(8.85e-12 * 50**2 * 1e8, 3), 2.212)            # ε0E0² (the ½ dropped), ×10⁻⁸
    c[(47, 2)] = lambda: (Rational(8, 9) / Rational(3, 4), Rational(32, 27))   # ratio of 1/λ values written the wrong way round
    c[(49, 3)] = lambda: (Rational(60, 2), 30)                                # closed fundamental matched to the open fundamental (v/4L = v/2L')
    c[(50, 2)] = lambda: (Rational(1, 10) + Rational(1, 10), Rational(2, 10))  # diameter's error counted once (R ∝ 1/d²)
    c[(52, 4)] = lambda: (Rational(1, 2) * 50 * Rational(4, 10)**2, 4)        # translational KE only
    c[(59, 16)] = lambda: (1 + 9 + 2 * 3, 16)                                 # cos 60° dropped: I2 = I + 9I + 2·3I
    c[(85, 10)] = lambda: (1 * 10, 10)                                        # 1 F taken to give 1 mol Cu (Cu²⁺ needs 2 e⁻)
    return c
