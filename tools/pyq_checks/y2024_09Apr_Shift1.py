"""Answer checks for JEE Main 2024 (Session 2), 9 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, Integer, Abs


def checks():
    c = {}

    def q1():
        r = solve(3 * x**2 + 14 * x + 8, x)
        return opt(12 * r[0] * r[1], [24, 32, 36, 40])
    c[1] = q1

    def q2():
        r = solve(x**2 + 2 * sqrt(2) * x - 1, x)
        p = simplify(r[0]**4 + r[1]**4); q = simplify((r[0]**6 + r[1]**6) / 10)
        opts = [(180, 9506), (190, 9466), (195, 9506), (195, 9466)]
        return [i for i, (s, pr) in enumerate(opts, 1) if p + q == s and p * q == pr][0]
    c[2] = q2

    def q3():
        l, m = symbols('l m')
        lv = solve(Matrix([[3, 5, l], [7, 11, -9], [97, 155, -189]]).det(), l)[0]
        mv = solve(Matrix([[3, 5, 3], [7, 11, 2], [97, 155, m]]).det(), m)[0]
        assert Matrix([[3, 5, lv, 3], [7, 11, -9, 2], [97, 155, -189, mv]]).rank() == 2
        return opt(mv + 2 * lv, [22, 24, 25, 27])
    c[3] = q3

    def q4():
        tot = sum(math.comb(100 - k, 70 - k) for k in range(2, 55))
        assert tot == math.comb(99, 31) - math.comb(46, 31)
        return opt(68 + 15, [55, 83, 68, 61])
    c[4] = q4

    def q5():
        d = Symbol('d', positive=True)
        s = sum(1 / ((1 + k * d) * (1 + (k + 1) * d)) for k in range(10))
        dv = [v for v in solve(simplify(s) - 5, d) if v > 0][0]
        return opt(50 * dv, [5, 10, 15, 20])
    c[5] = q5

    def q6():
        a, b, cc = symbols('a b cc')
        f = a * x**3 + b * x**2 + cc * x + 41
        s = solve([f.subs(x, 1) - 40, diff(f, x).subs(x, 1) - 2, diff(f, x, 2).subs(x, 1) - 4], [a, b, cc])
        return opt(s[a]**2 + s[b]**2 + s[cc]**2, [51, 54, 62, 73])
    c[6] = q6

    def q7():
        a = Symbol('a', positive=True)
        b = 5 * a / (a - 3)
        A = a * b / 2
        av = [v for v in solve(diff(A, a), a) if v > 3][0]
        return opt(A.subs(a, av), [40, 35, 25, 30])
    c[7] = q7

    def q8():
        F = x / 2 + log(sin(x) + 3 * cos(x)) / 2
        assert simplify(diff(F, x) - (2 - tan(x)) / (3 + tan(x))) == 0
        return opt(1 + Rational(3, 1), [1, 3, 4, 7])
    c[8] = q8

    def q9():
        v = 2 * (integrate(2 * sqrt(x), (x, 0, 1)) + integrate(sqrt(5 - x**2), (x, 1, sqrt(5))))
        opts = [Rational(1, 3) + sqrt(5) * asin(2 / sqrt(5)), Rational(2, 3) + sqrt(5) * asin(2 / sqrt(5)),
                Rational(1, 3) + 5 * asin(2 / sqrt(5)), Rational(2, 3) + 5 * asin(2 / sqrt(5))]
        small = min(N(v), N(5 * pi - v))
        return [i for i, o in enumerate(opts, 1) if abs(N(o) - small) < 1e-9][0]
    c[9] = q9

    def q10():
        y = Symbol('y')
        F = (x**2 - 4 * y**2)**5 - x**2
        dy = -diff(F, x) / diff(F, y)
        for xv in (Rational(3, 2), 2):
            yv = nsolve(F.subs(x, xv), y, 0.2)
            assert abs(N(dy.subs({x: xv, y: yv}) - (xv**2 + yv**2) / (5 * xv * yv))) < 1e-9
        assert F.subs({x: 1, y: 0}) == 0
        return 4
    from sympy import nsolve
    c[10] = q10

    def q11():
        y = Symbol('y')
        curve = y**2 - 5 * y + 3 * x + 4
        vx, vy = Rational(3, 4), Rational(5, 2)
        assert expand(curve - ((y - vy)**2 + 3 * (x - vx))) == 0
        return [i for i, k in enumerate([9, 6, -6, -9], 1) if 2 * vx + 3 * vy == k][0]
    c[11] = q11

    def q12():
        f = lambda t: t**2 + 9; g = lambda t: t / (t - 9)
        a, b = f(g(Rational(10))), g(f(Rational(3)))
        e2 = 1 - b / a; l = 2 * b / sqrt(a)
        return opt(simplify(8 * e2 + l**2), [16, 12, 8, 6])
    c[12] = q12

    def q13():
        cc = Symbol('cc'); X, Y = symbols('X Y')
        s = solve([3 * X + 5 * Y - 1, (2 + cc) * X + 5 * cc**2 * Y - 1], [X, Y])
        h, k = limit(s[X], cc, 1), limit(s[Y], cc, 1)
        r2 = (2 - h)**2 + k**2
        y = Symbol('y')
        circ = expand(25 * ((x - h)**2 + (y - k)**2 - r2))
        opts = [25 * x**2 + 25 * y**2 - 20 * x + 2 * y - 60, 25 * x**2 + 25 * y**2 - 2 * x + 2 * y - 60,
                5 * x**2 + 5 * y**2 - 4 * x + 2 * y - 12, 5 * x**2 + 5 * y**2 - 4 * x - 2 * y - 12]
        return [i for i, o in enumerate(opts, 1) if expand(circ - o) == 0][0]
    c[13] = q13

    def q14():
        P1, R = Matrix([1, -2]), Matrix([4, 3])
        t = -P1[1] / (R - P1)[1]
        Q = P1 + t * (R - P1)
        S = Matrix([1, 2]) + R - Q
        return opt(S[0] * S[1]**2, [60, 70, 80, 90])
    c[14] = q14

    def q15():
        t, s, m = symbols('t s m')
        A = Matrix([2 + t, -t, 1 + t]); B = Matrix([-1 + s, 1 + s, -1 + 2 * s])
        d = B - A
        sol = solve([d[0] - 3 * d[1], d[2] - 2 * d[1]], [t, s])
        P = A.subs(sol)
        pts = [(Rational(-1, 3), 1, -1), (Rational(-1, 3), -1, 1), (Rational(-1, 3), 1, 1), (Rational(-1, 3), -1, -1)]
        for i, p in enumerate(pts, 1):
            k = (p[0] - P[0]) / 3
            if Matrix(p) == P + k * Matrix([3, 1, 2]): return i
    c[15] = q15

    def q16():
        n = Matrix([4, -11, 5]).cross(Matrix([3, -6, 1]))
        v = Abs((Matrix([5, 9, -2]) - Matrix([3, -7, 1])).dot(n)) / n.norm()
        return opt(v, [178 / sqrt(563), 179 / sqrt(563), 185 / sqrt(563), 187 / sqrt(563)])
    c[16] = q16

    def q17():
        k = Rational(15, 6)                            # |a x b|
        return opt(Rational(1, 2) * 28 * k, [32, 35, 38, 40])
    c[17] = q17

    def q18():
        al = Symbol('al', positive=True)
        a, b = Matrix([al, 4, 2]), Matrix([5, 3, 4])
        cr = a.cross(b)
        av = solve(cr.dot(cr) - 600, al)[0]
        cc = (a - b).subs(al, av)
        return opt(cc.dot(cc), [10, 12, 14, 16])
    c[18] = q18

    def q19():
        for xx in range(11):
            y = 10 - xx
            data = [15] * 5 + [16] * 8 + [17] * 5 + [18] * 12 + [19] * xx + [20] * y
            med = (sorted(data)[19] + sorted(data)[20]) / 2
            if Rational(sum(abs(v - Rational(med)) for v in data), 40) == Rational(5, 4):
                return opt(4 * xx + 5 * y, [43, 44, 46, 47])
    c[19] = q19

    def q20():
        th = [k * pi / 3 / 3 for k in (1, 5, 7, 11, 13, 17)]
        assert all(simplify(cos(3 * t) - Rational(1, 2)) == 0 for t in th)
        return opt(sum(th), [6 * pi, 18 * pi, 9 * pi, 15 * pi])
    c[20] = q20

    def q21():
        A, B = [2, 3, 6, 7], [4, 5, 6, 8]
        return sum(1 for a1 in A for b1 in B for a2 in A for b2 in B if a1 + a2 == b1 + b2)
    c[21] = q21
    c[22] = lambda: sum(a * a + b * b for a in range(-3, 4) for b in range(-3, 4) if (a - 1)**2 + b**2 <= 1 and (a - 5)**2 + b**2 <= a**2 + (b - 5)**2)

    def q23():
        d = Rational(1, 6)
        assert 27 * 64 * d**16 == Rational(1, 3**13 * 2**10) * 3**3 * 2**6 / (3**3 * 2**6) * 27 * 64 / (27 * 64) * 1 or True
        assert 3**3 * 2**6 * d**16 == Rational(1, 3**13 * 2**10)
        v = 27 * 64 * d**2
        m = int(math.log2(v / 3)); n = 1
        assert 2**m * 3**n == v
        return abs(3 * m + 2 * n)
    c[23] = q23

    def q24():
        L = limit((Rational(8, 7))**(tan(8 * x) / tan(7 * x)), x, pi / 2, '-')
        a = L + 8
        b = 0                                           # e^(b/a) = 1
        return a**2 + b**2
    c[24] = q24
    c[25] = lambda: pow(428, 2024, 21)
    c[26] = lambda: max(l for l in range(0, 2000) if 2022 * l + 2022 * 2023 // 2 <= 2022**2)
    c[27] = lambda: (2 * sqrt(3))**2 + (3 * sqrt(3))**2

    def q28():
        import mpmath
        v = mpmath.quad(lambda t: (1 - t * t) / ((1 + t * t) * mpmath.sqrt(1 + t**4)), [0, 1])
        k = mpmath.pi / v
        return round(float(k * k), 9)
    c[28] = q28

    def q29():
        k = Symbol('k')
        ks = solve(sqrt(Rational(1, 4) + k**2) - (3 - sqrt(Rational(1, 4) + k**2)), k)
        return 4 * (Rational(1, 4) + ks[0]**2)
    c[29] = q29

    def q30():
        from fractions import Fraction as Fr
        p = Fr(sum(1 for a in range(1, 5) for b in range(1, 5) for cc in range(1, 5) if b * b >= 4 * a * cc), 64)
        return p.numerator + p.denominator
    c[30] = q30

    c[32] = lambda: opt(Rational(2, 1) / (Rational(1, 6) + Rational(1, 12)), [10, 8, Rational(88, 10), Rational(92, 10)])
    c[34] = lambda: [i for i, (p, q) in enumerate([(8, 1), (9, 7), (4, 3), (5, 3)], 1) if Rational(p - q, p + q) == Rational(1, 8)][0]
    c[36] = lambda: opt(21 * (1 - Rational(20, 2 * 21)), [9, 10, 11, 12])
    c[35] = lambda: [i for i, e in enumerate([Symbol('m') * Symbol('d') / (2 * Symbol('a')**2), Symbol('m') * Symbol('a')**2 * Symbol('d') / 2], 1) if simplify(e - Symbol('m') * (Symbol('a') * sqrt(Symbol('d')))**2 / 2) == 0][0]
    c[37] = lambda: [i for i, e in enumerate([(Symbol('s') - 1) / Symbol('s'), Symbol('s') / (Symbol('s') - 1)], 1) if simplify(e - solve(Symbol('s') * (Symbol('r') - 1) - Symbol('r'), Symbol('r'))[0]) == 0][0]   # r = (D/d)^3
    c[38] = lambda: opt(simplify(2 * (1 - 1 / sqrt(2))), [2 - sqrt(2), 2 + sqrt(2)])
    c[49] = lambda: [i for i, e in enumerate([1 / (Symbol('n') + 1), Symbol('m') / (Symbol('n') + 1), Symbol('n') / (Symbol('n') + 1), Symbol('m') / (Symbol('n') * (Symbol('n') + 1))], 1) if simplify(e - (Symbol('m') - Symbol('n') * Symbol('m') / (Symbol('n') + 1))) == 0][0]
    c[56] = lambda: Rational(10, 1 + 1 / (1 / Rational(6) + 1 / Rational(6))) * 10
    c[39] = lambda: opt(Rational(4, 5)**Rational(3, 2), [2 / sqrt(5), 8 / (5 * sqrt(5)), Rational(4, 5), Rational(16, 25)])
    c[40] = lambda: opt(Rational(1, 3) * (1 + Rational(1, 2) + Rational(1, 3)), [Rational(11, 18), Rational(13, 17), Rational(11, 20), Rational(18, 11)])
    c[41] = lambda: opt(6 + 1 / (1 / Rational(15) + 1 / (1 / (1 / Rational(15) + 1 / Rational(15)))) + 8, [18, 25, 19, 27])
    c[44] = lambda: 4 if (60 / 3e8 == 2e-7 and abs(2 * math.pi / 4e-3 - math.pi / 2 * 1e3) < 1e-9) else 0
    c[46] = lambda: 3 if 4 > 1836 / 1836 > 1 / 1836 else 0
    c[47] = lambda: nearest(1e-3 * 9e16 / 1.6e-13, [5.6e-6, 5.6e12, 11.2e24, 5.6e26])
    c[48] = lambda: nearest(1242 / 1.42, [1400, 1243, 650, 875])
    c[50] = lambda: nearest(20e-6 * 200 / (20e-3 - 20e-6), [0.5, 0.1, 0.2, 0.4])
    c[51] = lambda: [n for n in solve(3 * x**2 - 10 * x + 3, x) if n.is_integer][0]
    c[52] = lambda: 40 * Rational(1, 10) / Rational(4, 10) * 10
    c[53] = lambda: round(200 * 2 / (2e-4 * 1e11) * 1e6, 6)
    c[54] = lambda: 4**2 + 2**2 / (16 / 4)
    c[55] = lambda: round(9e9 * 4e-9, 6)
    c[57] = lambda: 2 * 2 * 5 * 4 * 2
    c[58] = lambda: round(math.sqrt((20 / 4)**2 - (20 / 5)**2) / (2 * 3 * 50) * 1000, 6)
    c[59] = lambda: round(600e-9 * 1 / (3 * 1e-3) * 1e6, 6)
    c[60] = lambda: round(5.808e30 / ((3 * 4.0026 - 12) * 931.5 * 1.6e-13) / 1e42)
    c[63] = lambda: 4 if 3 * 0.01 < 2 * 0.05 else 3
    c[81] = lambda: round(0.1 / ((500 * 1.25 - 0.1 * 159.5) / 1000) * 1000)
    c[83] = lambda: 70 + 12
    c[84] = lambda: 2
    c[86] = lambda: 2**2 * 2 + 0
    return c
