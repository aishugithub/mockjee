"""Answer checks for JEE Main 2024 (Session 2), 9 Apr Shift 2."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, asinh, Abs


def checks():
    c = {}

    def q1():
        a, b = 1 / (2 + sqrt(2)), 1 / (2 - sqrt(2))
        return opt(simplify(((a + b) / 2) / sqrt(a * b)), [2, sqrt(2), pi, sqrt(pi)])
    c[1] = q1

    def q2():
        X, Y = symbols('X Y', real=True)
        z = X + sympy_I * Y
        e = simplify(((z - 2 * sympy_I) * (X - sympy_I * Y - 2 * sympy_I * -1)).expand())
        num = expand((z - 2 * sympy_I) * (X - sympy_I * (Y + 2)))
        assert expand(re(num) - (X**2 + Y**2 - 4)) == 0
        return opt(2 + 10, [8, 10, 12, oo])
    from sympy import re
    c[2] = q2

    def q3():
        r = solve(x**2 - sqrt(2) * x - sqrt(3), x)
        P = lambda n: expand((r[0]**n - r[1]**n))
        v = expand((11 * sqrt(3) - 10 * sqrt(2)) * P(10) + (11 * sqrt(2) + 10) * P(11) - 11 * P(12))
        opts = [11 * sqrt(3), 11 * sqrt(2), 10 * sqrt(3), 10 * sqrt(2)]
        return [i for i, o in enumerate(opts, 1) if abs(N(v - o * P(9), 40)) < 1e-20 * abs(N(v, 40))][0]
    c[3] = q3

    def q4():
        B = Matrix([[1, 3], [1, 5]])
        a, b = symbols('a b')
        s = solve(list(B**2 + a * B + b * eye(2)), [a, b])
        return opt(2 * s[b] - s[a], [2, 8, 10, 16])
    from sympy import eye
    c[4] = q4
    c[5] = lambda: opt(limit((E - (1 + 2 * x)**(1 / (2 * x))) / x, x, 0), [E, 0, E - E**2, -2 / E])
    from sympy import E

    def q6():
        tot = 0
        for r in range(10):
            p = Rational(2, 3) * (9 - r) - Rational(2, 5) * r
            if p in (Rational(2, 3), Rational(-2, 5)):
                tot += math.comb(9, r) * Rational(1, 2**r)
        return opt(tot, [Rational(21, 4), Rational(63, 16), Rational(19, 4), Rational(69, 16)])
    c[6] = q6

    def q7():
        a, r = symbols('a r')
        s = [v for v in solve([a / (1 - r) - 57, a**3 / (1 - r**3) - 9747], [a, r], dict=True) if 0 < v[r] < 1][0]
        return opt(s[a] + 18 * s[r], [27, 31, 38, 46])
    c[7] = q7

    def q8():
        y = exp(3 * asin(x))
        v = simplify(((1 - x**2) * diff(y, x, 2) - x * diff(y, x)).subs(x, Rational(1, 2)))
        return opt(v, [9 * exp(pi / 2), 9 * exp(pi / 6), 3 * exp(pi / 2), 3 * exp(pi / 6)])
    c[8] = q8

    def q9():
        g = -3 * x**2 * (sin(2 * x) + cos(x))           # derivative of the numerator
        v = diff(g, x).subs(x, pi / 2) / 2
        return opt(simplify(v), [3 * pi**2 / 2, 5 * pi**2 / 9, 9 * pi**2 / 8, 11 * pi**2 / 10])
    c[9] = q9

    def q10():
        import mpmath
        a, b = mpmath.sqrt(18), mpmath.sqrt(6)
        f = lambda t: (mpmath.sqrt((18 - t * t) / 3) if t * t <= 18 else 0)
        X = 3 / mpmath.sqrt(2)
        area = mpmath.quad(lambda t: t, [0, X]) + mpmath.quad(f, [X, a])
        return nearest(float(area), [math.sqrt(3) * math.pi, math.sqrt(3) * math.pi - 0.75, math.sqrt(3) * math.pi + 0.75, math.sqrt(3) * math.pi + 1])
    c[10] = q10

    def q11():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.cos(2 * mpmath.acot(mpmath.sqrt((1 - t) / (1 + t)))), [0.25, 0.75])
        return nearest(float(v), [0.25, -0.25, 0.5, -0.5])
    c[11] = q11

    def q12():
        v = integrate(asinh(x), (x, -1, 2))
        opts = [sqrt(2) - sqrt(5) + log((9 + 4 * sqrt(5)) / (1 + sqrt(2))), sqrt(5) - sqrt(2) + log((9 + 4 * sqrt(5)) / (1 + sqrt(2))),
                sqrt(2) - sqrt(5) + log((7 + 4 * sqrt(5)) / (1 + sqrt(2))), sqrt(5) - sqrt(2) + log((7 + 4 * sqrt(5)) / (1 + sqrt(2)))]
        return [i for i, o in enumerate(opts, 1) if abs(N(v - o)) < 1e-12][0]
    c[12] = q12

    def q14():
        al, be = symbols('al be')
        s = solve([(al + 2) * -2 + (be - 3) * 2, (al - 3) * 3 + (be + 1) * -2], [al, be])
        h, k = symbols('h k')
        cs = solve([(h - 1)**2 + (k - 1)**2 - (h - 3)**2 - (k + 1)**2, (h - 1)**2 + (k - 1)**2 - (h + 2)**2 - (k - 3)**2], [h, k])
        return opt(s[al] + s[be] + 2 * (cs[h] + cs[k]), [5, 15, 51, 81])
    c[14] = q14

    def q15():
        eE = sqrt(1 - Rational(75, 100)); ae = 10 * eE
        a = ae / (1 / eE); b2 = a**2 * ((1 / eE)**2 - 1)
        return opt(3 * (2 * a)**2 + 2 * (4 * b2), [205, 242, 237, 225])
    c[15] = q15

    def q16():
        t, s = symbols('t s')
        P = Matrix([Rational(11, 3), Rational(11, 3), Rational(19, 3)]); d = Matrix([2, 1, 2])
        sol = solve(list(P + s * d - Matrix([1 + t, 2 + t, 3 + 2 * t]))[:2], [t, s])
        Q = P + sol[s] * d
        assert Q[2] == 3 + 2 * sol[t]
        return opt((Q - P).norm(), [6, 5, 4, 3])
    c[16] = q16

    def q17():
        a, b = Matrix([1, 2, -3]), Matrix([2, 1, -1])
        r = b - a.dot(b) / a.dot(a) * a
        I_ = simplify(r.norm()) == sqrt(10)
        import random
        random.seed(2)
        II = all(math.cos(2 * A) + math.cos(2 * B) + math.cos(2 * (math.pi - A - B)) >= -1.5 - 1e-12
                 for A, B in [(random.uniform(0, 3), random.uniform(0, 3)) for _ in range(2000)] if A + B < math.pi)
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(I_, II)]
    c[17] = q17

    def q18():
        sols = []
        for al in range(-6, 7):
            if al and -6 % al == 0:
                be = -6 // al
                cr = Matrix([1, al, 2]).cross(Matrix([-1, be, 0]))
                if cr.dot(cr) == 21: sols.append((al, be))
        (a1, b1), (a2, b2) = sols
        return opt(a1**2 + b1**2 - a2 * b2, [17, 19, 21, 24])
    c[18] = q18

    def q19():
        for cv in range(1, 20):
            d = [cv, cv, 2 * cv, 3 * cv, 4 * cv, 5 * cv, 6 * cv]
            m = Rational(sum(d), 7)
            if sum((v - m)**2 for v in d) / 7 == 160: return opt(cv, [6, 7, 8, 5])
    c[19] = q19
    c[20] = lambda: opt(Rational(sum(1 for a in range(1, 7) for b in range(1, 7) for cc in range(1, 7) if a < b < cc), 216), [Rational(5, 54), Rational(3, 54), Rational(2, 54), Rational(1, 54)])
    c[21] = lambda: math.factorial(sum(1 for xx in range(1, 23) for y in range(1, 23) if 2 * xx + 3 * y == 23))

    def q22():
        m = Symbol('m')
        d = 2 * m + 15
        X, Y = 25 * m / d, (2 * m - 60) / d
        assert N(X.subs(m, -3)) < 0 and N(Y.subs(m, -3)) < 0 and N(X.subs(m, 1)) > 0
        return 8 * integrate(2 * m + 15, (m, Rational(-15, 2), 0))
    c[22] = q22
    c[23] = lambda: sum(1 for n in range(101, 1000) if sum(map(int, str(n))) == 14)

    def q24():
        F = Fraction
        right = sum(F(1, k) for k in range(1013, 2025))
        for al in range(1000, 1020):
            if sum(F(1, al + k) for k in range(1, 1013)) - right == F(1, 2024): return al
    c[24] = q24

    def q25():
        p = Symbol('p')
        lo, hi = solve(1 - 2 * (p - 4), p)[0], solve(1 + 2 * (p - 4), p)[0]
        return 16 * lo * hi if lo > hi else 16 * lo * hi
    c[25] = q25

    def q26():
        al, C = Rational(-21), -6
        f = C * exp(3 * x) - al / 3
        assert f.subs(x, 0) == 1 and diff(f, x) - 3 * f - al == 0
        return 9 * f.subs(x, -log(3))
    c[26] = q26

    def q27():
        p, q = 8, 4 + 2 * sqrt(5)
        h = Symbol('h', positive=True)
        assert solve(h**2 + 8 * h - 4, h)[0] == q - 8
        return expand((2 * q - p)**2)
    c[27] = q27

    def q28():
        a = Rational(3, 2)
        t1, t2, t3 = Rational(1), Rational(-2), Rational(3, 2)
        A, B, C = (a * t1**2, 2 * a * t1), (a * t2**2, 2 * a * t2), (a * t3**2, 2 * a * t3)
        yL = C[1]
        xD = A[0] + (B[0] - A[0]) * (yL - A[1]) / (B[1] - A[1])
        AM, BN, CD = Abs(A[1] - yL), Abs(B[1] - yL), Abs(C[0] - xD)
        return (AM * BN / CD)**2
    c[28] = q28

    def q29():
        P0, d, Q = Matrix([1, 0, 2]), Matrix([3, 2, 4]), Matrix([6, 1, 5])
        F = P0 + d * (Q - P0).dot(d) / d.dot(d)
        I_ = 2 * F - Q
        return I_.dot(I_)
    c[29] = q29
    c[30] = lambda: len([t for t in [k / 1000 for k in range(-1000, 1001)] if abs(2 * math.asin(t) + 3 * math.acos(t) - 2 * math.pi / 5) < 1e-3])

    c[32] = lambda: opt(300 - 2 * Rational(20**2, 4), [50, 100, 200, 25])
    c[34] = lambda: opt(10 * tan(pi / 4), [10, 10 / sqrt(2), 1 / (10 * sqrt(2)), 1])
    c[36] = lambda: nearest(integrate(2400 / x**3, (x, 2, 4)) + 10 * (2 - 4), [20, -20, 205, 225])
    c[37] = lambda: nearest((26.7 / 4) / (200 / 235), [7.62, 9.13, 25.6, 15.04])
    c[38] = lambda: opt(1 / (Rational(1, 2) - Rational(1, 3)), [Rational(5, 2), 3, 4, 6])
    c[39] = lambda: [i for i, r in enumerate([Rational(1, 3), Rational(1, 9), Rational(1, 27), Rational(1, 81)], 1) if r == Rational(1, 3)**3][0]
    c[40] = lambda: nearest((2 * 1e-8 * 1e5 * 9.8 / (9 * 9.8e-6))**2 / (2 * 9.8), [2296, 2249, 2396, 2518])
    c[41] = lambda: opt(2 * (273 - 78) - 273, [117, 127, -78, -39])
    c[42] = lambda: opt(5 + 1 - 2, [4, 5, 3, 1])
    c[43] = lambda: opt(1 + Rational(1, 3) + Rational(1, 3) + 1, [Rational(2, 3), Rational(4, 3), Rational(5, 3), Rational(8, 3)])
    c[44] = lambda: [i for i, r in enumerate([sqrt(2), 1 / sqrt(2), Rational(1, 2), 1], 1) if r == sqrt(2)][0]
    c[46] = lambda: opt(10 + 15, [10, 15, 25, 35])
    c[47] = lambda: nearest(4.13 - 3.13, [1, 3.13, 4.13, 7.26])
    c[51] = lambda: integrate(3 * x**2 + 2 * x - 5, (x, 2, 4))
    c[52] = lambda: round(4 * 500e-9 / 0.5 * 1e6, 6)
    c[53] = lambda: (8 / sqrt(16 + 48))**2 * 4
    c[54] = lambda: 44 * 2 / Rational(22, 7)
    c[55] = lambda: round(27 + 12 / (50 * 2.4e-4))
    c[56] = lambda: (2 * 4 - 2 * 2) * 4
    c[57] = lambda: 2 * Rational(22, 7) / sqrt(Rational(50, Rational(1, 2))) * 35
    c[58] = lambda: 2 * Rational(3, 2)
    c[59] = lambda: round(math.degrees(math.acos(-math.sqrt(3) / 2)))
    c[60] = lambda: 1 / (Rational(1, 2000) - Rational(1, 10000))
    c[63] = lambda: nearest(1.2e-4 * (0.24e-3)**2, [6.91e-12, 27.65e-12, 0.069e-12, 0.276e-12])
    c[81] = lambda: round(6.626e-34 / (4 * 3.14 * 9.1e-31 * 1e-15) / 1e9)
    c[83] = lambda: 30000 / 75
    c[84] = lambda: round(24 / (80 + 24) * 100)
    c[85] = lambda: round(0.693 / 23 * 100)
    c[86] = lambda: round(math.sqrt(35))
    c[88] = lambda: round((6 / 8) / (4 / 8) * 10)
    return c
