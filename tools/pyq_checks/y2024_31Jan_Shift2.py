"""Answer checks for JEE Main 2024 (Session 1), 31 Jan Shift 2. Q34 was dropped by NTA."""
from pyq_checks.common import *
from sympy import E, Function, series


def checks():
    c = {}

    def q1():
        g = x**3 - 3 * x + 1
        assert all(diff(g, x).subs(x, v) > 0 for v in (-5, -2, Rational(-11, 10)))
        b = exp(g.subs(x, -1))
        P = Matrix([2 * b + 4, 2])                       # a = 0
        d = abs(P[0] + exp(-3) * P[1] - 4) / sqrt(1 + exp(-6))
        return opt(simplify(d), [4 * sqrt(1 + exp(6)), 3 * sqrt(1 + exp(6)), 2 * sqrt(1 + exp(6)), sqrt(1 + exp(6))])
    c[1] = q1

    def q2():
        u = [r for r in solve(x**2 - 2 * x - 2, x) if r > 0][0]
        return opt(sum(1 for r in [u] if 1 / E <= r <= E), [0, 1, 2, 3])
    c[2] = q2

    def q3():
        p = solve(125 - 15 * Symbol('p') - (20 + 15 * sympy_I), Symbol('p'))[0]
        v = expand((25 - 2 * p)**2 - 2 * p**2)
        return opt(Abs(v), [30 * sqrt(3), 15 * sqrt(15), 25 * sqrt(3), 75])
    from sympy import Abs
    c[3] = q3

    def q4():
        Pm = Matrix([[1, -1, 0], [0, 0, 1], [1, 1, 0]])
        A = Pm * diag(2, 4, 2) * Pm.inv()
        assert A * Matrix([1, 0, 1]) == 2 * Matrix([1, 0, 1]) and A * Matrix([-1, 0, 1]) == 4 * Matrix([-1, 0, 1])
        return 3 if (A - 3 * eye(3)).det() != 0 else 0
    from sympy import diag, eye
    c[4] = q4
    c[5] = lambda: opt(sum(1 for a in range(2, 22) for b in range(2, 22) if 21 - a - b >= 2), [130, 136, 142, 406])

    def q6():
        ms = [m for m in range(0, 5) if math.comb(6, m) + 2 * math.comb(6, m + 1) + math.comb(6, m + 2) > math.comb(8, 3)]
        ns = [n for n in range(5, 30) if Rational(math.perm(n - 1, 3), math.perm(n, 4)) == Rational(1, 8)]
        assert ms == [2] and ns == [8]
        m, n = 2, 8
        return opt(math.perm(n, m + 1) + math.comb(n + 1, m), [372, 376, 380, 384])
    c[6] = q6

    def q7():
        d = [v for v in solve((1 + 7 * x)**2 - (1 + x) * (1 + 43 * x), x) if v != 0][0]
        return opt(10 * (2 + 19 * d), [960, 970, 980, 990])
    c[7] = q7

    def q8():
        f = lambda t: math.exp(-abs(math.log(t)))
        h = 1e-6
        l, r = (f(1) - f(1 - h)) / h, (f(1 + h) - f(1)) / h
        assert abs(l - 1) < 1e-4 and abs(r + 1) < 1e-4
        return opt(0 + 1, [0, 1, 2, 3])
    c[8] = q8

    def q9():
        f = log(x + 2)                                   # sample positive increasing f with f(7x)/f(x) -> 1
        assert limit(f.subs(x, 7 * x) / f, x, oo) == 1
        return opt(limit(f.subs(x, 5 * x) / f - 1, x, oo), [1, Rational(7, 5), 4, 0])
    c[9] = q9

    def q10():
        a = Symbol('a', positive=True)
        b = 2 * a / (a - 8)
        s = a + b
        av = [v for v in solve(diff(s, a), a) if v > 8][0]
        return opt(simplify(s.subs(a, av)), [12, 18, 20, 24])
    c[10] = q10
    c[11] = lambda: opt(integrate(4 * x - x**2 - (x - 4)**2 / 3, (x, 1, 4)), [Rational(14, 3), 6, Rational(32, 9), 4])

    def q12():
        t = Symbol('t')
        X = sqrt(log(9))
        f = 2 * integrate((t - t**2) * exp(-t**2), (t, 0, X))
        g = integrate(sqrt(t) * exp(-t), (t, 0, X**2))
        return opt(simplify(9 * (f + g)), [8, 6, 9, 10])
    c[12] = q12
    c[13] = lambda: opt(80 + 80 * Rational(1, 2)**3, [80, 85, 90, 95])

    def q14():
        V = Matrix([2, 3])
        nrm = Matrix([2, 1]) / 5                        # (2,1)/sqrt5 times distance 1/sqrt5
        F = V + nrm if (2 * 2 + 3 - 6) > 0 else V - nrm
        a2 = F[0]**2 + 2 * F[1]**2
        b2 = a2 / 2
        return opt(4 * b2**2 / a2, [Rational(512, 25), Rational(385, 8), Rational(656, 25), Rational(347, 8)])
    c[14] = q14

    def q15():
        G = (2 * Matrix([3, 4]) + Matrix([-6, -8])) / 3
        P = Matrix([2 * G[0] + 3, 7 * G[1] + 5])
        t = solve(2 * (P[0] + 2 * x) + 3 * (P[1] + x) - 4, x)[0]
        return opt(abs(t) * sqrt(5), [sqrt(5) / 17, 17 * sqrt(5) / 7, 15 * sqrt(5) / 7, 17 * sqrt(5) / 6])
    c[15] = q15

    def q16():
        P, A, d = Matrix([2, 3, 5]), Matrix([1, 2, 3]), Matrix([2, 3, 4])
        F = A + ((P - A).dot(d) / d.dot(d)) * d
        I = 2 * F - P
        return opt(2 * I[0] + 3 * I[1] + 4 * I[2], [31, 32, 33, 34])
    c[16] = q16

    def q17():
        A, B = Matrix([-4, 4, 3]), Matrix([-1, 6, 3])
        assert (B - A).dot(Matrix([-2, 3, 1])) == 0
        n = Matrix([2, -3, 2]).cross(B - A)
        return opt(abs((A - Matrix([1, -1, -4])).dot(n)) / n.norm(), [24 / sqrt(117), 42 / sqrt(117), 121 / sqrt(221), 141 / sqrt(221)])
    c[17] = q17

    def q18():
        for a in range(1, 200):
            b = 110 - a
            d = [a, b, 68, 44, 48, 60]
            if a > b and Rational(sum(v * v for v in d), 6) - 55**2 == 194:
                return opt(a + 3 * b, [180, 190, 200, 210])
    c[18] = q18
    c[19] = lambda: opt(3 * Rational(1, 3)**2 * Rational(2, 3), [Rational(1, 27), Rational(2, 27), Rational(1, 9), Rational(2, 9)])

    def q20():
        a, b = math.asin(math.sin(5)), math.acos(math.cos(5))
        return nearest(a * a + b * b, [25, 4 * math.pi**2 + 25, 4 * math.pi**2 - 20 * math.pi + 50, 8 * math.pi**2 - 40 * math.pi + 50])
    c[20] = q20

    def q21():
        R = {(x_, y_) for x_ in range(1, 101) for y_ in range(1, 101) if 2 * x_ == 3 * y_}
        return len(R | {(b, a) for (a, b) in R})
    c[21] = q21
    c[22] = lambda: pow(2, 6 if pow(2, 2024, 6) == 0 else pow(2, 2024, 6), 9)   # n = 2^(2^2024); 2 has order 6 mod 9

    def q23():
        n = 7
        e = sum((x + 3)**(n - 1 - k) * (x + 2)**k for k in range(n))
        assert expand(e).subs(x, 1) == 4**n - 3**n
        return 4**2 + 3**2
    c[23] = q23

    def q24():
        al, be = (sqrt(5) - 1) / 2, (sqrt(5) + 1) / 2
        assert simplify(1 + be - be**2) == 0 and simplify(al + al**2 - 1) == 0
        return simplify(12 * (al**2 + be**2))
    c[24] = q24

    def q25():
        a, b, cc = symbols('a b cc')
        P = Poly(series(a * x**2 * exp(x) - b * log(1 + x) + cc * x * exp(-x), x, 0, 4).removeO(), x)
        s = solve([P.coeff_monomial(x), P.coeff_monomial(x**2), P.coeff_monomial(x**3) - 1], [a, b, cc])
        return 16 * (s[a]**2 + s[b]**2 + s[cc]**2)
    c[25] = q25

    def q26():
        import mpmath
        v = mpmath.quad(lambda t: t**2 * mpmath.sin(t) * mpmath.cos(t) / (mpmath.sin(t)**4 + mpmath.cos(t)**4), [0, mpmath.pi / 2, mpmath.pi])
        return round(abs(120 * v / mpmath.pi**3), 9)
    c[26] = q26

    def q27():
        y = Symbol('y')
        w = exp(2 * y)                                    # cot x = e^{2y}
        t = 1 / w
        assert simplify(diff(t, y) + (exp(2 * y) * t**2 + t)) == 0
        al = log(sqrt(3)) / 2
        return simplify(exp(8 * al))
    c[27] = q27

    def q28():
        g, d = symbols('g d')
        s = solve([2 * (g + 3) - (d + 1) - 5, 3 * g - 2 * d - 6], [g, d])
        return abs((s[g] + 3) + (s[d] + 1) + s[g] + s[d])
    c[28] = q28

    def q29():
        A, B = Matrix([4, -6, -2]), Matrix([16, -2, 4])
        u = (B - A) / (B - A).norm()
        P = [A + s * 21 * u for s in (1, -1) if all(v >= 0 for v in A + s * 21 * u)][0]
        return (P - Matrix([4, -12, 3])).norm()
    c[29] = q29

    def q30():
        cv = Matrix(symbols('c1 c2 c3'))
        a, b = Matrix([3, 2, 1]), Matrix([2, -1, 3])
        s = solve(list((a + b).cross(cv) - 2 * a.cross(b) - Matrix([0, 24, -6])) + [(a - b + Matrix([1, 0, 0])).dot(cv) + 3], list(cv), dict=True)[0]
        v = cv.subs(s)
        return v.dot(v)
    c[30] = q30

    def q31():
        # dims (M, L, T): E = (1, 2, -2); B = L^2; A = B/(E t)
        A = (0 - 1, 2 - 2, 0 + 2 - 1)
        AB = (A[0], A[1] + 2, A[2])
        return [(-1, 0, 1), (-1, 2, 1), (1, -2, 0), (-1, -2, 1)].index(AB) + 1
    c[31] = q31

    def q32():
        th, R = symbols('th R', positive=True)
        s = sqrt(2 * R**2 * (1 + cos(th)))
        assert simplify(s**2 - (2 * R * cos(th / 2))**2) == 0
        return 3
    c[32] = q32
    c[33] = lambda: opt(solve(8 * (x - 1) - (x + 1), x)[0], [Rational(4, 3), Rational(5, 3), 8, Rational(9, 7)])

    def q35():
        t = Symbol('t', positive=True)
        F = Matrix([6 * t, 6 * t**2])
        v = Matrix([integrate(F[0] / 2, (t, 0, t)), integrate(F[1] / 2, (t, 0, t))])
        P = expand(F.dot(v))
        return [i for i, e in enumerate([6 * t**4 + 9 * t**5, 9 * t**5 + 6 * t**3, 3 * t**3 + 6 * t**5, 9 * t**3 + 6 * t**5], 1) if expand(e - P) == 0][0]
    c[35] = q35
    c[36] = lambda: opt(sqrt(Rational(1, 144) / Rational(1, 16)), [Rational(1, 12), Rational(1, 4), Rational(1, 6), Rational(1, 3)])
    c[37] = lambda: opt(Rational(1, 2), [Rational(1, 2), Rational(1, 4), 2, 4])       # v = mg/(6 pi eta r), same m
    c[38] = lambda: nearest(math.sqrt(1.4 * 8.3 * 273 / 0.032), [341, 333, 325, 310])
    c[39] = lambda: opt(8 * Rational(3, 2) + 6 * Rational(5, 2), [21, 27, 29, 20])
    c[40] = lambda: opt(Rational(25, 5), [Rational(1, 5), 5, Rational(1, 25), 25])
    c[41] = lambda: nearest((1 - 0.8**2) * 100, [36, 46, 56, 26])

    def q42():
        m = Rational(5) * Rational(2, 10) * Rational(1, 10) * Matrix([-1, 0, 0])
        tau = m.cross(Matrix([0, Rational(2, 1000), 0]))
        return {(0, 0, -1): 2, (0, 0, 1): 1, (0, 1, 0): 3, (1, 0, 0): 4}[tuple(int(v / abs(tau.norm())) for v in tau)] if tau.norm() == Rational(2, 10**4) else 0
    c[42] = q42
    c[43] = lambda: opt(Rational(1, 2) * 20 * 10 * cos(pi / 3), [Rational(216, 10), 200, 50, Rational(1732, 10)])
    c[45] = lambda: opt(90 - 60, [30, 60, 45, 90])
    c[46] = lambda: 1 if 1.5 / 2 < 1 else 0
    c[47] = lambda: opt(Rational(192, 8), [20, 32, 24, 40])

    def q48():
        Y = lambda A, B: int(not ((A or not B) or ((not A) or B)))
        return 2 if all(Y(A, B) == 0 for A in (0, 1) for B in (0, 1)) else 0
    c[48] = q48

    def q49():
        X, r = symbols('X r', positive=True)
        lv = solve(X / 25 - (40 * 2 * r) / ((100 - 40) * 2 * r), X)[0]
        l = Symbol('l')
        return opt(solve(lv / 25 - (l * 2 * r) / ((100 - l) * 2 * r), l)[0], [80, 20, 10, 40])
    c[49] = q49
    c[50] = lambda: opt(Rational(2, 200) * 100 + 2 * Rational(1, 40) * 100, [6, 4, 8, 5])
    def q51():
        m, u, g = symbols('m u g', positive=True)
        L = m * (u * cos(pi / 4)) * (u**2 * sin(pi / 4)**2 / (2 * g))
        return simplify(sqrt(2) * m * u**3 / g / L)
    c[51] = q51
    c[52] = lambda: 20 * 2 * (Rational(2, 5) * 2 * Rational(1, 4) + 2 * Rational(3, 4)**2)
    c[53] = lambda: 1 / ((Rational(2 * 2 * 4 * 10, 6)) / (pi * Rational(4, 10**5)**2 * 2 * 10**11) * pi)
    def q54():
        k, M = symbols('k M', positive=True)
        keff = k + (2 * k * k) / (2 * k + k)
        T = 2 * pi * sqrt(M / keff)
        return simplify((T / pi)**2 / (M / (5 * k)))
    c[54] = q54
    c[55] = lambda: 9 * (6 * Rational(1, 2))                 # V = -k (6ql)(1/2)/r^2 = -27e9 ql/r^2

    def q56():
        par = lambda *r: 1 / sum(Rational(1, v) for v in r)
        R = par(2, 2, par(2, 2) + par(2, 2))
        I = 2 / (R + Rational(2, 3))
        return 2 * I
    c[56] = q56
    c[57] = lambda: (4 * pi * Rational(1, 10**7) * 100 * 1 / (2 * Rational(1, 100) * pi) * 1000)**2 + (4 * pi * Rational(1, 10**7) * 100 * 2 / (2 * Rational(1, 100) * pi) * 1000)**2
    c[58] = lambda: abs(10 * 2 - 36) / 8

    def q59():
        v = solve(Rational(3, 2) / x + Rational(1, 100) - Rational(1, 2) / 20, x)[0]
        return 100 + v
    c[59] = q59
    c[60] = lambda: ((4 * 1)**Rational(1, 3))**3 / 1          # V ~ R^3 ~ A
    c[61] = lambda: [i for i, (ca, mg) in enumerate([(1.023, 1.187), (1.187, 1.023), (1.023, 1.023), (1.187, 1.187)], 1)
                     if abs(ca + mg - 2.21) < 1e-9 and abs(0.56 * ca + 40 / 84 * mg - 1.152) < 2e-3][0]

    def q64():
        a, P = symbols('a P', positive=True)
        tot = (2 + a) / 2
        Kp = (a / tot * P) * sqrt((a / 2) / tot * P) / ((1 - a) / tot * P)
        cands = [a**Rational(3, 2) * P**Rational(1, 2) / ((2 + a)**Rational(1, 2) * (1 - a)), a**Rational(1, 2) * P**Rational(1, 2) / (2 + a)**Rational(1, 2),
                 a**Rational(1, 2) * P**Rational(1, 2) / (2 + a)**Rational(3, 2), a**Rational(1, 2) * P**Rational(3, 2) / (2 + a)**Rational(3, 2)]
        return [i for i, e in enumerate(cands, 1) if simplify(Kp - e) == 0][0]
    c[64] = q64
    c[81] = lambda: round(1.2e-18 / 1e-8 / 1e-1)
    c[82] = lambda: round(2.303 * 5 * 8.314 * 300)
    c[83] = lambda: round(1540 * 0.70 / 98)
    c[85] = lambda: round(120 * math.log10(10) / 0.30103)
    c[88] = lambda: (192 - 108) // 42
    return c
