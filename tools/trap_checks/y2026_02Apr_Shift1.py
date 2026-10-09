"""
Trap checks, JEE Main 2026 Session 2, 2 Apr Shift 1 (pyq/2026/02Apr_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
import math

from trap_checks.common import Fraction, Matrix, Rational, expand, limit, log, pi, product, simplify, sin, cos, solve, sqrt, symbols, x


def checks():
    c = {}

    def q1_2():   # sum written from k = 1 to n instead of 0 to n-1
        for N in range(1, 40):
            r = solve(expand(sum((x + j) * (x + j + 2) for j in range(1, N + 1)) - 4 * N), x)
            if len(r) == 2 and all(t.is_integer for t in r) and abs(r[0] - r[1]) == 2:
                return N + min(r), 1
    c[(1, 2)] = q1_2

    def q4(s1_transpose, s2_power):
        A = Matrix([[1, 2], [1, 3]]); B = Matrix([[3, 3], [4, 2]])      # alpha = 3, beta = 4 (solution step)
        M = (B - A) * (B + A)
        s1 = (M.T if s1_transpose else M) == Matrix([[13, 15], [7, 10]])
        s2 = (A + B).det() ** s2_power == -5                              # det(adj M) = (det M)^(n-1), n = 2
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(s1, s2)]
    c[(4, 3)] = lambda: (q4(False, 1), 3)     # transpose forgotten
    c[(4, 4)] = lambda: (q4(True, 2), 4)      # det(adj M) taken as (det M)^2

    c[(6, 4)] = lambda: (5 * math.factorial(7) // math.factorial(3) + 10 * math.factorial(7) // 2, 29400)

    def q7_1():   # only k^2 - 3 = 1 (k^2 = 4) considered
        return sum(1 for r in range(36) for k in range(-50, 51)
                   if k * k == 4 and Fraction(math.comb(36, r + 1)) == Fraction(6 * math.comb(35, r), k * k - 3)), 2
    c[(7, 1)] = q7_1

    def q9_4():   # centroid of the triangle = centroid of the midpoints
        G = (Matrix([Rational(5, 2), 7]) + Matrix([Rational(5, 2), 3]) + Matrix([4, 5])) / 3
        return 3 * G[0] + G[1], 14
    c[(9, 4)] = q9_4

    def q10_1():  # a^2/b (semi-latus rectum) with the correct a^2 = 20, b^2 = 45
        a2, b2 = symbols('a2 b2', positive=True)
        s = solve([16 / a2 + 9 / b2 - 1, 1 - a2 / b2 - Rational(5, 9)], [a2, b2], dict=True)[0]
        return s[a2] / sqrt(s[b2]), 4 * sqrt(5) / 3
    c[(10, 1)] = q10_1

    c[(11, 4)] = lambda: (sin(10 * Rational(1, 4) * pi / 3), Rational(1, 2))

    def q12(lose_sin, lose_cos):
        # every solution of sin x (sin x + cos x) = a (a = 0, 1) in [-pi, pi] is a multiple of pi/4
        grid = [k * pi / 4 for k in range(-4, 5)]
        a0 = [t for t in grid if (sin(t) + cos(t) == 0 if lose_sin else sin(t) * (sin(t) + cos(t)) == 0)]
        a1 = [t for t in grid if (sin(t) == cos(t) if lose_cos else simplify(sin(t) * (sin(t) + cos(t)) - 1) == 0)]
        return len(set(a0) | set(a1))
    assert q12(False, False) == 9
    c[(12, 2)] = lambda: (q12(True, False), 6)
    c[(12, 3)] = lambda: (q12(False, True), 7)

    c[(14, 2)] = lambda: (3 * sqrt(72 + 12 * 6) + 4 * sqrt(72 - 12 * 6), 36)   # a.b = |a||b| = 6

    def q16_1():  # denominator taken as (x-2) ln(x-1), i.e. sqrt(x-1) - 1 ~ (x-2)
        p = x**3 - 5 * x**2 + 8 * x - 4
        return 8 - 4 + limit(sin(p) / ((x - 2) * log(x - 1)), x, 2), 5
    c[(16, 1)] = q16_1

    c[(18, 2)] = lambda: (1 + 2, 3)          # x = 0 and the two roots of tan x = x, no corners
    c[(18, 4)] = lambda: (2 + 1 + 2 + 2, 7)  # plus x = +-2pi

    def q23():    # discriminant <= 0 allowed
        f = Fraction(sum(1 for a, b, cc in product(range(1, 5), repeat=3) if 8 * b * b - 4 * a * cc <= 0), 64)
        return f.numerator + f.denominator, 85
    c[(23, 85)] = q23

    c[(26, 3)] = lambda: (2 * 1 + (-1) + (-2), -1)

    c[(28, 1)] = lambda: (sqrt((-1)**2 + 2**2 + (-1)**2), sqrt(6))
    c[(28, 3)] = lambda: (sqrt(1**2 + (2 * 2)**2 + 4**2), sqrt(33))
    c[(28, 4)] = lambda: (0, 0)               # d/dt of an expression with no t

    def q29_1():  # cross product with only the x*P_y term
        r, p, F = (10, 5), (2, 1.5), (2, 3)
        st = {'A': True, 'B': True, 'C': r[0] * p[1] == 15, 'D': r[0] * F[1] == 20}
        return ['ABC', 'BCD', 'ACD', 'ABD'].index(''.join(k for k in 'ABCD' if st[k])) + 1, 1
    c[(29, 1)] = q29_1

    c[(30, 1)] = lambda: (1 / sqrt(Rational(2**3, 1) * Rational(2, 4)), Rational(1, 2))
    c[(30, 3)] = lambda: (sqrt(Rational(2**3, 1) * Rational(4, 2)), 4)

    c[(31, 1)] = lambda: (Rational(3, 2) * 10**2, 150)
    c[(31, 4)] = lambda: (Rational(3, 2) * 10**2 + 2 * 10, 170)

    c[(32, 3)] = lambda: (((Rational(5) + 1) / 2 - 1) * 100, 200)   # parallel halves: (K + 1)C/2
    c[(32, 4)] = lambda: ((5 - 1) * 100, 400)

    c[(33, 2)] = lambda: (tuple(t * 2 for t in (Rational(5, 2), Rational(3, 2), 1)), (5, 3, 2))
    c[(33, 3)] = lambda: (tuple(t * 2 for t in (1, Rational(5, 2), Rational(7, 2))), (2, 5, 7))

    c[(34, 3)] = lambda: (Rational(8, 18), Rational(4, 9))

    c[(35, 2)] = lambda: (Rational(200, 2) * Rational(150, 100), 150)   # f = 200pi/2pi = 100 Hz, lambda = 1.5 m

    def q36(axial_factor, swapped):
        p1, p2 = symbols('p1 p2', positive=True)
        EA, EB = (p1, axial_factor * p2) if swapped else (axial_factor * p1, p2)
        return solve(EB / EA - sqrt(3), p2)[0] / p1
    c[(36, 1)] = lambda: (q36(2, True), sqrt(3) / 2)
    c[(36, 4)] = lambda: (q36(1, False), sqrt(3))

    c[(44, 1)] = lambda: (round(-13.6 / 3**2, 2), -1.51)   # 3h/pi = n h/pi -> n = 3
    c[(45, 3)] = lambda: (round(0.08 * 4 * math.pi * 512 * (1e-3 / 8)**2 * 1e6), 8)
    c[(46, 18)] = lambda: (round(628e-9 / 0.2e-3 * 180 / math.pi * 100), 18)
    c[(49, 6)] = lambda: (solve(2 / symbols('g') - Rational(1, 3))[0], 6)

    c[(52, 1)] = lambda: (2**2 * Fraction('2.18'), Fraction('8.72'))           # in units of 1e-18 J
    c[(52, 2)] = lambda: (3**2 * Fraction('2.18') / 10, Fraction('1.962'))     # 19.62 -> 1.962 with the exponent unchanged

    def q56_2():
        X, Y, s = symbols('X Y s', positive=True)
        sA = solve(2 * s**2 - 32 * X, s)[0]; sB = solve(s**2 - 4 * Y, s)[0]
        return simplify(sA / sB), 2 * sqrt(X / Y)
    c[(56, 2)] = q56_2

    c[(57, 2)] = lambda: (Fraction('-0.88') - Fraction('0.07'), Fraction('-0.95'))

    c[(74, 314)] = lambda: (round(1 / (1 / 300 - 0.48 / (60000 / (2.3 * 8.3)))), 314)
    c[(75, 1000)] = lambda: (10**Fraction(105, 35), 1000)
    return c
