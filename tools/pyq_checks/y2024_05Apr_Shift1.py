"""Answer checks for JEE Main 2024 (Session 2), 5 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, eye, floor, Abs, cot, csc, E as e_


def checks():
    c = {}

    def q1():
        from itertools import permutations
        B = [2, 4, 5, 7, 8, 10, 12]
        return opt(sum(1 for p in permutations(B, 5) if p[0] + p[1] == 14), [120, 180, 240, 480])
    c[1] = q1
    c[3] = lambda: opt(Rational(3**4 * (4**3 * 2)**2, (2**3 * 3)**2 * 6**2), [32, 64, 81, 108])

    def q4():
        l, m = symbols('l m')
        M = Matrix([[11, 1, l], [2, 3, 5], [8, -19, -39]])
        lv = solve(M.det(), l)[0]
        A = M.subs(l, lv)
        aug = A.row_join(Matrix([-5, 3, m]))
        mv = solve(aug[:, [0, 1, 3]].det(), m)[0]
        assert A.rank() == 2 and aug.subs(m, mv).rank() == 2
        return opt(lv**4 - mv, [45, 47, 49, 51])
    c[4] = q4

    def q5():
        f = sin(x) + 3 * x - 2 / pi * (x**2 + x)
        f2 = diff(f, x, 2)
        assert simplify(f2 + sin(x) + 4 / pi) == 0                # f'' < 0 on the interval
        II = True
        I_ = N(diff(f, x).subs(x, pi / 2)) > 0                   # f' decreasing, so f' > f'(pi/2) > 0
        return {(True, True): 4, (True, False): 1, (False, True): 2, (False, False): 3}[(I_, II)]
    c[5] = q5

    def q6():
        m = sum(1 / (sqrt(k) + sqrt(k + 1)) for k in range(1, 100))
        m = nsimplify(N(m, 30)); n = sum(Rational(1, k * (k + 1)) for k in range(1, 100))
        X, Y = m, n
        return [i for i, e in enumerate([11 * X - 100 * Y, 11 * (X - 1) - 100 * Y, 11 * (X - 2) - 100 * (Y - 1), 11 * (X - 1) - 100 * (Y - 2)], 1) if e == 0][0]
    c[6] = q6

    def q7():
        a, b = symbols('a b')
        s = series(sin(3 * x) + a * sin(x) - b * cos(3 * x), x, 0, 4).removeO()
        sol = solve([s.coeff(x, 0), s.coeff(x, 1)], [a, b])
        return opt(s.coeff(x, 3).subs(sol), [2, -2, 4, -4])
    from sympy import series
    c[7] = q7

    def q8():
        f = x**5 + 2 * x**3 + 3 * x + 1
        r = 1; assert f.subs(x, r) == 7
        return opt(r * diff(f, x).subs(x, r), [1, 7, 14, 42])
    c[8] = q8

    def q9():
        t = Symbol('t')
        A = (2 * cos(t) + 4 * sin(t)) * (2 * sin(t) + 4 * cos(t))
        tv = [v for v in solve(diff(A, t), t) if 0 < N(v) < N(pi / 2)][0]
        return opt(simplify(((2 * cos(t) + 4 * sin(t)) + (2 * sin(t) + 4 * cos(t)))**2).subs(t, tv), [72, 64, 80, 60])
    c[9] = q9

    def q10():
        import mpmath
        v = mpmath.quad(lambda y: 2 * y * (1 + mpmath.sin(y)) / (1 + mpmath.cos(y)**2), [-mpmath.pi, 0, mpmath.pi])
        return nearest(float(v), [math.pi**2, math.pi**2 / 2, 2 * math.pi**2, math.pi / 2])
    c[10] = q10

    def q11():
        import mpmath
        v = mpmath.quad(lambda t: 136 * mpmath.sin(t) / (3 * mpmath.sin(t) + 5 * mpmath.cos(t)), [0, mpmath.pi / 4])
        l2, l5 = math.log(2), math.log(5)
        opts = [3 * math.pi - 10 * math.log(2 * math.sqrt(2)) + 10 * l5, 3 * math.pi - 30 * l2 + 20 * l5, 3 * math.pi - 25 * l2 + 10 * l5, 3 * math.pi - 50 * l2 + 20 * l5]
        return [i for i, o in enumerate(opts, 1) if abs(o - v) < 1e-9][0]
    c[11] = q11

    def q12():
        y = Function('y')
        s = dsolve(Eq(y(x).diff(x) + 2 * y(x), sin(2 * x)), y(x), ics={y(0): Rational(3, 4)})
        return opt(simplify(s.rhs.subs(x, pi / 8)), [exp(-pi / 4), exp(pi / 4), exp(pi / 8), exp(-pi / 8)])
    c[12] = q12

    def q13():
        cands = [(3 + p, 2 + q) for p in (1, -1) for q in (1, -1)]
        C = min(cands, key=lambda t: t[0]**2 + t[1]**2)
        return opt(sqrt((5 - C[0])**2 + (5 - C[1])**2) - 1, [5, 2 * sqrt(2), 4, 4 * sqrt(2)])
    c[13] = q13

    def q14():
        h = Rational(12, 5); PQ = 2 * h
        return opt(floor(2 * PQ**2), [48, 42, 44, 46])
    c[14] = q14

    def q15():
        k = Symbol('k', positive=True)
        kv = solve(k / 2 - 3, k)[0]; assert kv / 3 == 2
        a, b = kv, kv / 3                     # x^2/k^2 + y^2/(k/3)^2 = 1
        LR = Rational(2 * b**2, a)
        return opt(2 * LR.p + LR.q, [10, 11, 12, 13])
    c[15] = q15

    def q16():
        l, m = symbols('l m')
        d1 = Matrix([-3, (4 * l + 1) / 3, -1]); d2 = Matrix([3 * m, -3, -7])
        assert expand(d1.dot(d2) - (6 - 4 * l - 9 * m)) == 0       # perpendicular: 4l + 9m = 6
        return opt(6, [4, 5, 6, 13])
    c[16] = q16

    def q17():
        t, s = symbols('t s')
        sol = solve([-6 + 3 * t - 7 - 4 * s, 2 * t - 9 - 3 * s], [t, s])
        P = Matrix([-6 + 3 * sol[t], 2 * sol[t], -1 + sol[t]])
        assert P == Matrix([7 + 4 * sol[s], 9 + 3 * sol[s], 4 + 2 * sol[s]])
        d = P - Matrix([7, 8, 9])
        return opt(d.dot(d) + 6, [69, 72, 75, 78])
    c[17] = q17

    def q18():
        A, B, C, D = Matrix([1, -1, 2]), Matrix([5, 7, -6]), Matrix([3, 4, -10]), Matrix([-1, -4, -2])
        assert (B - A).cross(C - A).dot(D - A) == 0
        return opt((C - A).cross(D - B).norm() / 2, [12 * sqrt(29), 24 * sqrt(29), 48 * sqrt(7), 24 * sqrt(7)])
    c[18] = q18
    c[19] = lambda: opt(Rational(sum(1 for a in range(1, 9) for b in range(1, 9) for cc in range(1, 9) if b * b == 4 * a * cc), 512),
                        [Rational(3, 256), Rational(1, 128), Rational(3, 128), Rational(1, 64)])

    def q20():
        t = Symbol('t')
        th = [v for v in solve(4 * cos(t) - 3 * sin(t) - 1, t) if 0 <= N(v) <= N(pi / 4)][0]
        cv = cos(th)
        return [i for i, o in enumerate([(6 - sqrt(6)) / (3 * sqrt(6) - 2), 4 / (3 * sqrt(6) - 2), 4 / (3 * sqrt(6) + 2), (6 + sqrt(6)) / (3 * sqrt(6) + 2)], 1) if abs(N(o - cv)) < 1e-12][0]
    c[20] = q20

    def q21():
        sols = [Rational(1 - n, 4) for n in range(-10, 10) if floor(Rational(1 - n, 4)) == n]
        sols = [a for a in sols if abs(2 * a - 1) == 3 * floor(a) + 2 * (a - floor(a))]
        assert not any(floor(a) == -1 for a in [Rational(1, 2)])        # branch a >= 1/2 forces [a] = -1: impossible
        return 72 * sum(sols)
    c[21] = q21

    def q22():
        roots = set()
        pieces = [(-oo, -2, x * (x + 2) + 5 * (x + 1) - 1), (-2, -1, -x * (x + 2) + 5 * (x + 1) - 1),
                  (-1, 0, -x * (x + 2) - 5 * (x + 1) - 1), (0, oo, x * (x + 2) - 5 * (x + 1) - 1)]
        for lo, hi, e in pieces:
            for r in solve(e, x):
                if r.is_real and lo <= r <= hi:
                    roots.add(nsimplify(r))
        return len(roots)
    c[22] = q22
    c[23] = lambda: sum(1 for p in product(range(1, 7), repeat=4) if sum(p) == 16)

    def q24():
        e = expand((1 + 2 * x - 3 * x**3) * (Rational(3, 2) * x**2 - 1 / (3 * x))**9)
        return 108 * e.as_independent(x)[0]
    c[24] = q24

    def q25():
        a, d = symbols('a d')
        S_ = lambda n: n * (2 * a + (n - 1) * d) / 2
        sol = [s for s in solve([-d * S_(6) + 153, -d * S_(10) + 435], [a, d], dict=True) if s[a] > 0 and s[d] > 0][0]
        T = lambda n: (a + (n - 1) * d).subs(sol)
        assert T(1)**2 + T(2)**2 + T(3)**2 == 66
        return T(17) - sum((-1)**(k + 1) * T(k)**2 for k in range(1, 15))
    c[25] = q25

    def q26():
        f = Function('f')
        s = dsolve(Eq(2 * x * f(x) - x**2 * f(x).diff(x), 1), f(x), ics={f(1): 1})
        F = s.rhs
        return simplify(2 * F.subs(x, 2) + 3 * F.subs(x, 3))
    c[26] = q26
    c[27] = lambda: integrate((7 * x - x**2) - (x**2 - 5 * x), (x, 0, 6))

    def q28():
        vals = set()
        for tv in (pi / 6, pi / 4, pi / 5):
            m = tan(tv)
            xs = solve(m**2 * (x - 3)**2 - 12 * x, x)
            P = [(xx, m * (xx - 3)) for xx in xs]
            l = sqrt((P[0][0] - P[1][0])**2 + (P[0][1] - P[1][1])**2)
            d = Abs(3 * m) / sqrt(1 + m**2)
            vals.add(round(float(N(l * d**2, 30)), 9))
        assert len(vals) == 1
        return vals.pop()
    c[28] = q28

    def q29():
        a, b = Matrix([1, -3, 7]), Matrix([2, -1, 1])
        mu = Symbol('mu'); cc = mu * (2 * a + b)
        assert (a + 2 * b).cross(cc) == 3 * cc.cross(a)
        mv = solve(a.dot(cc) - 130, mu)[0]
        return b.dot(cc.subs(mu, mv))
    c[29] = q29

    def q30():
        P = {k: Rational(math.comb(3, k) * math.comb(7, 5 - k), math.comb(10, 5)) for k in range(4)}
        mean = sum(k * p for k, p in P.items())
        return 96 * (sum(k * k * p for k, p in P.items()) - mean**2)
    c[30] = q30

    c[33] = lambda: nearest(30 * (9.8 - 0.1), [297, 294, 291, 196])
    c[35] = lambda: [i for i, xv in enumerate([17, 67, 51, 34], 1) if Rational(2, 3) / (Rational(1, 4) + Rational(16, 3)) == Rational(8, xv)][0]
    c[38] = lambda: nearest(math.pi * 140e3 * 140e-6, [431.2, 616, 61.6, 19.6])
    c[39] = lambda: opt(sqrt(Rational(400, 300)), [2 / sqrt(3), sqrt(3) / 2, Rational(4, 3), Rational(3, 4)])
    c[40] = lambda: [i for i, (p, q) in enumerate([(1, 1), (2, 1), (3, 2), (2, 3)], 1) if Rational(2, 3) * p == q][0]   # p*T1 = q*T2, T1/T2 = 2/3
    c[41] = lambda: [i for i, e in enumerate([36, 39, 29, 19], 1) if e == math.floor(math.log10(9e9 * 1.6e-19**2 / (6.67e-11 * 9.1e-31 * 1.67e-27)))][0]
    c[42] = lambda: [i for i, (r, I) in enumerate([(10.5, 1.14), (12, 11.4), (12, 1), (10.5, 1)], 1) if r == 10 + 1 / (1 / 8 + 1 / 4 + 1 / 8) and I == 12 / r][0]
    def q44():
        mu0, I, a, b = symbols('mu0 I a b', positive=True)
        M = (mu0 * I / (2 * b)) * pi * a**2 / I
        return [i for i, e in enumerate([mu0 / (2 * pi) * b**2 / a, mu0 / (2 * pi) * a**2 / b, mu0 * pi * b**2 / (2 * a), mu0 * pi * a**2 / (2 * b)], 1) if simplify(e - M) == 0][0]
    c[44] = q44
    c[45] = lambda: nearest(40 * 2 * math.pi * 4000 * 12e-6, [10, 12, 13, 8])
    c[50] = lambda: opt(Rational(round((4.62 + 4.632 + 4.6 + 4.64) / 4, 1) * 10, 10), [Rational(4623, 1000), Rational(462, 100), Rational(46, 10), 5])
    c[51] = lambda: [xv for xv in range(1, 100) if Rational(2 * 9 - 1, 2 * 10 - 1) == 1 - Rational(2, xv)][0]
    c[52] = lambda: (4 + 6 + 10) * (10 + 2)
    c[53] = lambda: round(1.2e8 / (6e4 * 10 / 3))
    c[54] = lambda: Rational(9, 1) / (Rational(1, 1) / (Rational(1, 25) + Rational(1, 30) + Rational(1, 45)) / 100)
    c[55] = lambda: round(6.6e-6 / (1.5e-6 * 1.1), 9)
    c[56] = lambda: round(0.5 * 10 / (2 * (1 * 10e-6 / 2e-6)) * 10, 9)
    c[57] = lambda: round(50 / math.hypot(300, 100 * 1 - 1 / (100 * 20e-6)) * (1 / (100 * 20e-6)), 9)
    c[58] = lambda: round(3 * 5e-7 * 2 / 3e-4 * 1000, 9)
    c[59] = lambda: round((3 * 4.002603 - 12) * 931 * 100)
    c[60] = lambda: Rational(2) * (Rational(2 - 1) / (6 - 2)) * 10
    c[62] = lambda: [i for i, pr in enumerate([(3, 1), (5, 1), (4, 1), (5, 2)], 1) if pr == (4 + 1, 1)][0]   # 4 C-H + 1 C-C sigma, 1 pi
    c[65] = lambda: opt(57 + 73, [130, 65, 260, 187])
    c[68] = lambda: opt((11 - 5) + 3, [6, 3, 9, 4])
    c[71] = lambda: [i for i, n in enumerate([4, 5, 4, 3], 1) if n == 3][0]

    def q73():
        cands = [(12, 22, 11), (11, 18, 12), (14, 20, 10), (12, 20, 12)]
        ok = [i for i, (C, H, O) in enumerate(cands, 1) if 12 * C + H + 16 * O == 342 and abs(1200 * C / 342 - 42.1) < 0.1 and abs(100 * H / 342 - 6.4) < 0.1]
        return ok[0]
    c[73] = q73
    c[81] = lambda: round(math.sqrt(2 * 2.18e-18 / 9.1e-31) / 1e5)
    c[83] = lambda: -(7 - Rational(15, 2)) * 300
    c[84] = lambda: round((0.2 - 2 * 0.05) * 0.083 * 300 * 10)

    def q85():
        nA = math.log(2.4e-2 / 6e-3) / math.log(4)
        nB = math.log(2.88e-1 / 7.2e-2) / math.log(2)
        return round(nA + nB)
    c[85] = q85
    c[90] = lambda: round(26.4 / (9.3 / 93 * (93 - 3 + 3 * 80)) * 100)
    return c
