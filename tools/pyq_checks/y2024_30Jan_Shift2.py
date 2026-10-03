"""Answer checks for JEE Main 2024 (Session 1), 30 Jan Shift 2. Q5 was dropped by NTA."""
from pyq_checks.common import *
from sympy import Abs, Function


def checks():
    c = {}

    def q1():
        ok = []
        for k in range(-3000, 5001):
            v = k / 1000
            den = 4 * v * v + v - 3
            if v == -2 or den == 0: continue
            if (2 * v + 3) / den > 0 and -1 <= (2 * v - 1) / (v + 2) <= 1:
                ok.append(v)
        al, be = min(ok), max(ok)
        assert abs(al - 0.75) < 2e-3 and be == 3
        return opt(5 * 3 - 4 * Rational(3, 4), [9, 10, 11, 12])
    c[1] = q1

    def q2():
        assert factor(x**3 + 2 * x**2 + 2 * x + 1) == (x + 1) * (x**2 + x + 1)
        w = (-1 + sqrt(3) * sympy_I) / 2
        roots = [-1, w, w**2]                      # use w^3 = 1 to reduce the big powers exactly
        def val(r, n):
            return (-1)**n if r == -1 else r**(n % 3)
        hits = sum(1 for r in roots if simplify(expand(val(r, 1985) + val(r, 100) + 1)) == 0)
        return opt(hits, [0, 1, 2, 3])
    c[2] = q2

    def q3():
        th = Symbol('th')
        for tv in (0.3, 1.1, 2.0, 4.0):
            k = 1.0
            xs = [k / math.sin(tv + j * 2 * math.pi / 3) for j in range(3)]
            assert abs(sum(xs)) > 1e-6                       # trace R != 0: I false
            assert abs(xs[0] * xs[1] * xs[2] * sum(xs)) > 1e-6   # trace(adj adj R) = det(R) trace(R) never 0: II vacuous
        return 2
    c[3] = q3

    def q4():
        l, m = symbols('l m')
        A = Matrix([[1, 1, 1], [1, 2, l**2], [1, 3, l]])
        roots = solve(A.det(), l)
        assert set(roots) == {1, Rational(-1, 2)}
        Aa = A.subs(l, Rational(-1, 2))
        assert Aa.rank() == 2                               # lambda = -1/2 also fails 'unique'
        return 3
    c[4] = q4
    c[6] = lambda: opt(1 + 4 * 5, [21, 20, 24, 25])          # (p - 1)/4 = 5

    def q7():
        Y = Symbol('Y', positive=True)
        assert simplify((x / Y)**2024 - x**2024 / Y**2024) == 0          # f(x) = x^2024 fits, with f'(1) = 2024
        e = x * diff(x**2024, x) - 2024 * x**2024
        return 1 if simplify(e) == 0 else 0
    c[7] = q7

    def q8():
        a, b = symbols('a b')
        s = solve([1 + 3 + a - (b + 2), 2 + 3 - b], [a, b])
        I = integrate(x**2 + 3 * x + s[a], (x, -2, 1)) + integrate(s[b] * x + 2, (x, 1, 2))
        return opt(I, [Rational(15, 6), Rational(19, 6), 17, 21])
    c[8] = q8

    def q9():
        f = (x + 3)**2 * (x - 2)**3
        pts = [-4, 4] + [r for r in solve(diff(f, x), x) if -4 <= r <= 4]
        vals = [f.subs(x, p) for p in pts]
        return opt(max(vals) - min(vals), [600, 392, 608, 108])
    c[9] = q9

    def q10():
        a, b, cc = symbols('a b cc')
        f = a * exp(2 * x) + b * exp(x) + cc * x
        s = solve([f.subs(x, 0) + 1, diff(f, x).subs(x, log(2)) - 21,
                   integrate(a * exp(2 * x) + b * exp(x), (x, 0, log(4))) - Rational(39, 2)], [a, b, cc])
        return opt(abs(s[a] + s[b] + s[cc]), [8, 10, 12, 16])
    c[10] = q10

    def q11():
        k = Symbol('k')
        A, B = symbols('A B')
        e = expand(3 * (sin(A) * cos(B) + cos(A) * sin(B)) - 2 * (sin(A) * cos(B) - cos(A) * sin(B)))
        # sin A cos B (1) + cos A sin B (5) = 0  ->  tan A = -5 tan B
        return opt(-e.coeff(cos(A) * sin(B)) / e.coeff(sin(A) * cos(B)), [Rational(2, 3), Rational(-2, 3), -5, 5])
    c[11] = q11

    def q12():
        p = Symbol('p')
        F = p**3 / 3 + p
        v = 27 * (F.subs(p, 1) - F.subs(p, 1 / sqrt(3)))
        v = expand(simplify(v))
        al, be = v.coeff(sqrt(3), 0), v.coeff(sqrt(3), 1)
        assert simplify(al + be * sqrt(3) - v) == 0
        return opt(al + be, [26, 36, -14, -16])
    c[12] = q12

    def q13():
        u = 1 + 4 * x**4
        v = integrate(x**3 / u**Rational(1, 4), (x, 0, sqrt(2 * sqrt(5))))
        return opt(simplify(18 * v), [33, 42, 36, 39])
    c[13] = q13

    def q14():
        A, B = Matrix([10, 0]), Matrix([0, Rational(50, 7)])
        P = (3 * A + 7 * B) / 10
        ae = P[0]
        a2 = ae * Rational(25, 3)
        b2 = a2 - ae**2
        return opt(2 * b2 / sqrt(a2), [Rational(25, 3), Rational(25, 9), Rational(32, 5), Rational(32, 9)])
    c[14] = q14

    def q15():
        y = 2 * 2 * sqrt(13) / (2 * sqrt(13))
        x2 = 9 * (1 + y**2 / 4)
        return opt(x2 + y**2, [18, 20, 22, 26])
    c[15] = q15

    def q16():
        X, Y = symbols('X Y')
        e = expand(-((X + 2 * Y + 7)**2 - (2 * X - Y + 8)**2) / 3)
        P = Poly(e, X, Y)
        assert P.coeff_monomial(X**2) == 1 and P.coeff_monomial(Y**2) == -1
        h, g, f, cc = P.coeff_monomial(X * Y) / 2, P.coeff_monomial(X) / 2, P.coeff_monomial(Y) / 2, P.coeff_monomial(1)
        return opt(g + cc + h - f, [6, 8, 14, 29])
    c[16] = q16

    def q17():
        p = solve(Matrix([1, -1, 2]).dot(Matrix([3, 1, Symbol('p')])), Symbol('p'))[0]
        d = Matrix([1, -1, 2]).cross(Matrix([3, 1, p]))
        cands = [Matrix([1, 7, -4]), Matrix([-1, 7, 4]), Matrix([1, -7, 4]), Matrix([-1, -7, 4])]
        return [i for i, v in enumerate(cands, 1) if v.cross(d) == Matrix([0, 0, 0])][0]
    c[17] = q17

    def q18():
        b = Matrix([1, 0, 0]); a = Matrix([0, 2, 0])         # |b| = 1, |b x a| = 2
        assert b.cross(a).norm() == 2
        return opt((b.cross(a) - b).norm()**2, [1, 3, 4, 5])
    c[18] = q18

    def q19():
        bn = sqrt(6)
        an = 3 * sqrt(2) / (bn * cos(pi / 4))
        ab2 = an**2 - 1
        return opt(simplify(ab2 * an**2 * bn**2 * sin(pi / 4)**2), [75, 90, 85, 95])
    c[19] = q19
    c[20] = lambda: opt(Rational(3, 10) / (Rational(3, 10) + Rational(3, 5)), [Rational(1, 4), Rational(1, 3), Rational(1, 9), Rational(3, 10)])

    def q21():
        from itertools import combinations
        S = range(1, 5)
        offd = list(combinations(S, 2))
        sym = 2**(4 + len(offd)); refl_sym = 2**len(offd)
        return sym - refl_sym
    c[21] = q21

    def q22():
        g = lambda t: t * (t * t + 3 * abs(t) + 5 * abs(t - 1) + 6 * abs(t - 2))
        roots = set()
        xs = [k / 1000 for k in range(-10000, 10001)]
        for a, b in zip(xs, xs[1:]):
            if g(a) == 0: roots.add(a)
            elif g(a) * g(b) < 0: roots.add(round((a + b) / 2, 2))
        return len(roots)
    c[22] = q22

    def q23():
        tot = 0
        for a in range(4, 9):
            for b in range(4, 7):
                cc = 15 - a - b
                if 4 <= cc <= 6:
                    tot += math.comb(8, a) * math.comb(6, b) * math.comb(6, cc)
        return tot
    c[23] = q23

    def q24():
        for n in range(1, 40):
            al = sum(Rational(math.comb(n, k)**2, k + 1) for k in range(n + 1))
            be = sum(Rational(math.comb(n, k) * math.comb(n, k + 1), k + 2) for k in range(n))
            if 5 * al == 6 * be:
                return n
    c[24] = q24

    def q25():
        S = lambda k: sum(3 + 4 * j for j in range(k))
        return [n for n in range(1, 50) if 40 < Rational(6, n * (n + 1)) * sum(S(k) for k in range(1, n + 1)) < 42][0]
    c[25] = q25

    def q26():
        y = Symbol('y')
        return integrate((y - 2)**2 + 1, (y, 0, 2)) + integrate((y - 2)**2 + 1 - (2 * y - 4), (y, 2, 3))
    c[26] = q26

    def q27():
        Y = x**2 * (Rational(2, 3) / x**3 + Rational(1, 3))
        p = diff(Y, x)
        area = Rational(1, 2) * (x - Y / p) * (Y - x * p)
        assert simplify(area - (-Y**2 / (2 * p) + 1)) == 0 and Y.subs(x, 1) == 1
        return 12 * Y.subs(x, 2)
    c[27] = q27

    def q28():
        cs = Rational(1, 8)
        al = sqrt(25 + 16 - 40 * cs)
        area = Rational(1, 2) * 5 * 4 * sqrt(63) / 8
        be = 2 * (2 * area / al)
        return simplify((al * be)**2)
    c[28] = q28

    def q29():
        s, t, k = symbols('s t k')
        P = Matrix([-1, 2, 3])
        M = Matrix([1 + 3 * s, 2 + 2 * s, -1 - 2 * s]); N = Matrix([-2 - 3 * t, 2 - 2 * t, 1 + 4 * t])
        sol = solve(list(M - P - k * (N - P)), [s, t, k], dict=True)[0]
        return (sum(M.subs(sol)))**2 / (sum(N.subs(sol)))**2
    c[29] = q29

    def q30():
        xs = [0, 1, 5, 6, 10, 12, 17]; fs = [3, 2, 3, 2, 6, 3, 3]
        N = sum(fs); m = Rational(sum(a * b for a, b in zip(xs, fs)), N)
        v = Rational(sum(f * a * a for a, f in zip(xs, fs)), N) - m**2
        return round(v)
    c[30] = q30

    def q31():
        P = Symbol('P')
        # dims (M, L, T): c = (0,1,-1), G = (-1,3,-2), h = (1,2,-1); m = (1,0,0)
        L = P * 1 - Rational(1, 2) * 3 + Rational(1, 2) * 2
        T = -P + Rational(1, 2) * 2 - Rational(1, 2)
        Mx = Rational(1, 2) + Rational(1, 2)
        sol = solve([L, T], P)
        assert Mx == 1
        return opt(sol[P], [Rational(1, 3), 2, Rational(-1, 3), Rational(1, 2)])
    c[31] = q31
    def q32():
        r = cos(pi / 3) / cos(pi / 4)                 # vA/vB from equal vertical components
        cands = [Rational(1, 2), 1 / sqrt(2), sqrt(2), 1 / sqrt(3)]
        return [i for i, v in enumerate(cands, 1) if simplify(v - r) == 0][0]
    c[32] = q32
    c[33] = lambda: [i for i, v in enumerate([(40, 64), (60, 80), (88, 96), (80, 100)], 1) if v == (5 * 8, 8 * 8)][0]
    c[34] = lambda: opt(Rational(1, 2)**2 * 4 / 4, [Rational(1, 4), Rational(1, 6), Rational(1, 2), Rational(1, 3)])   # x = 2mu = 1, y = x^2/4
    c[35] = lambda: nearest(0.1 * 1 * 10 * 0.5 * 10, [5 * math.sqrt(3), 5, 5e3, 10])
    c[36] = lambda: nearest(11.2 * math.sqrt((1 / 6) / (1 / 3)), [4.2, 7.9, 8.4, 11.2])
    c[39] = lambda: nearest((3 * 2.5 + 2 * 3.5) / (3 * 1.5 + 2 * 2.5), [1.40, 1.52, 1.75, 1.35])
    def q40():
        m, k, lam, q, r, v = symbols('m k lam q r v', positive=True)
        vv = solve(m * v**2 / r - q * 2 * k * lam / r, v)[0]
        T = 2 * pi * r / vv
        cands = [2 * pi * r * sqrt(m / (2 * k * lam * q)), sqrt(4 * pi**2 * m / (2 * k * lam * q) * r**3),
                 sqrt(2 * k * lam * q / m) / (2 * pi), sqrt(m / (2 * k * lam * q)) / (2 * pi * r)]
        return [i for i, e in enumerate(cands, 1) if simplify(e - T) == 0][0]
    c[40] = q40
    c[41] = lambda: opt(4, [2, Rational(1, 2), 4, Rational(1, 4)])
    c[43] = lambda: nearest((math.pi / 2 - math.pi / 6) / (100 * math.pi) * 1000, [3.3, 2.2, 7.2, 5])
    c[44] = lambda: nearest(6.48e5 / 3e8 * 1e3, [2.16, 4.32, 1.58, 2.46])
    c[45] = lambda: opt(Rational(1, 2) * Rational(1, 2), [1, Rational(1, 2), Rational(1, 4), Rational(1, 8)])
    def q47():
        M, dM, cc, v = symbols('M dM cc v', positive=True)
        vv = solve(3 * Rational(1, 2) * (M / 3) * v**2 - dM * cc**2, v)[0]
        cands = [dM * cc**2 / 3, cc * sqrt(2 * dM / M), cc * sqrt(3 * dM / M), sqrt(2 * cc * dM / M)]
        return [i for i, e in enumerate(cands, 1) if simplify(e - vv) == 0][0]
    c[47] = q47
    c[49] = lambda: nearest((15 - 0.3 - 0.7) / 4000 * 2500, [8.5, 8.75, 9.0, 14.0])
    c[50] = lambda: nearest((1 - 49 / 50) * 0.5, [0.1, 0.1, 0.01, 1.0])       # in mm: 0.1 mm, 0.01 cm, 0.01 mm, 0.1 cm
    c[51] = lambda: (5 * Matrix([4, 3]) / 5)[0]
    c[52] = lambda: (Rational(1, 2) * 4 * 100 + Rational(1, 2) * 2 * 16) - Rational(1, 2) * 6 * Rational(48, 6)**2
    c[53] = lambda: Rational(1000, 1) / 10**2
    c[54] = lambda: Rational(16, 2**2) - Rational(16, 4**2)
    c[55] = lambda: 1 / (1 - Rational(7, 14))
    c[56] = lambda: 1 / (Rational(3, 200) - Rational(1, 100))
    c[57] = lambda: round(4 * (1e-7 * 5 / 0.5) * 2 * math.sin(math.pi / 4) / (math.sqrt(2) * 1e-7))
    c[58] = lambda: Rational(9, 10) * 2300 * 5 / 230
    c[59] = lambda: sqrt(20 * 20)
    c[60] = lambda: round(2 * math.pi * math.sqrt(4 / (math.pi**2 / 4)))
    c[81] = lambda: (6 - 2) * (6 - 2 + 1) // 2
    c[82] = lambda: 3 * (-110) - (-822)
    c[83] = lambda: round(300 / (1 + 10**(4.5 - 4.20)))
    c[85] = lambda: round((3 - 2.75) / 30 * 2 * 1000)
    return c
