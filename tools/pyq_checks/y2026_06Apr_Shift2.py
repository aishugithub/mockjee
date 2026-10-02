"""Answer checks for JEE Main 2026 (Session 2), 6 Apr Shift 2."""
from pyq_checks.common import *
from sympy import Eq, Function, dsolve


def checks():
    c = {}

    def q1():
        f = (2 * x**2 - 3 * x + 2) / (3 * x**2 + x + 3)
        two_roots = len([r for r in solve(f - 1, x) if r.is_real]) == 2      # not one-one
        bounded = limit(f, x, oo) == limit(f, x, -oo) == Rational(2, 3)     # continuous, bounded: not onto
        return 4 if two_roots and bounded else 0
    c[1] = q1

    def q2():
        ts = [n * n - 2 * n + 2 for n in [k / 100 for k in range(-500, 501)]]
        a, b = min(ts), max(3 / t for t in ts)
        return opt(sum(Rational(a) * Rational(1, 3)**k for k in range(6)) if (a, b) == (1, 3) else 0,
                   [Rational(61, 37), Rational(121, 81), Rational(364, 243), Rational(1093, 729)])
    c[2] = q2
    c[3] = lambda: opt(simplify(sum(r**8 for r in solve(x**2 + sqrt(6) * sympy_I * x - 3, x))), [162, 184, 262, 324])

    def q4():
        roots = set()
        for cv in solve(4 * x**3 + 4 * x**2 - 3 * x, x):
            if abs(cv) <= 1:
                a = math.acos(float(cv)); roots |= {round(a, 9), round(2 * math.pi - a, 9)}
        for r in roots:
            M = Matrix([[cos(3 * r), -8, -12], [cos(2 * r), 3, 3], [1, 1, 3]])
            assert abs(float(M.det())) < 1e-6
        return nearest(sum(roots), [math.pi, 2 * math.pi, 3 * math.pi, 4 * math.pi])
    c[4] = q4

    def q5():
        B = Matrix([[1, 0, 0], [3, 1, 0], [9, 3, 1]])**99 - Matrix.eye(3)
        return opt((B[2, 0] - B[1, 0]) / B[2, 1], [99, 199, 149, 159])
    c[5] = q5
    c[6] = lambda: opt(sum(Rational(sum(k * k for k in range(1, n + 1)), n) for n in range(1, 11)), [130, 155, Rational(315, 2), Rational(325, 2)])

    def q7():
        floors = range(3, 11)
        return opt(math.comb(9, 4) * sum(1 for a in floors for b in floors if a != b), [2184, 3064, 7056, 11340])
    c[7] = q7

    def q8():
        for a in range(1, 30):
            for b in range(a + 1, 30):
                d = [2, 4, a, 8, b, 12, 14]
                if Rational(sum(d), 7) == 8 and Rational(sum(v * v for v in d), 7) - 64 == 16:
                    s, p = 3 * a + 2 + 2 * b + 1, (3 * a + 2) * (2 * b + 1)
                    return [(35, 306), (41, 420), (45, 506), (37, 342)].index((s, p)) + 1
    c[8] = q8

    def q9():
        p = Rational(1)
        for k in range(6, 0, -1):          # k blue and k green left
            p *= Rational(k * k, math.comb(2 * k, 2))
        return opt(p, [Rational(63, 925), Rational(17, 231), Rational(16, 231), Rational(64, 925)])
    c[9] = q9

    def q10():
        r = [v for v in solve(2 * sqrt(x**2 - 9) - 6 * sqrt(3), x) if v > 0][0]
        d = abs(3 - r - 3) / sqrt(2)
        return opt(2 * sqrt(r**2 - d**2), [8, 6, 6 * sqrt(2), 8 * sqrt(2)])
    c[10] = q10

    def q11():
        e = sqrt(3) / 2
        a = 4 * sqrt(6) / 3 * e
        b2 = a**2 * (1 - e**2)
        eh = a
        A = Symbol('A', positive=True)
        Av = solve(2 * (A**2 * (eh**2 - 1)) / A - 2 * sqrt(b2), A)[0]
        return opt(simplify(2 * Av * eh), [4 * sqrt(2) / sqrt(7), 4 * sqrt(2) / 7, 4 / sqrt(7), Rational(8, 7)])
    c[11] = q11

    def q12():
        a, e = 3, Rational(1, 3)
        b2 = a**2 * (1 - e**2)
        h, k = symbols('h k')
        lhs = expand(72 * (h * 1 / 9 - h**2 / 9 - k**2 / b2))   # chord through the focus (1, 0)
        return [i for i, f in enumerate([9 * k**2 - 8 * h * (1 - h), 3 * k**2 - 4 * h * (1 - h),
                                         9 * k**2 - 8 * h * (h - 1), 3 * k**2 - 4 * h * (h - 1)], 1)
                if simplify(lhs + expand(f)) == 0][0]
    c[12] = q12

    def q13():
        f = lambda t: math.sin(math.atan(t * math.sqrt(2))) - 1 / math.tan(math.asin(math.sqrt(1 - t * t)))
        hits = [i for i, v in enumerate([0.5, 1 / 3, 2 / 3, 5 / 8], 1) if abs(f(v)) < 1e-12]
        assert len(hits) == 1
        return hits[0]
    c[13] = q13

    def q14():
        A, B = Matrix([4, 3, 2]), Matrix([-2, 6, 5])
        n = Matrix([1, 2, -3]).cross(Matrix([2, 4, -5]))
        return opt(abs((B - A).dot(n)) / n.norm(), [5 * sqrt(6) / 6, 2 * sqrt(5), 3 * sqrt(5), 4 * sqrt(5)])
    c[14] = q14

    def q15():
        a, b = Matrix([2, 3, 3]), Matrix([6, 3, 3])
        return opt(((2 * a + 3 * b).cross(a - b).norm() / 2)**2, [450, 900, 1800, 2400])
    c[15] = q15

    def q16_exact():
        p, q = symbols('p q')
        rv = 1                                      # x = 2 must be a root: 4r - 4 = 0
        pv = solve(limit(tan(x - 2) * (x**2 + (p - 2) * x - 2 * p) / (x - 2)**2, x, 2) - 5, p)[0]
        lo = solve(4 - 2 * pv + q, q)[0]            # f(2) > 0
        hi = solve(pv**2 - 4 * q, q)[0]             # D >= 0
        assert 0 < pv / 2 < 2 and lo > 0
        return opt(4 * (lo + hi), [11, 13, 17, 21])
    c[16] = q16_exact

    def q17():
        a, t = symbols('a t')
        av = solve(Matrix([[1, 3, -1], [2, 1, a], [0, 1, -1]]).det(), a)[0]
        return opt(3 * integrate(t**2 + 2 * t + 3, (t, 1, av)), [64, 68, 72, 76])
    c[17] = q17

    def q18():
        g = Function('g')
        sol = dsolve(Eq(x**2 * g(x).diff(x) + 3 * x * g(x), x**2), g(x), ics={g(1): 0})
        return opt(simplify(sol.rhs.subs(x, 2)), [Rational(13, 8), Rational(11, 16), Rational(15, 32), Rational(17, 64)])
    c[18] = q18
    c[19] = lambda: opt(integrate(-x - (x**2 - 8 * x), (x, 0, 7)), [Rational(343, 6), Rational(637, 6), Rational(437, 6), Rational(523, 6)])
    c[20] = lambda: nearest(2 * float(integrate((x + 1) / (x + 1)**2, (x, 0, 1))),
                            [3 * math.log(2), 2 * math.log(2), 5 * math.log(3), 3 * math.log(3)])

    def q21():
        U = range(1, 20)
        R = {(a, b) for a in U for b in U if math.log(a + b) <= 2}
        T = set(R)
        while True:
            new = {(a, d) for (a, b) in T for (b2, d) in T if b == b2} - T
            if not new: break
            T |= new
        return len(T - R)
    c[21] = q21

    def q22():
        lhs = expand((1 - x**3)**10)
        a = [math.comb(10, r) * 3**r for r in range(11)]
        assert expand(sum(a[r] * x**r * (1 - x)**(30 - 2 * r) for r in range(11)) - lhs) == 0
        return Rational(9 * a[9], a[10])
    c[22] = q22

    def q23():
        t = Symbol('t')
        out = set()
        for tv in solve(2 * t**2 - 9, t):
            al, be = 4 + tv, -3 - tv
            out.add(simplify((6 * al + 8 * be)**2))
        assert len(out) == 1
        return out.pop()
    c[23] = q23

    def q24():
        def image(P, A, d):
            t = (P - A).dot(d) / d.dot(d)
            return 2 * (A + t * d) - P
        P, Q = Matrix([0, -5, 0]), Matrix([0, Rational(-1, 2), 0])
        R = image(P, Matrix([1, 0, -1]), Matrix([2, 1, -2]))
        S = image(Q, Matrix([1, -9, -1]), Matrix([-1, 4, 1]))
        assert P + R == Q + S                       # diagonals bisect each other
        return ((R - P).cross(S - Q).norm() / 2)**2
    c[24] = q24

    def q25():
        f = lambda t: t**3 + 8 if t < 0 else t * t - 4
        g = lambda u: -abs(u - 8)**(1 / 3) if u < 0 else math.sqrt(u + 4)
        h = lambda t: g(f(t))
        bad = 0
        for k in range(-500, 501):
            t = k / 100
            if abs(h(t - 1e-7) - h(t)) > 1e-3 or abs(h(t + 1e-7) - h(t)) > 1e-3:
                bad += 1
        return bad
    c[25] = q25
    c[26] = lambda: opt(3 * 2, [1, 2, 6, 8])

    def q28():
        F, m = 1, 1
        acc = lambda M, k: Rational(2 * F) / (M * (1 + k))
        return opt(acc(5 * m, Rational(2, 5)) / acc(m, Rational(2, 3)), [Rational(5, 21), Rational(6, 10), Rational(21, 25), Rational(1, 5)])
    c[28] = q28
    c[29] = lambda: opt(Rational(1, 2) * 1 * (2 * 5**2)**2, [0, 250, 1250, 1000])
    c[30] = lambda: nearest(9 * (8 / 27)**(1 / 1.5), [3, 4, 14, 9])

    def q32():
        v = (Matrix([4, 0]) + Matrix([0, 4])) / 2
        a = (Matrix([6, 6]) + Matrix([0, 0])) / 2
        return 3 if v[0] * a[1] - v[1] * a[0] == 0 else 2
    c[32] = q32
    c[33] = lambda: nearest((60 / 1e-5) / (6e-4 / 1), [1e11, 2e10, 1e10, 2e11])

    def q34():
        H = Rational(528, 1000) / (Rational(22, 7) * Rational(4, 10)**2)       # m
        assert H == Rational(105, 100)
        depth, height = Rational(70, 100), H + (H - Rational(70, 100))
        return opt(100 * 2 * sqrt(depth * height), [120 * sqrt(2), 140 * sqrt(2), 140 * sqrt(3), 120 * sqrt(3)])
    c[34] = q34
    c[35] = lambda: opt(Rational(2 * 1 + 6 * 2, 8), [Rational(5, 2), Rational(5, 4), Rational(7, 2), Rational(7, 4)])

    def q36():
        k = 0.2 * 10 / 0.002
        f = math.sqrt(k / 0.2) / (2 * math.pi)
        E = 0.5 * k * 0.004**2
        opts = [(5 * math.sqrt(50) / math.pi, 8e-3), (5 * math.sqrt(50) / math.pi, 8), (10 * math.sqrt(50), 2e-3), (5 * math.sqrt(50) / math.pi, 16e-3)]
        return [i for i, (a, b) in enumerate(opts, 1) if abs(a - f) < 1e-9 and abs(b - E) < 1e-12][0]
    c[36] = q36

    def q37():
        X, Y = symbols('X Y')
        V = 5 * (X**2 - Y**2)
        E = (-diff(V, X).subs({X: 2, Y: 3}), -diff(V, Y).subs({X: 2, Y: 3}))
        return [(-20, 30), (20, -30), (20, 45), (-4, 6)].index(E) + 1
    c[37] = q37
    c[38] = lambda: nearest(2 * (2e-7 * 30 / 0.04) * 1e6, [30, 300, 150, 0])
    c[39] = lambda: nearest(0.4 * 4e-4 * 300 * 0.5 * 1000, [12, 18, 21, 24])
    c[40] = lambda: opt(Rational(1, 2) * Rational(100, 10**12) * 100**2 / 2 * 10**7, [5, Rational(5, 2), Rational(7, 2), Rational(9, 2)])
    c[41] = lambda: nearest(4 * 7.2 - 2 * 2 * 1.1, [6.1, 24.4, 26.6, 5])
    c[42] = lambda: nearest(math.sin(math.radians(45)) / math.sin(math.radians(30)), [1.5, math.sqrt(3), math.sqrt(2), 1.65])

    def q43():
        Y = lambda A, B: int(not (((1 - A) | B) | ((1 - A) & B)))
        return [(1, 0), (0, 1), (0, 0), (1, 1)].index((Y(1, 1), Y(0, 1))) + 1
    c[43] = q43
    c[44] = lambda: nearest(math.sqrt(2 * (4 * 10 / 8) * 6), [7.74, 7.20, 6.55, 4.50])

    def q45():
        lam = 6000
        ok = [i for i, d in enumerate([4000, 3000, 2000, 1000], 1)
              if abs(4 * math.cos(math.pi * d / lam)**2 - 1) < 1e-9]
        assert ok == [1, 3]
        return 1
    c[45] = q45

    def q46():
        mu = Symbol('mu')
        return solve(Rational(1, 4) - (1 - mu), mu)[0] * 100
    c[46] = q46
    c[47] = lambda: 9 / Rational(3, 2)**2            # V1/V2 = (lam2/lam1)^2 = 9/alpha

    def q48():
        G, I = symbols('G I', positive=True)
        return solve([I * G - (Rational(1, 2) - I) * 2, I * (G + 470) - 10], [G, I], dict=True)[0][G]
    c[48] = q48

    def q49():
        req = Rational(2 * 1, 3)
        E = (Rational(1, 2) + 2) / Rational(3, 2)
        R = solve(E / (Symbol('R') + req) - 1)[0]
        E2 = abs(Rational(1, 2) - 2) / Rational(3, 2)
        return E2 / (R + req) * 5
    c[49] = q49

    def q50():
        u = Symbol('u')
        f = -10
        us = [solve(f / (f - u) - m, u)[0] for m in (-2, 2)]
        return abs(us[0] - us[1])
    c[50] = q50

    def q51():
        atoms = {'A': Rational(2, 32) * 2, 'B': Rational(4, 64) * 3, 'C': Rational(1400, 22400) * 2,
                 'D': Rational(50, 22400), 'E': Rational(625, 10000) * 2}
        same = sorted(k for k in atoms if list(atoms.values()).count(atoms[k]) > 1)
        return [['A', 'B'], ['B', 'C'], ['C', 'D'], ['A', 'C', 'E']].index(same) + 1
    c[51] = q51

    def q52():
        hits = [(Z, n) for Z in (1, 2, 3) for n in range(1, 6) if abs(52.9 * n * n / Z - 70.53) < 0.01]
        return [(3, 3), (2, 3), (2, 2), (3, 2)].index(hits[0]) + 1
    c[52] = q52

    def q55():
        c1, c2 = Rational(18, 180) / Rational(1, 10), Rational(30, 180) / Rational(1, 4)
        s1_true = c2 > c1                  # water flows towards the more concentrated side
        pi_ = 3 * (0.05 / 174 / 2) * 0.083 * 300
        s2_true = abs(pi_ - 0.0107) < 0.0001
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(s1_true, s2_true)]
    c[55] = q55

    def q56():
        X, Y, cc, al = 2, 3, Rational(1, 10), Rational(1, 50)
        K = (X * cc * al)**X * (Y * cc * al)**Y / cc            # weak electrolyte: 1 - alpha ~ 1
        forms = [(K * cc**(X + Y - 1) * X**X * Y**Y)**(X + Y), (K / (cc**(X + Y - 1) * X**X * Y**Y))**Rational(1, X + Y),
                 (cc**(X + Y - 1) * X**X * Y**Y / K)**(X + Y), (cc**(X + Y - 1) * X**X * Y**Y / K)**Rational(1, X + Y)]
        return opt(al, forms)
    c[56] = q56
    c[71] = lambda: Rational(100, 1000) * Rational(5, 100) * 1 * 1000
    c[72] = lambda: [4 for n in range(1, 20) if Rational(3 * n + 1, 2) == 8][0]      # C5H12, all H equivalent: C(CH3)4

    def q73():
        e = Rational(500, 1000) * Rational(2, 10) * 3
        assert Rational(500, 1000) * Rational(15, 10) > e        # iodide in excess
        return (e / 2) * 2 / Rational(300, 1000)
    c[73] = q73

    def q74():
        a = Rational(3, 4)
        n1, n2 = 1 - a, 2 * a
        p1, p2 = n1 / (n1 + n2), n2 / (n1 + n2)
        K = p2**2 / p1
        assert K == Rational(36, 7)
        logK = 2 * (0.3 + 0.48) - 0.84
        return round(abs(-2.3 * 8.3 * 600 * logK) / 1000)
    c[74] = q74
    c[75] = lambda: round(28000 * 8.3 / 1000)
    return c
