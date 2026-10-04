"""Answer checks for JEE Main 2024 (Session 2), 8 Apr Shift 2."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, Integer, series, asinh


def checks():
    c = {}

    def q1():
        A, B = [2, 3, 6, 8, 9, 11], [1, 4, 5, 10, 15]
        P = [(a, b) for a in A for b in B]
        R = lambda p, q: (3 * p[0] * q[1] - 7 * p[1] * q[0]) % 2 == 0
        refl = all(R(p, p) for p in P)
        sym = all(R(q, p) for p in P for q in P if R(p, q))
        trans = all(R(p, r) for p in P for q in P for r in P if R(p, q) and R(q, r))
        return {(True, True, True): 1, (True, False, False): 2, (True, True, False): 4}[(refl, sym, trans)]
    c[1] = q1

    def q2():
        a = 2.0
        f = lambda t: -a if t <= 0 else t + a
        g = lambda t: (f(abs(t)) - abs(f(t))) / 2
        xs = [-a + k * 2 * a / 4000 for k in range(4001)]
        vals = [round(g(t), 9) for t in xs]
        one_one = len(set(vals)) == len(vals)
        onto = min(vals) <= -a + 1e-9 and max(vals) >= a - 1e-9 and any(abs(v + a / 2) < 1e-3 for v in vals)
        return {(True, True): 3, (True, False): 1, (False, True): 2, (False, False): 4}[(one_one, onto)]
    c[2] = q2

    def q3():
        l, m = symbols('l m')
        mv = solve(Matrix([[1, 4, -1], [7, 9, m], [5, 1, 2]]).det(), m)[0]
        lv = solve(Matrix([[1, 4, l], [7, 9, -3], [5, 1, -1]]).det(), l)[0]
        assert Matrix([[1, 4, -1, lv], [7, 9, mv, -3], [5, 1, 2, -1]]).rank() == 2
        return opt(2 * mv + 3 * lv, [3, -3, 2, -2])
    c[3] = q3

    def q4():
        al, be, ga, a, b, cc = symbols('al be ga a b cc')
        D = Matrix([[al, b, cc], [a, be, cc], [a, b, ga]]).det()
        E = a / (al - a) + b / (be - b) + ga / (ga - cc)
        assert simplify(E * (al - a) * (be - b) * (ga - cc) - D) == 0
        return opt(0, [2, 0, 1, 3])
    c[4] = q4

    def q5():
        from collections import Counter
        cnt = Counter('MATHEMATICS')
        letters = list(cnt)
        def ways(i, left):
            if left == 0: return 1
            if i == len(letters): return 0
            return sum(ways(i + 1, left - k) for k in range(0, min(cnt[letters[i]], left) + 1))
        return opt(ways(0, 5), [175, 177, 179, 181])
    c[5] = q5

    def q6():
        a = Symbol('a', positive=True)
        av = solve(math.comb(10, 4) * a**3 / 16 - 105, a)[0]
        return opt(av**2, [2, 4, 6, 9])
    c[6] = q6

    def q7():
        th = [t for t in [k * pi / 4 for k in range(-4, 9)] if -pi <= t <= 2 * pi and simplify(1 - 2 * cos(t)**2) == 0]
        return opt(sum(th), [2 * pi, 3 * pi, 4 * pi, 5 * pi])
    c[7] = q7

    def q8():
        r2 = [v for v in solve(7 / x + 7 * x - Rational(70, 3), x) if v > 1][0]      # x = r^2
        return opt(7 * (1 + r2 + r2**2), [78, 84, 91, 96])
    c[8] = q8

    def q9():
        a, b = symbols('a b', positive=True)
        L = limit((tan((a + 1) * x) + b * tan(x)) / x, x, 0, '-')
        R = limit((sqrt(a * x + b**2 * x**2) - sqrt(a * x)) / (b * sqrt(a) * x * sqrt(x)), x, 0, '+')
        s = solve([L - 3, R - 3], [a, b], dict=True)[0]
        return opt(s[b] / s[a], [6, 5, 4, 8])
    c[9] = q9

    def q10():
        a = Symbol('a', positive=True)
        f = 2 * x**3 - 9 * a * x**2 + 12 * a**2 * x + 1
        av = solve(a**2 - 2 * a, a)[0]                       # max at a, min at 2a (from f')
        assert set(solve(diff(f, x).subs(a, av), x)) == {av, 2 * av}
        opts = [8 * x**2 - 6 * x + 1, 8 * x**2 + 6 * x - 1, x**2 - 6 * x + 8, x**2 + 6 * x + 8]
        return [i for i, e in enumerate(opts, 1) if e.subs(x, av) == 0 and e.subs(x, av**2) == 0][0]
    c[10] = q10

    def q11():
        al = Symbol('al')
        F = lambda t: 2 * atan(sqrt(exp(t) - 1))
        av = solve(F(log(4)) - 2 * atan(Symbol('u')) - pi / 6, Symbol('u'))[0]
        ea = av**2 + 1
        opts = [x**2 + 2 * x - 8, x**2 - 2 * x - 8, 2 * x**2 - 5 * x + 2, 2 * x**2 - 5 * x - 2]
        return [i for i, e in enumerate(opts, 1) if e.subs(x, ea) == 0 and e.subs(x, 1 / ea) == 0][0]
    c[11] = q11

    def q12():
        y = Symbol('y')
        inside = integrate(sqrt(8 - y**2) - y**2 / 2, (y, 0, 2))
        return opt(simplify(2 * pi - inside), [pi - Rational(2, 3), pi / 2 - Rational(2, 3), pi - Rational(1, 3), pi / 2 - Rational(1, 3)])
    c[12] = q12

    def q13():
        u = (x**2 - 1) / 2
        assert simplify(diff(u, x) + 2 * x * u - x**3) == 0 and u.subs(x, 1) == 0
        return opt(atan(u.subs(x, sqrt(3))), [pi / 12, pi / 6, pi / 4, pi / 3])
    c[13] = q13

    def q14():
        a = Symbol('a')
        sols = solve((5 * a - 4)**2 - (10 + 2 * a)**2, a)
        return opt(abs(sols[0] * sols[1]), [2, 8, 6, 4])
    c[14] = q14

    def q15():
        P = Matrix([-4, 5]); n = Matrix([1, 2])
        img = P - 2 * (n.dot(P) - 2) / n.dot(n) * n
        return opt((img - Matrix([-4, 3])).norm(), [1, 2, 3, 4])
    c[15] = q15

    def q16():
        l = Symbol('l')
        d = Matrix([2, 3, 4]); AB = Matrix([2 - l, 0, 4])
        sols = solve(AB.cross(d).dot(AB.cross(d)) / d.dot(d) - Rational(169, 29), l)
        return [i for i, o in enumerate([-1, Rational(13, 25), 1, Rational(-13, 25)], 1) if o in sols][0]
    c[16] = q16

    def q17():
        a, b = Matrix([4, -1, 1]), Matrix([11, -1, 1])
        l = Symbol('l'); cc = l * (4 * b - a)
        lv = solve((2 * a + 3 * b).dot(cc) - 1670, l)[0]
        cc = cc.subs(l, lv)
        assert (a + b).cross(cc) == cc.cross(-2 * a + 3 * b)
        return opt(cc.dot(cc), [1609, 1600, 1618, 1627])
    c[17] = q17

    def q18():
        l = Symbol('l')
        v = Matrix([2, 3, -5]) + Matrix([3, -1, l])
        lv = [s for s in solve((v.dot(Matrix([1, 2, 3])))**2 - 9 * v.dot(v), l) if v.dot(Matrix([1, 2, 3])).subs(l, s) > 0][0]
        return opt(3 * lv, [25, 27, 30, 21])
    c[18] = q18
    c[19] = lambda: opt(Rational(4, 5 + 4 + 3), [Rational(5, 12), Rational(1, 3), Rational(1, 4), Rational(1, 2)])

    def q20():
        v = (3 * cos(pi / 5) + 5 * sin(pi / 10)) / (5 * cos(pi / 5) - 3 * sin(pi / 10))
        assert abs(N(v - (17 * sqrt(5) - 24) / 11)) < 1e-12 and math.gcd(17, 11) == 1
        return opt(17 + 24 + 11, [40, 50, 52, 54])
    c[20] = q20

    def q21():
        roots = set()
        for lo, hi, e in [(-oo, -3, (x + 1) * (x + 3) + 4 * (x + 2) + 5), (-3, -2, -(x + 1) * (x + 3) + 4 * (x + 2) + 5),
                          (-2, -1, -(x + 1) * (x + 3) - 4 * (x + 2) + 5), (-1, oo, (x + 1) * (x + 3) - 4 * (x + 2) + 5)]:
            for r in solve(e, x):
                if r.is_real and lo <= r <= hi: roots.add(r)
        return len(roots)
    c[21] = q21

    def q22():
        P, n = Matrix([7, 2]), Matrix([2, 1])
        img = P - 2 * (n.dot(P) - 6) / n.dot(n) * n
        A = Matrix([3, 10])
        d = img - A
        a, b = symbols('a b')
        s = solve([a * A[0] + b * A[1] + 1, a * img[0] + b * img[1] + 1], [a, b])
        return s[a]**2 + s[b]**2 + 3 * s[a] * s[b]
    c[22] = q22
    c[23] = lambda: sum(3 * n - 1 for n in range(46, 56))

    def q24():
        t = Symbol('t', positive=True)
        A = 2 * sqrt(2 * t) * (24 - t)
        tv = solve(diff(A, t), t)[0]
        return A.subs(t, tv)
    c[24] = q24

    def q25():
        al = 1
        be = limit((1 + sin(x))**(cot(x) / 2), x, 0)
        a = Symbol('a'); b = Symbol('b')
        s = solve([-sqrt(E) / a - al * be, -b / a - (al + be)], [a, b], dict=True)[0]
        return simplify(12 * log(s[a] + s[b]))
    from sympy import cot, E
    c[25] = q25

    def q26():
        A, B = Rational(5, 4), Rational(1, 5)
        F = A * ((x - 1) / (x + 3))**B
        import mpmath
        d = diff(F, x)
        for xv in (2, 3.5, 7):
            assert abs(N(d.subs(x, xv) - 1 / ((x - 1)**4 * (x + 3)**6)**Rational(1, 5)).subs(x, xv)) < 1e-12
        return 1 + 1 + 20 * A * B
    c[26] = q26

    def q27():
        y = Function('y')
        Y = 2 * x * exp(2 - x * Symbol('Y'))     # implicit: y = 2x e^{2 - xy}
        Ys = Symbol('Y')
        F = Ys - 2 * x * exp(2 - x * Ys)
        dy = -diff(F, x) / diff(F, Ys)
        de = x * dy - Ys + x * Ys * (x * dy + Ys)
        assert all(abs(N(de.subs({x: xv, Ys: yv}))) < 1e-9 for xv, yv in [(1, 2)])
        return 2 + 2
    c[27] = q27

    def q28():
        S = Matrix([sqrt(3 + 5), 0]); A = Matrix([sqrt(6), sqrt(5)])
        B = 2 * A - S
        area = Abs(S[0] * B[1] - S[1] * B[0]) / 2
        return simplify(area**2)
    from sympy import Abs
    c[28] = q28

    def q29():
        P0, d, Q = Matrix([0, 1, 2]), Matrix([1, 2, 3]), Matrix([1, 6, 4])
        F = P0 + d * (Q - P0).dot(d) / d.dot(d)
        I_ = 2 * F - Q
        return 2 * I_[0] + I_[1] + I_[2]
    c[29] = q29

    def q30():
        for a in range(1, 40):
            for b in range(a + 1, 40):
                cc = 90 - 9 - 25 - a - b
                if cc > b:
                    d = [9, 25, a, b, cc]
                    if sum(abs(v - 18) for v in d) == 20 and sum((v - 18)**2 for v in d) == 136:
                        return 2 * a + b - cc
    c[30] = q30

    c[32] = lambda: opt(4, [2, 4, Rational(1, 4), Rational(1, 2)])
    c[33] = lambda: [i for i, e in enumerate([1 - Symbol('n')**2, 1 - 1 / Symbol('n')**2, sqrt(1 - Symbol('n')**2), sqrt(1 - 1 / Symbol('n')**2)], 1) if simplify(1 / (1 - e) - Symbol('n')**2) == 0][0]   # n^2 = a_smooth/a_rough
    c[34] = lambda: opt(sqrt(2 * (5 * 10 * 5 - Rational(1, 2) * 5 * 10 * 2) / 100), [sqrt(5), sqrt(6), 1, 2])
    c[35] = lambda: opt(Rational(1, Rational(3, 2)), [Rational(5, 4), Rational(2, 3), Rational(4, 5), Rational(3, 2)])
    c[36] = lambda: opt(3 * sqrt(4), [3, Rational(4, 3), 6, 12])
    c[37] = lambda: [i for i, (p, q) in enumerate([(5, 4), (8, 9), (9, 10), (1, 1)], 1) if Rational(p, q) == (Rational(9, 10) - Rational(8, 10)) / (1 - Rational(9, 10))][0]
    c[38] = lambda: opt(100 * Rational(14, 10) / Rational(4, 10), [250, 350, 150, 490])
    c[40] = lambda: opt(solve(Rational(2, 10) + Rational(6, 10) / x - Rational(6, 10), x)[0], [Rational(3, 2), Rational(66, 100), 1, Rational(133, 100)])
    c[42] = lambda: opt(Rational(1, 2) / 1 / (1 / Rational(2)), [Rational(1, 4), Rational(3, 4), 1, 4])
    c[43] = lambda: nearest(math.sqrt(120**2 - 36**2) / (36 / 90) / (2 * math.pi * 60), [2.86, 0.91, 0.286, 0.76])
    c[44] = lambda: opt(330, [660, 340, 330, 165])

    def q45():
        v1 = 1 / (Rational(1, 10) - Rational(1, 30))           # 15 cm right of L1
        u2 = v1 - 5                                            # virtual object 10 cm right of L2
        inv = Rational(-1, 10) + 1 / u2
        assert inv == 0                                        # parallel rays leave L2
        return 4
    c[45] = q45
    c[46] = lambda: 2 if Rational(1, 1836) < 1 else 1                 # same p: K = p^2/2m, proton heavier so K_p < K_e
    c[49] = lambda: opt(Rational(4) + Rational(60, 100) - Rational(5, 100), [Rational(460, 100), Rational(465, 100), Rational(335, 100), Rational(455, 100)])

    def q50():
        N_, m = symbols('N m', positive=True)
        mv = solve(1 - m / N_ - 1 / (2 * N_), m)[0]
        return [i for i, e in enumerate([(2 * N_ - 1) / (20 * N_), (2 * N_ - 1) / 2, 2 * N_ - 1, (2 * N_ - 1) / (2 * N_)], 1) if simplify(e - mv) == 0][0]
    c[50] = q50
    c[51] = lambda: round(100 * (1 / 2) * math.sqrt(4))
    c[52] = lambda: simplify(sqrt(9 - 1) / sqrt(2))
    c[53] = lambda: 10 * 2**2
    c[54] = lambda: round(math.sqrt(0.9 / (0.5 * 0.2 * 50**2)) * 100, 6)

    def q55():
        r = (20 * sqrt(20) / 125)
        xv = solve(8 / (5 * sqrt(Symbol('x'))) - r, Symbol('x'))[0]
        return xv
    c[55] = q55
    c[56] = lambda: 25 / ((100 - 25) / 10 - 25 / 10)
    c[57] = lambda: round(5e3 * 0.3 / 150, 6)
    c[58] = lambda: round(110 * 100 * 2e-6 * 1000, 6)
    c[59] = lambda: round(1e-3 / 5 / 1e-4, 6)
    c[60] = lambda: round((1.8 + 3.2) / (20 / 20), 6)
    c[63] = lambda: 2 if diff(-Rational(59, 2000) * log(Rational(1, 10**6) / Symbol('cu', positive=True)), Symbol('cu', positive=True)).subs(Symbol('cu', positive=True), Rational(1, 100)) > 0 else 0   # E rises with [Cu2+]
    c[65] = lambda: [i for i, e in enumerate([None, None, None, Symbol('K1') / Symbol('K2')], 1) if e is not None and solve(Symbol('K1') * Symbol('A') - Symbol('K2') * Symbol('B'), Symbol('B'))[0] == e * Symbol('A')][0]
    c[81] = lambda: round(46 / (46 + 9 * 18) * 100)
    c[82] = lambda: round(1 / 5800e-8 / 10)
    c[84] = lambda: round(40.79 - 8.3 * 373.15 / 1000)
    c[85] = lambda: round(4.44 / (4.44 + 1000 / 18) * 1000)
    return c
