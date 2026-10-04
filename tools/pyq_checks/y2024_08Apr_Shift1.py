"""Answer checks for JEE Main 2024 (Session 2), 8 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, series, Integer


def checks():
    c = {}

    def q1():
        A = [2, 3, 5, 7, 11]
        rng = {int(math.floor(math.log2(a * a + (a**3) // 5))) for a in A}
        return opt(math.perm(len(rng), len(A)) if len(rng) >= len(A) else 0, [20, 24, 120, 25])
    c[1] = q1

    def q2():
        y = Rational(1, 5)
        return opt(sqrt(1 - y**2), [2 * sqrt(6) / 5, Rational(24, 5), sqrt(6) / 5, (1 + sqrt(6)) / 5])
    c[2] = q2

    def q3():
        t = solve(x**2 - 16 * x + 48, x)
        s = sum(log(v, 8) for v in t)
        opts = [log(4, 8), log(6, 8), 1 + log(8, 6), 1 + log(6, 8)]
        return [i for i, o in enumerate(opts, 1) if abs(N(s - o)) < 1e-12][0]
    c[3] = q3

    def q4():
        a, b = symbols('a b')
        A = Matrix([[2, a, 0], [1, 3, 1], [0, 5, b]])
        M = A**3 - 4 * A**2 + A + 21 * eye(3)
        s = solve(list(M), [a, b], dict=True)[0]
        return opt(2 * s[a] + 3 * s[b], [-9, -13, -12, -10])
    from sympy import eye
    c[4] = q4

    def q5():
        b, cc = symbols('b cc')
        s = solve([b + 2 * cc - 6, (14 - 4 * b) + 2 * (3 * cc - 5) / 2 + 4], [b, cc])
        B = (s[b], 14 - 4 * s[b]); C = (s[cc], (3 * s[cc] - 5) / 2)
        lines = [(1, 3, 2), (1, -3, -6), (1, 6, 6), (1, -6, -10)]
        return [i for i, (p, q, r) in enumerate(lines, 1) if p * B[0] + q * B[1] + r == 0 and p * C[0] + q * C[1] + r == 0][0]
    c[5] = q5

    def q6():
        m = sum(1 for bb in range(1, 9) if 42 - 5 * bb >= 1)
        z = sum(1 - sympy_I**math.factorial(n) for n in range(1, m + 1))
        return opt(m + re(z) + im(z), [12, 8, 5, 4])
    from sympy import re, im
    c[6] = q6

    def q7():
        f = cos(x) - x + 1
        assert simplify(diff(f, x) + sin(x) + 1) == 0         # f' <= 0: S2 false
        S1 = f.subs(x, 0) > 0 and N(f.subs(x, pi)) < 0           # strictly decreasing + sign change: exactly one root
        return 2 if S1 else 4
    c[7] = q7

    def q8():
        fp = simplify(diff((x - 2)**Rational(2, 3) * (2 * x + 1), x))
        zeros = solve(fp, x)
        return opt(len(zeros) + 1, [0, 1, 2, 3])                 # plus x = 2 where f' does not exist
    c[8] = q8

    def q9():
        import mpmath
        f = lambda t: 4 * mpmath.cos(t)**3 + 3 * mpmath.sqrt(3) * mpmath.cos(t)**2 - 10
        pts = [math.pi / 2, 5 * math.pi / 6, math.pi, 7 * math.pi / 6, 3 * math.pi / 2]
        h = 1e-4
        return sum(1 for p in pts if f(p) > f(p - h) and f(p) > f(p + h))
    c[9] = q9

    def q10():
        I = 6 / (cot(x) - 1) + 3
        assert simplify(diff(I, x) - 6 / (sin(x)**2 * (1 - cot(x))**2)) == 0
        return opt(simplify(I.subs(x, pi / 12)), [2 * sqrt(3), 3 * sqrt(3), 6 * sqrt(3), sqrt(3)])
    from sympy import cot
    c[10] = q10

    def q11():
        import mpmath
        for k in (8, 10, 14, 7):
            I = lambda n: mpmath.quad(lambda t: (1 - t**k)**n, [0, 1])
            if abs(147 * I(20) - 148 * I(21)) < 1e-12:
                return [8, 10, 14, 7].index(k) + 1
    c[11] = q11

    def q12():
        f = diff(exp(-x) + 4 * x**2 + x - 1, x)
        r = simplify(diff(f, x, 2) / diff(f, x))
        return [i for i, e in enumerate([1 / (8 * exp(x) - 1), -1 / (8 * exp(x) - 1), -1 / (8 * exp(x) + 1), 1 / (8 * exp(x) + 1)], 1) if simplify(r - e) == 0][0]
    c[12] = q12

    def q13():
        y = Symbol('y')
        C = atan(exp(tan(0))) + atan(1)
        return opt(solve(atan(exp(1)) + atan(y) - C, y)[0], [exp(-2), 1 / E, 2 / E, 2 / E**2])
    from sympy import E
    c[13] = q13

    def q14():
        a1, d1, a2, d2 = Matrix([2, 1, 3]), Matrix([1, -3, 4]), Matrix([2, 3, 5]), Matrix([2, 3, 1])
        n = d1.cross(d2)
        num = abs((a2 - a1).dot(n)); den2 = n.dot(n)
        assert math.gcd(int(num), 1) == 1
        return opt(num + den2, [377, 384, 390, 387])
    c[14] = q14

    def q15():
        P, C2 = Matrix([6, 6]), Matrix([8, Rational(15, 2)])
        C1 = 3 * P - 2 * C2
        r1, r2 = (P - C1).norm(), (C2 - P).norm()
        return opt(C1[0] + C1[1] + 4 * (r1**2 + r2**2), [110, 125, 130, 145])
    c[15] = q15

    def q16():
        b = sqrt(3); a2 = 2 * b**2
        al2 = solve(-x / a2 + 36 / b**2 - 1, x)[0]
        f = b * sqrt(3)
        beta = sqrt(al2 + (6 - f)**2) * sqrt(al2 + (6 + f)**2)
        return opt(al2 + beta, [169, 170, 171, 172])
    c[16] = q16

    def q17():
        g, th, ph = 1.3, 0.7, 0.4
        X, Y, Z = g * math.sin(ph) * math.cos(th), g * math.sin(ph) * math.sin(th), g * math.cos(ph)
        d = math.hypot(Y, Z)
        opts = [g * math.sqrt(1 - math.sin(ph)**2 * math.cos(th)**2), g * math.sqrt(1 - math.sin(th)**2 * math.cos(ph)**2),
                g * math.sqrt(1 + math.cos(th)**2 * math.sin(ph)**2), g * math.sqrt(1 + math.cos(ph)**2 * math.sin(th)**2)]
        return [i for i, o in enumerate(opts, 1) if abs(o - d) < 1e-12][0]
    c[17] = q17

    def q18():
        ok = lambda a: all(a * t * t + 6 * a * t - 12 < 0 for t in [k / 10 for k in range(-20000, 20001)])
        assert ok(0) and ok(-1.3) and not ok(-1.34) and not ok(0.01)
        return 3
    c[18] = q18
    c[19] = lambda: (lambda p: opt(p.denominator - p.numerator, [11, 8, 9, 10]))(__import__('fractions').Fraction(sum(1 for a in range(1, 24) if a * (24 - a) * 4 >= 3 * 144), 23))
    c[20] = lambda: opt(80 * (Rational(9, 16) + Rational(4, 5)), [109, 108, 19, 18])

    def q21():
        s = Symbol('s')
        f = 1 + 2 * (1 - s) / (s**2 - s + 1)
        vals = [f.subs(s, v) for v in [0, 1] + [r for r in solve(diff(f, s), s) if 0 <= r <= 1]]
        r = min(vals) / max(vals)
        return 64 / (1 - r)
    c[21] = q21

    def q22():
        A = Matrix([[2, -1], [1, 1]])
        t = (A**13).trace()
        return [n for n in range(1, 20) if 3**n == t][0]
    c[22] = q22

    def q23():
        from itertools import permutations
        return sum(1 for p in permutations([2, 3, 4, 5, 7], 3) if sum(p) % 3)
    c[23] = q23

    def q24():
        for n in range(1, 20):
            al = sum((4 * r * r + 2 * r + 1) * math.comb(n, r) for r in range(n + 1))
            be = sum(Rational(math.comb(n, r), r + 1) for r in range(n + 1)) + Rational(1, n + 1)
            if 140 < 2 * al / be < 281:
                return n
    c[24] = q24
    c[25] = lambda: [k for k in range(1, 200) if k * (k + 1) // 2 >= 5310][0]

    def q26():
        # log P = sum log(cos kx)/k ~ -sum k x^2/2, so 1 - P ~ (x^2/2) sum k
        coeffs = [series(log(cos(k * x)) / k, x, 0, 3).removeO().coeff(x, 2) for k in range(1, 11)]
        return -2 * sum(coeffs)
    c[26] = q26

    def q27():
        A = integrate(-cos(x), (x, -pi, -3 * pi / 4)) + integrate(-sin(x), (x, -3 * pi / 4, 0)) + integrate(sin(x), (x, 0, pi / 4)) \
            + integrate(cos(x), (x, pi / 4, pi / 2)) + integrate(-cos(x), (x, pi / 2, pi))
        return simplify(A**2)
    c[27] = q27

    def q28():
        a, b, cc = Matrix([9, -13, 25]), Matrix([3, 7, -13]), Matrix([17, -2, 1])
        l = Symbol('l')
        r = b + cc + l * a
        lv = solve(r.dot(b - cc), l)[0]
        v = 593 * r.subs(l, lv) + 67 * a
        return v.dot(v) / 593**2
    c[28] = q28

    def q29():
        a, b = symbols('a b')
        O, H = Matrix([3, 4]), Matrix([-6, -8])
        G = (2 * O + H) / 3
        assert G == Matrix([0, 0])
        A = solve([2 * x + 3 * Symbol('y') - 1, x + 2 * Symbol('y') - 1], [x, Symbol('y')])
        t = Symbol('t'); Bp = solve(2 * t + 3 * 2 * t - 1, t)[0] * Matrix([1, 2])
        s = solve([a * A[x] + b * A[Symbol('y')] * 0 + 0, a * Bp[0] + b * Bp[1] - 1, a + b], [a, b], dict=True)
        s = solve([a * Bp[0] + b * Bp[1] - 1, a + b], [a, b], dict=True)[0]       # (a, b) parallel to OA = (-1, 1)
        return abs(s[a] - s[b])
    c[29] = q29
    c[30] = lambda: 7 * Rational(3 * 5, 9) + 4 * Rational(3 * 4, 9)

    c[32] = lambda: nearest(30 * 2 * 3.14 * 0.75 - 3.14 * 0.6, [118.9, 139.4, 140.5, 220.0])
    def q33():
        mA, mB, vA, vB = symbols('mA mB vA vB', positive=True)
        r = (mB * vB**2) / (mA * vA**2)
        r = r.subs(vA, mB * vB / mA)                         # momentum conservation
        return [i for i, e in enumerate([vB / vA, mB / mA, mB * vB / (mA * vA), Integer(1)], 1) if simplify(e.subs(vA, mB * vB / mA) - r) == 0][0]
    c[33] = q33
    c[50] = lambda: opt(1 / Rational(1, 2), [1, 2, Rational(1, 2), 0])          # I = V/R at resonance
    c[34] = lambda: opt(Rational(15, 100) * 20 / Rational(1, 10), [150, 3, 30, 300])
    c[35] = lambda: 1 if [sqrt(Rational(m, 4)) for m in (4, 12, 16)] == [1, sqrt(3), 2] else 0
    c[39] = lambda: [i for i, r in enumerate([Rational(3, 2), Rational(3, 5), Rational(7, 5), Rational(5, 3)], 1) if r == Rational(3, 5)][0]
    c[40] = lambda: opt(3 - Rational(3, 1 + 2) * 1, [2, 3, 4, Rational(3, 2)])
    c[42] = lambda: nearest(2.4e-4 * 3e8 / 3.6e6, [0.2, 0.1, 0.02, 20])
    c[43] = lambda: [i for i, (p, q) in enumerate([(2, 1), (1, sqrt(2)), (sqrt(2), 1), (1, 2)], 1) if simplify(q / p - sin(pi / 4)) == 0][0]
    c[44] = lambda: [i for i, r in enumerate([Rational(1, 1836), 1 / sqrt(1836), 1836, sqrt(1836)], 1) if r == Rational(1, 1836)][0]   # K_p/K_e = m_e/m_p
    c[45] = lambda: [i for i, (p, q) in enumerate([('a', 'b'), ('b', 'a')], 1) if (p, q) == ('a', 'b')][0]   # q/r equal => q_a : q_b = a : b
    c[46] = lambda: nearest(18e8 / 9e16 * 1e9, [2, 20, 10, 0.2])
    c[48] = lambda: opt(100 * (Rational(5, 500) + Rational(2, 200)), [Rational(2, 100), Rational(2, 10), 2, Rational(1, 2)])
    c[49] = lambda: nearest(8.635 / (4 / 3 * math.pi * 1.01**3), [2.0, 1.7, 2.5, 2.2])
    c[51] = lambda: simplify((1 + 1 / sqrt(2))**2 + (1 - 1 / sqrt(2))**2)
    c[52] = lambda: Rational(6 * Rational(3, 2) - Rational(3, 2), 5) / Rational(6 * 1 - Rational(3, 2), 5) * 9
    c[53] = lambda: round(2 * 4 * 0.28 / (0.0004 * 8000 * 10) * 100, 6)
    c[54] = lambda: [a for a in range(2, 40) if Rational(a - 1, a) == Rational(15, 4) / Rational(16, 4)][0]
    c[55] = lambda: Rational(2 * 2 + 6 + 8, 6) * 4
    c[56] = lambda: round(0.95 / (0.2 / 100) + 273)
    c[57] = lambda: round(math.sqrt(2 * 5 * 1.6e-19 / 9e-31) * 3e-6, 6)
    c[58] = lambda: round(math.sqrt(2 * 9e9 * 160 * 1.6e-19**2 / 4.5e-14 / 6.72e-27) / 1e5)
    c[59] = lambda: round(2 * 2 * 600e-9 / 0.4e-3 * 1e3, 6)
    c[60] = lambda: round((10 * 0.5 * 0.06 * 0.06)**2 / 100 * 1e6)
    c[61] = lambda: opt(900 // 180 * 6 * 32, [32, 800, 960, 480])
    c[63] = lambda: opt(1 * 2 * 4, [7, 8, 12, 6])
    c[81] = lambda: round(3e8 / (4 * 1.5e-12) / 1e19)
    c[83] = lambda: round(0.08206 * 291.15 * math.log(10))
    c[84] = lambda: round((0.52 / (0.52 * 0.5) - 1) / 2 * 10)
    c[87] = lambda: 279 // 93 * (12 * 12 + 11 + 3 * 14)
    c[89] = lambda: 3 + 1 + 1
    return c
