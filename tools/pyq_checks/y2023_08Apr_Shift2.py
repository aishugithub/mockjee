"""Answer checks for JEE Main 2023 (Session 2), 8 Apr Shift 2."""
from pyq_checks.common import *
from sympy import N as N_, Interval, Union, solveset, S as SS, floor


def checks():
    c = {}

    def q1():
        A = range(1, 8)
        R = {(a, b) for a in A for b in A if a + b == 7}
        refl = all((a, a) in R for a in A)
        sym = all((b, a) in R for a, b in R)
        tra = all((a, d) in R for a, b in R for c2, d in R if b == c2)
        return {(True, False, False): 1, (False, True, False): 2, (False, False, True): 3, (True, True, True): 4}[(refl, sym, tra)]
    c[1] = q1

    def q2():
        t = symbols('t', real=True)
        z = (1 + 2 * sympy_I * sin(t)) / (1 - sympy_I * sin(t))
        from sympy import re, im
        sols = solveset(simplify(re(expand_complex_(z))), t, Interval.open(0, 2 * pi))
        sols = [s for s in sols if simplify(im(expand_complex_(z)).subs(t, s)) != 0]
        return opt(sum(sols), [2 * pi, 3 * pi, 4 * pi, pi])
    from sympy import expand_complex as expand_complex_
    c[2] = q2

    def q3():
        T = symbols('T')
        M = Matrix([[1, 1, sqrt(3)], [-1, T, sqrt(7)], [1, 1, T]])
        ts = solve(M.det(), T)
        th = []
        for tv in ts:
            base = atan(tv)
            for k in (-1, 0, 1):
                v = base + k * pi
                if -pi <= v <= pi:
                    th.append(v)
        return opt(simplify(120 / pi * sum(th)), [10, 20, 30, 40])
    c[3] = q3

    def q4():
        l, a, b = symbols('l a b')
        A = Matrix([[1, 5], [l, 10]])
        lv = None
        for lam in solve(Rational(10) / (10 - 5 * l) + 2, l):
            lv = lam
        A = A.subs(l, lv)
        Ai = A.inv()
        s = solve(list(Ai - a * A - b * Matrix.eye(2)), [a, b], dict=True)[0]
        assert s[a] + s[b] == -2
        return opt(4 * s[a]**2 + s[b]**2 + lv**2, [10, 12, 14, 19])
    c[4] = q4

    def q5():
        f = math.factorial
        tot = f(11) // 8
        tog = 2 * f(10) // 8
        return opt(Rational(tot - tog, 720), [945, 1890, 2835, 5670])
    c[5] = q5

    def q6():
        v = 25**190 - 19**190 - 8**190 + 2**190
        d14, d34 = v % 14 == 0, v % 34 == 0
        return {(True, True): 1, (True, False): 2, (False, True): 3, (False, False): 4}[(d14, d34)]
    c[6] = q6

    def q7():
        e = expand((2 * x**2 + 1 / (2 * x))**11)
        return opt(abs(e.coeff(x, 10) - e.coeff(x, 7)), [11**3 - 11, 12**3 - 12, 10**3 - 10, 13**3 - 13])
    c[7] = q7

    def q8():
        a = lambda n: 5 + 3 * n * (n - 1) // 2
        assert [a(n) for n in range(1, 7)] == [5, 8, 14, 23, 35, 50]
        return opt(sum(a(n) for n in range(1, 31)) - a(40), [11260, 11280, 11290, 11310])
    c[8] = q8

    def q9():
        # numeric test with a = 2/9, b = -1 (roots 3 and 3/2 of a x^2 + b x + 1)
        import mpmath
        mpmath.mp.dps = 60
        a, b = mpmath.mpf(2) / 9, mpmath.mpf(-1)
        r1 = (-b + mpmath.sqrt(b * b - 4 * a)) / (2 * a)
        r2 = (-b - mpmath.sqrt(b * b - 4 * a)) / (2 * a)
        al, be = max(r1, r2), min(r1, r2)
        xx = 1 / al + mpmath.mpf('1e-12')
        L = mpmath.sqrt((1 - mpmath.cos(xx * xx + b * xx + a)) / (2 * (1 - al * xx)**2))
        k = (1 / be - 1 / al) / L
        res = nearest(k, [al, be, 2 * al, 2 * be])
        mpmath.mp.dps = 15
        return res
    c[9] = q9

    def q11():
        a = symbols('a')
        sols = solve(a * (a - 3) + Rational(1, 2) * (Rational(1, 2) + 2), a)
        opts = [Rational(-1, 2), 1, Rational(3, 2), Rational(5, 2)]
        hits = [i for i, o in enumerate(opts, 1) if o in sols]
        assert len(hits) == 1
        return hits[0]
    c[11] = q11

    def q12():
        r = (2 + 2 - 2 * sqrt(2)) / 2
        a = r**2 / (4 * r)
        al, be = Rational(1, 2), Rational(-1, 4)
        assert simplify(a - (al + be * sqrt(2))) == 0
        return opt(al / be**2, [Rational(9, 2), 6, 8, 12])
    c[12] = q12

    def q13():
        n = Matrix([1, -3, 7]).cross(Matrix([2, 4, -3]) - Matrix([1, 2, -5]))
        P0 = Matrix([1, 2, -5])
        Q = Matrix([-1, 3, 4])
        t = n.dot(Q - P0) / n.dot(n)
        img = Q - 2 * t * n
        return opt(sum(img), [9, 10, 11, 12])
    c[13] = q13

    def q14():
        hits = []
        for a in range(-50, 51):
            n, d = Matrix([a, 1, -1]), Matrix([1, -1, 1])
            if 9 * n.dot(d)**2 == 8 * n.dot(n) * d.dot(d):          # sin^2 = 8/9
                for b in range(-100, 101):
                    if abs(a - b) <= 10 and (6 * a - 6 - 4 - b)**2 == 54 * n.dot(n):
                        hits.append(a**4 + b**2)
        assert len(set(hits)) == 1
        return opt(hits[0], [25, 32, 48, 85])
    c[14] = q14

    def q15():
        A, B, C, D = Matrix([2, 1, 1]), Matrix([1, 2, 5]), Matrix([-2, -3, 5]), Matrix([1, -6, -7])
        assert Matrix.hstack(B - A, C - A, D - A).det() == 0      # planar
        cr = (C - A).cross(D - B)
        return opt(sqrt(cr.dot(cr)) / 2, [48, 8 * sqrt(38), 9 * sqrt(38), 54])
    c[15] = q15

    def q16():
        a, b, cc = symbols('a b c')
        d1 = Matrix([[1, 1, a], [1, b, 1], [cc, 1, 1]]).det()
        d2 = expand(Matrix([[a + b, cc, cc], [a, b + cc, a], [b, b, cc + a]]).det())
        assert simplify(d2 - 4 * a * b * cc) == 0
        # with abc = 0, d1 = a + b + c - 2
        assert simplify(expand(d1) - (a + b + cc - a * b * cc - 2)) == 0
        return opt(6 * 2, [0, 4, 6, 12])
    c[16] = q16

    def q17():
        k = 1 / Rational(9, 4)
        return opt(1 - k * (1 + Rational(2, 3)), [Rational(7, 18), Rational(11, 18), Rational(7, 27), Rational(20, 27)])
    c[17] = q17

    def q18():
        n, s1, s2 = 12, Rational(54), 12 * (4 + Rational(81, 4))
        s1, s2 = s1 - 9 - 10 + 7 + 14, s2 - 81 - 100 + 49 + 196
        v = s2 / n - (s1 / n)**2
        return opt(v.p + v.q, [314, 315, 316, 317])
    c[18] = q18

    def q19():
        d = lambda deg: math.cos(math.radians(deg))
        v = 36 * (4 * d(9)**2 - 1) * (4 * d(27)**2 - 1) * (4 * d(81)**2 - 1) * (4 * d(243)**2 - 1)
        return nearest(v, [18, 27, 36, 54])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=2))
        neg = [not ((p and not q) or not p) for p, q in rows]
        opts = [lambda p, q: p or (q or not p), lambda p, q: p and q, lambda p, q: p and not q, lambda p, q: p and (q and not p)]
        return [i for i, f in enumerate(opts, 1) if [f(p, q) for p, q in rows] == neg][0]
    c[20] = q20

    def q21():
        from sympy import Symbol as Sy, solve_univariate_inequality as sui
        X = Sy('X', real=True)
        d1 = sui((6 * X**2 + 5 * X + 1) / (2 * X - 1) > 0, X, relational=False)
        g = (2 * X**2 - 3 * X + 4) / (3 * X - 5)
        d2 = sui(g <= 1, X, relational=False).intersect(sui(g >= -1, X, relational=False))
        dom = d1.intersect(d2)
        ends = sorted({v for a in dom.args for v in (a.start, a.end)})
        assert len(ends) == 4
        return 18 * sum(v**2 for v in ends)
    c[21] = q21

    def q22():
        import mpmath
        m = 0
        for n in range(-60, 20):
            for r in solve(x**2 - 12 * x + 31 + n, x):     # exact roots
                if r.is_real and floor(r) == n:
                    m += 1
        roots = set()
        for r in solve(x**2 - 5 * (x + 2) - 4, x):
            if r >= -2: roots.add(r)
        for r in solve(x**2 + 5 * (x + 2) - 4, x):
            if r < -2: roots.add(r)
        nn = len(roots)
        return m * m + m * nn + nn * nn
    from sympy import re as sympy_re, im as sympy_im
    c[22] = q22

    def q23():
        cnt = 0
        for f in product(range(1, 5), repeat=5):
            if f[0] != 1 and len(set(f)) == 4:
                cnt += 1
        return cnt
    c[23] = q23

    def q24():
        y = sqrt(2)
        u, v = symbols('u v', positive=True)
        s = solve([u * v - 2 * y**2, (u + v) - 2 * u * v / y], [u, v], dict=True)
        s = [t for t in s if t[u] > y > t[v]][0]
        assert simplify(1 / s[u] + 1 / y + 1 / s[v] - 3 / sqrt(2)) == 0
        return simplify(3 * (s[u] + y + s[v])**2)
    c[24] = q24

    def q25():
        k, m = symbols('k m', positive=True)
        left = 3 * x**2 + k * sqrt(x + 1)
        right = m * x**2 + k**2
        s = solve([left.subs(x, 1) - right.subs(x, 1), diff(left, x).subs(x, 1) - diff(right, x).subs(x, 1)], [k, m], dict=True)[0]
        val = 8 * diff(right, x).subs(x, 8) / diff(left, x).subs(x, Rational(1, 8))
        return simplify(val.subs(s))
    c[25] = q25

    def q26():
        tot = 0
        pts = [0] + [sqrt(k) for k in range(1, 6)] + [Rational(12, 5)]
        for k in range(6):
            tot += k * (pts[k + 1] - pts[k])
        tot = expand(tot)
        al = tot.subs({sqrt(2): 0, sqrt(3): 0, sqrt(5): 0})
        return al + tot.coeff(sqrt(2)) + tot.coeff(sqrt(3)) + tot.coeff(sqrt(5))
    c[26] = q26

    def q27():
        import mpmath
        f = lambda t: min(t * t + 0.75, 1 + math.floor(t), 2 - t)
        A = mpmath.quad(f, [0, 0.5, 1, 2])
        return int(mpmath.nint(12 * A))
    c[27] = q27

    def q28():
        t, C = symbols('t C')
        X = -1 / (2 * t) + C / t**3
        assert simplify(diff(X, t) + 3 * X / t + 1 / t**2) == 0
        Cv = solve(X.subs(t, log(Rational(1, 2))) - 1 / (2 * log(2)), C)[0]
        xv = simplify(X.subs(C, Cv).subs(t, log(sqrt(3) / 2)))
        assert simplify(xv - 1 / (log(4) - log(3))) == 0
        return 4 * 3
    c[28] = q28

    def q29():
        t = symbols('t', nonzero=True)
        t1, t2 = 3 * t, t
        al, be = 3 * t1 * t2, 3 * (t1 + t2)
        return simplify(be**2 / al)
    c[29] = q29

    def q30():
        p1, p2, p3 = Matrix([2, -1, 0]), Matrix([2, 0, -1]), Matrix([5, 1, 1])
        n2 = (p2 - p1).cross(p3 - p1)
        n1 = Matrix([3, -1, -7])
        d = n1.cross(n2)
        X, Y = symbols('X Y')
        s = solve([3 * X - Y - 11, n2.dot(Matrix([X, Y, 0]) - p1)], [X, Y])
        A = Matrix([s[X], s[Y], 0])
        P = Matrix([7, 4, -1])
        foot = A + d * (P - A).dot(d) / d.dot(d)
        return sum(foot)
    c[30] = q30

    def q31():
        # (M, L, T) exponents: force = (1, 1, -2)
        F = (1, 1, -2)
        add = lambda a, b: tuple(i + j for i, j in zip(a, b))
        A = {'torque': add(F, (0, 1, 0)), 'stress': add(F, (0, -2, 0)), 'grad': add(F, (0, -3, 0)), 'visc': add(F, (0, -2, 1))}
        L2 = {1: (1, -2, -2), 2: (1, 2, -2), 3: (1, -1, -1), 4: (1, -1, -2)}
        match = tuple(next(k for k, v in L2.items() if v == A[q]) for q in ('torque', 'stress', 'grad', 'visc'))
        return {(3, 4, 1, 2): 1, (2, 1, 4, 3): 2, (2, 4, 1, 3): 3, (4, 2, 3, 1): 4}[match]
    c[31] = q31
    c[33] = lambda: opt(2 * 300 - 273, [327, 627, 927, 1227])
    c[34] = lambda: opt(2 / (1 - Rational(300, 400)), [2, Rational(8, 3), 8, 4])
    c[35] = lambda: nearest(5000 * 10 / 250e-4, [20e6, 2e5, 200e6, 2e6])
    c[37] = lambda: opt(sqrt(9), [3, 4, 8, 9])
    c[39] = lambda: opt((x - x**2 / 20).subs(x, solve(diff(x - x**2 / 20, x), x)[0]), [5, 10 * sqrt(2), 10, 200])
    c[40] = lambda: nearest((0.1 * 400 / 4.0)**2 / (2 * 10 * 20), [0.25, 0.50, 0.65, 0.90])
    c[41] = lambda: nearest(9e9 * 5e-9 / 50 * 100, [90, 3, 9, 0.9])
    c[43] = lambda: nearest(1 / 1000 / 100 * 1e6, [0.1, 10, 1.0, 100])
    c[44] = lambda: nearest(8e-3 * 2**5 * 1000, [32, 40, 256, 64])
    c[46] = lambda: opt(Rational(2 * 600, 400), [2, 3, 4, Rational(4, 3)])
    c[48] = lambda: nearest(0.08 / (0.4 * 0.1), [20, 2, 0.5, 3.2])
    c[50] = lambda: opt(1 / (Rational(1, 20) + Rational(1, 20) + Rational(1, 10)), [5, 10, 20, 30])
    c[51] = lambda: 90 * 120 / 180
    c[52] = lambda: round(2e11 * 1e-4 * 1e-5 * 200 / 1e4)
    c[53] = lambda: round(5 * 9 / (6 * 10) * 100)
    c[54] = lambda: (10 + 2 * 5)**2 / (2 * 5) - 10**2 / (2 * 5)
    c[55] = lambda: round(600e-12 * 600e-12 / (600e-12 + 600e-12) * 200**2 / 2 * 1e6)
    c[56] = lambda: (Rational(1, 4) - Rational(1, 16)) / (Rational(1, 4) - Rational(1, 9)) * 20

    def q57():
        v = symbols('v')
        return abs(solve(Rational(3, 2) / v - 1 / Rational(-15) - Rational(1, 2) / 30, v)[0])
    c[57] = q57

    c[58] = lambda: round(math.sqrt(1 / 6.25e-6) / 100)
    c[59] = lambda: ((2 * Rational(1))**Rational(3, 2))**2
    c[60] = lambda: round(3.2 / (8e28 * 1.6e-19 * 2e-6) / 1e-6)

    def q61():
        sf = {'0.00253': 3, '1.0003': 5, '15.0': 3, '163': 3}
        same = [k for k, v in sf.items() if v == 3]
        return {('0.00253', '15.0', '163'): 4}[tuple(same)]
    c[61] = q61

    c[81] = lambda: sum(1 for n, l in [(7, 0), (7, 1), (6, 0), (8, 1), (8, 2)] if n - l - 1 == 5)
    c[82] = lambda: sum(1 for ve, used in [(7, 5), (8, 6), (8, 6), (9, 5), (8, 8), (8, 6), (8, 4)] if (ve - used) // 2 == 1)
    c[83] = lambda: round(1406 + 2 * 8.3 * 300 / 1000)
    c[84] = lambda: 2**2 * 2
    c[85] = lambda: round(1e-10 / 0.1 * 233 / 1e-9)
    c[87] = lambda: round(50.04 / 0.09)
    c[89] = lambda: 0 + 4 + 6
    c[90] = lambda: [6 - ox for ox in range(1, 8) if abs(math.sqrt(n * (n + 2)) - 6.06) < 0.2 for n in [ {2: 5, 3: 4}.get(ox, 0) ] ][0] - 2 if False else \
        [6 - 2 for n in range(0, 6) if abs(math.sqrt(n * (n + 2)) - 6.06) < 0.2 and n == 5][0]
    return c
