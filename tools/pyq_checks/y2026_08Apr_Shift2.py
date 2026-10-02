"""Answer checks for JEE Main 2026 (Session 2), 8 Apr Shift 2. Q64 is disputed (see solutions.csv)."""
from pyq_checks.common import *
from sympy import Eq, Function, dsolve


def checks():
    c = {}

    def q1():
        U = [-2, -1, 0, 1, 2]
        R = {(a, b) for a in U for b in U if 1 + a * b > 0}
        transitive = all((a, d) in R for (a, b) in R for (b2, d) in R if b == b2)
        reflexive = all((a, a) in R for a in U)
        symmetric = all((b, a) in R for (a, b) in R)
        s1, s2 = len(R) == 17, reflexive and symmetric and transitive
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(s1, s2)]
    c[1] = q1

    def q2():
        X, Y = symbols('X Y', real=True)
        z = X + Y * sympy_I
        circ = (X - 4)**2 + (Y - 8)**2 - 10
        a2, c2 = 20, 10                       # semi-major^2 and focal distance^2 (centre (4, 8))
        # ellipse axes: major along (1, 3)/sqrt(10); write in rotated coordinates
        u = ((X - 4) * 1 + (Y - 8) * 3) / sqrt(10)
        v = (-(X - 4) * 3 + (Y - 8) * 1) / sqrt(10)
        ell = u**2 / a2 + v**2 / (a2 - c2) - 1
        sols = solve([circ, ell], [X, Y], dict=True)
        pts = {(simplify(s[X]), simplify(s[Y])) for s in sols}
        for px, py in pts:                      # confirm against the focal-sum definition
            d = sqrt((px - 3)**2 + (py - 5)**2) + sqrt((px - 5)**2 + (py - 11)**2)
            assert abs(float(d) - 4 * math.sqrt(5)) < 1e-9
        return opt(len(pts), [0, 2, 1, 4])
    c[2] = q2

    def q3():
        l, m = symbols('l m')
        lv = solve(Matrix([[1, 1, 1], [1, 2, 5], [2, 3, l]]).det(), l)[0]
        A = Matrix([[1, 1, 1, 6], [1, 2, 5, 10], [2, 3, lv, m]])
        assert A[2, :3] - A[0, :3] - A[1, :3] == Matrix([[0, 0, 0]])     # row 3 = row 1 + row 2 on the left
        mv = solve(A[2, 3] - A[0, 3] - A[1, 3], m)[0]
        assert Matrix([[1, 1, 1, 6], [1, 2, 5, 10], [2, 3, lv, mv]]).rank() == 2
        return opt(lv + mv, [12, 16, 22, 28])
    c[3] = q3

    def q4():
        a = Symbol('a')
        A = Matrix([[a, 1, 2], [2, 3, 0], [0, 4, 5]])
        B = Matrix([[1, 0, 0], [0, -5 * a, 0], [0, 4 * a, -2 * a]]) + A.adjugate()
        av = solve(B.det() - 66, a)
        assert len(av) == 1
        return opt(A.adjugate().det().subs(a, av[0]), [289, 361, 441, 529])
    c[4] = q4

    def q5():
        terms = []
        t = 3
        while len(terms) < 40:
            terms += [t, t + 1]; t += 5
        al = sum(terms[:40])
        e = Rational(al, 1020)
        tb = [r for r in solve(x**2 + x - 2, x) if r > 0][0]**(1 / e)     # tan(beta) > 0 in (0, pi/2)
        b = atan(tb)
        return opt(simplify(sin(b)**2 + 3 * cos(b)**2), [2, Rational(7, 4), Rational(5, 2), Rational(3, 2)])
    c[5] = q5

    def q6():
        P = [Rational(2, 5), Rational(1, 5), Rational(2, 5)]
        L = [Rational(1, 5), Rational(1, 3), Rational(1, 4)]
        return opt(P[0] * L[0] / sum(p * l for p, l in zip(P, L)), [Rational(11, 37), Rational(12, 37), Rational(13, 37), Rational(14, 37)])
    c[6] = q6

    def q7():
        s1, q1_ = 4 * 1, 4 * (13 + 1)
        s2, q2_ = 6 * 2, 6 * (1 + 4)
        n = 10
        return nearest(Rational(q1_ + q2_, n) - Rational(s1 + s2, n)**2, [5.96, 6.14, 6.04, 6.24])
    c[7] = q7

    def q8():
        S = 26 * sum(Rational(2**(2 * k + 1), 2 * k + 1) * math.comb(12, 2 * k) for k in range(1, 7))
        return opt(3**13 - S, [45, 48, 51, 54])
    c[8] = q8
    c[9] = lambda: opt(sum(1 for f in product(range(3), repeat=4) if len(set(f)) == 3), [18, 36, 39, 72])

    def q10():
        a, b, h, k = symbols('a b h k')
        P = solve([4 * x + 3 * Symbol('y') - 1, 3 * x + 4 * Symbol('y') - 1], [x, Symbol('y')])
        px, py = P[x], P[Symbol('y')]
        rel = expand((px / (2 * h) + py / (2 * k) - 1) * 14 * h * k)        # line x/a + y/b = 1 with a = 2h, b = 2k
        cands = [h + k - 7, h + k - 14 * h * k, 2 * h + k + 14 * h * k, h + 2 * k - 14 * h * k]
        return [i for i, f in enumerate(cands, 1) if simplify(rel + f) == 0 or simplify(rel - f) == 0][0]
    c[10] = q10

    def q11():
        t1 = Symbol('t1')
        t2 = -4 / t1
        hx = (t1**2 + t2**2) / 2
        ky = t1 + t2
        assert simplify(ky**2 - 2 * (hx - 4)) == 0              # locus y^2 = 2(x - 4)
        return opt(2, [1, 2, 4, 8])
    c[11] = q11

    def q12():
        al, be = 3 * math.asin(6 / 11), 3 * math.acos(4 / 9)
        s1, s2 = math.cos(al + be) > 0, math.cos(al) < 0
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(s1, s2)]
    c[12] = q12

    def q13():
        f = lambda t: math.exp(math.sin(abs(t))) - abs(t)
        h = 1e-6
        s1 = abs((f(h) - f(0)) / h - (f(0) - f(-h)) / h) < 1e-4
        xs = [-math.pi + k * (math.pi / 2) / 1000 for k in range(1, 1000)]
        s2 = all(f(b) > f(a) for a, b in zip(xs, xs[1:]))
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(s1, s2)]
    c[13] = q13

    def q14():
        a, b = Matrix([4, -1, 3]), Matrix([10, 2, -1])
        t = Symbol('t')
        cv = (2 * a + t * b) / 3
        tv = solve(a.dot(cv) - 15, t)[0]
        cv = cv.subs(t, tv)
        assert 2 * a.cross(b) + 3 * b.cross(cv) == Matrix([0, 0, 0])
        return opt(cv.dot(Matrix([1, 1, -3])), [-6, -5, -4, -3])
    c[14] = q14

    def q15():
        lam, t = symbols('lam t')
        tv = solve(4 + t - 1, t)[0]
        foot = Matrix([4 + tv, 9 + 2 * tv, 5 + tv]); mu = foot[1]
        lv = solve((foot - Matrix([lam, 2, 3])).dot(Matrix([1, 2, 1])), lam)[0]
        d = Matrix([2, 3, 6])
        AB = Matrix([lv, mu, -5]) - Matrix([1, 2, -4])
        return opt(AB.cross(d).norm() / d.norm(), [Rational(12, 7), sqrt(145) / 7, sqrt(146) / 7, sqrt(143) / 7])
    c[15] = q15

    def q16():
        import mpmath
        f = lambda t: mpmath.sqrt(t * (t * t + t + 1)) / (mpmath.sqrt(t + 1) * mpmath.sqrt(t**4 + t * t + 1))
        v = float(mpmath.quad(f, [0, 2]))
        return nearest(v, [math.log(3 - 2 * math.sqrt(2)) / 3, 2 * math.log(4 + math.sqrt(2)) / 3,
                           2 * math.log(3 + 2 * math.sqrt(2)) / 3, math.log(1 + 6 * math.sqrt(2)) / 3])
    c[16] = q16

    def q17():
        y = Function('y')
        C = Symbol('C')
        gen = (-(sqrt(1 - x**2) * acos(x) + x) + C) / x
        ode = x * sqrt(1 - x**2) * diff(gen, x) + (gen * sqrt(1 - x**2) - x * acos(x))
        assert simplify(ode) == 0
        Cv = solve(limit(gen, x, 1, '-') - 1, C)[0]
        return opt(simplify(gen.subs(C, Cv).subs(x, Rational(1, 2))),
                   [3 - pi / sqrt(3), 4 - sqrt(3) * pi, 4 - 2 * pi / sqrt(3), 3 - pi / (2 * sqrt(3))])
    c[17] = q17

    def q18():
        f = lambda e: (e - 1) / (e + 1)
        g = x
        for _ in range(26):
            g = simplify(f(g))
        gx = -g
        assert simplify(gx - 1 / x) == 0
        xi = [r for r in solve(gx - (x - Rational(3, 2)), x) if r > 1][0]
        area = integrate(x - Rational(3, 2), (x, Rational(3, 2), xi)) + integrate(gx, (x, xi, 4))
        return opt(simplify(area), [Rational(1, 8) + log(2), Rational(1, 4) + log(2), Rational(5, 6) + 3 * log(2), Rational(5, 6) + log(2)])
    c[18] = q18

    def q19():
        b = Symbol('b')
        bv = solve(limit(b * (1 - sin(x)) / (pi - 2 * x)**2, x, pi / 2, '+') - Rational(1, 3), b)[0]
        up = 3 * bv - 6
        return opt(integrate(-(x**2 + 2 * x - 3), (x, 0, 1)) + integrate(x**2 + 2 * x - 3, (x, 1, up)), [5, 2, 3, 4])
    c[19] = q19

    def q20():
        a = Symbol('a', real=True)
        bad = solve(a**2 + 4 * a - 12, a)                # boundary of 3a + 15 < a^2 + 7a + 3
        return opt(sum(v**2 for v in bad), [28, 40, 61, 24])
    c[20] = q20

    def q21():
        sols = []
        for r in solve(x**2 - 2, x) + [-2]:
            xv = float(r)
            if xv > -1 and xv != 0:
                lhs = math.log(2 * xv * xv + 5 * xv + 3, xv + 1)
                rhs = 4 - math.log(xv * xv + 2 * xv + 1, 2 * xv + 3)
                if abs(lhs - rhs) < 1e-9: sols.append(r)
        return sum(s**2 for s in sols)
    c[21] = q21

    def q22():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.cot(t - mpmath.pi / 3) * mpmath.cot(t + mpmath.pi / 3) + 1, [mpmath.pi / 6, mpmath.pi / 4])
        al = v / mpmath.log(mpmath.sqrt(3) - 1)
        assert abs(al + 2 / mpmath.sqrt(3)) < 1e-12
        return 9 * Rational(4, 3)
    c[22] = q22

    def q23():
        s, t = symbols('s t')
        n = Matrix([1, 2, 2]).cross(Matrix([2, 2, 1]))
        sol = solve(list(Matrix([3 + t, 2 * t - 1, 2 * t + 4]) - s * n), [s, t], dict=True)[0]
        P = s * n
        P = P.subs(sol)
        u = Symbol('u')
        for uv in solve((Matrix([3 + 2 * u, 3 + 2 * u, 2 + u]) - P).dot(Matrix([3 + 2 * u, 3 + 2 * u, 2 + u]) - P) - 17, u):
            Q = Matrix([3 + 2 * uv, 3 + 2 * uv, 2 + uv])
            if Q[0].is_integer:
                return sum(Q)**2
    c[23] = q23

    def q24():
        h, k, X, Y = symbols('h k X Y')
        p = h**2 + k**2
        L = (h * X + k * Y) / p                              # = 1 on the chord
        hom = expand((X**2 + Y**2 - (6 * X + 8 * Y) * L - 11 * L**2) * p**2)
        cond = factor(Poly(hom, X, Y).coeff_monomial(X**2) + Poly(hom, X, Y).coeff_monomial(Y**2))
        loc = expand(cond / (h**2 + k**2))                  # 2(h^2 + k^2) - 6h - 8k - 11
        al, be, ga = -loc.coeff(h, 1) / 2, -loc.coeff(k, 1) / 2, -loc.subs({h: 0, k: 0}) / 2
        assert loc.coeff(h, 2) == 2
        return al + be + 2 * ga
    c[24] = q24

    def q25():
        f = lambda t: 1 + t**2
        assert f(6) == 37
        for t in (Rational(1, 2), 2, 3):
            assert abs(math.log2(f(t)) - math.log2(3) * math.log(1 + f(t) / f(1 / t), 3)) < 1e-12
        return sum(f(n) for n in range(1, 11))
    c[25] = q25
    c[26] = lambda: opt(6 * 60 + 40, [200, 400, 300, 500])

    def q27():
        # exponents of (M, L, T, A): x, eps, E, t
        dims = {'x': (0, 1, 0, 0), 'e': (-1, -3, 4, 2), 'E': (1, 1, -3, -1), 't': (0, 0, 1, 0)}
        H = (0, -1, 0, 1)
        for i, (p, q, r, s) in enumerate([(1, 1, 1, 1), (-1, 1, 2, 1), (1, -1, -2, 1), (-1, -2, -2, 1)], 1):
            d = tuple(p * dims['x'][j] + q * dims['e'][j] + r * dims['E'][j] - s * dims['t'][j] for j in range(4))
            if d == H:
                return i
    c[27] = q27
    c[28] = lambda: nearest((54 / 3.6)**2 / (20 * 10), [0.5, 0.75, 1.125, 0.25])

    def q29():
        t = [v for v in solve(-75 - (10 * x - 5 * x**2), x) if v > 0][0]
        return opt(75 + 10 * t, [85, 150, 129, 125])
    c[29] = q29

    def q30():
        fl = 1 / (Rational(1, 2) * (Rational(1, 20) + Rational(1, 20)))
        P = 2 / fl + 1 / Rational(10)
        return opt(2 / P, [10, Rational(25, 2), 13, Rational(27, 2)])
    c[30] = q30
    c[31] = lambda: opt(Rational(10 * 5 * 10, 2), [250, 25, 500, 125])

    def q32():
        t = Symbol('t')
        v0, mu, g, R = 49, Rational(1, 4), Rational(98, 10), Symbol('R', positive=True)
        return opt(solve((v0 - mu * g * t) - (v0 / (4 * R) + 2 * mu * g * t / R) * R, t)[0], [15, 5, 10, Rational(15, 2)])
    c[32] = q32

    def q33():
        v1 = Rational(1, 10)
        v2 = v1 * 100 / 20
        return opt(Rational(1, 2) * 600 * (v2**2 - v1**2), [18, 144, 36, 72])
    c[33] = q33
    c[34] = lambda: opt((1 / (Rational(1, 64))**Rational(1, 3))**2, [4, Rational(1, 4), 32, 16])

    def q36():
        P, V = symbols('P V', positive=True)
        g = Rational(5, 3)
        P2 = P * Rational(1, 27)**g
        dU = (P2 * 27 * V - P * V) / (g - 1)
        return opt(simplify(dU / (P * V)), [-2 * (3 * sqrt(3) - 1), Rational(4, 3), Rational(-4, 3), Rational(3, 4)])
    c[36] = q36
    c[37] = lambda: opt(sqrt(2), [1, 2, sqrt(2), sqrt(3)])

    def q38():
        lam = 6.6e-34 * 3e8 / (15000 / 2.5e22)
        return 4 if lam < 400e-9 and lam > 10e-9 else 0
    c[38] = q38

    def q39():
        m = 100 * sqrt(2) * Rational(314, 100) * Rational(2, 100)**2 * Matrix([1, 0, 1]) / sqrt(2)
        tau = m.cross(Rational(4, 1000) * Matrix([3, 0, 2]))
        return [i for i, v in enumerate([Matrix([0, 0, 16e-5]), Matrix([0, 0, 5024e-7]), Matrix([5024e-7, 0, 0]), Matrix([0, 5024e-7, 0])], 1)
                if all(abs(float(tau[j]) - float(v[j])) < 1e-12 for j in range(3))][0]
    c[39] = q39

    def q40():
        L = 4 * math.pi * 1e-7 * 1000**2 * 5e-4 * 0.3
        return nearest(L * 2 / 3.14 / 1e-5, [60, 12, 120, 34])
    c[40] = q40

    def q41():
        r = Matrix([1, 1, 1]) - Matrix([2, 3, 3])
        F = 9 * 10**9 * Rational(3, 10**6) * Rational(-4, 10**6) * r / r.norm()**3
        return [i for i, v in enumerate([Matrix([12, 24, 24]), Matrix([4, 8, 8]), Matrix([3, 6, 6]), Matrix([-4, -8, -8])], 1)
                if F == v / 1000][0]
    c[41] = q41

    def q42():
        C = Symbol('C', positive=True)
        cv = solve(Rational(4, 13) * (C**2 + 16) - Rational(9, 4) * C**2, C)[0]
        return nearest(float(cv), [1.6, 0.16, 11.6, 16])
    c[42] = q42

    def q43():
        K1, K2, phi, E = symbols('K1 K2 phi E')
        s = solve([K1 - (E - phi), K2 - (2 * E - phi)], [phi, E], dict=True)[0]
        return [i for i, f in enumerate([K2 + 2 * K1, 2 * K2 - K1, K1 - 2 * K2, K2 - 2 * K1], 1) if simplify(s[phi] - f) == 0][0]
    c[43] = q43
    c[44] = lambda: opt(Rational(196, 200) / Rational(208, 212), [Rational(2548, 2650), Rational(2706, 2646), Rational(2597, 2600), Rational(2862, 2499)])

    def q45():
        A = lambda t: 1 if 1 <= t < 3 else 0
        B = lambda t: 1 if (t < 2 or t >= 3) else 0
        Y = lambda t: (A(t) & B(t)) | ((1 - A(t)) & B(t))
        ys = [Y(t + 0.5) for t in range(3)]
        assert ys == [B(t + 0.5) for t in range(3)] == [1, 1, 0]
        return 2
    c[45] = q45

    def q46():
        Ar = Rational(10**13) * Rational(885, 10**6) / (Rational(177, 10) * 10**14)
        er = Rational(1, 10**6) * Rational(885, 10**6) / (Rational(885, 10**14) * Ar)
        return er / 10**7
    c[46] = q46
    c[47] = lambda: round(1.22 * 500e-9 / 3e-7 * 100)
    c[48] = lambda: Rational(2, 100) * 5 * (2 * pi * Rational(5, 10**6) / (5 * pi * Rational(1, 10**6) * Rational(1, 10)))

    def q49():
        par = Rational(1, 1) / (Rational(1, 10) + Rational(1, 4 + 4 + 2))
        I = 12 / (5 + par + 2)
        return Rational(100) * (I * par / 10) * 4          # muC: branch current x 4 ohm
    c[49] = q49

    def q50():
        a1 = Rational(104 - 5) / Rational(9, 2); a2 = Rational(129 - 12) / Rational(9, 2)
        return 8 * (Rational(34, 10) * (5 + 10 * a1)) / (Rational(25, 10) * (12 + 10 * a2))
    c[50] = q50

    def q51():
        atoms = {'A': Rational(18, 10) / 18 * 3, 'B': Rational(98, 10) / 98 * 7, 'C': Rational(18, 10) / 12, 'D': Rational(585, 100) / Rational(585, 10) * 2}
        lst = {'I': 2, 'II': Rational(3, 2), 'III': 3, 'IV': 7}
        match = {k: [n for n, v in lst.items() if v * Rational(1, 10) == atoms[k]][0] for k in atoms}
        opts = [dict(A='IV', B='III', C='I', D='II'), dict(A='III', B='II', C='IV', D='I'), dict(A='III', B='IV', C='II', D='I'), dict(A='III', B='IV', C='I', D='II')]
        return opts.index(match) + 1
    c[51] = q51

    def q52():
        x_ccl4 = (70 / 154) / (70 / 154 + 30 / 32)
        return 1 if abs(x_ccl4 - 0.33) < 0.005 else 0      # II (positive deviation) is a known fact
    c[52] = q52
    c[55] = lambda: nearest((1 / math.sqrt(2.5e5)) * 5e-3, [2.5e-3, 2.5e3, 1.0e-5, 5e-3])

    def q56():
        X, Y = symbols('X Y')
        E = (-3 * Y - (-2 * X)) / -1                       # dG(Fe3+ -> Fe2+) = -3FY + 2FX = -1 F E
        return [i for i, f in enumerate([2 * X - 3 * Y, 3 * Y - 2 * X, 3 * Y + 2 * X, Y + X], 1) if simplify(E - f) == 0][0]
    c[56] = q56

    def q57():
        Ea = 12.6 * 4.2 * 1000
        ratio = math.exp(Ea / 8.314 * (1 / 298 - 1 / 308))
        s1 = abs(ratio - 2) < 0.05
        return 3 if s1 else 2                               # II false: first-order t1/2 does not depend on [A]0
    c[57] = q57
    c[73] = lambda: Rational(6000, 2000)
    c[74] = lambda: round(abs(2 * (-286.0) + 2 * (-297.0) - 2 * (-20.1)))
    c[75] = lambda: sqrt(2 * Rational(8, 100)) * 10
    return c
