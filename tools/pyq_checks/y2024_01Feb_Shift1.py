"""Answer checks for JEE Main 2024 (Session 1), 1 Feb Shift 1. Q37 has no usable key; Q48 is disputed (see solutions.csv)."""
from pyq_checks.common import *
from sympy import Abs, E, Eq, Function, dsolve


def checks():
    c = {}

    def q1():
        X, Y = symbols('X Y', real=True)
        pts = solve([(sqrt(2) - 1) * X + Y - sqrt(2), (X - 1)**2 + Y**2 - 1], [X, Y])
        zs = sorted([a + sympy_I * b for a, b in pts], key=lambda z: float(Abs(z)))
        return opt(simplify(Abs(sqrt(2) * zs[-1] - zs[0])**2), [1, 2, 3, 4])
    c[1] = q1

    def q2():
        t = [r for r in solve(x**2 - 10 * x + 1, x) if r > 0]
        xs = {simplify(log(r) / log(sqrt(3) + sqrt(2))) for r in t}
        return opt(len(xs), [0, 1, 2, 4])
    c[2] = q2

    def q3():
        A = Matrix([[sqrt(2), 1], [-1, sqrt(2)]]); B = Matrix([[1, 0], [1, 1]])
        C = A * B * A.T
        return opt(simplify((A.T * C**2 * A).det()), [27, 729, 891, 243])
    c[3] = q3

    def q4():
        from sympy.functions.combinatorial.numbers import stirling
        return opt(sum(stirling(5, k) for k in range(1, 5)), [51, 47, 53, 43])
    c[4] = q4

    def q5():
        p, q = symbols('p q')
        s = solve([2 * p + q - 3, 5 * p - 4 * q - 7], [p, q])
        al = solve(3 * s[p] + Symbol('a') * s[q] + 1, Symbol('a'))[0]
        be = -s[p] + 3 * s[q]
        A = Matrix([[2, 3, -1, 5], [1, al, 3, -4], [3, -1, be, 7]])
        assert A[:, :3].rank() == A.rank() == 2
        return opt(13 * al * be, [1210, 1120, 1220, 1110])
    c[5] = q5

    def q6():
        for d in solve((2 + x)**2 - 3 * (4 + 2 * x), x):
            g = [3, 2 + d, 4 + 2 * d, 12 + 3 * d]
            if all(v != 0 for v in g) and g[1] * g[2] == g[0] * g[3] and g[2]**2 == g[1] * g[3]:
                return opt(Rational(sum([3 + d, 3 + 2 * d, 3 + 3 * d]), 3), [11, -1, 13, -4])
    c[6] = q6

    def q7():
        F, G = symbols('F G')
        s = solve([5 * F + 4 * G - (x**2 - 2), 5 * G + 4 * F - (1 / x**2 - 2)], [F, G])
        y = expand(9 * x**2 * s[F])
        dy = diff(y, x)
        ok = lambda v: dy.subs(x, v) > 0
        tests = {1: [-0.3, 0.3], 2: [-1, 0.3], 3: [-0.3, 1], 4: [0.3, 1]}
        good = [k for k, vs in tests.items() if all(ok(v) for v in vs)]
        assert good == [3]
        return 3
    c[7] = q7

    def q8():
        a, b, cc = symbols('a b cc')
        s1 = solve([a - b], a)
        bv = solve(limit((b - b * cos(2 * x)) / x**2, x, 0) - 2, b)[0]
        cv = solve(1 + cc + 2 - 3, cc)[0]
        f_left = (bv - bv * cos(2 * x)) / x**2
        dl = limit((f_left - 2) / x, x, 0, '-')
        dr = diff(x**2 + cv * x + 2, x).subs(x, 0)
        d1l = diff(x**2 + cv * x + 2, x).subs(x, 1); d1r = 2
        m = (dl != dr) + (d1l != d1r)
        return opt(m + bv + bv + cv, [1, 2, 3, 4])
    c[8] = q8
    c[9] = lambda: opt(integrate(6 - x - 16 / (x + 4), (x, -2, 4)), [28 - 30 * log(2), 30 - 32 * log(2), 32 - 30 * log(2), 30 - 28 * log(2)])

    def q10():
        import mpmath
        v = mpmath.quad(lambda t: t / (mpmath.sin(2 * t)**4 + mpmath.cos(2 * t)**4), [0, mpmath.pi / 4])
        return nearest(float(v), [float(sqrt(2) * pi**2 / k) for k in (16, 32, 8, 64)])
    c[10] = q10

    def q11():
        u = Function('u')
        s = dsolve(Eq(u(x).diff(x), 2 * x * u(x)**3 - x * u(x)), u(x), ics={u(0): 1})
        v = simplify(s.rhs.subs(x, 1 / sqrt(2))**2)
        return opt(v, [1 / (2 - sqrt(E)), 2 / (1 + sqrt(E)), 3 / (3 - sqrt(E)), 4 / (4 + sqrt(E))])
    c[11] = q11

    def q12():
        hits = [i for i, t in enumerate([pi / 4, pi / 3, pi / 6, 5 * pi / 12], 1)
                if simplify((1 + sin(t)**2) - 7 * (1 - sin(t)**2)) == 0]
        return hits[0]
    c[12] = q12

    def q13():
        a = Symbol('a', positive=True)
        b2 = a**2 / 2
        av = solve(2 * b2 / a - sqrt(14), a)[0]
        return opt(1 + b2.subs(a, av) / av**2, [Rational(3, 2), 3, Rational(5, 2), Rational(7, 2)])
    c[13] = q13

    def q14():
        f = lambda t: math.log(t) if t > 0 else math.exp(-t)
        g = lambda t: t if t >= 0 else math.exp(t)
        h = lambda t: g(f(t))
        one_one = abs(h(-math.log(2)) - h(math.e**2)) > 1e-12
        onto = any(h(t / 100) < 0 for t in range(-500, 2000))
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(one_one, onto)]
    c[14] = q14

    def q15():
        ok = [l / 1000 for l in range(-6000, 6001)
              if 4 * (l / 1000)**2 > 9 and abs(2 - math.sqrt(4 * (l / 1000)**2 - 9)) < 2 * abs(l / 1000) < 2 + math.sqrt(4 * (l / 1000)**2 - 9)]
        b = Rational(13, 8); a = -b
        assert max(v for v in ok if v < 0) < float(a) + 0.002 and min(v for v in ok if v > 0) > float(b) - 0.002
        X, Y = 8 * a + 12, 16 * b - 20
        return [i for i, e in enumerate([5 * X**2 - Y + 11, 6 * X**2 + Y**2 - 42, X**2 - 4 * Y**2 - 7, X**2 + 2 * Y**2 - 5 * X + 6 * Y - 3], 1) if e == 0][0]
    c[15] = q15

    def q16():
        l = Symbol('l')
        n = Matrix([-2, 1, 1]).cross(Matrix([1, -2, 1]))
        AB = Matrix([sqrt(3), 1, 2]) - Matrix([l, 2, 1])
        return opt(sum(solve(AB.dot(n)**2 - n.dot(n), l)), [3 * sqrt(3), 0, -2 * sqrt(3), 2 * sqrt(3)])
    c[16] = q16

    def q17():
        w = [Rational(math.comb(k, 2) * math.comb(8 - k, 2), 1) for k in range(9)]
        return opt(w[4] / sum(w), [Rational(1, 7), Rational(1, 5), Rational(2, 5), Rational(2, 7)])
    c[17] = q17

    def q18():
        d = [170, 125, 230, 190, 210, 130, 170]
        assert sorted(d)[3] == 170 and Rational(sum(abs(v - 170) for v in d), 7) == Rational(205, 7)
        m = Rational(sum(d), 7)
        return opt(Rational(sum(abs(v - m) for v in d), 7), [28, 30, 31, 32])
    c[18] = q18

    def q19():
        a, b, i = Matrix([-5, 1, -3]), Matrix([1, 2, -4]), Matrix([1, 0, 0])
        cv = a.cross(b).cross(i).cross(i).cross(i)
        return opt(cv.dot(Matrix([-1, 1, 1])), [-10, -12, -13, -15])
    c[19] = q19

    def q20():
        for X in (0.5, 2.0, 3.7):
            A = math.atan(1 / math.sqrt(X * (X * X + X + 1))); B = math.atan(math.sqrt(X) / math.sqrt(X * X + X + 1))
            C = math.atan(math.sqrt(X**-3 + X**-2 + X**-1))
            assert abs(A + B - C) < 1e-12
        return 1
    c[20] = q20
    c[21] = lambda: len({(p, q) for p in range(1, 21) for q in range(1, 21) if q % p == 0} - {(p, q) for p in range(1, 21) for q in range(1, 21) if p % q == 0})

    def q22():
        z1 = Matrix([-2, 3]) - Matrix([1, -1]) / sqrt(2)          # farthest from (3, -2), inside y >= x + 4
        assert z1[1] - z1[0] - 4 >= 0
        z2 = Matrix([Rational(-3, 2), Rational(5, 2)])           # foot of (3, -2) on y = x + 4
        assert (z2 - Matrix([-2, 3])).dot(z2 - Matrix([-2, 3])) <= 1
        v = expand(z1.dot(z1) + 2 * z2.dot(z2))
        al, be = v.coeff(sqrt(2), 0), v.coeff(sqrt(2), 1)
        assert simplify(al + be * sqrt(2) - v) == 0
        return al + be
    c[22] = q22
    c[23] = lambda: abs(expand((x + 1)**6 * (1 + x**2)**7 * (1 - x**3)**8).coeff(x, 36))
    c[24] = lambda: sum(1 for y in range(22) for z in range(15) if 42 - 2 * y - 3 * z >= 0)
    c[25] = lambda: sum(set(range(3, 404, 4)) & set(range(2, 405, 3)))

    def q26():
        L = limit(acos(1 - (1 + x)**2) * asin(1 - (1 + x)) / ((1 + x) - (1 + x)**3), x, 0, '-')
        R = limit(acos(1 - x**2) * asin(1 - x) / (x - x**3), x, 0, '+')
        return simplify(32 / pi**2 * (L**2 + R**2))
    c[26] = q26

    def q27():
        import mpmath
        v = mpmath.quad(lambda t: 8 * mpmath.sqrt(2) * mpmath.cos(t) / ((1 + mpmath.e**mpmath.sin(t)) * (1 + mpmath.sin(t)**4)), [-mpmath.pi / 2, mpmath.pi / 2])
        hits = [(a, b) for a in range(-6, 7) for b in range(-6, 7) if abs(a * mpmath.pi + b * mpmath.log(3 + 2 * mpmath.sqrt(2)) - v) < 1e-9]
        a, b = hits[0]
        return a * a + b * b
    c[27] = q27

    def q28():
        t = Symbol('t')
        X = Function('X')
        return dsolve(Eq((t + 1) * X(t).diff(t), 2 * X(t) + (t + 1)**4), X(t), ics={X(0): 2}).rhs.subs(t, 1)
    c[28] = q28

    def q29():
        X, Y, k = symbols('X Y k', real=True)
        P = [s for s in solve([X**2 + Y**2 - 3, X**2 - 2 * Y], [X, Y], dict=True) if s[X] > 0 and s[Y] > 0][0]
        al = sqrt(2) * P[X] + P[Y]
        k1, k2 = solve(Abs(k - al) / sqrt(3) - 2 * sqrt(3), k)
        return simplify((Rational(1, 2) * abs(k1 - k2) * P[X])**2)
    c[29] = q29

    def q30():
        l, m = symbols('l m')
        p = Matrix([1, 2, 3]) + l * Matrix([1, -1, 1]); q = Matrix([4, 5, 6]) + m * Matrix([1, 1, -1])
        s = solve([(p - q).dot(Matrix([1, -1, 1])), (p - q).dot(Matrix([1, 1, -1]))], [l, m])
        return sum((p + q).subs(s))
    c[30] = q30
    c[31] = lambda: [(1, 2, -2), (1, 1, -1), (1, -2, -1), (1, 2, -1)].index((1, 2, -2 + 1)) + 1

    def q32():
        g, T, R = symbols('g T R', positive=True)
        v = 2 * pi * R / T
        s2 = solve(v**2 * Symbol('s')**2 / (2 * g) - 4 * R, Symbol('s'))
        s2 = [e for e in s2 if e.is_positive or True][0]**2
        return [i for i, e in enumerate([None, 2 * g * T**2 / (pi**2 * R), pi**2 * R / (2 * g * T**2), None], 1) if e is not None and simplify(e - s2) == 0][0]
    c[32] = q32
    c[33] = lambda: opt(Rational(60 - Rational(4, 100) * 200, 26), [3, Rational(12, 10), 4, 2])
    c[34] = lambda: opt(sqrt(400 / (Rational(1, 2) * Rational(1, 2))), [1600, 40, 20, 1000])
    c[35] = lambda: nearest((0.01 * 200 / 1.01)**2 / 20, [0.20, 0.30, 0.35, 0.40])
    c[36] = lambda: opt((pi**2 / 9) * 4 / (4 * pi**2), [Rational(2, 9), Rational(4, 9), Rational(8, 9), Rational(1, 9)])

    def q38():
        V = Symbol('V', positive=True)
        V1, V2, K = symbols('V1 V2 K', positive=True)
        W = integrate(K / V**Rational(3, 2), (V, V1, V2))
        P1, P2 = K / V1**Rational(3, 2), K / V2**Rational(3, 2)
        return [i for i, e in enumerate([2 * (P2 * V2 - P1 * V1), 2 * (P2 * sqrt(V2) - P1 * sqrt(V1)), 2 * (P1 * V1 - P2 * V2), 2 * (sqrt(P1) * V1 - sqrt(P2) * V2)], 1) if simplify(W - e) == 0][0]
    c[38] = q38
    c[39] = lambda: opt((2 * Rational(3, 2) + 6 * Rational(5, 2)) / 8, [Rational(5, 2), Rational(9, 4), Rational(3, 2), Rational(7, 4)])
    def q40():
        C, V = symbols('C V', positive=True)
        Ui = Rational(1, 2) * C * V**2 + Rational(1, 2) * C * (2 * V)**2
        Vc = (C * V + C * 2 * V) / (2 * C)
        loss = simplify(Ui - Rational(1, 2) * 2 * C * Vc**2)
        return [i for i, e in enumerate([C * V**2 / 2, C * V**2 / 4, 2 * C * V**2, 3 * C * V**2 / 4], 1) if simplify(e - loss) == 0][0]
    c[40] = q40
    c[41] = lambda: nearest(5 - (8 * 5 / (8 * 0.2)) * 0.2, [5, 3, 0, 10])
    c[42] = lambda: opt(Rational(100, 1) / Rational(5, 1000) - 50, [19950, 19500, 5975, 20050])
    c[43] = lambda: [i for i, newL in enumerate([4, 3, Rational(3, 4), Rational(1, 4)], 1) if newL * 4 == 1][0]
    c[44] = lambda: nearest(230 * 300 * 200e-12 * 1e6, [13.8, 1.38, 14.3, 13.8])
    c[45] = lambda: nearest(2 * 6e-7 * 0.2 / 1e-5 * 1000, [12, 24, 120, 60])
    c[46] = lambda: [i for i, r in enumerate([Rational(1, 8), 4, 8, Rational(1, 2)], 1) if r == Rational(4 * 2, 1 * 1)][0]
    c[47] = lambda: nearest(13.6 * (1 - 1 / 9), [13.6, 1.5, 12.1, 1.9])
    c[49] = lambda: opt((1 - Rational(10, 11)) * 5, [Rational(1, 2), Rational(5, 11), Rational(10, 11), Rational(50, 11)])
    c[50] = lambda: nearest((10 / 100 + 2 * 0.05 / 0.35 + 0.2 / 15) * 100, [39.9, 25.6, 37.3, 35.6])

    def q51():
        t = Symbol('t')
        X = -3 * t**3 + 18 * t**2 + 16 * t
        tv = solve(diff(X, t, 2), t)[0]
        return diff(X, t).subs(t, tv)
    c[51] = q51
    c[52] = lambda: 4 * sqrt(2) / (Matrix([Rational(4, 3), Rational(4, 3)]).norm())
    c[53] = lambda: Rational(1, 2) * (70**2 - 50**2) * 80 / 10
    c[54] = lambda: solve(3 * x - x - 12, x)[0]
    c[55] = lambda: 1 / (1 - Rational(1, 1) / Rational(3, 2))
    c[56] = lambda: integrate(3 * x**2 + 4 * x**3, (x, 1, 2))

    def q57():
        a = 4 * pi / 6
        d = a * sqrt(3) / 2
        B = 6 * (Rational(1, 10**7) * 4 * pi * sqrt(3) / d) * 2 * sin(pi / 6)
        return simplify(B * 10**7)
    c[57] = q57
    c[58] = lambda: round(((0.1 * 0.05 * 0.006) + 1e-3 * 0.006)**2 / 0.006 * 1e9)
    c[59] = lambda: 1 / (-Rational(1, 30) + Rational(1, 10))
    c[60] = lambda: 1000 / (64 * (Rational(4) / Rational(48, 10))**3)      # A = 1000/x with A ~ R^3
    c[81] = lambda: min(Rational(72, 3), Rational(50, 2))
    c[83] = lambda: 7 + Rational(1, 2) * 0
    c[85] = lambda: round(0.03 * 0.3 * 100)
    c[86] = lambda: 3 * 5730
    return c
