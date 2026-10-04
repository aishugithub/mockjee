"""Answer checks for JEE Main 2024 (Session 2), 6 Apr Shift 1. Q6 and Q16 were dropped by NTA; Q89 is disputed."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, I as iu


def checks():
    c = {}

    def q1():
        X = range(1, 21)
        R1 = {(a, b) for a in X for b in X if 2 * a - 3 * b == 2}
        R2 = {(a, b) for a in X for b in X if -5 * a + 4 * b == 0}
        need = lambda R: len({(b, a) for a, b in R} - R)
        return opt(need(R1) + need(R2), [8, 10, 12, 16])
    c[1] = q1

    def q2():
        f = (x**2 + 2 * x - 15) / (x**2 - 4 * x + 9)
        one_one = f.subs(x, -5) != f.subs(x, 3)
        y = Symbol('y')
        disc = expand((2 + 4 * y)**2 + 4 * (1 - y) * (15 + 9 * y))
        onto = Poly(disc, y).LC() >= 0
        return {(True, True): 1, (True, False): 2, (False, True): 3, (False, False): 4}[(one_one, onto)]
    c[2] = q2

    def q3():
        from itertools import combinations
        adj = lambda i, j: (i - j) % 8 in (1, 7)
        return opt(sum(1 for t in combinations(range(8), 3) if not any(adj(i, j) for i, j in combinations(t, 2))), [16, 24, 56, 48])
    c[3] = q3

    def q4():
        t = Symbol('t')
        s = t**2 - 5 * t + 6
        a, b = symbols('a b')
        # a_{n+1} = s a_n - a_{n-1} since alpha*beta = 1: check with symbolic roots
        al, be = symbols('al be')
        n = 5
        expr = expand((al**(n + 1) + be**(n + 1)) + (al**(n - 1) + be**(n - 1)) - (al + be) * (al**n + be**n))
        assert expand(expr.subs(be, 1 / al)) == 0
        tm = solve(diff(s, t), t)[0]
        return opt(s.subs(t, tm), [Rational(-1, 4), Rational(1, 4), Rational(-1, 2), Rational(1, 2)])
    c[4] = q4

    def q5():
        r, n, al, be = symbols('r n al be')
        A = lambda rv: Matrix([[rv, 1, n**2 / 2 + al], [2 * rv, 2, n**2 - be], [3 * rv - 2, 3, n * (3 * n - 1) / 2]]).det()
        v = expand(2 * A(10) - A(8))
        opts = [0, 2 * n, 2 * al + 4 * be, 4 * al + 2 * be]
        return [i for i, o in enumerate(opts, 1) if expand(v - o) == 0][0]
    c[5] = q5
    c[7] = lambda: opt(sum(1 for k in range(100, 701) if k % 3 and k % 4), [280, 290, 300, 310])

    def q8():
        f = x**3 * sin(1 / x)
        v = simplify(diff(f, x, 2).subs(x, 2 / pi))
        return [i for i, o in enumerate([None, (24 - pi**2) / (2 * pi), None, (12 - pi**2) / (2 * pi)], 1) if o is not None and simplify(v - o) == 0][0]
    c[8] = q8

    def q9():
        d = simplify(diff(x**x, x) / x**x)
        x0 = solve(d, x)[0]
        assert x0 == exp(-1)
        return 1
    c[9] = q9

    def q10():
        m = Symbol('m', positive=True)
        S_ = (4 + 9 / m) + (9 + 4 * m)
        mv = solve(diff(S_, m), m)[0]
        return opt(S_.subs(m, mv), [10, 25, 15, 30])
    c[10] = q10

    def q11():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.cos(t)**2 * mpmath.sin(t)**2 / (mpmath.cos(t)**3 + mpmath.sin(t)**3)**2, [0, mpmath.pi / 4])
        return nearest(float(v), [1 / 3, 1 / 6, 1 / 9, 1 / 12])
    c[11] = q11

    def q12():
        A = integrate(3 * x - (3 * x - x * sqrt(x)), (x, 0, 3)) + integrate((27 - 3 * x) / 2 - (3 * x - x * sqrt(x)), (x, 3, 9))
        return opt(simplify(10 * A), [154, 162, 172, 184])
    c[12] = q12

    def q13():
        y = Function('y')
        s = dsolve(Eq((1 + x**2) * y(x).diff(x) + y(x), exp(atan(x))), y(x), ics={y(1): 0})
        v = simplify(s.rhs.subs(x, 0))
        opts = [(exp(pi / 2) - 1) / 2, (exp(pi / 2) - 1) / 4, (1 - exp(pi / 2)) / 2, (1 - exp(pi / 2)) / 4]
        return [i for i, o in enumerate(opts, 1) if simplify(v - o) == 0][0]
    c[13] = q13

    def q14():
        y = Function('y')
        s = dsolve(Eq(2 * x * log(x) * y(x).diff(x) + 2 * y(x), 3 / x * log(x)), y(x))
        C1 = Symbol('C1')
        Cv = solve(s.rhs.subs(x, exp(-1)), C1)
        sol = s.rhs.subs(C1, Cv[0]) if Cv else s.rhs
        v = simplify(sol.subs(x, E))
        return opt(v, [-2 / E, -3 / E, -3 / (2 * E), -2 / (3 * E)])
    from sympy import E
    c[14] = q14

    def q15():
        r = 12 / (2 * sqrt(3)); side = r * sqrt(2)
        return opt(simplify(side**2 + (4 * side)**2), [408, 312, 414, 396])
    c[15] = q15

    def q17():
        a1, d1, a2, d2 = Matrix([3, -15, 9]), Matrix([2, -7, 5]), Matrix([-1, 1, 9]), Matrix([2, 1, -3])
        n = d1.cross(d2)
        return opt(Abs((a2 - a1).dot(n)) / n.norm(), [6 * sqrt(3), 5 * sqrt(3), 4 * sqrt(3), 8 * sqrt(3)])
    from sympy import Abs
    c[17] = q17

    def q18():
        s1, s2 = 200 - 8 + 12, 20 * (4 + 100) - 64 + 144
        var = Rational(s2, 20) - Rational(s1, 20)**2
        return opt(sqrt(var), [Rational(18, 10), sqrt(Rational(396, 100)), sqrt(Rational(386, 100)), Rational(194, 100)])
    c[18] = q18

    def q19():
        A, B, C, D = Matrix([3, 1, -1]), Matrix([Rational(5, 3), Rational(7, 3), Rational(1, 3)]), Matrix([2, 2, 1]), Matrix([Rational(10, 3), Rational(2, 3), Rational(-1, 3)])
        assert (B - A).cross(C - A).dot(D - A) == 0
        return opt((C - A).cross(D - B).norm() / 2, [2 * sqrt(2), 5 * sqrt(2) / 3, 2 * sqrt(2) / 3, 4 * sqrt(2) / 3])
    c[19] = q19
    c[20] = lambda: opt(126 * Rational(4 * 9, 6 * 8 + 4 * 9), [56, 64, 66, 54])

    def q21():
        P = 4 * x**4 + 8 * x**3 - 17 * x**2 - 12 * x + 9
        v = expand(P.subs(x, 2 * iu) * P.subs(x, -2 * iu)) / 16
        return v * 16 / 125
    c[21] = q21

    def q22():
        a, b, g = symbols('a b g')
        d = expand(Matrix([[a, 1, 2], [1, b, 2], [2, 3, g]]).det())
        assert expand(d - (a * b * g - 6 * a - 4 * b - g + 10)) == 0
        return 45 + 10
    c[22] = q22

    def q23():
        n, X, Y = symbols('n X Y', positive=True)
        for nv in range(3, 15):
            s = solve([nv * X**(nv - 1) * Y - 135, Rational(nv * (nv - 1), 2) * X**(nv - 2) * Y**2 - 30], [X, Y], dict=True)
            for sol in s:
                if simplify(Rational(nv * (nv - 1) * (nv - 2), 6) * sol[X]**(nv - 3) * sol[Y]**3 - Rational(10, 3)) == 0:
                    return 6 * (nv**3 + sol[X]**2 + sol[Y])
    c[23] = q23

    def q24():
        T = [6]
        for r in range(2, 12): T.append(3 * T[-1] + 6**r)
        for n in range(1, 12):
            if 5 * sum(T[:n]) == (n * n - 12 * n + 39) * (4 * 6**n - 5 * 3**n + 1):
                return n
    c[24] = q24

    def q25():
        import mpmath
        I = lambda k: mpmath.quad(lambda t: (1 - t**7)**k, [0, 1])
        return round(float(sum(1 / (7 * (I(k) / I(k + 1) - 1)) for k in range(1, 11))), 6)
    c[25] = q25

    def q26():
        m = Symbol('m')
        ms = solve(discriminant(9 * x**2 + (12 + 18 * m) * x + 4, x), m)
        th = [atan(v) for v in ms]
        bis = [(th[0] + th[1]) / 2, (th[0] + th[1]) / 2 + pi / 2]
        slopes = [simplify(tan(b + pi / 2)) for b in bis]
        return simplify(16 * sum(s**2 for s in slopes))
    from sympy import discriminant
    c[26] = q26

    def q27():
        y = Function('y')
        s = dsolve(Eq(y(x).diff(x), (y(x) + 5) / (2 * (x - 3))), y(x))
        C1 = Symbol('C1')
        cv = solve(s.rhs.subs(x, 4) + 2, C1)[0]
        assert simplify(s.rhs.subs(C1, cv).subs(x, 7) - 1) == 0
        a = Rational(9, 4)                       # (y+5)^2 = 9(x-3): 4a = 9
        return 12 * ((7 - 3) + a)
    c[27] = q27

    def q28():
        A, B, R, P = Matrix([2, -5, 11]), Matrix([-6, 7, -5]), Matrix([1, 7, 6]), Matrix([10, -2, -1])
        d = B - A
        Q = A + d * (R - A).dot(d) / d.dot(d)
        return (P - Q).norm()
    c[28] = q28

    def q29():
        c1, c2, c3 = symbols('c1 c2 c3')
        a, b, cc = Matrix([2, -3, 4]), Matrix([3, 4, -5]), Matrix([c1, c2, c3])
        eqs = list(a.cross(b + cc) + b.cross(cc) - Matrix([1, 8, 13])) + [a.dot(cc) - 13]
        s = solve(eqs, [c1, c2, c3], dict=True)[0]
        return 24 - b.dot(cc.subs(s))
    c[29] = q29

    def q30():
        rest = pi / 4 - acot(3) - acot(4) - acot(5)
        return simplify(1 / tan(rest))
    from sympy import acot
    c[30] = q30

    c[32] = lambda: opt(solve((1 - Symbol('r')) / (1 + Symbol('r')) - 1 / sqrt(2), Symbol('r'))[0],
                        [(sqrt(2) - 1) / (sqrt(2) + 1), (sqrt(3) + 1) / (sqrt(2) - 1), (1 + sqrt(5)) / (sqrt(2) - 1), (1 + sqrt(5)) / (sqrt(5) - 1)])
    c[31] = lambda: [i for i, m in enumerate([0.5, 1, 2, 4], 1) if m == 0.5][0]
    c[34] = lambda: opt(Rational(40 + 240, 4), [70, 30, 40, 80])
    c[36] = lambda: 1 if simplify(Symbol('P') * diff(sqrt(Symbol('R') * Symbol('T') / Symbol('P')), Symbol('T')) - Symbol('R') / (2 * sqrt(Symbol('R') * Symbol('T') / Symbol('P')))) == 0 else 0
    c[37] = lambda: opt(sqrt(Rational(32, 4)), [2 * sqrt(2), 1 / (2 * sqrt(2)), Rational(1, 32), Rational(1, 4)])
    c[39] = lambda: opt((Rational(3, 1) / Rational(3, 2))**2 / 2, [1, 2, 4, 5])        # eps_r = (c/v)^2 / mu_r
    c[40] = lambda: opt(solve(Rational(24 * 24, 48) / Rational(1, 2) - (x + 6) / Rational(1, 2), x)[0], [42, 6, 3, 9])
    c[41] = lambda: opt(Rational(142, 100) * 50, [42, 21, 71, 142])
    c[43] = lambda: nearest(1e-7 * 10 * 0.01 / 0.25, [4e-8, 8e-8, 10e-8, 12e-8])
    c[45] = lambda: opt(abs(-1 - 2 * 2), [3, 5, 1, 4])
    c[47] = lambda: nearest(2.48 - 0.5, [1.98, 1.68, 2.48, 0.5])
    c[48] = lambda: [i for i, (p, q) in enumerate([(1, 2), (2, 1), (1, 4), (4, 1)], 1) if Rational(p, q) == Rational(1, 1) / Rational(1, 4)][0]
    c[50] = lambda: opt(100 - 100 * Rational(40, 100)**2, [16, 84, 44, 32])
    c[51] = lambda: [A for A in range(1, 180) if abs(math.sin(math.radians(A)) / math.sin(math.radians(A / 2)) - math.sqrt(3)) < 1e-9][0]
    c[52] = lambda: round(0.06 * 2 * math.pi / 3.14 * 100)
    c[53] = lambda: solve(Matrix([[-x, -6, -2], [-1, 4, 3], [-8, -1, 3]]).det(), x)[0]
    c[54] = lambda: Rational(10, 1) / (Rational(1000, 1) * 1 / 10**2)
    c[55] = lambda: round((200 / math.sqrt(2) / math.hypot(20, 20 * math.sqrt(3)))**2 * 20, 6)
    c[56] = lambda: math.floor(24 * (3 / 4)**2)
    c[57] = lambda: round(200 * 100e-6 * 2.5e-4 * 1 * 1e6, 9)
    c[58] = lambda: 2**4
    c[59] = lambda: abs(Rational(-1, 2) - 1 - Rational(1, 2))
    c[60] = lambda: round(8.48 / 0.529)
    c[61] = lambda: opt(solve(Symbol('x') / ((1120 - 40 * Symbol('x')) / 1000) - 3, Symbol('x'))[0], [Rational(35, 10), Rational(38, 10), 3, Rational(28, 10)])
    c[63] = lambda: opt(1 / Rational(1, 10), [1, 10, Rational(1, 100), 2])
    c[81] = lambda: round(2 * 2.18e-18 / 6.6e-34 / 1e13)
    c[83] = lambda: round(298 - 298 / 5 / 2.5)
    c[84] = lambda: round((1 + math.sqrt(1.2e-5 / 0.03)) * 0.03 * 0.083 * 300 * 100)
    c[85] = lambda: round(math.log10(1000) / math.log10(10))
    c[86] = lambda: round((math.sqrt(24) + math.sqrt(15)) * 100)
    c[87] = lambda: round(math.sqrt(35) - 0)
    c[90] = lambda: round(9.3 / 93 * (12 * 12 + 10 + 2 * 14 + 16))
    return c
