"""Answer checks for JEE Main 2023 (Session 2), 10 Apr Shift 1."""
from pyq_checks.common import *
from sympy import floor, N as N_


def checks():
    c = {}

    def q1():
        a, b, cc = tan(pi / 180), log(123), log(1234)
        f = lambda t: (a * t + b) / (t * cc - a)
        assert simplify(f(f(x)) - x) == 0
        g = x + 4 / x
        m = g.subs(x, solve(diff(g, x), x)[1])
        return opt(m, [0, 2, 4, 8])
    c[1] = q1

    def q2():
        X, Y = symbols('X Y', real=True)
        from sympy import re as Re
        z = X + sympy_I * Y
        w = expand_complex((2 * z - 3 * sympy_I) * (2 * X - sympy_I * (2 * Y + 1)))   # numerator times conj(2z + i)
        r = expand(Re(w).subs(X, -Y**2) / 4)                 # real part = 0
        val = expand(r + Rational(3, 4) - (Y**4 + Y**2 - Y))
        assert val == 0                                      # so y^4 + y^2 - y = 3/4
        return opt(Rational(3, 4), [Rational(2, 3), Rational(3, 2), Rational(3, 4), Rational(4, 3)])
    from sympy import expand_complex
    c[2] = q2

    def q3():
        al, be = symbols('al be')
        M = Matrix([[2, -1, 3], [3, 2, -1], [4, 5, al]])
        a0 = solve(M.det(), al)[0]
        def kind(av, bv):
            A = Matrix([[2, -1, 3, 5], [3, 2, -1, 7], [4, 5, av, bv]])
            r1, r2 = A[:, :3].rank(), A.rank()
            return 'unique' if r1 == 3 else ('none' if r2 > r1 else 'inf')
        truth = [kind(a0, 8) == 'none', kind(a0 + 1, 8) == 'unique', kind(a0, 9) == 'inf', kind(-6, 9) == 'inf']
        return [i for i, t in enumerate(truth, 1) if not t][0]
    c[3] = q3

    def q4():
        dA = 2
        d3A = 3**3 * dA
        dB = d3A**3 * dA**2
        v = 3**3 * dB**2
        return opt(v, [3**12 * 6**11, 3**12 * 6**10, 3**10 * 6**11, 3**11 * 6**10])
    c[4] = q4

    def q5():
        a, b = symbols('a b', positive=True)
        c1 = math.comb(13, 2) * a**11 * (-1)**2 / b**2
        c2 = math.comb(13, 6) * a**7 / b**6
        t = symbols('t', positive=True)                     # t = a^4 b^4
        val = solve(simplify(c1 / c2).subs(a**4, t / b**4) - 1, t)[0]
        return opt(val, [11, 22, 33, 44])
    c[5] = q5

    def q6():
        for a in range(1, 200):
            for r in range(1, 50):
                if a * a * (1 + r * r + r**4) == 33033:
                    return opt(a * (1 + r + r * r), [231, 220, 210, 241])
    c[6] = q6

    def q7():
        V = x * (30 - 2 * x)**2
        xs = [s for s in solve(diff(V, x), x) if 0 < s < 15][0]
        return opt(900 - 4 * xs**2, [675, 1025, 900, 800])
    c[7] = q7

    def q8():
        F = exp(sin(x)**2) * cos(x)
        assert simplify(diff(F, x) - exp(sin(x)**2) * (cos(x) * sin(2 * x) - sin(x))) == 0
        C = 1 - F.subs(x, 0)
        return opt(simplify(F.subs(x, pi / 3) + C), [-exp(Rational(3, 4)), exp(Rational(3, 4)), -exp(Rational(3, 4)) / 2, exp(Rational(3, 4)) / 2])
    c[8] = q8

    def q9():
        C = symbols('C')
        f = x**2 * (-1 / (3 * x**3) + C)
        assert simplify(x**2 * diff(f, x) - 2 * x * f - 1) == 0
        f = f.subs(C, solve(f.subs(x, 1) - Rational(2, 3), C)[0])
        return opt(18 * f.subs(x, 3), [150, 160, 180, 210])
    c[9] = q9

    def q10():
        K, y = symbols('K y')
        Kv = solve(4 - 0 - K * 2, K)[0]
        ys = solve(64 - y**2 - Kv * 8, y)
        opts = [4 * sqrt(3), -4 * sqrt(2), 2 * sqrt(3), -2 * sqrt(3)]
        hits = [i for i, o in enumerate(opts, 1) if any(simplify(o - s) == 0 for s in ys)]
        assert len(hits) == 1
        return hits[0]
    c[10] = q10

    def q11():
        Y = symbols('Y')
        ys = solve((3 - 3 * Y)**2 + Y**2 - 9, Y)
        yp = [v for v in ys if v != 0][0]
        area = Rational(1, 2) * 3 * yp
        return opt(area.p - area.q, [15, 16, 17, 18])
    c[11] = q11

    def q12():
        l = symbols('l', positive=True)
        r2 = (l * sqrt(3) / 2)**2 + (l / 2 - 2 * l / 5)**2
        return opt(sqrt(r2), [sqrt(19) / 7 * l, sqrt(19) / 5 * l, 2 * l / 3, 3 * l / 5])
    c[12] = q12

    def q13():
        C = 3 * Matrix([2, 1, -1]) - Matrix([2, 4, 6]) - Matrix([0, -2, -5])
        n = Matrix([1, 2, 4])
        t = (n.dot(C) - 11) / n.dot(n)
        I = C - 2 * t * n
        a, b, g = I
        return opt(a * b + b * g + g * a, [70, 72, 74, 76])
    c[13] = q13

    def q14():
        t = symbols('t')
        P = Matrix([3 * t - 3, t - 2, 1 - 2 * t])
        tv = solve(sum(P) - 2, t)[0]
        P = P.subs(t, tv)
        q = abs(3 * P[0] - 4 * P[1] + 12 * P[2] - 32) / 13
        opts = [x**2 + 18 * x + 72, x**2 - 18 * x - 72, x**2 + 18 * x - 72, x**2 - 18 * x + 72]
        return [i for i, f in enumerate(opts, 1) if f.subs(x, q) == 0 and f.subs(x, 2 * q) == 0][0]
    c[14] = q14

    def q15():
        d1, d2 = Matrix([1, -2, 2]), Matrix([1, 2, 0])
        w = Matrix([4, 1, -3]) - Matrix([-2, 0, 5])
        cr = d1.cross(d2)
        return opt(abs(w.dot(cr)) / sqrt(cr.dot(cr)), [6, 7, 8, 9])
    c[15] = q15

    def q16():
        A, B, C, P = Matrix([-2, 1, -3]), Matrix([2, 4, -2]), Matrix([-4, 2, -1]), Matrix([-1, -2, 3])
        n = (B - A).cross(C - A)
        return opt(abs(P.dot(n)) / sqrt(n.dot(n)), [Rational(7, 3), Rational(8, 3), 3, Rational(10, 3)])
    c[16] = q16

    def q17():
        u, v, Q = Matrix([1, 0]), Matrix([1, 1]) / sqrt(2), Matrix([0, 1])
        a, b = symbols('a b')
        s = solve(list(Q - a * u - b * v), [a, b], dict=True)[0]
        opts = [3 * x**2 - 2 * x - 1, 3 * x**2 + 2 * x - 1, x**2 - x - 2, x**2 + x - 2]
        return [i for i, f in enumerate(opts, 1) if simplify(f.subs(x, s[a])) == 0 and simplify(f.subs(x, s[b]**2)) == 0][0]
    c[17] = q17

    def q18():
        good = sum(1 for d1 in range(1, 7) for d2 in range(1, 7) if 2**(d1 + d2) < math.factorial(d1 + d2))
        p = Fraction(good, 36)
        return opt(4 * p.numerator - 3 * p.denominator, [12, 10, 8, 6])
    c[18] = q18

    def q19():
        v = 96 * math.prod(math.cos(2**k * math.pi / 33) for k in range(5))
        return nearest(v, [1, 2, 3, 4])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=3))
        neg = [not ((p or q) and (q or not r)) for p, q, r in rows]
        opts = [lambda p, q, r: (p or r) and not q, lambda p, q, r: ((not p) or r) and not q,
                lambda p, q, r: ((not p) or (not q)) or not r, lambda p, q, r: ((not p) or (not q)) and not r]
        return [i for i, f in enumerate(opts, 1) if [f(*t) for t in rows] == neg][0]
    c[20] = q20

    c[22] = lambda: sum(1 for n in range(-100, 100) if abs(n * n - 10 * n + 19) < 6)

    def q23():
        from itertools import permutations
        cnt = 0
        for p in permutations('1234567'):
            s = ''.join(p)
            if '153' not in s and '2467' not in s:
                cnt += 1
        return cnt
    c[23] = q23

    def q24():
        n = [n for n in range(2, 50) if math.comb(n, 2) * math.comb(n - 2, 2) * 2 == 840][0]
        return 2 * n
    c[24] = q24

    c[25] = lambda: Poly(expand((1 - x + 2 * x**3)**10), x).coeff_monomial(x**7)

    def q26():
        terms = list(range(3, 374, 5))
        return sum(t for t in terms if t % 3 != 0)
    c[26] = q26

    def q27():
        import mpmath
        def f(t):
            fl = math.floor(t)
            return abs(t * fl) if t < 0 else abs((t - 1) * fl)
        pts = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]
        cand = [-1, 0, 1]
        h = 1e-7
        disc = [p for p in cand if abs(f(p - h) - f(p)) > 1e-4 or abs(f(p + h) - f(p)) > 1e-4]
        nd = [p for p in cand if p in disc or abs((f(p) - f(p - h)) / h - (f(p + h) - f(p)) / h) > 1e-3]
        return len(disc) + len(nd)
    c[27] = q27

    def q28():
        A = integrate(sqrt(1 - (x + 1)**2) - x**2, (x, -1, 0))
        return simplify(12 * (pi - 4 * A))
    c[28] = q28

    def q29():
        m = symbols('m', positive=True)
        mv = solve((4 * m + 1 / m)**2 - 16 * (1 + m * m), m)[0]
        P = Matrix([1 / mv**2, 2 / mv])
        return simplify((P[0] - 4)**2 + P[1]**2 - 16)
    c[29] = q29

    def q30():
        X = symbols('X')
        mids, fs = [5, 15, 25, 35, 45], [2, 3, X, 5, 4]
        xv = solve(sum(f * m for f, m in zip(fs, mids)) - 28 * sum(fs), X)[0]
        fs = [f.subs(X, xv) if hasattr(f, 'subs') else f for f in fs]
        N = sum(fs)
        return sum(f * (m - 28)**2 for f, m in zip(fs, mids)) / N
    c[30] = q30

    c[31] = lambda: opt(asin(Rational(1, 2)), [pi / 2, pi / 3, pi / 4, pi / 6])
    c[33] = lambda: opt(Rational(8)**Rational(5, 3) / 8, [8**Rational(3, 2), 4, 8, Rational(1, 8)])
    c[34] = lambda: opt(sqrt(3), [1, sqrt(3), 9, 3])
    c[35] = lambda: opt(2 * 1 + 3 * 2 + 3 + Rational(1, 2) * 4, [12, 14, 16, 13])
    c[37] = lambda: opt(200 * (1 - Rational(1, 2)), [300, 500, 400, 100])
    c[39] = lambda: opt(50 * sin(pi / 2) / sin(pi / 6), [50, 50 * sqrt(2), 100, 100 * sqrt(2)])
    c[40] = lambda: [1, Rational(1, 2), Rational(1, 3), Rational(1, 4)].index(Rational(1, 3)) + 1
    c[42] = lambda: opt(Rational(15 + 3, 15 - 3), [2, 5, 1, Rational(3, 2)])
    c[43] = lambda: opt((10 - 8) / (Rational(16, 10) / 8), [10, 12, 13, Rational(133, 10)])
    c[44] = lambda: [2, 1, Rational(1, 2), 0].index(2 - 1) + 1
    c[46] = lambda: opt(1 / sqrt(Rational(600, 300)), [Rational(1, 2), 2, 1 / sqrt(2), sqrt(2)])
    c[47] = lambda: 3 if (2 * 12 - 2 * (12 - 4)) == 8 else 0

    def q50():
        # nodes: a, b, T (top), O (centre); conductances
        import itertools
        Va, Vb = symbols('Va Vb')
        T, O = symbols('T O')
        R = {('a', 'T'): 4, ('T', 'b'): 4, ('a', 'b'): 16, ('O', 'T'): 4, ('O', 'a'): 4, ('O', 'b'): 4}
        V = {'a': 1, 'b': 0, 'T': T, 'O': O}
        eqs = []
        for node in ('T', 'O'):
            eqs.append(sum((V[node] - V[o]) / r for (p, o2), r in R.items() for (n1, o) in [(p, o2), (o2, p)] if n1 == node))
        s = solve(eqs, [T, O])
        I = sum((1 - V[o].subs(s) if hasattr(V[o], 'subs') else 1 - V[o]) / r for (p, o2), r in R.items() for (n1, o) in [(p, o2), (o2, p)] if n1 == 'a')
        return opt(1 / I, [16, 20, 24, Rational(16, 5)])
    c[50] = q50

    c[51] = lambda: round((2 + 1.14) * 10 * 1.6 / (math.pi * 0.002**2 * 2e11) / 1e-6)
    c[52] = lambda: 6 / 0.003 / 100
    c[53] = lambda: 4**2
    c[54] = lambda: 0.5 * 1 * 22**2 + 1 * 10 * 0.30
    def q55():
        cc = symbols('cc', positive=True)
        a, b = 2, 3
        return solve((a - b + cc) - (a * a - b * b + cc * cc) / cc, cc)[0]
    c[55] = q55
    c[56] = lambda: round(1.5e-5 * (1e-6 / 60 * 6e23) / 1e10)

    def q57():
        th = symbols('th')
        sols = [s for s in solve(16 * cos(th)**2 * sin(th)**2 - 3, th) if 0 < s < pi / 2]
        degs = sorted(round(float(s * 180 / pi)) for s in sols)
        return degs[0]
    c[57] = q57

    c[58] = lambda: round(0.15 * (0.15 * 4 * 1 / 5) * 1 * 1000)
    c[59] = lambda: 2.4e3 / (60 / 0.15)
    c[60] = lambda: (10 * 10) / (10 / 10)
    def q61():
        n = Rational(28375, 10000) / Rational(227, 10)
        N = n * Rational(6022, 1000) * 10**23
        opts = [(1.505e23, 0.250), (7.527e23, 0.125), (7.527e22, 0.125), (7.527e22, 0.250)]
        return [i for i, (m, mo) in enumerate(opts, 1) if abs(float(N) - m) < 1e20 and abs(float(n) - mo) < 1e-9][0]
    c[61] = q61
    def q62():
        X, Y = symbols('X Y')
        target = -Y - (-X) / 2                                # (B) - (A)/2
        opts = [(X + 2 * Y) / 2, 2 * Y - X, (2 * X - Y) / 2, (X - 2 * Y) / 2]
        return [i for i, o in enumerate(opts, 1) if simplify(o - target) == 0][0]
    c[62] = q62
    c[81] = lambda: round(940.3 / 0.6)
    c[84] = lambda: round((1 + 0.3 - 1) * 100)
    c[86] = lambda: round((3 * 2.2 + 1 * 0.70) / 4 * 1000)
    c[87] = lambda: round(1 / (1 / 12 + 1 / 3))
    return c
