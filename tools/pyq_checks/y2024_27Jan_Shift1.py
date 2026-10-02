"""Answer checks for JEE Main 2024 (Session 1), 27 Jan Shift 1."""
from pyq_checks.common import *
from sympy import Abs, Eq, Function, dsolve


def checks():
    c = {}

    def q1():
        from itertools import combinations
        U = [frozenset(s) for r in range(0, 4) for s in combinations(range(1, 4), r)]   # same pattern on a 3-element set
        R = {(A, B) for A in U for B in U if A & B}
        refl = all((A, A) in R for A in U)
        sym = all((B, A) in R for (A, B) in R)
        trans = all((A, D) in R for (A, B) in R for (B2, D) in R if B == B2)
        return {(True, True, False): 1, (True, False, True): 2, (True, False, False): 3, (False, False, True): 4}[(sym, trans, refl)]
    c[1] = q1

    def q2():
        from sympy import primefactors
        vals = [max(primefactors(n)) for n in range(2, 200)]
        one_one = len(set(vals)) == len(vals)
        onto = 4 in vals
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(one_one, onto)]
    c[2] = q2

    def q3():
        X, Y = symbols('X Y', real=True)
        z = X + sympy_I * Y
        e1 = expand(abs(z - sympy_I)**2 - abs(z + sympy_I)**2)
        e2 = expand(abs(z - sympy_I)**2 - abs(z - 1)**2)
        return opt(len(solve([e1, e2], [X, Y], dict=True)), [0, 1, 2, 3])
    c[3] = q3

    def q4():
        t, u = symbols('t u')
        f = lambda a: Matrix([[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]])
        s1 = simplify(f(-t) * f(t) - Matrix.eye(3)) == Matrix.zeros(3)
        s2 = simplify(f(t) * f(u) - f(t + u)) == Matrix.zeros(3)
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(s1, s2)]
    c[4] = q4

    def q5():
        vals = set()
        for n in range(1, 30):
            for r in range(0, n):
                vals.add(Rational(math.comb(n - 1, r), math.comb(n, r + 1)) + 8)       # = k^2
        lo, hi = min(vals), max(vals)
        assert hi == 9 and lo > 8
        return 1
    c[5] = q5

    def q6():
        n = Symbol('n', positive=True, integer=True)
        A, B = (1 - 3 + 10)**n, (1 + 1)**n
        return [i for i, e in enumerate([A - 3 * B, A - B**3, B - A**3, 3 * A - B], 1) if simplify(e) == 0][0]
    c[6] = q6
    c[7] = lambda: opt(len({4 + 5 * k for k in range(25)} & {3 * k for k in range(1, 38)}), [5, 7, 8, 9])

    def q8():
        a, b = symbols('a b')
        left = limit(a * (7 * x - 12 - x**2) / (b * Abs(x**2 - 7 * x + 12)), x, 3, '-')
        right = limit(2**(sin(x - 3) / (x - 3)), x, 3, '+')        # [x] = 3 just right of 3
        sols = solve([left - b, right - b], [a, b], dict=True)
        return opt(len(sols), [4, oo, 1, 2])
    c[8] = q8

    def q9():
        a = limit((sqrt(1 + sqrt(1 + x**4)) - sqrt(2)) / x**4, x, 0)
        b = limit(sin(x)**2 / (sqrt(2) - sqrt(1 + cos(x))), x, 0)
        return opt(simplify(a * b**3), [25, 30, 36, 32])
    c[9] = q9

    def q10():
        t = Symbol('t', real=True)
        D = (t**2 - 2)**2 + (2 * t - 8)**2
        return opt(min(D.subs(t, r) for r in solve(diff(D, t), t) if r.is_real), [16, 20, 24, 36])
    c[10] = q10

    def q11():
        v = integrate((sqrt(3 + x) - sqrt(1 + x)) / 2, (x, 0, 1))
        a, b, cc = 3, Rational(-2, 3), -1
        assert simplify(v - (a + b * sqrt(2) + cc * sqrt(3))) == 0
        return opt(2 * a + 3 * b - 4 * cc, [4, 7, 8, 10])
    c[11] = q11

    def q12():
        X, Y = symbols('X Y')
        A, B, C = Matrix([1, 2]), Matrix([2, 3]), Matrix([3, 1])
        H = Matrix([X, Y])
        s = solve([(H - A).dot(C - B), (H - B).dot(C - A)], [X, Y])
        a, b = s[X], s[Y]
        import mpmath
        I1 = mpmath.quad(lambda t: t * mpmath.sin(4 * t - t * t), [float(a), float(b)])
        I2 = mpmath.quad(lambda t: mpmath.sin(4 * t - t * t), [float(a), float(b)])
        return nearest(36 * I1 / I2, [72, 80, 88, 66])
    c[12] = q12

    def q13():
        a, b, t = symbols('a b t', positive=True)
        # x = 2e^{-at}, y = e^{-bt}; 3y(1) = 2x(1) -> e^{a-b} = 4/3
        tv = log(2) / log(Rational(4, 3))
        return nearest(float(tv), [math.log(2) / math.log(2 / 3), math.log(3) / math.log(4), math.log(2) / math.log(4 / 3), math.log(4) / math.log(3)])
    c[13] = q13

    def q14():
        k = Symbol('k')
        return opt([v for v in solve(4 * k**2 + 9 * k**2 - 2 * k - 3 * k, k) if v != 0][0], [Rational(1, 13), Rational(2, 13), Rational(3, 13), Rational(5, 13)])
    c[14] = q14

    def q15():
        P, Q = Matrix([5, 0]), Matrix([0, 4])
        T1, T2 = (2 * P + Q) / 3, (P + 2 * Q) / 3
        m1, m2 = T1[1] / T1[0], T2[1] / T2[0]
        return opt(abs((m2 - m1) / (1 + m1 * m2)), [Rational(2, 5), Rational(8, 5), Rational(25, 41), Rational(30, 41)])
    c[15] = q15

    def q16():
        Y = Symbol('Y')
        line = solve(x / 25 + Rational(2, 5) * Y / 16 - (Rational(1, 25) + Rational(4, 25) / 16), Y)[0]
        xs = solve(x**2 / 25 + line**2 / 16 - 1, x)
        p1 = Matrix([xs[0], line.subs(x, xs[0])]); p2 = Matrix([xs[1], line.subs(x, xs[1])])
        assert simplify((p1 + p2) / 2 - Matrix([1, Rational(2, 5)])) == Matrix([0, 0])
        return opt(simplify((p1 - p2).norm()), [sqrt(2009) / 5, sqrt(1741) / 5, sqrt(1691) / 5, sqrt(1541) / 5])
    c[16] = q16

    def q17():
        t, s = symbols('t s')
        sol = solve(list(Matrix([7, -2, 11]) + t * Matrix([2, -3, 6]) - Matrix([6 + s, 4, 8 + 3 * s])), [t, s], dict=True)[0]
        return opt(abs(sol[t]) * 7, [12, 14, 18, 21])
    c[17] = q17

    def q18():
        lam = Symbol('lam')
        n = Matrix([1, 2, -3]).cross(Matrix([2, 4, -5]))
        AB = Matrix([lam, -1, 2]) - Matrix([4, -1, 0])
        sols = solve((AB.dot(n))**2 / n.dot(n) - Rational(36, 5), lam)
        return opt(sum(sols), [5, 7, 8, 10])
    c[18] = q18

    def q19():
        a, b = Matrix([1, 2, 1]), 3 * Matrix([1, -1, 1])
        cv = (3 * a - a.cross(b)) / a.dot(a)
        assert a.cross(cv) == b and a.dot(cv) == 3
        return opt(a.dot(cv.cross(b) - b - cv), [20, 24, 36, 32])
    c[19] = q19
    c[20] = lambda: opt(sqrt(Rational(50**2 - 2 * 1100, 10) - 25), [5, 10, sqrt(5), sqrt(115)])

    def q21():
        w = (-1 + sqrt(3) * sympy_I) / 2
        val = expand((1 + w)**7)
        for A_ in range(0, 5):
            for B_ in range(0, 5):
                for C_ in range(0, 5):
                    if simplify(A_ + B_ * w + C_ * w**2 - val) == 0:
                        return 5 * (3 * A_ - 2 * B_ - C_)
    c[21] = q21

    def q22():
        A = Matrix([[2, 0, 1], [1, 1, 0], [1, 0, 1]])
        B = A.inv() * Matrix([[1, 2, 3], [0, 3, 2], [0, 0, 1]])
        return B.det()**3 + B.trace()**3
    c[22] = q22
    c[23] = lambda: sum(1 / (Rational(1, n * n)) + 1 for n in range(1, 21))

    def q24():
        p = Symbol('p')
        k = Symbol('k', integer=True, positive=True)
        from sympy import summation
        return solve(3 + summation((3 + k * p) / 4**k, (k, 1, oo)) - 8, p)[0]
    c[24] = q24

    def q25():
        a, b, cc = symbols('a b cc')
        f = x**3 + a * x**2 + b * x + cc
        s = solve([diff(f, x).subs(x, 1) - a, diff(f, x, 2).subs(x, 2) - b, diff(f, x, 3).subs(x, 3) - cc], [a, b, cc])
        return diff(f, x).subs(s).subs(x, 10)
    c[25] = q25

    def q26():
        y = Symbol('y')
        A = integrate(8 - 4 * y**2 + 2 * y**2, (y, 0, 1)) + integrate(8 - 4 * y**2 - (2 * y - 4), (y, 1, Rational(3, 2)))
        A = Rational(A)
        return A.p + A.q
    c[26] = q26

    def q27():
        y = Function('y')
        F = x + 2 * y(x) + 3 * log(2 * x + 3 * y(x) - 8)
        # implicit derivative of the claimed solution satisfies the ODE
        dydx = solve(diff(F, x), diff(y(x), x))[0]
        ode = (2 * x + 3 * y(x) - 2) + (4 * x + 6 * y(x) - 7) * dydx
        assert simplify(ode) == 0
        assert F.subs(y(x), 3).subs(x, 0) == 6
        return 1 + 2 * 2 + 3 * 8
    c[27] = q27

    def q28():
        for al in range(1, 50):
            u, v = Matrix([al, -2, 2]), Matrix([al, 2 * al, -2])
            if u.dot(v) > 0 and u.cross(v) != Matrix([0, 0, 0]):
                return al
    c[28] = q28

    def q29():
        p, q = Rational(1, 6), Rational(5, 6)
        a = q**2 * p
        b = q**2
        cc = q**5 / q**3
        return (b + cc) / a
    c[29] = q29

    def q30():
        a = Symbol('a')
        ok = [av for av in [k / 100 for k in range(-1000, 1001)] if -1 <= (av - 4) / 2 <= 1]
        p, q = min(ok), max(ok)
        r = math.tan(math.radians(9)) - math.tan(math.radians(27)) - 1 / (1 / math.tan(math.radians(63))) + math.tan(math.radians(81))
        return round(p * q * r, 6)
    c[30] = q30
    def q32():
        T = Symbol('T')
        v = diff(Matrix([0, 2 * T**2, 5]), T).subs(T, 1)
        return [(4, 0), (16, 1), (4, 1), (9, 2)].index((v.norm(), [i for i in range(3) if v[i] != 0][0])) + 1
    c[32] = q32
    c[33] = lambda: opt(Rational(1000 * 6, 1200), [6, 5, 3, 2])
    c[34] = lambda: nearest(1.5 * 12**2 / (400 * 10) * 100, [4.2, 4.8, 5.4, 6.0])
    c[35] = lambda: [i for i, (m, n) in enumerate([(2, 5), (5, 4), (4, 5), (3, 5)], 1) if Rational(m, n) == sqrt(Rational(4, 25))][0]
    c[36] = lambda: opt(1 / Rational(1, 2)**2, [4, Rational(1, 4), Rational(1, 2), 2])
    c[38] = lambda: nearest(0.08 * 0.17 * 5 * 1000 * 4.18, [142, 284, 298, 318])
    c[39] = lambda: nearest(2 * 0.414 * 1.6e-19 / (3 * 1.38e-23), [1500, 1600, 3000, 3200])
    c[40] = lambda: opt(Rational(1, 10**12) * 9 * 10**9 * (1 / sqrt(3 + 3) - 1 / sqrt(6 + 0)), [sqrt(6), sqrt(3), 0, 3])
    c[41] = lambda: opt(Rational(1, 5) / 5, [Rational(1, 5), Rational(1, 25), 5, 25])
    c[43] = lambda: opt(-(0 - 4 * Rational(5) * Rational(1, 2)) / 10, [-1, 1, -2, 2])
    c[44] = lambda: nearest(0.5 * 8.85e-12 * (1.5e7 / 0.05) * 200**2, [53.1, 106.2, 26.6, 35.4])

    def q45():
        A = Symbol('A', positive=True)
        for Av in (0.5, 0.7, 0.9):                  # check the formula numerically for several prism angles
            mu = 1 / math.tan(Av / 2)
            if mu * math.sin(Av / 2) > 1: continue
            dm = 2 * math.asin(mu * math.sin(Av / 2)) - Av
            assert abs(dm - (math.pi - 2 * Av)) < 1e-12
        return 1
    c[45] = q45
    c[47] = lambda: opt(Rational(16, 9), [Rational(9, 16), Rational(16, 9), Rational(4, 3), Rational(3, 4)])
    c[50] = lambda: nearest(4.5 * 40 / 60 * (22 / 7) * 7e-8 / 0.1 / 1e-7, [35, 63, 66, 70])

    def q51():
        t = [v for v in solve(5 * x + Rational(3, 2) * x**2 - 84, x) if v > 0][0]
        return (5 + 3 * t)**2 + (2 * t)**2
    c[51] = q51
    c[52] = lambda: 1 * (0 + 4 + 4 + 8)
    c[53] = lambda: Rational(1000 * 10 * 4000, 2 * 10**9) * 100
    c[54] = lambda: 16 - (5 / Rational(10, 4))**2
    c[55] = lambda: Rational(9 * 10**9) * Rational(30, 10**12) * 2 * pi / (2 * pi * Rational(3, 10)**2)
    c[56] = lambda: 150 * ((10 - Rational(10, 3)) - (10 - Rational(10 * 6, 10)))
    c[57] = lambda: 2 * (2 * Rational(1, 10**7) * 10 / Rational(25, 1000)) * 10**6
    c[58] = lambda: pi / (Rational(2, 1000) * 5 * 50 * pi)
    c[59] = lambda: 4 * (6 / Rational(8, 5) + 6 / Rational(3, 2))
    c[60] = lambda: round(236 * (8.6 - 7.6))
    c[81] = lambda: Rational(22, 44) * 16
    c[82] = lambda: (2 + 6 + 10 + 14) // 2
    c[83] = lambda: Rational(10 - 4, 2) + Rational(10 - 4, 2)          # CO and NO+ are both 14-electron species
    c[84] = lambda: 80 * 10**3 * (45 - 30) * Rational(1, 1000)

    def q85():
        ox = {'SO3': 6, 'H2SO3': (2 * 3 - 2) // 1, 'SOCl2': 2 + 2, 'SF4': 4, 'BaSO4': 8 - 2, 'H2S2O7': (14 - 2) // 2}
        return sum(1 for v in ox.values() if v == 4)
    c[85] = q85
    c[86] = lambda: Rational(5600, 22400) * 4 * 108
    c[87] = lambda: round(math.log(3.0e-3 / 7.5e-4) / math.log(2))
    return c
