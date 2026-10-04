"""Answer checks for JEE Main 2023 (Session 2), 6 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, Abs


def checks():
    c = {}

    def q1():
        xs = [k / 100 for k in range(-1000, 1000)]
        A = [t for t in xs if math.floor(t + 3) + math.floor(t + 4) <= 3]
        B = [t for t in xs if 3**t * (1 / 3)**(t - 3) < 3**(-3 * t)]
        return 1 if A == B else 0
    c[1] = q1

    def q2():
        roots = [r for r in solve(x**2 - 10 * x + 22, x) if not (3 <= r <= 5)] + [r for r in solve(x**2 - 6 * x + 8, x) if 3 <= r <= 5]
        return opt(sum(roots), [9 - sqrt(3), 9 + sqrt(3), 11 + sqrt(3), 11 - sqrt(3)])
    c[2] = q2

    def q3():
        A = Matrix([[2, 3], [-1, -2]])                    # an example; Cayley-Hamilton gives tr 0, det -1 for all such A
        assert A**2 == eye(2) and all(v != 0 for v in A)
        return opt(3 * A.trace()**2 + 4 * A.det()**2, [3, 4, 7, 14])
    from sympy import eye
    c[3] = q3

    def q4():
        a, b = symbols('a b')
        av = solve(Matrix([[1, 1, a], [2, 5, 2], [1, 2, 3]]).det(), a)[0]
        bv = solve(Matrix([[1, 1, b], [2, 5, 6], [1, 2, 3]]).det(), b)[0]
        return opt(2 * av + 3 * bv, [20, 23, 25, 28])
    c[4] = q4

    def q5():
        n = [n for n in range(3, 50) if math.comb(2 * n, 3) == 10 * math.comb(n, 3)][0]
        r = Rational(n * n + 3 * n, n * n - 3 * n + 4)
        return [i for i, (p, q) in enumerate([(27, 11), (35, 16), (2, 1), (65, 37)], 1) if Rational(p, q) == r][0]
    c[5] = q5

    def q6():
        a, b = Rational(2)**Rational(1, 4), Rational(3)**Rational(-1, 4)
        for n in range(8, 20):
            if simplify((a / b)**(n - 8) - sqrt(6)) == 0:
                return opt(simplify(math.comb(n, 2) * a**(n - 2) * b**2), [60 * sqrt(2), 60 * sqrt(3), 30 * sqrt(2), 30 * sqrt(3)])
    c[6] = q6
    c[7] = lambda: opt(sum(n * n + 3 * n + 1 for n in range(1, 21)), [3250, 3450, 3420, 3520])

    def q8():
        a1, d = 2.0, 3.0
        n = 10**6
        s = (math.sqrt(a1 + (n - 1) * d) - math.sqrt(a1)) / d
        return nearest(math.sqrt(d / n) * s, [1, 0, math.sqrt(d), 1 / math.sqrt(d)])
    c[8] = q8

    def q9():
        y = Symbol('y')
        F = 2 * x**y + 3 * y**x - 20
        dy = -diff(F, x) / diff(F, y)
        v = dy.subs({x: 2, y: 2})
        opts = [-(3 + log(4)) / (2 + log(8)), -(3 + log(16)) / (4 + log(8)), -(3 + log(8)) / (2 + log(4)), -(2 + log(8)) / (3 + log(4))]
        return [i for i, o in enumerate(opts, 1) if abs(N(v - o)) < 1e-12][0]
    c[9] = q9

    def q10():
        f = (5 / x - 4 * x + 3) / 9
        assert simplify(5 * f + 4 * f.subs(x, 1 / x) - (1 / x + 3)) == 0
        v = 18 * integrate(f, (x, 1, 2))
        return opt(simplify(v), [5 * log(2) - 3, 5 * log(2) + 3, 10 * log(2) - 6, 10 * log(2) + 6])
    c[10] = q10

    def q11():
        I = -x**2 / (x * tan(x) + 1) + 2 * log(x * sin(x) + cos(x))
        assert simplify(diff(I, x) - x**2 * (x / cos(x)**2 + tan(x)) / (x * tan(x) + 1)**2) == 0 and I.subs(x, 0) == 0
        v = I.subs(x, pi / 4)
        opts = [log((pi + 4)**2 / 32) - pi**2 / (4 * (pi + 4)), log((pi + 4)**2 / 16) + pi**2 / (4 * (pi + 4)),
                log((pi + 4)**2 / 16) - pi**2 / (4 * (pi + 4)), log((pi + 4)**2 / 32) + pi**2 / (4 * (pi + 4))]
        return [i for i, o in enumerate(opts, 1) if abs(N(v - o)) < 1e-12][0]
    c[11] = q11

    def q12():
        P1, P2 = Matrix([Rational(10, 3), 3]), Matrix([Rational(5, 3), 6])
        m = P1[1] / P1[0] + P2[1] / P2[0]
        X = solve(9 * x + 5 * m * x - 45, x)[0]; Y = m * X
        return [i for i, f in enumerate([Y - 2 * X - 5, 6 * X - Y - 15, Y - X - 5, 6 * X + Y - 10], 1) if f == 0][0]
    c[12] = q12

    def q13():
        l = Symbol('l')
        n = Matrix([2 + 4 * l, -1 - 3 * l, 1 + 5 * l])
        lv = solve(n.dot(Matrix([-2, 4, 5])), l)[0]
        n = n.subs(l, lv); const = -3 + 9 * lv
        k = 6 / const
        return opt(sum(k * n), [12, 13, 14, 15])
    c[13] = q13

    def q14():
        nn = Matrix([3, 4, 5]).cross(Matrix([0, 0, 1]))
        return opt(Abs(Matrix([3, 0, 0]).dot(nn)) / nn.norm(), [Rational(12, 5), 12 / (5 * sqrt(5)), 12 * sqrt(5), 12 / sqrt(5)])
    c[14] = q14

    def q15():
        l = Symbol('l')
        A, B, C, D = Matrix([5, 5, 2 * l]), Matrix([1, 2, 3]), Matrix([-2, l, 4]), Matrix([-1, 5, 6])
        ls = solve(Matrix.hstack(B - A, C - A, D - A).det(), l)
        return opt(sum((v + 2)**2 for v in ls), [13, 25, 41, Rational(37, 2)])
    c[15] = q15

    def q16():
        a = Matrix([2, 3, 4]); dd = Matrix([1, -2, -2]).cross(Matrix([-1, 4, 3]))
        d = dd * 18 / a.dot(dd)
        v = a.cross(d)
        return opt(v.dot(v), [640, 680, 720, 760])
    c[16] = q16

    def q17():
        s = Symbol('s')
        tot = 15 * (14 + 144) + 15 * (s + 196)
        return opt(solve(tot / 30 - 13**2 - 13, s)[0], [12, 11, 10, 9])
    c[17] = q17

    def q18():
        p = Rational(4, 36)
        P = 5 * p**4 * (1 - p) + p**5
        return opt(P * 3**11, [75, 82, 123, 164])
    c[18] = q18

    def q19():
        BQ = 30 / sqrt(3)
        PQ = 30 - BQ * (2 - sqrt(3))
        return opt(simplify(BQ * PQ), [200 * (3 - sqrt(3)), 600 * (sqrt(3) - 1), 300 * (sqrt(3) - 1), 300 * (sqrt(3) + 1)])
    c[19] = q19

    def q20():
        imp = lambda a, b: (not a) or b
        expr = lambda P, Q, R: imp(P, Q) and imp(R, Q)
        opts = [lambda P, Q, R: imp(P, R) and imp(Q, R), lambda P, Q, R: imp(P and R, Q),
                lambda P, Q, R: imp(P, R) or imp(Q, R), lambda P, Q, R: imp(P or R, Q)]
        from itertools import product as pr
        return [i for i, o in enumerate(opts, 1) if all(o(*v) == expr(*v) for v in pr([True, False], repeat=3))][0]
    c[20] = q20
    c[21] = lambda: sum(1 for a in range(1, 11) for b in range(1, 11) if 2 * (a - b)**2 + 3 * (a - b) in range(5))

    def q22():
        p = Symbol('p')
        a = 1; b = [v for v in solve(p**2 + p - 4, p) if v > 0][0]
        return simplify(b**2 + b - a**2)
    c[22] = q22
    c[23] = lambda: 3**20 - 3 * 2**20 + 3
    c[24] = lambda: [math.comb(15, r) * (-1)**r for r in range(16) if 60 - 7 * r == 18][0]
    c[25] = lambda: 12 * 2 + 1

    def q26():
        import mpmath
        n = 1500; h = 2 / n; area = 0
        for i in range(n):
            for j in range(n):
                X, Y = (i + .5) * h, (j + .5) * h
                if 2 * Y - Y * Y <= X * X <= 2 * Y and X >= Y: area += h * h
        return [k for k in range(2, 20) if abs((k + 2) / (k + 1) - math.pi / (k - 1) - area) < 2e-3][0]
    c[26] = q26
    c[27] = lambda: (11 * sqrt(2))**2 / 2
    c[28] = lambda: (16 - 0)**2 + (8 - 2)**2

    def q29():
        y = (sin(x) + sqrt(3) * cos(x)) / x
        assert simplify(x * cos(x) * diff(y, x) + x * y * sin(x) + y * cos(x) - 1) == 0
        assert simplify(pi / 3 * y.subs(x, pi / 3) - sqrt(3)) == 0
        return Abs(simplify((x * diff(y, x, 2) + 2 * diff(y, x)).subs(x, pi / 6)))
    c[29] = q29

    def q30():
        P, R = Matrix([1, 2, 3]), Matrix([6, 10, 7]); n = Matrix([2, -1, 1])
        Q = P - 2 * (n.dot(P) - 9) / n.dot(n) * n
        v = (Q - P).cross(R - P)
        return v.dot(v) / 4
    c[30] = q30

    c[31] = lambda: opt(round((math.sqrt(1.21) - 1) * 100), [14, 10, 12, 15])
    def q35():
        mp = 1836; mK = {'e': 1 * 4, 'a': 4 * mp * 2, 'p': mp * 1}        # lambda ~ 1/sqrt(mK)
        return 2 if mK['a'] > mK['p'] > mK['e'] else 0
    c[35] = q35
    c[36] = lambda: [i for i, (l, f) in enumerate([(sqrt(2), 1), (1 / sqrt(2), 1), (1, 1 / sqrt(2)), (1, sqrt(2))], 1) if simplify(l - sin(pi / 6) / sin(pi / 4)) == 0 and f == 1][0]
    c[39] = lambda: opt([xv for xv in (7, 5, 2, 1) if abs(math.pi / (xv * math.sqrt(2)) - math.pi / (2 * math.sqrt(2))) < 1e-12][0], [7, 5, 2, 1])
    c[44] = lambda: opt(1000 - 200, [500, 600, 1200, 800])
    c[45] = lambda: nearest(3 / 12, [0.25, 0.5, 0.75, 1.25])
    c[46] = lambda: nearest(36 * (0.5 / 100 + 0.5 / 225) / 6 * 100, [4.33, 6.33, 2.33, 5.33])
    c[48] = lambda: nearest(7.5 * [xv for xv in [k / 1000 for k in range(1, 1000)] if abs(7.5 * xv - 0.1 * 25 * (0.2 + xv)) < 1e-9][0], [0.25, 0.5, 0.75, 1.5])
    c[50] = lambda: opt(Rational(2)**Rational(1, 3), [1, 2, Rational(2)**Rational(2, 3), Rational(2)**Rational(1, 3)])
    c[51] = lambda: Rational(40 * 315, 30)
    c[52] = lambda: round((2.15 - 1.5 * math.tan(math.asin(math.sin(math.pi / 3) * 3 / 4))) / math.tan(math.pi / 3) * 100)
    c[53] = lambda: round(0.51e-10 * 25 / 3 / 1e-12)
    c[54] = lambda: Rational(120**2, 60000) * 1000
    c[55] = lambda: round((1.2 / 0.96 - 1) * 100)
    c[56] = lambda: Rational(2) * Rational(3, 4) / Rational(1, 2)
    c[57] = lambda: round(math.sqrt(2) * 4 * 3.14e-7 * math.sqrt(2) / 0.4 / 1e-8)
    c[58] = lambda: round(62.8e3 / (3.14 * 0.02**2 * 2e11) / 1e-5, 6)
    c[60] = lambda: round(2 * (0.4 * 2 * 0.01 + 2 * 0.04) * 1000, 6)
    c[61] = lambda: [i for i, (a, b) in enumerate([(1, 3), (3, 1), (2, 3), (3, 2)], 1) if Rational(a, b) == Rational(2, 3)][0]
    c[81] = lambda: min(5 // 3, 2 // 2)
    c[82] = lambda: round(6.6e-34 / math.sqrt(2 * 9e-31 * 4.5e-29) / 1e-5)
    c[84] = lambda: round((54070 + 298 * 10) / 5705)
    c[85] = lambda: round(0.25 / 0.75 * 1000 / 18 * 60)
    c[87] = lambda: round((41400 - 30000) / (8.3 * 300) / 2.3)

    def q59():
        m, X, n = Rational(1, 100), symbols('X', positive=True), symbols('n')
        loss = integrate(m * 2 * x, (x, 0, X))          # retarding force m*(2x)
        for nv in range(-5, 6):
            if simplify(loss - (10 / X)**(-nv)) == 0:
                return nv
    c[59] = q59
    return c
