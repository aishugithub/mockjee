"""Answer checks for JEE Main 2023 (Session 2), 6 Apr Shift 2."""
from pyq_checks.common import *
from sympy import real_roots


def checks():
    c = {}

    def q2():
        both = 75 + 40 - 100
        al, be = 75 - both, 40 - both
        a2, b2 = Rational(al, 5)**2, Rational(be, 5)**2
        return opt(sqrt(1 - b2 / a2), [sqrt(117) / 12, sqrt(119) / 12, sqrt(129) / 12, 3 * sqrt(15) / 12])
    c[2] = q2

    def q4():
        # P^n = a_n I + b_n P using P^2 = I - P
        pw = {1: (0, 1)}
        for n in range(2, 30):
            a, b = pw[n - 1]
            pw[n] = (b, a - b)          # (aI + bP)P = aP + b(I - P)
        hits = []
        for al in range(1, 30):
            for be in range(1, 30):
                s = (pw[al][0] + pw[be][0], pw[al][1] + pw[be][1])
                d = (pw[al][0] - pw[be][0], pw[al][1] - pw[be][1])
                if s[1] == -29 and d[1] == -13 and s[0] > 0 and d[0] > 0:
                    hits.append(al + be + s[0] - d[0])
        assert len(set(hits)) == 1
        return opt(hits[0], [40, 24, 22, 18])
    c[4] = q4

    def q5():
        a, b, y, z = symbols('a b y z')
        M = Matrix([[1, 1, 1], [1, 2, a], [1, 3, 5]])
        assert solve(M.det(), a) == [3]
        def nsol(av, bv):
            A = Matrix([[1, 1, 1, 6], [1, 2, av, 10], [1, 3, 5, bv]])
            r1, r2 = Matrix(A[:, :3]).rank(), A.rank()
            return 'unique' if r1 == 3 else ('none' if r2 > r1 else 'inf')
        truth = [nsol(-3, 14) == 'unique', nsol(3, 24) == 'none', nsol(3, 14) == 'inf', nsol(3, 15) == 'unique']
        return [i for i, t in enumerate(truth, 1) if not t][0]
    c[5] = q5

    def q6():
        s1 = (pow(2023, 2022, 8) - pow(1999, 2022, 8)) % 8 == 0
        ns = [n for n in range(1, 1000) if (13 * pow(13, n, 144) - 11 * n - 13) % 144 == 0]
        s2 = len(ns) >= 6 and all((n2 - n1) == 144 for n1, n2 in zip(ns, ns[1:]))
        return 4 if s1 and s2 else 0
    c[6] = q6

    def q7():
        a, b = symbols('a b', positive=True)
        c7 = math.comb(11, 5) * a**6 / (2 * b)**5
        cm7 = math.comb(11, 6) * a**5 / (3 * b)**6
        t = simplify(solve(c7 - cm7, a)[0] * b)           # value of ab
        return [i for i, ok in enumerate([32 * t == 729, 64 * t == 243, 243 * t == 64, 729 * t == 32], 1) if ok][0]
    c[7] = q7

    def q8():
        from itertools import permutations
        words = sorted(set(''.join(p) for p in permutations('PUBLIC')))
        return opt(words.index('PUBLIC') + 1, [576, 578, 580, 582])
    c[8] = q8

    def q10():
        s = sum((-1)**(k + 1) * k * k for k in range(1, 2024))
        assert s % 1012 == 0
        v = s // 1012
        mn = [(m, v // (m * m)) for m in range(1, 100) if v % (m * m) == 0 and math.gcd(m, v // (m * m)) == 1 and m > 1]
        m, n = mn[0]
        return opt(m * m - n * n, [240, 220, 200, 180])
    c[10] = q10

    def q11():
        # f(x) = pi^2/2 + g(x) with g odd about pi/2; the g part integrates to 0
        return opt(integrate(pi**2 / 2 * sin(x), (x, 0, pi)), [2 * pi**2, pi**2 / 4, pi**2 / 2, pi**2])
    c[11] = q11

    def q12():
        y = Symbol('y')
        # x ln x = y e^y through (1, 0); at y = 2: ln(alpha^alpha) = 2 e^2
        u = y * exp(y)
        assert simplify(diff(u, y) - u - exp(y)) == 0 and u.subs(y, 0) == 0
        return opt(exp(u.subs(y, 2)), [exp(exp(2)), exp(sqrt(2) * exp(2)), exp(2 * exp(sqrt(2))), exp(2 * exp(2))])
    c[12] = q12

    def q13():
        cx, cy = Rational(1), Rational(-1, 2)
        r2 = cx**2 + cy**2 + 5
        R = (Rational(9, 4), Rational(2))
        L2 = (R[0] - cx)**2 + (R[1] - cy)**2 - r2
        r, L = sqrt(r2), sqrt(L2)
        return opt(r * L**3 / (r2 + L2), [Rational(13, 8), Rational(13, 4), Rational(5, 8), Rational(5, 4)])
    c[13] = q13

    def q14():
        A = integrate(3 - (3 - 2 * x), (x, 0, 1)) + integrate(2, (x, 1, 2)) + integrate(3 - (2 * x - 3), (x, 2, 3))
        return opt(A, [3, 4, 5, 6])
    c[14] = q14

    def q15():
        l = symbols('l')
        P = lambda X, Y, Z: (X + Y + Z - 6) + l * (2 * X + 3 * Y + 4 * Z + 5)
        lv = solve(P(0, 2, -2), l)[0]
        a, b, cc = 1 + 2 * lv, 1 + 3 * lv, 1 + 4 * lv
        d0 = -6 + 5 * lv
        d2 = (a * 12 + b * 12 + cc * 18 + d0)**2 / (a * a + b * b + cc * cc)
        return opt(d2, [155, 310, 620, 1240])
    c[15] = q15

    def q16():
        t = symbols('t')
        A = Matrix([0, 1, 2])
        B = Matrix([1 + 2 * t, 2 + 3 * t, 3 + 4 * t])
        tv = solve((B - A).dot(Matrix([2, 1, -3])), t)[0]
        d = (B - A).subs(t, tv)
        AP = Matrix([1, -10, 0])
        dist2 = AP.cross(d).dot(AP.cross(d)) / d.dot(d)
        return opt(sqrt(dist2), [sqrt(54), sqrt(69), sqrt(74), 9])
    c[16] = q16

    def q17():
        a = symbols('a')
        A, B = Matrix([1, -2, 3]), Matrix([2, -3, 4])
        C, D = Matrix([a + 1, 0, 2]), Matrix([9, a - 8, 6])
        sols = solve(Matrix.hstack(B - A, C - A, D - A).det(), a)
        return opt(sum(sols), [-2, 2, 4, 6])
    c[17] = q17

    def q18():
        a, b, cc = Matrix([1, 0, 0]), Matrix([0, 1, 0]), Matrix([0, 0, 1])
        V = Matrix.hstack(a, b, cc).det()
        V2 = Matrix.hstack(a, b + cc, a + 2 * b + 3 * cc).det()
        return [1, 2, 3, 6].index(abs(V2 / V)) + 1
    c[18] = q18

    def q19():
        p = Fraction(6 * 5 * 4, 216)
        return opt(p.denominator - p.numerator, [4, 3, 2, 1])
    c[19] = q19

    def q20():
        imp = lambda a, b: (not a) or b
        rows = list(product([True, False], repeat=2))
        s1 = all(imp(p, q) or ((not p) and q) for p, q in rows)
        s2 = all(not imp(imp(q, p), (not p) and q) for p, q in rows)
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(s1, s2)]
    c[20] = q20

    def q21():
        # |z-a|^2 + |z-b|^2 = 2|z-m|^2 + |a-b|^2/2 ; radius^2 = lam - |a-b|^2/4 = lam - 1
        lam, d = symbols('lam d', positive=True)
        return solve(Eq_(lam - d**2 / 4, lam - 1), d)[0]
    from sympy import Eq as Eq_
    c[21] = q21

    def q22():
        from itertools import permutations
        letters = 'UNIVERSE'
        vow = set('UIEE')
        words = set()
        for p in permutations(range(8), 4):
            w = ''.join(letters[i] for i in p)
            if len(set(w)) == 4 and sum(ch in vow for ch in w) == 2:
                words.add(w)
        return len(words)
    c[22] = q22

    def q23():
        lhs = sum(r * 21**(r - 1) * 20**(20 - r) for r in range(1, 21))
        assert lhs % 20**19 == 0
        return lhs // 20**19
    c[23] = q23

    def q24():
        return len(real_roots(x**5 - 20 * x**3 + 50 * x + 2))
    c[24] = q24

    def q25():
        C = symbols('C')
        y = Rational(3, 2) / x + C * x
        assert simplify(x * y - x**2 * diff(y, x) - 3) == 0
        y = y.subs(C, solve(y.subs(x, 1) - Rational(3, 2), C)[0])
        a = solve(y - Rational(1, 2), x)[0]
        return (a - 1)**2 + (Rational(1, 2) - Rational(3, 2))**2
    c[25] = q25

    def q26():
        import mpmath
        vals = []
        for n in (50, 200, 1000):
            vals.append(mpmath.quad(lambda t: t**(n - 2) * t / (1 + n * t**n)**(mpmath.mpf(1) / n), [0, 1]))
        assert vals[0] > vals[1] > vals[2] and vals[2] < 0.002
        return 0
    c[26] = q26

    def q27():
        eh = sqrt(2)
        ee = 1 / eh
        fh = sqrt(Rational(1, 2)) * eh          # hyperbola focus
        a = fh / ee
        b2 = a**2 * (1 - ee**2)
        return simplify((2 * b2 / a)**2)
    c[27] = q27

    def q28():
        s, t, al = symbols('s t al')
        sol = solve([1 + 2 * s - 4 - 5 * t, 2 + 3 * s - 1 - 2 * t], [s, t])
        be = solve(3 + al * sol[s] - Symbol('be') * sol[t], Symbol('be'))[0]
        f = 8 * al * be
        am = solve(diff(f, al), al)[0]
        return abs(f.subs(al, am))
    c[28] = q28

    def q29():
        xs = [2, 4, 6, 8, 10, 12, 14, 16]
        a = symbols('a')
        fs = [4, 4, a, 15, 8, a, 4, 5]                 # mean condition gives alpha = beta
        N = sum(fs)
        assert simplify(sum(f * v for f, v in zip(fs, xs)) - 9 * N) == 0
        av = solve(sum(f * v * v for f, v in zip(fs, xs)) / N - 81 - Rational(1508, 100), a)
        av = [v for v in av if v > 0][0]
        return av**2 + av**2 - av * av
    c[29] = q29

    def q30():
        d = lambda deg: tan(deg * pi / 180)
        v = d(9) - d(27) - d(63) + d(81)
        assert abs(N_(v) - 4) < 1e-12
        return 4
    from sympy import N as N_
    c[30] = q30

    def q31():
        u, v, du = 20.0, 80.0, 0.4
        f = u * v / (u + v)
        df = f * f * (du / u**2 + du / v**2)
        return nearest(100 * df / f, [0.51, 0.85, 1.02, 1.70])
    c[31] = q31

    def q32():
        R = 1.0
        disp = 2 * R * math.sin(math.radians(60))
        t = (2 * math.pi * R / 3) / math.pi
        return nearest(disp / t, [math.pi, math.sqrt(3), 1.5 * math.sqrt(3), 2 * math.sqrt(3)])
    c[32] = q32

    c[33] = lambda: opt(Rational(60 - 10, 2), [6, 25, 30, 3])
    c[34] = lambda: nearest(5 * (2 * 3.14 / 3.14)**2 * 2, [40, 50, 80, 100])
    c[36] = lambda: opt(100 * Rational(1, 1) / Rational(5, 4)**2, [25, 50, 64, 100])

    def q38():
        k = Rational(20, 7) / (50 - 10)
        T = symbols('T')
        return nearest(solve((40 - T) / 7 - k * ((40 + T) / 2 - 10), T)[0], [28, 30, 32, 34])
    c[38] = q38

    c[39] = lambda: [Rational(1, 4), 2, 1, 4].index(sqrt(Rational(800, 200))) + 1
    c[40] = lambda: opt(sqrt(Rational(32, 2)), [1, Rational(1, 2), Rational(1, 4), 4])
    c[41] = lambda: opt(Rational(3) / Rational(4, 10) * Rational(16, 10), [5, 10, 12, 15])

    def q43():
        n, m, w, h = symbols('n m w h', positive=True)
        r = symbols('r', positive=True)
        rv = solve(m * w * r * r - n * h / (2 * pi), r)[0]
        e = simplify(diff(log(rv), n) * n)          # exponent of n
        return opt(e, [1, 2, Rational(1, 2), -1])
    c[43] = q43

    c[44] = lambda: opt(Rational(1), [Rational(124, 100), 1, Rational(3, 2), 2])
    c[47] = lambda: nearest(36 * 120 * math.pi * 150e-6, [math.sqrt(2), 2 * math.sqrt(2), 1 / math.sqrt(2), 2])

    def q49():
        V = symbols('V')
        Vj = solve((30 - V) / 10 - (V - 12) / 20 - (V - 2) / 30, V)[0]
        return opt((Vj - 12) / 20, [Rational(2, 10), Rational(6, 10), Rational(4, 10), 1])
    c[49] = q49

    c[51] = lambda: (1 - Rational(1, 16)) * 100 * 4
    c[52] = lambda: 1 / (sqrt(Rational(2, 5)) / sqrt(2))**2
    c[53] = lambda: round(7e5 * (22 / 7) * (7e-3)**2 / 9.8)
    c[54] = lambda: round(4 * 10 * 1e-7 * 10 * 200 * 1e-4 / (2 * 10) / 1e-8)   # pi^2 = 10

    def q55():
        from math import lcm
        pos = lcm(7000, 5500) * 1e-10 * 1.5 / 2.5e-3
        return round(pos / 1e-5)
    c[55] = q55

    c[56] = lambda: round(1 / (9e9 * (1.6e-19)**2 / (2 * 12.8 * 1.6e-19) / 9e-10))
    c[57] = lambda: round(math.sqrt(2 * 2 * 1.6e-19 / 1.6e-27) * 0.5 * 2 * math.pi * 1.6e-27 / (1.6e-19 * math.pi / 2 * 1e-3) * 100)

    def q58():
        Rv = symbols('Rv', positive=True)
        I = Rational(3 - 2, 2)
        return solve(5 * Rv / (5 + Rv) - Rational(2) / I, Rv)[0]
    c[58] = q58

    c[59] = lambda: round(200e-4 / ((5 - 1) * 1e-3))
    c[60] = lambda: round(40 * 0.25 * 9.8 * (1 + (0.1 / 1.0)**2))
    c[61] = lambda: opt(Rational(2 * 1 * 10, 100) / Rational(2, 100), [Rational(25, 10), 5, Rational(75, 10), 10])
    c[62] = lambda: [3 * pi, 6 * pi, pi / 3, pi / 6].index(2 * pi * 9 / 3) + 1
    c[83] = lambda: round(-(2 * -393.5 + 3 * -241.8 + 1234.7))
    c[84] = lambda: sum(1 for p, q in [(2 * 1, 1 * 2), (3 * 1, 2 * 1.5), (4 * 1.5, 3 * 2), (2 * 2.5, 5 * 1)] if abs(p - q) < 1e-12)

    def q85():
        t = symbols('t')
        Kc = Rational(40, 100) / (Rational(2, 10) * Rational(1, 10))
        assert Kc == 20
        sols = [s for s in solve((Rational(40, 100) + t) - Kc * (Rational(2, 10) - t) * (Rational(3, 10) - t), t) if 0 < s < Rational(2, 10)]
        return round(float(Rational(40, 100) + sols[0]) * 100)
    c[85] = q85

    c[86] = lambda: sum(1 for e in (-1.19, -0.04, 0.80, 1.40) if e < 0.97)
    return c
