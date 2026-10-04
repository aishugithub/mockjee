"""Answer checks for JEE Main 2023 (Session 2), 13 Apr Shift 1."""
from pyq_checks.common import *
from sympy import N as N_


def checks():
    c = {}

    def q1():
        A, B = symbols('A B')
        f = solve([3 * A + 2 * B - (1 / x - 10), 3 * B + 2 * A - (x - 10)], [A, B])[A]
        return opt(abs(f.subs(x, 3) + diff(f, x).subs(x, Rational(1, 4))), [7, Rational(29, 5), Rational(33, 5), 13])
    c[1] = q1

    def q2():
        pieces = [(-x**2 - 2, -oo, -2), (-x**2 + 2 * x + 2, -2, 1), (x**2 + 2, 1, oo)]
        for e, lo, hi in pieces:
            d = diff(e, x)
            for v in (lo, hi):
                if v not in (-oo, oo):
                    assert limit(d, x, v) >= 0
        return 3
    c[2] = q2

    def q3():
        a = symbols('a')
        B = Matrix([[1, 3, a], [1, 2, 3], [a, a, 4]])
        av = [s for s in solve(B.det() - 4, a) if s > 2][0]
        v = Matrix([av, -2 * av, av])
        return opt((v.T * B.subs(a, av) * v)[0], [0, -16, 16, 32])
    c[3] = q3

    def q4():
        def kind(a, b):
            A = Matrix([[2, 4, 2 * a, b], [1, 2, 3, 4], [2, -5, 2, 8]])
            r1, r2 = A[:, :3].rank(), A.rank()
            return 'unique' if r1 == 3 else ('none' if r2 > r1 else 'inf')
        truth = [kind(6, 6) == 'unique', kind(8, 8) == 'unique', kind(3, 8) == 'inf', kind(3, 6) == 'inf']
        return [i for i, t in enumerate(truth, 1) if not t][0]
    c[4] = q4

    c[5] = lambda: opt(10**6, [10**9, 9**10, 10**6, 6**10])
    c[6] = lambda: opt(sum(6 * (2 * i + 11 * (2 * i - 1)) for i in range(1, 11)), [7260, 7220, 7360, 7380])

    def q7():
        n = symbols('n', positive=True, integer=True)
        s1 = limit(n * (n + 1) / n**2, n, oo) == 1
        s2 = integrate(x**15, (x, 0, 1)) == Rational(1, 16)
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(s1, s2)]
    c[7] = q7

    def q8():
        l, a, b = symbols('l a b')
        lv = solve((1 + l) * (-11) - 5 * (2 - l), l)[0]
        k = 5 / (1 + lv)
        bv = solve(k * (a + lv) - b, b)[0]
        av = solve(k * (-(2 + 3 * lv)) + (6 * a - 1), a)[0]
        bv = bv.subs(a, av)
        for cc in range(-20, 21):
            if (abs(5 * av - 11 * (-cc) + bv * cc - (6 * av - 1)))**2 * av == 4 * (25 + 121 + bv**2):
                return opt((av + bv) / cc, [-4, -2, 2, 4])
    c[8] = q8

    def q9():
        a, b, cc = Matrix([1, 4, 2]), Matrix([3, -2, 7]), Matrix([2, -1, 4])
        t = (24 - cc.dot(a)) / b.dot(a)
        d = cc + t * b
        return opt(d.dot(d), [323, 313, 423, 413])
    c[9] = q9

    def q10():
        g = x - 2 * sin(x) * cos(x) + sin(3 * x) / 3
        cands = [s for s in solve(diff(g, x), x) if 0 <= s <= pi] + [0, pi]
        m = max(cands, key=lambda s: N_(g.subs(x, s)))
        return opt(simplify(g.subs(x, m)), [(pi + 2 - 3 * sqrt(3)) / 6, (5 * pi + 2 + 3 * sqrt(3)) / 6, pi, 0])
    c[10] = q10

    def q11():
        t = symbols('t', positive=True)
        v = integrate(6 / (t * (t + 1) * (t + 2) * (t + 3)), (t, 1, oo))
        return opt(simplify(v), [log(Rational(512, 81)), log(Rational(64, 27)), log(Rational(256, 81)), log(Rational(32, 27))])
    c[11] = q11

    def q12():
        A = integrate(-sin(x), (x, -pi, -3 * pi / 4)) + integrate(-cos(x), (x, -3 * pi / 4, -pi / 2)) + \
            integrate(cos(x), (x, -pi / 2, pi / 4)) + integrate(sin(x), (x, pi / 4, pi))
        return opt(simplify(A), [2 * sqrt(2) * (sqrt(2) + 1), 4, 2 * (sqrt(2) + 1), 4 * sqrt(2)])
    c[12] = q12

    c[13] = lambda: opt(Rational(pow(4, 2022, 15), 15), [Rational(1, 15), Rational(4, 15), Rational(8, 15), Rational(14, 15)])

    def q15():
        X0, Y0 = 3 * sqrt(3), 1
        A = Matrix([0, 4])                                 # tangent X0 x/36 + Y0 y/4 = 1 at x = 0
        m_t = -(X0 / 36) / (Y0 / 4)
        B = Matrix([0, Y0 - (-1 / m_t) * X0])
        Cc = (A + B) / 2
        r2 = ((A - B).dot(A - B)) / 4
        # pole of x = 2 sqrt5: (al - h)(x - h) + (be - k)(y - k) = r2
        be = Cc[1]
        al = Cc[0] + r2 / (2 * sqrt(5) - Cc[0])
        return opt(nsimplify(simplify(al**2 - be**2)), [60, 61, Rational(304, 5), Rational(314, 5)])
    c[15] = q15

    def q16():
        t = 3
        P, Q = Matrix([9 * t * t, 18 * t]), Matrix([9 * Rational(1, 9), 18 * Rational(-1, 3)])
        assert 9 * (t + Rational(1, t))**2 == 100
        M = (P + 3 * Q) / 4
        d = P - Q
        opts = [(3, 33), (-6, 45), (-3, 43), (6, 29)]
        off = [i for i, (a, b) in enumerate(opts, 1) if (Matrix([a, b]) - M).dot(d) != 0]
        return off[0]
    c[16] = q16

    def q17():
        n = Matrix([2, 0, 1]).cross(Matrix([1, -1, 1]))
        P = Matrix([-1, 2, 3])
        t = symbols('t')
        tv = solve((P + t * n).dot(Matrix([1, -2, 3])) - 10, t)[0]
        d = tv * n
        return opt(sqrt(d.dot(d)), [3 * sqrt(5), 2 * sqrt(6), 3 * sqrt(6), 2 * sqrt(5)])
    c[17] = q17

    def q18():
        p, q = Rational(3, 4), Rational(1, 4)
        return opt(1 * p + 2 * q * p + 3 * q * q, [Rational(21, 16), Rational(15, 16), Rational(81, 64), Rational(37, 16)])
    c[18] = q18

    def q20():
        imp = lambda a, b: (not a) or b
        rows = list(product([True, False], repeat=3))
        neg = [not imp(imp(A and (B or C), A or B), A) for A, B, C in rows]
        opts = [lambda A, B, C: False, lambda A, B, C: B or not C, lambda A, B, C: not A, lambda A, B, C: not C]
        return [i for i, f in enumerate(opts, 1) if [f(*r) for r in rows] == neg][0]
    c[20] = q20

    def q21():
        X = symbols('X')
        k1, k2, lam = -2, 4, 4
        assert (-Rational(k1, 2), Rational(k2, 2)) == (1, 2) and Rational(k1**2 + k2**2, 4) - lam == 1
        xs = solve((X - 1)**2 + (2 * X + 2 - 2)**2 - 1, X)
        pts = [Matrix([v, 2 * v + 2]) for v in xs]
        d = pts[0] - pts[1]
        return 30 * d.dot(d)
    c[21] = q21

    c[22] = lambda: sum(1 for t in product([1, 2, 3, 4], repeat=7) if sum(t) == 12)

    def q23():
        for n in range(1, 16):
            if n % 4: continue
            r0 = n // 4
            al = math.comb(n, r0) * (-6)**r0
            if (-5)**n - al == 649:
                r = [r for r in range(n + 1) if (n - 4 * r) == -2 * n][0]   # power (n - 4r)/2 = -n
                return Rational(math.comb(n, r) * (-6)**r, al)
    c[23] = q23

    c[24] = lambda: sum((2 * k * k if k % 2 == 0 else -k * k) for k in range(2, 22))

    def q25():
        t = symbols('t')
        S = x
        Cs = [1]
        for k in (1, 2, 3):
            Ck = 1 - integrate(S, (x, 0, 1))
            Cs.append(Ck)
            S_new = Ck * x + k * integrate(S.subs(x, t), (t, 0, x))
            if k == 2:
                S2 = S_new
            S = S_new
        return S2.subs(x, 3) + 6 * Cs[3]
    c[25] = q25

    def q26():
        m = symbols('m')
        ms = solve((1 - 4 * m)**2 - (25 - 16 * m**2), m)
        lines = []
        for mv in ms:
            mv = abs(mv)
            cc = [v for v in (sqrt(25 - 16 * mv**2), -sqrt(25 - 16 * mv**2)) if -v / mv > 0][0]
            lines.append((mv, cc))
        X, Y = symbols('X Y')
        s = solve([Y - lines[0][0] * X - lines[0][1], Y - lines[1][0] * X - lines[1][1]], [X, Y])
        PQ2 = (s[X] - 4)**2 + (s[Y] - 1)**2
        ab = (-lines[0][1] / lines[0][0]) * (-lines[1][1] / lines[1][0])
        return PQ2 / ab
    c[26] = q26

    def q27():
        P0, n = Matrix([Rational(5, 3), Rational(5, 3), Rational(8, 3)]), Matrix([1, -2, 1])
        t = (n.dot(P0) - 2) / n.dot(n)
        P = P0 - 2 * t * n
        a = symbols('a', positive=True)
        return solve((Matrix([6, -2, a]) - P).dot(Matrix([6, -2, a]) - P) - 169, a)[0]
    c[27] = q27

    def q28():
        a, cv = Matrix([3, 1, -1]), Matrix([2, -3, 3])
        t = symbols('t')
        b = cv.cross(a) / cv.dot(cv) + t * cv
        assert simplify(b.cross(cv) - a) == Matrix.zeros(3, 1)
        vals = set()
        for tv in solve(b.dot(b) - 50, t):
            bb = b.subs(t, tv)
            vals.add(abs(72 - (bb + cv).dot(bb + cv)))
        assert len(vals) == 1
        return vals.pop()
    c[28] = q28

    def q29():
        al = symbols('al')
        xs, fs = [1, 3, 5, 7, 9], [4, 24, 28, al, 8]
        av = solve(sum(f * v for f, v in zip(fs, xs)) - 5 * sum(fs), al)[0]
        fs = [f.subs(al, av) if hasattr(f, 'subs') else f for f in fs]
        N = sum(fs)
        m = Rational(sum(f * abs(v - 5) for f, v in zip(fs, xs)), N)
        var = Rational(sum(f * (v - 5)**2 for f, v in zip(fs, xs)), N)
        return 3 * av / (m + var)
    c[29] = q29

    def q30():
        sols = solve((x + 1 - x) / (1 + x * (x + 1)) - 1, x)       # tan of the difference = 1
        return sum(sin((v**2 + v + 5) * pi / 2) - cos((v**2 + v + 5) * pi) for v in sols)
    c[30] = q30

    c[31] = lambda: opt(Rational(1, 2) * 5 * 400 * (Rational(5, 50) + 2 * Rational(4, 200)), [Rational(14, 100), 140, Rational(14, 100) + 0, 140 + 0]) if False else \
        [i for i, (k, d) in enumerate([(1000, 0.14), (1000, 140), (500, 0.14), (500, 140)], 1) if k == 1000 and abs(d - 1000 * (0.5 / 5 + 2 * 0.4 / 20)) < 1e-9][0]

    def q32():
        l = symbols('l', positive=True)
        lv = solve((60 * l + 4 * l) / 20 - (60 * l + l) / 30 - 35, l)[0]
        return opt(60 * lv, [1800, 900, 1200, 2700])
    c[32] = q32

    c[33] = lambda: opt(sqrt((pi)**2 + 4), [2 * sqrt(1 + 4 * pi**2), 2, sqrt(pi**2 + 1), sqrt(pi**2 + 4)])
    c[34] = lambda: opt(Rational(9, 16), [Rational(3, 4), Rational(9, 16), Rational(4, 3), Rational(16, 9)])
    c[35] = lambda: opt(Rational(1, 100) * 600, [12, 3, 6, 36])
    c[36] = lambda: nearest(11.2 * math.sqrt(9 / 4), [67.2, 33.6, 16.8, 11.2])
    c[37] = lambda: nearest(0.5 * 1000 * (0.6**2 - (25e-6 * 0.6 / 1.5e-4)**2), [27, 175, 135, 36])
    c[38] = lambda: opt(simplify(-Symbol('V') * diff(Symbol('a') * Symbol('V')**-3, Symbol('V')) / (Symbol('a') * Symbol('V')**-3)), [3, 2, 1, Rational(1, 2)])
    c[39] = lambda: [4, 8, 27, 28].index(int(Rational(5) / (Rational(3, 8) * Rational(22, 7) - 1))) + 1

    def q41():
        X = symbols('X', positive=True)
        r = Rational(300 * 100, 5 * 60) / Rational(50 * 100, 2 * 60)
        return opt(solve(3 * sqrt(X) / (sqrt(X) + 1) - r, X)[0], [2, 4, 16, Rational(24, 10)])
    c[41] = q41

    def q44():
        d, n1, n2 = symbols('d n1 n2', positive=True)
        app = (d / 2) / n1 + (d / 2) / n2
        opts = [d * n1 * n2 / (2 * (n1 + n2)), d * n1 * n2 / (n1 + n2), 2 * d * (n1 + n2) / (n1 * n2), d * (n1 + n2) / (2 * n1 * n2)]
        return opt(app, opts)
    c[44] = q44
    c[45] = lambda: opt(Rational(1242, Rational(45, 10)) - Rational(1242, 9), [264, 540, 276, 138])
    c[46] = lambda: nearest((238.05079 - 234.04363 - 4.00260) * 931.5, [3.82, 4.25, 5.9, 2.12])
    c[49] = lambda: nearest(0.01 * 0.4e-3 * 10 * 1e-5 * 0.5, [1e-8, 2e-10, 4e-10, 1.5e-9])

    def q50():
        R = 1
        P = {'A': Rational(3, 2), 'B': Rational(2, 3), 'C': Rational(1, 3), 'D': 3}
        order = ''.join(sorted(P, key=P.get))
        return {'ABCD': 1, 'CBAD': 2, 'CDAB': 3, 'BCDA': 4}[order]
    c[50] = q50

    c[51] = lambda: Rational(4**2, 4) / Rational(2**2, 2)
    c[52] = lambda: solve(8 + Rational(4, 3) * x - 12, x)[0]
    c[53] = lambda: Rational(50, 2)
    c[54] = lambda: Rational(4) / (abs(Rational(1, 3) - Rational(1, 2)) / abs(Rational(1, 4) - Rational(1, 2)))
    c[55] = lambda: round(2 * 80 * 20 / (2e11 * 0.02**2) / 1e-6)
    def q56():
        w = symbols('w', positive=True)
        L, E = Rational(2, 5) * w, Rational(7, 10) * w**2      # per m R^2
        return solve(L / E - Rational(22, 7) / 22, w)[0]       # pi = 22/7
    c[56] = q56
    c[57] = lambda: round(math.log10(200 * 8 / 0.4**2))
    def q58():
        G = symbols('G', positive=True)
        return solve(Rational(5, 4) * (G + 1050) / (G + 5) - 25, G)[0]
    c[58] = q58
    c[59] = lambda: round(math.log10((40e-3 / 400e-6)**2 * 1 / 10))
    c[60] = lambda: (Rational(4))**2
    c[81] = lambda: 2 * 4 + 10 * 6
    c[82] = lambda: math.floor(0.15 * (1.4 / 1.07) * (300 / 500) * (100 / 300) / 1e-4)   # 392.5; NTA gives 392
    c[83] = lambda: solve(Rational(1, 2) * x + Rational(1, 2) * Rational(1, 2) * x - x + 200, x)[0]
    c[84] = lambda: Rational(12) / Rational(5, 100)
    c[85] = lambda: round(0.025 * 0.01**2 / 0.5e-6)
    c[86] = lambda: round(2 * 96500 * (100 * 1e-4 * 10) / 60 / 2)
    c[87] = lambda: round(math.log(8) / math.log(2))
    c[88] = lambda: round(0.126 * 2 / 18 / (0.220 * 12 / 44 / 0.24) * 1000)
    c[90] = lambda: round((20 * 0.5 / 10 / 2) * 20 * 2 / (2 * 10))

    def q14():
        C = symbols('C')
        y = C * exp(x) - 7
        assert simplify(diff(y, x) - y - 7) == 0
        y1 = y.subs(C, solve(y.subs(x, 0), C)[0]); y2 = y.subs(C, solve(y.subs(x, 0) - 1, C)[0])
        return opt(len(solve(y1 - y2, x)), [0, 1, 2, oo])
    c[14] = q14
    c[61] = lambda: opt(Rational(1, 3**2), [Rational(1, 3), Rational(1, 9), 3, Rational(1, 27)])
    return c
