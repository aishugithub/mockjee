"""
Trap checks, JEE Main 2026 Session 2, 4 Apr Shift 2 (pyq/2026/04Apr_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
from trap_checks.common import Matrix, Rational, Symbol, pi, simplify, solve, sqrt, x


def checks():
    c = {}
    c[(4, 2)] = lambda: (Rational(1, 1) * (-3 * Rational(1, 3) - 3), -4)     # even part over [0, 1] only, not doubled

    def q5_3():
        return len([l for l in range(-10, 1) if -Rational(32, 7) <= l <= -2]), 3   # λ = −2 counted
    c[(5, 3)] = q5_3
    c[(6, 4)] = lambda: (2 + 2, 4)                                           # 2 on the x-axis + 2 on the y-axis, origin twice
    c[(7, 1)] = lambda: (Rational(1, 2) ** -2, 4)                            # one term only: (0.2)^(log_√5 1/2) = 4
    def r_ordinates():
        xs = solve(x**2 - 10 * x + 21, x)                                    # Q on the circle and x + y = 10
        return sorted(9 - (10 - q) for q in xs)                              # R = (6, 9) − Q: ordinate 9 − y_Q
    c[(10, 1)] = lambda: (r_ordinates()[1], 6)                               # one R only
    c[(10, 2)] = lambda: (r_ordinates()[0], 2)                               # the other R only

    def q14_4():
        a = Symbol('a')
        P = Matrix([a, 2 * a, 1]); Q = Matrix([2 * a + 1, a**2 - 3 * a, (a - 1) / 2])
        return tuple(sorted(solve((Q - P).dot(Matrix([3, 2, 1])), a))), (Rational(1, 4), 3)   # perpendicularity only
    c[(14, 4)] = q14_4
    c[(16, 3)] = lambda: (sum(4 + 2 * n * n + n + 1 for n in range(1, 6)), 150)   # f = 2x² + x + 1 (f(0) taken as +1)
    c[(18, 2)] = lambda: (1 - Rational(1, 3), Rational(2, 3))                # y ≥ 0 half only
    c[(27, 1)] = lambda: (5 * Rational(18, 5), 18)                           # 5 m/s converted and given as v
    c[(28, 1)] = lambda: (Rational(100, 200), Rational(1, 2))                # 2x = 100 and 5y = 200 read as x and y
    c[(31, 2)] = lambda: (1 * 2 * 2, 4)                                      # equal tensions: A's 3Mg taken as 2Mg
    c[(32, 1)] = lambda: (round(30e-4 * 0.5 / 15e-6, 6), 100)                # one perforation only
    c[(32, 3)] = lambda: (round(30e-4 * 50 / (10 * 15e-6), 6), 1000)         # 50 cm/s used as 50 m/s
    c[(35, 3)] = lambda: ((Rational(1, 2) + 1) / 1, Rational(3, 2))          # I = MR²/2 + MR² (axis ⟂ disc), T² ∝ I/(MgR): 3R/2g
    c[(39, 1)] = lambda: (simplify(1 / (4 * pi * Rational(1, 10**7)) / 10**5), 25 / pi)   # μr left out
    c[(41, 2)] = lambda: (1 / (Rational(2, 5) * 1), Rational(5, 2))         # one curved surface: 1/f = (μ − 1)/R
    c[(41, 3)] = lambda: ((Rational(2, 5) * 2), Rational(4, 5))             # R/f instead of f/R
    c[(42, 4)] = lambda: (Rational(1, 8) / Rational(9, 32), Rational(4, 9))  # ratio upside down
    c[(46, 500)] = lambda: (round(25 / (0.5 / 10), 6), 500)                  # whole 25 V across R
    return c
