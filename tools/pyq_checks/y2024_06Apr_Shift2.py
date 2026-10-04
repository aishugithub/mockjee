"""Answer checks for JEE Main 2024 (Session 2), 6 Apr Shift 2. Q27 was dropped by NTA."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, Abs


def checks():
    c = {}
    c[1] = lambda: [i for i, (a, b) in enumerate([(Rational(1, 8), Rational(1, 5)), (Rational(1, 7), Rational(1, 5)), (Rational(1, 7), Rational(1, 6)), (Rational(1, 8), Rational(1, 6))], 1) if (a, b) == (Rational(1, 8), Rational(1, 6))][0]

    def q2():
        A = range(1, 6)
        R = {(a, b) for a in A for b in A if 4 * a <= 5 * b}
        return opt(len(R) + len({(b, a) for a, b in R} - R), [23, 24, 25, 26])
    c[2] = q2

    def q3():
        import random
        random.seed(1)
        ok = [0, 0]
        for _ in range(200):
            z2 = complex(random.uniform(-2, 2), random.uniform(-2, 2))
            t = random.uniform(0, 6.28)
            z1 = complex(math.cos(t), math.sin(t))                 # |z1| = 1 should always work
            ok[0] += abs(abs(z1 - 2 * z2) / abs(0.5 - z1 * z2.conjugate()) - 2) < 1e-9
            z1 = complex(random.uniform(-2, 2), random.uniform(-2, 2))
            z2 = 0.5 * complex(math.cos(t), math.sin(t))           # |z2| = 1/2 should always work
            ok[1] += abs(abs(z1 - 2 * z2) / abs(0.5 - z1 * z2.conjugate()) - 2) < 1e-9
        return 4 if ok == [200, 200] else 0
    c[3] = q3

    def q4():
        d = Rational(1, 8 * 3)                    # det((2A)^-1)
        d = d**2; d = 27 * d; d = d**2; d = -27 * d; d = d**2; d = -64 * d; d = d**2
        m = -int(math.log2(d.q)); n = int(round(math.log(d.p, 3)))
        assert d == Rational(3**n, 2**(-m))
        return opt(m + 2 * n, [2, 4, 3, 6])
    c[4] = q4

    def q5():
        from itertools import permutations
        words = sorted(''.join(p) for p in permutations('NAGPUR'))
        return [i for i, w in enumerate(['NRAGPU', 'NRAPGU', 'NRAGUP', 'NRAPUG'], 1) if w == words[314]][0]
    c[5] = q5

    def q6():
        for n in range(1, 40):
            for r in range(1, n + 1):
                a, b, cc = math.comb(n + 1, r + 1), math.comb(n, r), math.comb(n - 1, r - 1)
                if a * 35 == b * 55 and b * 21 == cc * 35:
                    return opt(2 * n + 5 * r, [50, 55, 60, 62])
    c[6] = q6
    c[7] = lambda: opt([m for m in range(1, 400) if sum(m - 4 * k for k in range(25)) == 17 * m][0], [150, 125, 160, 180])

    def q8():
        e, p = math.e, math.pi
        truth = [e**p > p**e, e**p < p**e, e**(2 * p) < (2 * p)**e, (2 * e)**p > p**(2 * e)]
        assert truth.count(True) == 1
        return truth.index(True) + 1
    c[8] = q8

    def q9():
        n = 4000
        num = sum((k * k - k) * (n - k) for k in range(1, n))
        den = sum(k**3 for k in range(1, n + 1)) - sum(k * k for k in range(1, n + 1))
        return nearest(num / den, [1 / 2, 1 / 3, 2 / 3, 3 / 4])
    c[9] = q9
    c[10] = lambda: opt(2 * 1 * 1 + 1 * 1 * 2, [3, 4, 5, 8])

    def q11():
        a = Symbol('a')
        av = solve(integrate(1 / x - a / x**2, (x, 1, 2)) - (log(2) - Rational(1, 7)), a)[0]
        return opt(7 * av - 3, [-1, 0, 1, 2])
    c[11] = q11

    def q12():
        a, b = symbols('a b', positive=True)
        s = solve([a / b - 3, a * b - 12], [a, b], dict=True)[0]
        return opt(sqrt(s[a]**2 + s[b]**2), [sqrt(42), sqrt(39), sqrt(40), sqrt(41)])
    c[12] = q12

    def q13():
        al = Symbol('al')
        av = solve(2 + al - 2 * al, al)[0]            # beta = 0, coefficient match
        g, f = Rational(2, 2 + av), Rational(4 * av, -2 * av)       # (4x+2)/(-4y+8) = -(x+g)/(y+f)
        y = Symbol('y')
        assert simplify(((2 + av) * x + 2) / (-2 * av * y + 4 * av) + (x + g) / (y + f)) == 0
        return opt(sqrt(g**2 + f**2), [sqrt(17) / 2, 2, sqrt(17), Rational(1, 2)])
    c[13] = q13

    def q14():
        y = Symbol('y')
        e = expand(25 * ((x - 1)**2 + (y - 3)**2) - 16 * ((x - 2)**2 + (y - 1)**2))
        e = e * 170 / e.subs({x: 0, y: 0})
        P = Poly(e, x, y)
        a, b, cc, d, ee = P.coeff_monomial(x**2), P.coeff_monomial(y**2), P.coeff_monomial(x * y), P.coeff_monomial(x), P.coeff_monomial(y)
        return opt(a**2 + 2 * b + 3 * cc + 4 * d + ee, [5, 437, -27, 37])
    c[14] = q14

    def q15():
        h, k = symbols('h k')
        s = solve([(Matrix([1, 3])).dot(Matrix([h - 8, k - 3])), Matrix([-2, -2]).dot(Matrix([h - 5, k + 2]))], [h, k])
        v = s[h]**2 + s[k]**2
        return [i for i, r in enumerate([52, 61, 65, 74], 1) if r == v][0]
    c[15] = q15

    def q16():
        a = Symbol('a', positive=True)
        P = 3 * a / (1 - Rational(1, 2)); Q = sqrt(3) / 4 * a**2 / (1 - Rational(1, 4))
        tests = [simplify(P - 36 * sqrt(3) * Q**2), simplify(P**2 - 6 * sqrt(3) * Q), simplify(P**2 - 36 * sqrt(3) * Q), simplify(P**2 - 72 * sqrt(3) * Q)]
        return [i for i, t in enumerate(tests, 1) if t == 0][0]
    c[16] = q16

    def q17():
        A, d, Q, R = Matrix([0, 3, 1]), Matrix([1, 1, -1]), Matrix([3, -3, 1]), Matrix([2, 5, -1])
        F = A + d * (Q - A).dot(d) / d.dot(d)
        P = 2 * F - Q
        lam = (Q - P).cross(R - P).norm() / 2
        return opt(lam**2 / 14, [18, 36, 72, 81])
    c[17] = q17

    def q18():
        a, i, j = Matrix([2, 1, -1]), Matrix([1, 0, 0]), Matrix([0, 1, 0])
        b = (a.cross(i + j)).cross(i).cross(i)
        return opt((a.dot(b))**2 / b.dot(b), [Rational(1, 3), 2, Rational(2, 3), Rational(1, 5)])
    c[18] = q18

    def q19():
        r = Symbol('r', positive=True)
        rv = max(solve(r**2 + 38 - 12 * r - 8, r))
        assert rv >= 6
        ab = Matrix([6, 1, -1]).cross(Matrix([1, 1, 0])).norm()
        return opt(simplify(ab * rv * sqrt(3) / 2), [Rational(3, 2) * sqrt(3), Rational(3, 2) * sqrt(6), Rational(9, 2) * (6 - sqrt(6)), Rational(9, 2) * (6 + sqrt(6))])
    c[19] = q19
    c[20] = lambda: opt(Rational(sum(1 for t in product(range(5), repeat=3) if len(set(t)) == 2), 125), [Rational(4, 25), Rational(6, 25), Rational(12, 25), Rational(18, 25)])

    def q21():
        r = solve(x**2 + sqrt(2) * x - 8, x)
        U = lambda n: expand(r[0]**n + r[1]**n)
        return simplify((U(10) + sqrt(2) * U(9)) / (2 * U(8)))
    c[21] = q21

    def q22():
        l, m = symbols('l m')
        mv = solve(Matrix([[2, 7, 3], [3, 2, 4], [1, m, -1]]).det(), m)[0]
        lv = solve(Matrix([[2, 7, l], [3, 2, 5], [1, mv, 32]]).det(), l)[0]
        assert Matrix([[2, 7, lv, 3], [3, 2, 5, 4], [1, mv, 32, -1]]).rank() == 2
        return lv - mv
    c[22] = q22

    def q23():
        S60 = sum(k * 61**k for k in range(1, 61))
        v = 3600 * S60
        b = 61
        a, rem = divmod(v - b, b**b)
        assert rem == 0
        return a + b
    c[23] = q23

    def q24():
        f = lambda t: math.floor(t / 2 + 3 + 1e-12) - math.floor(math.sqrt(t) + 1e-12)
        cands = [1, 2, 4, 6, 8]
        bad = [p for p in cands if abs(f(p - 1e-9) - f(p)) > 0.5 or (p < 8 and abs(f(p + 1e-9) - f(p)) > 0.5)]
        return sum(bad)
    c[24] = q24

    def q25():
        I1 = sum(3 - sqrt(k) for k in range(1, 9))
        I2 = sum(3 - sqrt(2 * k) for k in range(1, 5))
        tot = nsimplify(expand(I1 + I2))
        a = tot.as_independent(sqrt(2), sqrt(3), sqrt(5), sqrt(6), sqrt(7))[0]
        b = expand(tot).coeff(sqrt(2)); cc = expand(tot).coeff(sqrt(6))
        assert expand(tot - (a + b * sqrt(2) - sqrt(3) - sqrt(5) + cc * sqrt(6) - sqrt(7))) == 0
        import mpmath
        num = mpmath.quad(lambda t: mpmath.floor(t * t) + mpmath.floor(t * t / 2), [0] + [mpmath.sqrt(k) for k in range(1, 10)])
        assert abs(num - float(tot)) < 1e-9
        return a + b + cc
    c[25] = q25

    def q26():
        y = Symbol('y')
        C = (exp(0) + 1) * sin(pi / 2)
        return solve((y + 1) * sin(pi / 6) - C, y)[0]           # y here stands for e^y
    c[26] = q26

    def q28():
        l = Symbol('l')
        n = Matrix([3, -1, 1]).cross(Matrix([-3, 2, 4]))
        d = (Matrix([-2, -5, 4]) - Matrix([l, 2, 1])).dot(n) / n.norm()
        sols = solve(d**2 - Rational(44**2, 30), l)
        return max(abs(s) for s in sols)
    c[28] = q28

    def q29():
        from fractions import Fraction as Fr
        P = {k: Fr(math.comb(3, k) * math.comb(9, 5 - k), math.comb(12, 5)) for k in range(4)}
        mu = sum(k * p for k, p in P.items()); var = sum(k * k * p for k, p in P.items()) - mu * mu
        return var.denominator - var.numerator
    c[29] = q29

    def q30():
        al = [v for v in solve((64 + x**2 - 49) / (16 * x) - Rational(2, 3), x) if v.is_integer][0]
        cC = Rational(49 + 64 - al**2, 2 * 7 * 8)
        v = 49 * (4 * cC**3 - 3 * cC) + 42
        return v.p + v.q
    c[30] = q30

    c[31] = lambda: nearest(math.sqrt(300 * 10 * (1 / 1.73 + 0.2) / (1 - 0.2 / 1.73)), [51.4, 264, 102.8, 70.4])

    def q33():
        g, u, t1, t2 = symbols('g u t1 t2', positive=True)
        h1 = -u * t1 + g * t1**2 / 2; h2 = u * t2 + g * t2**2 / 2
        uv = solve(h1 - h2, u)[0]
        h = simplify(h1.subs(u, uv))
        return opt(simplify(sqrt(2 * h / g)), [sqrt(t1 * t2), sqrt(t1 + t2), sqrt(t1 - t2), sqrt(t1 / t2)])
    c[33] = q33
    c[34] = lambda: opt(200 + 10 * 10, [200, 100, 300, 150])
    c[36] = lambda: opt((sqrt(36) - 1) * 100, [6, 500, 60, 600])
    c[37] = lambda: opt(300 * (1 - Rational(1, 4)), [75, 225, 300, 375])
    c[39] = lambda: nearest(48 - 1.5 * 8.3 * 2, [24.9, 48, 72.9, 23.1])
    c[40] = lambda: opt(Rational(10, 1) / (Rational(4, 100) / 4 * 50), [10, 20, 40, 5])   # MSD = 50 LC, LC = 0.04/4 mm
    c[41] = lambda: 4 if Rational(7, 2) * 10 == 35 else 0
    c[42] = lambda: opt(16 * Rational(1, 2) * Rational(3, 4), [6, 12, 4, 1])
    c[43] = lambda: nearest(110 / 220 / 1.6e-19, [6.25e17, 1.25e19, 31.25e17, 6.25e18])
    c[44] = lambda: opt(Rational(1, 10) * Rational(2, 10) / 4 * 1000, [1, Rational(5, 2), 4, 5])
    c[45] = lambda: nearest(0.5 * 9e-12 * 600**2 * 3e8, [729, 972, 243, 486])
    c[46] = lambda: opt(1 + Rational(1, 20) / (Rational(1, 15) + Rational(1, 30)), [Rational(14, 10), Rational(15, 10), Rational(12, 10), Rational(18, 10)])
    c[47] = lambda: nearest(1240 / 300 - 2.13, [4.1, 1.5, 2, 4])
    c[48] = lambda: nearest(144 / (7 * 1.097e7), [2.973e-6, 1.876e-6, 1.094e-6, 3.646e-6])
    c[49] = lambda: nearest(1242 / 6, [207, 407, 414, 103.5])

    def q50():
        lc = 0.05 / 50
        r1, r2, r3 = 8.45 + 26 * lc, 7.12 + 41 * lc, 4.05 + 1 * lc
        return nearest((r1 - r3) / (r2 - r3), [1.24, 1.42, 1.35, 1.52])
    c[50] = q50
    c[51] = lambda: round(6 * 333 / 1.2 - 5 * 333 / 1.8, 6)
    c[52] = lambda: round(math.sqrt(8 * 2 * 0.01 / (10e-6 * 2.5)), 6)
    c[53] = lambda: round(24 / (140.4 + 240 * 10 / 250) * 1000, 6)
    c[54] = lambda: (1 + 2)**2 - (2 - 1)**2
    c[55] = lambda: round(1245 / 10.2)
    c[56] = lambda: Rational(2 + 4 + 6, 3)

    def q57():
        t = Symbol('t', positive=True)
        X = sqrt(1 + t**2)
        a = diff(X, t, 2)
        return [n for n in range(1, 6) if simplify(a - X**(-n)) == 0][0]
    c[57] = q57
    c[58] = lambda: round(100 * 5e-3 * 1e-3 * 0.2 * 1e6, 6)
    c[59] = lambda: round(1 / (2 * math.sqrt(10 * 0.1 * 2.5e-9)) / 1e3, 6)
    c[60] = lambda: round((20 / (2 * 0.01)) / (2e11 * 0.01**2 / 2) / 1e-4, 6)
    c[61] = lambda: nearest(3 / ((1250 - 3 * 58.5) / 1000), [2.79, 3.85, 2.90, 1.90])
    c[63] = lambda: 1 if (1 - Rational(3, 2)) == Rational(-1, 2) else 0
    c[81] = lambda: round(3.4 * 10)
    c[83] = lambda: 400 / Rational(2, 10)
    c[84] = lambda: round(2.5 / 1.86 * 0.1 * 32 / 0.792 * 100)
    c[85] = lambda: round(5 / 2 * 0.477 / 0.699 * 10)
    return c
