"""Answer checks for JEE Main 2023 (Session 2), 13 Apr Shift 2."""
from pyq_checks.common import *
from sympy import series


def checks():
    c = {}

    def q2():
        X, Y = symbols('X Y', real=True)
        sols = solve([X + 2 * X * Y, -Y - (X**2 - Y**2 + X)], [X, Y], dict=True)
        return opt(sum(s[X]**2 + s[Y]**2 for s in sols), [Rational(5, 2), 3, Rational(7, 2), 4])
    c[2] = q2

    def q3():
        a, b = solve(x**2 - sqrt(2) * x + 2, x)
        return opt(simplify(expand(a**14 + b**14)), [-64, -64 * sqrt(2), -128, -128 * sqrt(2)])
    c[3] = q3

    def q4():
        p, q = symbols('p q')
        s = solve([2 * p + q - 2, p + 2 * q + 5], [p, q])
        l, m = -s[p] - 5 * s[q], 5 * s[p] + 7 * s[q]
        assert Matrix([[2, 1, -1], [2, -5, l], [1, 2, -5]]).det() == 0
        return opt((l + m)**2 + (l - m)**2, [904, 912, 916, 920])
    c[4] = q4

    def q5():
        al = symbols('al')
        av = solve(Matrix([[1, 2, 3], [al, 3, 1], [1, 1, 2]]).det() - 2, al)[0]
        A = Matrix([[1, 2, 3], [av, 3, 1], [1, 1, 2]])
        M = 2 * (2 * (2 * A).adjugate()).adjugate()
        n = math.log(int(abs(M.det())), 32)
        return opt(3 * round(n) + av, [9, 10, 11, 12])
    c[5] = q5

    def q6():
        from itertools import permutations
        w = sorted(set(''.join(t) for t in permutations('MONDAY')))
        return opt(w.index('MONDAY') + 1, [324, 326, 327, 328])
    c[6] = q6

    c[7] = lambda: opt(expand((2 * x**3 - 1 / (3 * x**2))**5).coeff(x, 5), [8, 9, Rational(80, 9), Rational(26, 3)])

    def q8():
        r2 = symbols('r2', positive=True)
        r2v = solve(Rational(1, 3) * (r2 + r2**2) - 2, r2)[0]
        ar3 = Rational(1, 3)
        a4a6 = ar3 * (1 + r2v)
        a2a4 = ar3 / r2v * (1 + r2v)
        return opt(6 * a2a4 * a4a6, [2, 2 * sqrt(2), 3 * sqrt(3), 3])
    c[8] = q8

    def q9():
        a, b = symbols('a b')
        cc = 2 * a
        num = series(exp(a * x) - cos(b * x) - cc * x * exp(-cc * x) / 2, x, 0, 3).removeO()
        assert num.coeff(x, 1) == 0
        val = simplify(num.coeff(x, 2) / 2)               # (1 - cos 2x) ~ 2x^2
        assert simplify(4 * val - (5 * a**2 + b**2)) == 0     # limit = (5a^2 + b^2)/4 = 17
        return opt(4 * 17, [68, 64, 72, 76])
    c[9] = q9

    def q10():
        import mpmath
        mpmath.mp.dps = 30
        n = mpmath.e**(-mpmath.pi / 4) + mpmath.quad(lambda t: mpmath.e**(-t) * mpmath.tan(t)**50, [0, mpmath.pi / 4])
        d = mpmath.quad(lambda t: mpmath.e**(-t) * (mpmath.tan(t)**49 + mpmath.tan(t)**51), [0, mpmath.pi / 4])
        r = nearest(n / d, [25, 49, 50, 51])
        mpmath.mp.dps = 15
        return r
    c[10] = q10

    def q11():
        A = 2 * (integrate(4 - x**2 - 1, (x, 0, 1)) + integrate(4 - x**2 - x**2, (x, 1, sqrt(2))))
        return opt(simplify(A), [Rational(4, 3) * (4 * sqrt(2) - 1), Rational(4, 3) * (4 * sqrt(2) + 1), Rational(3, 4) * (4 * sqrt(2) - 1), Rational(3, 4) * (4 * sqrt(2) + 1)])
    c[11] = q11

    def q12():
        X, Y = symbols('X Y')
        L = [15 * X - Y - 82, 6 * X - 5 * Y + 4, 9 * X + 4 * Y - 17]
        P = [solve([L[i], L[j]], [X, Y]) for i, j in ((0, 1), (0, 2), (1, 2))]
        a, b = sum(p[X] for p in P) / 3, sum(p[Y] for p in P) / 3
        r1, r2 = a + 2 * b, 2 * a - b
        opts = [x**2 - 14 * x + 48, x**2 - 10 * x + 25, x**2 - 7 * x + 12, x**2 - 13 * x + 42]
        return [i for i, f in enumerate(opts, 1) if f.subs(x, r1) == 0 and f.subs(x, r2) == 0][0]
    c[12] = q12

    def q13():
        X, Y = symbols('X Y')
        for bis in (Y + 1, X - Rational(28, 3)):
            s = solve([bis, 4 * X + 3 * Y - 1], [X, Y])
            r = abs(3 * s[X] + 4 * s[Y] - 24) / 5
            if r < 8:
                return opt(s[X] - s[Y] + r, [5, 6, 7, 9])
    c[13] = q13

    def q14():
        A, B = Matrix([0, -1, 2]), Matrix([-1, 2, 1])
        n = (B - A).cross(Matrix([4, 2, -6]))
        opts = [(1, -2, 1), (-2, 5, 0), (2, 0, 1), (0, 5, -2)]
        return [i for i, P in enumerate(opts, 1) if n.dot(Matrix(P) - A) == 0][0]
    c[14] = q14

    def q15():
        a1, d1 = Matrix([-3, 1, 5]), Matrix([-3, 1, 5])
        opts = [((1, 2, 5), (-1, 2, 5)), ((-1, 2, 5), (-1, 2, 5)), ((-1, 2, 5), (-1, 2, 4)), ((-1, 2, 5), (1, 2, 5))]
        return [i for i, (p, d) in enumerate(opts, 1) if (Matrix(p) - a1).dot(d1.cross(Matrix(d))) == 0][0]
    c[15] = q15

    def q16():
        t = symbols('t')
        N = Matrix([4, 5, 8]) + t * Matrix([1, 4, 1])
        N = N.subs(t, solve((N - Matrix([1, -2, 3])).dot(Matrix([1, 4, 1])), t)[0])
        return opt(abs(2 * N[0] - 2 * N[1] + N[2] + 5) / 3, [6, 7, 8, 9])
    c[16] = q16

    c[17] = lambda: opt(49 * (2 * 3 * sin(pi / 4))**2, [441, 882, 482, 841])

    def q18():
        d = symbols('d', positive=True)
        AB, CA = Matrix([-2, 1, 3]), Matrix([4, 3, d])
        cr = AB.cross(CA)
        dv = solve(cr.dot(cr) - 4 * 150, d)[0]
        CB = AB + CA.subs(d, dv)                           # CB = CA + AB
        return opt(CB.dot(CA.subs(d, dv)), [60, 54, 120, 108])
    c[18] = q18

    def q19():
        n, p = symbols('n p', positive=True)
        for nv in range(2, 30):
            pv = Rational(3, nv + 2)
            if nv * pv**2 == 1:
                q = 1 - pv
                P = 1 - q**nv - nv * pv * q**(nv - 1)
                return opt(nv**2 * P, [15, 16, 12, 11])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=2))
        st = [(p and not q) or ((not p) and q) or ((not p) and (not q)) for p, q in rows]
        opts = [lambda p, q: (not p) or (not q), lambda p, q: p or not q, lambda p, q: (not p) or q, lambda p, q: p or q]
        return [i for i, f in enumerate(opts, 1) if [f(p, q) for p, q in rows] == st][0]
    c[20] = q20

    def q21():
        A = [-4, -3, -2, 0, 1, 3, 4]
        R = {(a, b) for a in A for b in A if b == abs(a) or b * b == a + 1}
        R2 = R | {(a, a) for a in A}
        R2 = R2 | {(b, a) for a, b in R2}
        return len(R2 - R)
    c[21] = q21

    c[22] = lambda: sum(1 for t in product(range(1, 6), repeat=3) if (100 * t[0] + 10 * t[1] + t[2]) % 6 == 0)
    c[23] = lambda: pow(7, 103, 17)
    c[24] = lambda: sum(math.isqrt(k) for k in range(1, 121))

    def q25():
        f = sum(k * x**k for k in range(1, 11))
        v = 2 * f.subs(x, 2) + diff(f, x).subs(x, 2)
        return [n for n in range(1, 30) if 119 * 2**n + 1 == v][0]
    c[25] = q25

    def q26():
        s = symbols('s')
        def fn(n):
            A = sum(s**(k - 1) for k in range(1, n + 1)); B = sum((2 * k - 1) * s**(k - 1) for k in range(1, n + 1))
            return integrate(expand(A * B), (s, 0, 1))
        return fn(21) - fn(20)
    c[26] = q26

    def q27():
        C = symbols('C')
        y = (sqrt(x**2 - 1) + 2 * log(x + sqrt(x**2 - 1)) + C) / (x**2 - 1)**2
        assert abs(N_((diff(y, x) + 4 * x / (x**2 - 1) * y - (x + 2) / (x**2 - 1)**Rational(5, 2)).subs({x: 3, C: 1}))) < 1e-12
        Cv = solve(y.subs(x, 2) - Rational(2, 9) * log(2 + sqrt(3)), C)[0]
        val = simplify(y.subs(C, Cv).subs(x, sqrt(2)))
        al, be, ga = 2, 1, 3
        assert abs(N_(val - (al * log(sqrt(al) + be) + be - sqrt(ga)))) < 1e-12
        return al * be * ga
    from sympy import N as N_
    c[27] = q27

    def q28():
        a2, b2 = Rational(16, 9), 4 - Rational(16, 9)
        m = Rational(3, 2)
        for cc in (sqrt(a2 * m * m - b2), -sqrt(a2 * m * m - b2)):
            px, py = -a2 * m / cc, -b2 / cc
            if px > 0 and py > 0:
                return abs(6 * (-cc / m)) + abs(5 * cc)
    c[28] = q28

    def q29():
        s1, s2 = 500 - 45 - 50 + 20 + 25, 10 * (144 + 2500) - 45**2 - 50**2 + 20**2 + 25**2
        return Rational(s2, 10) - Rational(s1, 10)**2
    c[29] = q29

    c[30] = lambda: len([v for v in solve(x * (1 + x**2) - 2 * x, x) if -1 < v <= 1 and abs(N_(asin(v) - 2 * atan(v))) < 1e-12])
    c[32] = lambda: opt(2 * Rational(25, 10) * 5, [5, Rational(125, 10), 25, Rational(625, 10)])
    c[33] = lambda: opt((90 + 54) * Rational(5, 18) * 8, [80, 120, 200, 320])
    c[34] = lambda: opt(200 * Rational(2, 10)**2 * 70, [14, 2240, 560, 2800])
    c[37] = lambda: opt(Rational(1, 2) * Rational(3, 2), [2, Rational(2, 3), Rational(3, 4), Rational(4, 3)])
    c[39] = lambda: nearest(1500 * 373 / 273, [1500, 750, 2049, 1098])
    c[40] = lambda: opt(1 / sqrt(2), [2, Rational(1, 2), 1 / sqrt(2), sqrt(2)])
    c[41] = lambda: [(8, 2), (7, 3), (5, 5), (9, 1)].index(max([(8, 2), (7, 3), (5, 5), (9, 1)], key=lambda t: t[0] * t[1])) + 1
    c[42] = lambda: nearest(4 * 3 / (4 + 6) * 6, [10.3, 4.8, 7.2, 12])
    c[46] = lambda: opt(Rational(3, 1)**2, [2, Rational(9, 4), 9, Rational(25, 9)])
    c[51] = lambda: (2**2 - 1**2) / 1
    c[52] = lambda: round(52.5 / (5 * 0.7), 6)
    c[53] = lambda: solve(84 * (100 - x) - 126 * x, x)[0]
    c[54] = lambda: 180 * Rational(50, 30)**2
    c[55] = lambda: round(9e9 * (2e-6)**2 / (0.02)**2 * (64 - Rational(32, 9)))
    def q56():
        Vl = 12 - 3 * Rational(12, 12)
        Vr = 12 - 4 * Rational(12, 6)
        return Rational(1, 2) * 6 * (Vl - Vr)**2
    c[56] = q56
    c[57] = lambda: round(0.04 * 10 / (0.4 * 0.5), 6)
    c[58] = lambda: round(100 * 2 * 1.5 * 24e-4 / 12 * 1000)
    c[59] = lambda: round(100 / 20)
    c[60] = lambda: round(6.6e-34 * 3e8 / 1.6e-19 * (1 / 500e-9 - 1 / 600e-9) / 1e-4)
    c[81] = lambda: round(1 / 0.01)
    c[82] = lambda: round(math.sqrt(3) * 4 / 4 * 10)
    def q84():
        n_part = 29.25 / 58.5 * 2 + 19 / 95 * 3
        return round(100 + 0.52 * n_part / ((100 - 29.25 - 19) / 1000))
    c[84] = q84
    c[85] = lambda: round((4.76 + 0.30 - 0.48) * 100)
    c[86] = lambda: round(-(0.34 + 0.059 / 2 * math.log10(1e-20)) * 100)
    c[87] = lambda: round(800 + 2 * 800 * (1 - 0.5**3))
    c[88] = lambda: 14 + 2 + 7
    c[90] = lambda: round(0.376 * 80 / 188 / 0.4 * 100)


    def q31():
        # a/Y^2 ~ pressure, b ~ volume: a/b ~ pressure * volume (M L^2 T^-2)
        P, V = (1, -1, -2), (0, 3, 0)
        ab = tuple(p + 2 * v - v for p, v in zip(P, V))
        dims = {1: (1, 2, -2), 2: (1, -2, -2), 3: (1, 1, -1), 4: (1, -1, -1)}
        return [k for k, d in dims.items() if d == ab][0]
    c[31] = q31

    def q36():
        r, dr = Rational(5), Rational(1, 10)
        A_true = 2 * dr / r * 100 == 4                            # v ~ r^2
        R_true = False                                            # v is not ~ 1/r
        return {(True, True): 1, (True, False): 3, (False, True): 4}[(A_true, R_true)]
    c[36] = q36
    c[38] = lambda: opt(4**Symbol('g'), [1, 4, 4**Symbol('g'), 4**(1 / Symbol('g'))])

    def q43():
        v, B = Matrix([1, 0, 0]), Matrix([0, 0, -1])
        F = -1 * v.cross(B)
        stm = {'A': F == Matrix([0, 1, 0]), 'B': F == Matrix([0, -1, 0]), 'C': F == Matrix.zeros(3, 1),
               'D': F == Matrix.zeros(3, 1), 'E': v.dot(B) == 0 and F != Matrix.zeros(3, 1)}
        got = ''.join(k for k, val in stm.items() if val)
        return {'AE': 1, 'CD': 2, 'BD': 3, 'BE': 4}[got]
    c[43] = q43

    def q45():
        d = Matrix([0, 0, -1]).cross(Matrix([1, 0, 0]))
        return {(0, 1, 0): 1, (0, -1, 0): 2, (0, 0, 1): 3}[tuple(d)]
    c[45] = q45
    return c
