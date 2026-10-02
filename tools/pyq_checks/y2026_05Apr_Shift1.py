"""Answer checks for JEE Main 2026 (Session 2), 5 Apr Shift 1 (Q25 left out: special key)."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        s, b = 3 * sympy_I, Symbol('b')          # alpha + beta = 3i from (b - a)(b + a)
        bv = solve(s**2 - 4 * b - 11, b)[0]
        return opt(expand((sqrt(11) * (s**2 - bv))**2), [160, 176, 194, 187])
    c[1] = q1
    c[2] = lambda: opt(sum((3 * n * n + 5 * n - 3 * (n - 1)**2 - 5 * (n - 1))**2 for n in range(1, 11)), [10220, 12860, 15220, 19780])

    def q3():
        a = Symbol('a')
        A = Matrix([[2, 1, 1], [1, a, 3], [3, 1, 1]])
        A = A.subs(a, solve(A.det() - 1, a)[0])
        assert A.T * Matrix([1, 0, 1]) == Matrix([5, 2, 2]) and A * Matrix([1, 0, 1]) == Matrix([3, 4, 4]) and A * Matrix([0, 0, 1]) == Matrix([1, 3, 1])
        return opt((A**2 + A).adjugate().det(), [16, 25, 49, 64])
    c[3] = q3

    def q4():
        t, f = symbols('t f')
        fv = solve(Matrix([[1, 2, t], [6, 1, 5 * t], [3, t**2, f]]).det(), f)[0]
        d = diff(fv, t)
        assert all(d.subs(t, v) > 0 for v in range(-20, 21))
        return 2
    c[4] = q4
    c[5] = lambda: opt(sum(Rational(528, n * (n + 1) * (n + 2)) for n in range(1, 11)), [65, 130, 220, 440])

    def q6():
        rts = sorted(float(r) for r in solve(x**2 - 2 * x - 5, x))
        s = math.atan(rts[0]) + math.atan(rts[1])
        return nearest(20 * math.sin(s / 2)**2, [10 + math.sqrt(10), 10 - 2 * math.sqrt(10), 10 - 3 * math.sqrt(10), 10 - math.sqrt(10)])
    c[6] = q6

    def q7():
        pk = Fraction(sum(1 for i in range(5) if 'KANPUR'[i:i + 2] == 'AN'), 5)
        pa = Fraction(sum(1 for i in range(7) if 'ANANTPUR'[i:i + 2] == 'AN'), 7)
        return opt(Rational(pa / (pa + pk)), [Rational(7, 10), Rational(10, 17), Rational(12, 19), Rational(7, 19)])
    c[7] = q7

    def q8():
        xs, fs = [5, 7, 9, 10, 12, 15], [8, 6, 2, 2, 2, 6]
        m = Rational(sum(a * b for a, b in zip(xs, fs)), sum(fs))
        return opt(sum(b * abs(a - m) for a, b in zip(xs, fs)) / sum(fs), [Rational(40, 13), Rational(42, 13), Rational(44, 13), Rational(46, 13)])
    c[8] = q8
    c[9] = lambda: opt(Rational(1, 2) * 4 * sqrt(9 * (1 - Rational(9, 25))), [Rational(12, 5), Rational(14, 5), Rational(24, 5), Rational(48, 5)])
    c[10] = lambda: opt(sqrt((3 + 3)**2 + (4 + 4)**2) + 2, [8, 10, 12, 9])

    def q11():
        P = Matrix([3, 5]); M = P - Rational(3 + 5 - 4, 2) * Matrix([1, 1])
        G = P + Rational(2, 3) * (M - P)
        return opt(9 * (G[0] + G[1]), [16, 27, 36, 48])
    c[11] = q11

    def q12():
        vals = {round(-3 * (k / 1000)**2 + 12 * k / 1000, 9) for k in range(-1000, 1001)}
        lo, hi = min(vals), max(vals)
        return opt(sum(range(math.ceil(lo), math.floor(hi) + 1)), [-54, -60, -75, -84])
    c[12] = q12

    def q13():
        AP, d = Matrix([3, 1, 5]), Matrix([2, 3, 4])
        return opt(AP.dot(AP) - AP.dot(d)**2 / d.dot(d), [3, 5, 6, 8])
    c[13] = q13

    def q14():
        a, b = Matrix([sqrt(7), 1, -1]), Matrix([0, 1, 2])
        r = b - (a.dot(b) / a.dot(a)) * a
        assert simplify(r.cross(a) + a.cross(b)).is_zero_matrix and simplify(r.dot(a)) == 0
        return opt(simplify(9 * r.dot(r)), [44, 54, 86, 132])
    c[14] = q14

    def q15():
        l, m, a = symbols('l m a')
        sols = [s for s in solve([1 + l * a - 4 - 2 * m, 1 - l, -1 + 1 - m * a], [l, m, a], dict=True) if s[a] != 0]
        P = Matrix([4 + 2 * sols[0][m], 0, -1 + sols[0][m] * sols[0][a]])
        return opt(P.dot(P), [5, 10, 17, 26])
    c[15] = q15

    def q16():
        A = integrate(x**2 - 1, (x, 1, 3)) + integrate(27 / x - 1, (x, 3, 27))
        return opt(simplify(A), [78 * log(3) - Rational(52, 3), 54 * log(3) - Rational(52, 3), 54 * log(3) - Rational(26, 3), 54 * log(3) + Rational(26, 3)])
    c[16] = q16

    def q17():
        a = Symbol('a')
        r = solve(a**2 + (a + 1)**2 + (a + 2)**2 - 4 * (a + 1)**2, a)
        lim = limit((1 - cos(r[0] * x) * cos((r[0] + 1) * x) * cos((r[0] + 2) * x)) / sin((r[0] + 1) * x)**2, x, 0)
        assert simplify(lim - 2) == 0
        return opt(expand(r[0] * r[1]), [-2, 1, -1, Rational(5, 4)])
    c[17] = q17

    def q18():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.log(t) / (t * t + 4), [0, 1, 2, mpmath.inf])
        return nearest(float(v), [math.pi * math.log(2) / 2, math.pi * math.log(2) / 4, 1 + math.pi * math.log(2), 2 + math.pi * math.log(2)])
    c[18] = q18

    def q19():
        g = 3 + exp(x) * 3 * x
        xm = solve(diff(g, x), x)[0]
        return opt(simplify(g.subs(x, xm)), [3 * (exp(1) + 1) / exp(1), 3 * (exp(1) - 1) / exp(1), (3 - exp(1)) / exp(1), 3 * exp(1)])
    c[19] = q19
    c[20] = lambda: opt(simplify(integrate((4 - 1 / sin(x)**2) / cos(x)**4, (x, pi / 6, pi / 3))),
                        [11 / sqrt(3), 16 / sqrt(3), 32 / (3 * sqrt(3)), 64 / (3 * sqrt(3))])

    def q21():
        from itertools import permutations
        return sum(1 for p in permutations(range(1, 7)) if p[0] >= 3 and p[2] <= 4 and p[1] + p[2] == 5)
    c[21] = q21
    c[22] = lambda: sum(math.comb(k - 1, 4) for k in range(5, 10))

    def q23():
        for n in range(1, 80):
            co = lambda e: sum(math.comb(n, r) * (-1)**r for r in range(n + 1) if 7 * r - 3 * n == e)
            if (any(7 * r - 3 * n == 7 for r in range(n + 1)) and co(7) + co(14) == 0 and co(7) != 0):
                return n
    c[23] = q23
    c[24] = lambda: round(math.tan(math.pi / 4 + sum(math.atan(2**(p - 1) / (1 + 2**(2 * p - 1))) for p in range(1, 12))), 6)

    # ---- Physics
    c[26] = lambda: [('neg', 0.07), ('neg', 0.7), ('pos', 0.07), ('pos', 0.7)].index(('pos', round(7 * 0.1 / 10, 2))) + 1
    c[28] = lambda: nearest(((1 - 16 / 6400) - (1 - 2 * 16 / 6400)) * 100, [0.12, 0.25, 0.50, 0.75])

    def q29():
        a = Rational(10 - 4, 14) * 10
        return opt((4 * (10 + a)) / (6 * (10 - a)), [Rational(5, 3), Rational(2, 3), Rational(3, 5), Rational(2, 5)])
    c[29] = q29

    def q30():
        M, m, g, s, co, f = 10, 2, 10, 0.6, 0.8, 24
        A = (f - m * g * co * s) / (M + m * s * s)          # wedge acceleration with the block sliding
        ar = g * s - A * co
        return nearest(math.sqrt(2 * 8.8 / ar), [2, 4, math.sqrt(2), 2 * math.sqrt(2)])
    c[30] = q30
    def q34():
        VL, VM = symbols('VL VM')             # V_B = 0, V_T = 5 (5 V cell, top to bottom); 10 V cell + 1 ohm from M to L
        IML = VM + 10 - VL
        s_ = solve([(VL - 5) / 4 + VL / 4 - IML, (VM - 5) / 2 + VM / 2 + IML], [VL, VM])
        I1, I3 = IML.subs(s_), s_[VL] / 4
        I2 = (5 - s_[VM]) / 2 - (s_[VL] - 5) / 4
        return [(Rational(5, 2), Rational(15, 8), Rational(15, 8)), (Rational(15, 8), Rational(5, 2), Rational(15, 8)),
                (Rational(15, 8), Rational(15, 8), Rational(5, 2)), (Rational(5, 2), Rational(5, 2), Rational(15, 8))].index((I1, I2, I3)) + 1
    c[34] = q34

    def q35():
        h, m, v0, e, E0, t = symbols('h m v0 e E0 t', positive=True)
        v = v0 + (-e) * (-2 * E0) / m * t            # force on the electron = (-e)(-2E0) along +x
        lam0 = h / (4 * m * v0)
        opts = [4 * lam0 / (1 - E0 * e * t / (2 * m * v0)), 4 * lam0 / (1 + E0 * e * t / (2 * m * v0)),
                4 * lam0 / (1 + 2 * E0 * e * t / (m * v0)), 4 * lam0 / (1 - 2 * E0 * e * t / (m * v0))]
        return opt(h / (m * v), opts)
    c[35] = q35
    c[36] = lambda: nearest(16 / (3 * 1.0973e7) * 1e9, [121, 242, 486, 974])
    c[37] = lambda: nearest(4 / 6e-6 / 1e6, [0.58, 0.67, 0.82, 0.75])
    c[38] = lambda: nearest(15 / (9 / 3 + 9), [12.5, 1.25, 7.5, 5])
    c[39] = lambda: nearest(2.4 / 1.2, [1.2, 2, 2.4, 2.88])
    c[40] = lambda: nearest(2 * math.degrees(math.asin(3 / 2.12 * 0.5)) - 60, [45, 30, 28, 58])
    c[41] = lambda: nearest((6.62e-34 * 3e8 / 331e-9 - 0.2 * 1.6e-19) / 1e-19, [3.68, 4.68, 5.68, 2.68])
    c[43] = lambda: opt(min(12 * 10**8 * Rational(8, 10**7) / 10 - 40, 12 * 10**8 * Rational(4, 10**7) / 10 - 10), [56, 38, 96, Rational(56, 10)])
    c[44] = lambda: opt(sqrt(Rational(7, 8)), [sqrt(Rational(6, 7)), sqrt(Rational(3, 5)), sqrt(Rational(7, 8)), sqrt(Rational(3, 4))])
    c[45] = lambda: [(0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)].index(next(v for v in [(0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)]
                                                                           if (v[0] | v[1]) and ((v[0] | v[1]) & v[2] & v[0]))) + 1
    c[46] = lambda: round(10 * 0.05 / (0.05**2 * 1e5) * 1000, 6)
    c[47] = lambda: 18 - 10**2 / (2 * 10)
    c[48] = lambda: round(2 * 3.14 / 0.018)
    c[49] = lambda: solve(Matrix([4, -x / 2]).dot(Matrix([3, 2])), x)[0]
    c[50] = lambda: (Rational(1, 2) + 2 * Rational(1, 2) * Rational(1, 4)) / (Rational(1, 2) * Rational(1, 4))

    # ---- Chemistry
    c[51] = lambda: opt(Rational(276, 100) / 276 * 2 * 108, [Rational(108, 100), Rational(216, 100), Rational(324, 100), Rational(432, 100)])
    c[52] = lambda: ['CDBAE', 'BAECD', 'ECDBA', 'EBADC'].index(''.join(sorted('ABCDE', key=lambda k: {'A': (5, 3), 'B': (4, 4), 'C': (7, 6), 'D': (6, 5), 'E': (3, 2)}[k]))) + 1
    c[54] = lambda: nearest(5 / (5 + 10 / 60), [0.825, 0.032, 0.867, 0.967])

    def q55():
        X, Y = symbols('X Y', positive=True)
        s = X / Y
        return opt(simplify(2 * s / (108 * s**5)), [Y**4 / (54 * X**4), Y**5 / (108 * X**4), 108 * X**5 / Y**5, Y**4 / (108 * X**4)])
    c[55] = q55

    def q56():
        ph = {}
        oh = 2 * 0.2 * 10 - 0.1 * 25; ph['A'] = 14 + math.log10(oh / 35)
        ph['B'] = 7.0 if abs(2 * 0.01 * 10 - 2 * 0.01 * 10) < 1e-12 else None
        h = 2 * 0.1 * 10 - 0.1 * 10; ph['C'] = -math.log10(h / 20)
        return ['BCA', 'CAB', 'CBA', 'ACB'].index(''.join(sorted(ph, key=ph.get))) + 1
    c[56] = q56
    c[71] = lambda: sum(1 for bp, lp in [(5, 1), (5, 2), (4, 0), (4, 2), (4, 2), (4, 1), (4, 0), (3, 2), (2, 3), (2, 3)] if bp + lp == 5)
    c[72] = lambda: round(0.6 / 231 * 32 / 0.2 * 100)
    c[73] = lambda: round((48 / 139 - 16 / 94) * 1000)
    c[74] = lambda: round(abs((2.5 - 3.5) / (0.06 - 0.05)) * 2.303)
    c[75] = lambda: round(2.303 * 2 / (0.693 / 6.93))
    return c
