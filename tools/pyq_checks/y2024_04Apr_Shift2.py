"""Answer checks for JEE Main 2024 (Session 2), 4 Apr Shift 2."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, eye, Abs, re, im, cot, csc
from fractions import Fraction as F


def checks():
    c = {}

    def q1():
        R = lambda p, q: p[0] <= q[0] or p[1] <= q[1]
        pts = [(a, b) for a in range(1, 6) for b in range(1, 6)]
        refl = all(R(p, p) for p in pts)
        sym = all(R(q, p) for p in pts for q in pts if R(p, q))
        trans = all(R(p, r) for p in pts for q in pts for r in pts if R(p, q) and R(q, r))
        return {(True, False, False): 1, (True, False, True): 3}[(refl, sym, trans)]
    c[1] = q1

    def q2():
        import mpmath
        f = lambda X, Y: 1 if ((X - 1)**2 + Y**2 <= 4 and X - Y <= 1 and Y >= 0) else 0
        n = 600; s = sum(f(-1 + (i + .5) * 4 / n, (j + .5) * 2 / n) for i in range(n) for j in range(n)) * (4 / n) * (2 / n)
        return nearest(s, [3 * math.pi / 2, 7 * math.pi / 3, 7 * math.pi / 4, 17 * math.pi / 8])
    c[2] = q2

    def q3():
        A = Matrix([[1, 2], [0, 1]]); J = A.adjugate()
        B = sum((J**k for k in range(1, 11)), eye(2))
        return opt(sum(B), [22, -110, -124, -88])
    c[3] = q3

    def q4():
        ns = [n for n in range(6, 100) if 2 * math.comb(n, 5) == math.comb(n, 4) + math.comb(n, 6)]
        return opt(max(ns), [7, 14, 21, 28])
    c[4] = q4
    c[5] = lambda: opt(Rational(sum(k * (k + 1)**2 for k in range(1, 101)), sum(k * k * (k + 1) for k in range(1, 101))),
                       [Rational(31, 30), Rational(305, 301), Rational(32, 31), Rational(306, 305)])

    def q6():
        a = Symbol('a')
        av = [v for v in solve(64 - (a + 1) * (16 - a + 3), a) if v > 10][0]
        return opt(av * 8 * (16 - av), [128, 312, 120, 316])
    c[6] = q6

    def q7():
        f = 3 * sqrt(x - 2) + sqrt(4 - x)
        cands = [f.subs(x, 2), f.subs(x, 4)] + [f.subs(x, v) for v in solve(diff(f, x), x)]
        return opt(simplify(min(cands, key=lambda e: float(e))**2 + 2 * max(cands, key=lambda e: float(e))**2), [24, 38, 44, 42])
    c[7] = q7

    def q8():
        import mpmath
        mpmath.mp.dps = 40
        L = (lambda t: (72**t - 9**t - 8**t + 1) / (mpmath.sqrt(2) - mpmath.sqrt(1 + mpmath.cos(t))))(mpmath.mpf('1e-8'))
        a = L / (mpmath.log(2) * mpmath.log(3))
        return nearest(float(a**2), [746, 968, 1152, 1250])
    c[8] = q8

    def q9():
        t = Symbol('t')
        fp = x + sin(1 - exp(x))
        return opt(limit(fp / (3 * x**2), x, 0), [Rational(2, 3), Rational(-2, 3), Rational(1, 6), Rational(-1, 6)])
    c[9] = q9

    def q10():
        import mpmath
        hits = [i for i, a in enumerate([math.pi / 4, math.pi / 3, math.pi / 2, math.pi / 6], 1)
                if abs(mpmath.quad(lambda t: mpmath.cos(a * t) / (1 + 3**t), [-1, 1]) - 2 / math.pi) < 1e-12]
        return hits[0]
    c[10] = q10

    def q11():
        y = Symbol('y')
        return opt(integrate((y + 1) / 4 - y**2 / 2, (y, Rational(-1, 2), 1)), [Rational(9, 32), Rational(8, 9), Rational(11, 32), Rational(11, 12)])
    c[11] = q11

    def q12():
        y = Function('y')
        s = dsolve(Eq((x**2 + 4)**2 * y(x).diff(x) + 2 * x**3 * y(x) + 8 * x * y(x) - 2, 0), y(x), ics={y(0): 0})
        return opt(simplify(s.rhs.subs(x, 2)), [pi / 32, pi / 16, pi / 8, 2 * pi])
    c[12] = q12

    def q13():
        d = sqrt(10 - 1)
        return opt(simplify(Abs(d * sqrt(2) - 2) / sqrt(2)), [sqrt(2) - 1, 3 - sqrt(2), sqrt(2) + 1, 2 - sqrt(3)])
    c[13] = q13

    def q14():
        a = 6; ae = 2 + a; b2 = ae**2 - a**2
        return opt(Rational(2 * b2, a), [Rational(28, 3), Rational(14, 3), Rational(10, 3), Rational(11, 3)])
    c[14] = q14

    def q15():
        X, Y = symbols('X Y')
        line = Y * 1 - 6 * (X + 4) - (1 - 48)           # T = S1 for y^2 = 12x at (4, 1)
        pts = [(3, -3), (2, -9), (Rational(3, 2), -16), (Rational(1, 2), -20)]
        return [i for i, (p, q) in enumerate(pts, 1) if line.subs({X: p, Y: q}) == 0][0]
    c[15] = q15

    def q16():
        t, s = symbols('t s')
        sol = solve([2 + t - 3 - 2 * s, 4 + 5 * t - 2 - 3 * s], [t, s])
        P = Matrix([2 + sol[t], 4 + 5 * sol[t], 2 + sol[t]])
        d = Matrix([1, 2, 4])
        return opt(simplify(P.cross(d).norm() / d.norm()), [3 * sqrt(14) / 7, sqrt(14) / 7, 5 * sqrt(14) / 7, 6 * sqrt(14) / 7])
    c[16] = q16

    def q17():
        X = Symbol('X')
        a, b = Matrix([1, 1, 1]), Matrix([2, 4, -5])
        v = b + Matrix([X, 2, 3])
        xv = [s for s in solve(a.dot(v)**2 - v.dot(v), X) if a.dot(v).subs(X, s) > 0][0]
        return opt(a.cross(b).dot(Matrix([xv, 2, 3])), [3, 6, 9, 11])
    c[17] = q17

    def q18():
        l = Symbol('l', positive=True)
        a, b = Matrix([1, l, -3]), Matrix([3, -1, 2])
        lv = solve((a + b).dot(a - b), l)[0]
        a = a.subs(l, lv)
        return opt((14 * a.dot(b) / (a.norm() * b.norm()))**2, [25, 20, 50, 40])
    c[18] = q18

    def q19():
        a, b = symbols('a b')
        P = [a, 2 * a, a + b, 2 * b, 3 * b]; X = [0, 2, 4, 6, 8]
        s = solve([sum(P) - 1, sum(p * v for p, v in zip(P, X)) - Rational(46, 9)], [a, b])
        P = [p.subs(s) for p in P]
        return opt(sum(p * v * v for p, v in zip(P, X)) - Rational(46, 9)**2, [Rational(151, 27), Rational(566, 81), Rational(581, 81), Rational(173, 27)])
    c[19] = q19

    def q20():
        best = min(xx * xx + yy * yy + 2 * xx * yy * math.sin(math.acos(xx) - math.asin(yy))
                   for xx in [i / 100 for i in range(-100, 101)] for yy in [j / 100 for j in range(-100, 101)]
                   if -math.pi / 2 <= math.acos(xx) - math.asin(yy) <= math.pi)
        return nearest(best, [-1, -0.5, 0, 0.5])
    c[20] = q20

    def q21():
        f = lambda e: 2 * e / sqrt(1 + 9 * e**2)
        e = x
        for _ in range(10): e = simplify(f(e))
        al = solve(Eq(e, 2**10 * x / sqrt(1 + 9 * Symbol('al') * x**2)).subs(x, 1), Symbol('al'))[0]
        return sqrt(3 * al + 1)
    c[21] = q21

    def q22():
        s = Symbol('s')
        roots = solve(3 * s**2 - 12 * s + 8, s)
        al = min(roots); be = 1
        assert 0 < al < 1
        return simplify(3 * ((al - 2)**2 + (be - 1)**2))
    c[22] = q22

    def q23():
        b = solve((3 - Symbol('b')) * (7 - Symbol('b')) - Symbol('b')**2 - 1, Symbol('b'))[0]
        A = Matrix([[3 - b, b], [b, 7 - b]])
        al, be = symbols('al be')
        s = solve(list(A.inv() - al * A - be * eye(2)), [al, be])
        return s[al] + s[be]
    c[23] = q23
    c[24] = lambda: sum((math.comb(4, k) * math.comb(5, 4 - k))**2 for k in range(5))

    def q26():
        al, be = symbols('al be')
        F_ = al * cot(x) * csc(x) * (csc(x)**2 + Rational(3, 2)) + be * log(tan(x / 2))
        d = diff(F_, x) - csc(x)**5
        s = solve([d.subs(x, pi / 3), d.subs(x, pi / 4)], [al, be])
        assert abs(N(d.subs(s).subs(x, 0.7))) < 1e-12
        return 8 * (s[al] + s[be])
    c[26] = q26

    def q27():
        y = tan(x) - x - 2
        assert simplify(diff(y, x) - (x + y + 2)**2) == 0
        al, be = y.subs(x, pi / 3), y.subs(x, 0)
        v = expand((3 * al + pi)**2 + be**2)
        return v.subs(sqrt(3), 0) + v.coeff(sqrt(3))
    c[27] = q27

    def q28():
        A = Matrix([1, 2]); M = A - Rational(3, 2) * Matrix([1, -1])
        h = 3 / sqrt(2) * sqrt(3)
        B, C = M + h / sqrt(2) * Matrix([1, 1]), M - h / sqrt(2) * Matrix([1, 1])
        assert simplify((B - A).dot(C - A) / ((B - A).norm() * (C - A).norm()) + Rational(1, 2)) == 0
        return simplify(B[0]**2 + C[0]**2)
    c[28] = q28

    def q29():
        P, Q, A = Matrix([1, 2, 1]), Matrix([2, 1, -1]), Matrix([2, 2, 2])
        d = Q - P; t = (A - P).dot(d) / d.dot(d)
        I_ = 2 * (P + t * d) - A
        return I_[0] + I_[1] + 6 * I_[2]
    c[29] = q29
    c[30] = lambda: Rational(sum(math.comb(10, k) * 2**(10 - k) for k in (4, 5, 6)), 3)

    c[33] = lambda: nearest(math.hypot(2, 2), [8, 4, math.sqrt(8), 6])
    c[34] = lambda: nearest(math.tan(math.pi / 4), [1, 1 / math.sqrt(3), 1.7, 0.5])
    c[35] = lambda: opt(Rational(90 * 10, 9), [300, 225, 120, 100])
    c[36] = lambda: nearest(math.sqrt(2 * 10 * (14 + 14 / 1.4)), [21.9, 16.7, 19.8, 10.6])
    c[39] = lambda: opt(2 * (1 - 1 / sqrt(2)), [2 - sqrt(2), sqrt(2) - 2, 2 * sqrt(2) - 1, 1 - 2 * sqrt(2)])
    c[42] = lambda: nearest(100**2 / (200**2 / 50), [12.5, 50, 100, 25])
    c[43] = lambda: nearest(2 * 0.5 * 8e-2, [0, 4e-2, 8e-2, 16e-2])
    c[46] = lambda: [i for i, r in enumerate([9, 16, 4, 1], 1) if r == ((2 + 1) / (2 - 1))**2][0]
    c[48] = lambda: opt(Rational(4, 2), [2, 1, 8, Rational(1, 2)])            # in units of h/pi
    c[51] = lambda: round((235.0439 - 139.9054 - 93.9063 - 1.0086) * 931)
    c[52] = lambda: round(4 * math.sqrt(3) * 0.25 / math.cos(math.radians(30)), 9)
    c[54] = lambda: Rational(1 + Rational(2, 3), Rational(1, 3) + 2) * 7
    c[55] = lambda: 2 * (4 // 2)**4
    c[56] = lambda: round(10 * (2 * math.pi / 3.14) * math.cos(math.pi / 3))
    c[57] = lambda: round((1e5 + 1.36e4 * 10 * 0.3) * (22 / 7) * 0.02**2)
    c[58] = lambda: Rational(3 * 2, 2)
    c[59] = lambda: round(72 / 3.6 / 2 * 4)
    c[60] = lambda: Rational(125, 10) * 144 / 2 * (1 - Rational(1, 6))
    c[63] = lambda: nearest(1 / 4.9e-2**2, [4.9, 416, 41.6, 49])
    c[69] = lambda: [i for i, z in enumerate([25, 23, 22, 26], 1) if abs(math.sqrt((n := [5, 3, 2, 4][i - 1]) * (n + 2)) - 3.86) < 0.05][0]
    c[81] = lambda: sum(1 for l in range(4) for m in range(-l, l + 1) if m == 0)
    c[83] = lambda: 5 * (60 - 20)
    c[84] = lambda: round(1.86 * (2700 / 60) / 2.7)
    c[85] = lambda: round(math.log(10) / 4.6e-2)
    c[87] = lambda: round(6.55 / 93 * 135 * 10)
    c[88] = lambda: (5 + 2 + 1 + 1 + 5) + (2 + 2)
    c[89] = lambda: 3 + (6 + 2)
    c[90] = lambda: 3 + 2 + 3
    return c
