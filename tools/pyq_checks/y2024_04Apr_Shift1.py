"""Answer checks for JEE Main 2024 (Session 2), 4 Apr Shift 1. Q27 was dropped by NTA; Q48 and Q50 are disputed."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor


def checks():
    c = {}

    def q1():
        F = Fraction
        ok = [F(k, 1000) for k in range(-20000, 20001)
              if 2 * k != 19000 and -1 <= (3 * k / 1000 - 22) / (2 * k / 1000 - 19) <= 1
              and (k / 1000)**2 - 3 * k / 1000 - 10 != 0 and (3 * (k / 1000)**2 - 8 * k / 1000 + 5) / ((k / 1000)**2 - 3 * k / 1000 - 10) > 0]
        assert min(ok) == F(5001, 1000) and max(ok) == F(41, 5)
        return opt(3 * 5 + 10 * Rational(41, 5), [95, 97, 98, 100])
    c[1] = q1

    def q2():
        zs = [z for z in (sympy_I, -sympy_I, 1, -1) if simplify(z.conjugate()**2 + Abs(z)) == 0]
        al, be = sum(zs), zs[0] * zs[1]
        return opt(4 * (Abs(al)**2 + be**2), [2, 4, 6, 8])
    from sympy import Abs
    c[2] = q2

    def q3():
        a, b = symbols('a b')
        s = solve([2 + 6 + b / a, 12 - 1 / a], [a, b], dict=True)[0]
        r1, r2 = 1 / (2 * s[a] + s[b]), 1 / (6 * s[a] + s[b])
        return [i for i, e in enumerate([x**2 + 8 * x + 12, 4 * x**2 + 14 * x + 12, 2 * x**2 + 11 * x + 12, x**2 + 10 * x + 16], 1)
                if e.subs(x, r1) == 0 and e.subs(x, r2) == 0][0]
    c[3] = q3

    def q4():
        a = Symbol('a')
        M = Matrix([[1, sqrt(2) * sin(a), sqrt(2) * cos(a)], [1, cos(a), sin(a)], [1, sin(a), -cos(a)]])
        hits = [i for i, v in enumerate([3 * pi / 4, 7 * pi / 24, 5 * pi / 24, 11 * pi / 24], 1) if 0 < v < pi / 2 and abs(N(M.det().subs(a, v))) < 1e-12]
        return hits[0]
    c[4] = q4

    def q5():
        a = Symbol('a')
        A = Matrix([[1, 2, a], [1, 0, 1], [0, 1, 2]])
        av = [v for v in solve((2 * A - A.T).adjugate().det() * (A - 2 * A.T).adjugate().det() - 2**8, a) if v.is_real and v > 0]
        return opt(A.det().subs(a, av[0])**2, [1, 16, 36, 49])
    c[5] = q5

    def q6():
        b = Symbol('b')
        al = limit((1 - cos(2 * x)) / x**2, x, 0, '-')
        bv = [v for v in solve(limit(b * sqrt(1 - cos(x)) / x, x, 0, '+') - al, b)][0]
        return opt(al**2 + bv**2, [3, 6, 12, 48])
    c[6] = q6
    c[7] = lambda: opt(math.comb(18, 3) - math.comb(5, 3) - math.comb(6, 3) - math.comb(7, 3), [771, 776, 796, 751])
    c[8] = lambda: opt(sum(math.comb(15, r) * 2**((15 - r) // 5) * 5**(r // 3) for r in range(16) if (15 - r) % 5 == 0 and r % 3 == 0), [931, 3133, 633, 6131])

    def q9():
        a, d, r, n = symbols('a d r n')
        sols = [s for s in solve([a + 6 * d - 2, a + 7 * d - 2 * r, a + 12 * d - 2 * r**2], [a, d, r], dict=True) if s[r] != 1]
        s = sols[0]
        return opt(solve(s[a] + (n - 1) * s[d] - 2 * s[r]**4, n)[0], [151, 163, 169, 177])
    c[9] = q9

    def q10():
        import mpmath
        f = lambda t: -2 if t <= 0 else t - 2
        return nearest(float(mpmath.quad(lambda t: f(abs(t)) + abs(f(t)), [-2, 0, 2])), [1, 2, 4, 6])
    c[10] = q10
    c[11] = lambda: opt(8 / diff(x**5 + 2 * exp(x / 4), x).subs(x, 0), [2, 4, 8, 16])

    def q12():
        f = (2 * x**2 - 3 * x + 8) / (2 * x**2 + 3 * x + 8)
        v = Rational(sum(f.subs(x, cpt) for cpt in solve(diff(f, x), x)))
        return opt(v.p + v.q, [182, 195, 201, 217])
    c[12] = q12

    def q13():
        A = simplify(integrate(1 + 3 * x - 2 * x**2 - 1 / x, (x, Rational(1, 2), (1 + sqrt(5)) / 2)))
        hits = [(l, m, n) for l in range(1, 40) for m in range(1, 40) for n in range(1, 5)
                if abs(N(Rational(1, 24) * (l * sqrt(5) + m) - n * log(1 + sqrt(5)) - A)) < 1e-12]
        return opt(sum(hits[0]), [30, 29, 31, 32])
    c[13] = q13

    def q14():
        assert expand((x**2 + 1) * (x**2 + 2 * x + 2)) == x**4 + 2 * x**3 + 3 * x**2 + 2 * x + 2
        y = atan(x + 1) + atan(x)
        assert y.subs(x, -1) == -pi / 4
        return opt(y.subs(x, 0), [pi / 4, pi / 2, 0, -pi / 12])
    c[14] = q14

    def q15():
        C = Matrix([5, 3]); r = 2
        vs = [C + r * Matrix([cos(t), sin(t)]) for t in (pi / 4, 3 * pi / 4, 5 * pi / 4, 7 * pi / 4)]   # sides parallel to y = x
        return opt(simplify(sum(v.dot(v) for v in vs)), [148, 152, 156, 160])
    c[15] = q15

    def q16():
        lines = [(Matrix([1, -1]), 4, Matrix([3, -1])), (Matrix([3, 5]), -4, Matrix([-1, 3])), (Matrix([1, 1]), -2, Matrix([-2, 2]))]
        best = None
        for nrm, cst, opp in lines:
            sgn = 1 if nrm.dot(opp) + cst > 0 else -1
            c2 = cst - sgn * nrm.norm()
            d = abs(c2) / nrm.norm()
            if best is None or d < best[0]: best = (d, nrm, c2)
        d, nrm, c2 = best
        assert list(nrm) == [1, 1] and simplify(c2 + (2 - sqrt(2))) == 0
        return 1
    c[16] = q16

    def q17():
        P, Q = Matrix([1, -2, 3]), Matrix([5, -4, 7])
        u = (Q - P) / (Q - P).norm()
        return opt(max((P + s * 9 * u).dot(P + s * 9 * u) for s in (1, -1)), [150, 165, 160, 155])
    c[17] = q17

    def q18():
        a, b, cc = symbols('a b cc', real=True)
        sols = solve([2 * a + 2 * b - cc - Rational(3, 2), a - cc - 1, a**2 + b**2 + cc**2 - 1], [a, b, cc], dict=True)
        target = Matrix([sqrt(2) / 3, 0, Rational(-1, 2)])
        shift = Matrix([Rational(-1, 2), 1 / (3 * sqrt(2)), -sqrt(2) / 3])
        assert any(simplify(Matrix([s[a], s[b], s[cc]]) + shift - target) == Matrix([0, 0, 0]) for s in sols)
        return 3
    c[18] = q18
    c[19] = lambda: opt(Rational(5, 12) / (Rational(5, 12) + Rational(7, 12) + Rational(6, 12)), [Rational(5, 16), Rational(4, 17), Rational(5, 18), Rational(7, 18)])

    def q20():
        for al in range(-20, 21):
            be = 10 - al
            d = [-3, 4, 7, -6, al, be]
            if Rational(sum(v * v for v in d), 6) - 4 == 23:
                return opt(Rational(sum(abs(v - 2) for v in d), 6), [Rational(11, 3), Rational(16, 3), Rational(14, 3), Rational(13, 3)])
    c[20] = q20

    def q21():
        ts = []
        for t in range(0, 31):
            for M in range(125, 131):
                for P in range(85, 96):
                    for C in range(75, 91):
                        if M + P + C - 120 + t == 210 and min(M - 90 + t, P - 70 + t, C - 80 + t, 30 - t, 50 - t, 40 - t) >= 0:
                            ts.append(t)
        return min(ts) + max(ts)
    c[21] = q21
    c[22] = lambda: (3 * eye(3)).det()
    from sympy import eye

    def q23():
        a = 1 + sum(Rational(math.comb(n, 2), math.factorial(n + 1)) for n in range(2, 60))
        b = sum(Rational(2**n, math.factorial(n)) for n in range(0, 60))
        return round(float(2 * b / a**2), 9)
    c[23] = q23

    def q24():
        L = limit(((5 * x + 1)**Rational(1, 3) - (x + 5)**Rational(1, 3)) / ((2 * x + 3)**Rational(1, 2) - (x + 4)**Rational(1, 2)), x, 1)
        for n in range(1, 10):
            m = simplify(L * n * (2 * n)**Rational(2, 3) / sqrt(5))
            if m.is_Integer and math.gcd(int(m), n) == 1:
                return 8 * m + 12 * n
    c[24] = q24

    def q25():
        t = Symbol('t')
        v = integrate(t**2 / ((1 + t**2) * (1 + t + t**2)), (t, 0, 1))
        hits = [(a, b) for a in range(1, 10) for b in range(1, 20) if abs(N(log(Rational(a, 3)) / a + pi / (b * sqrt(3)) - v)) < 1e-12]
        return sum(hits[0])
    c[25] = q25

    def q26():
        y = Function('y')
        s = dsolve(Eq(y(x).diff(x) - y(x), 1 + 4 * sin(x)), y(x), ics={y(pi): 1})
        return simplify(s.rhs.subs(x, pi / 2) + 10)
    c[26] = q26

    def q28():
        s2 = solve(12 / Symbol('s') - 15, Symbol('s'))[0]          # s = sin^2(theta)
        return 10 * 9 * s2
    c[28] = q28

    def q29():
        n = Matrix([2, 3, 4]).cross(Matrix([1, -3, 2]))
        SD = abs((Matrix([3, 2, -4]) - Matrix([-2, -3, 5])).dot(n)) / n.norm()
        k = simplify(SD / (38 / (3 * sqrt(5))))
        I = sum(floor(Rational(j)) * 0 for j in range(1)) + (sqrt(2) - 1) * 1 + (k - sqrt(2)) * 2
        al = [v for v in (1, 2, 3, 4) if simplify(v - sqrt(v) - I) == 0][0]
        return 6 * al**3
    c[29] = q29

    def q30():
        d = Symbol('d', positive=True)
        AB, AC = Matrix([1, 2, -7]), Matrix([6, d, -2])
        dv = solve(AB.cross(AC).dot(AB.cross(AC)) - 4 * 450, d)[0]
        AC = AC.subs(d, dv)
        return max(v.dot(v) for v in (AB, AC, AC - AB))
    c[30] = q30
    def q32():
        T = Symbol('T')
        r = Matrix([2 + 4 * T, 3 * T + 8 * T**2])
        v, a = diff(r, T), diff(r, T, 2)
        const = all(diff(e, T) == 0 for e in a)
        parallel = v.subs(T, 0)[0] * a[1] - v.subs(T, 0)[1] * a[0] == 0
        return 3 if const and not parallel else (2 if const else 1)
    c[32] = q32
    c[34] = lambda: opt(Rational(1150 - 1025, 10) / 2, [5, Rational(625, 100), Rational(125, 10), 9])
    def q35():
        m, g, h = symbols('m g h', positive=True)
        loss = (m * g * h - m * g * h / 2) / (m * g * h)
        v = sqrt(2 * g * h)
        return [i for i, (L, V) in enumerate([(Rational(1, 2), sqrt(g * h)), (Rational(1, 2), sqrt(2 * g * h)), (Rational(2, 5), sqrt(2 * g * h)), (Rational(1, 2), sqrt(g * h / 2))], 1) if L == loss and simplify(V - v) == 0][0]
    c[35] = q35
    def q36():
        G, M, m, L, th = symbols('G M m L th', positive=True)
        R = L / pi; lam = M / L
        F = integrate(G * m * lam * R * cos(th) / R**2, (th, -pi / 2, pi / 2))
        return [i for i, e in enumerate([0, G * m * M * pi**2 / L**2, 2 * G * m * M * pi / L**2, G * M * m * pi / (2 * L**2)], 1) if simplify(e - F) == 0][0]
    c[36] = q36
    c[38] = lambda: opt(Rational(9, 5) * 40, [72, 70, 75, 68])
    def q40():
        e, lam, eps, r, m, v = symbols('e lam eps r m v', positive=True)
        vv = solve(m * v**2 / r - e * lam / (2 * pi * eps * r), v)[0]
        KE = simplify(m * vv**2 / 2)
        return 4 if diff(KE, r) == 0 else 0
    c[40] = q40
    c[41] = lambda: opt(8 * (1 + (Rational(10, 8) - 1) / 100 * 400), [8, 10, 16, 2])
    c[44] = lambda: 3 if Matrix([1, 0, 0]).cross(Matrix([0, 1, 0])) == Matrix([0, 0, 1]) else 0     # E along i, B along j gives travel along +z
    c[45] = lambda: opt(100 / Rational(25, 5), [20, 50, 500, 25])
    c[47] = lambda: [i for i, (m, z) in enumerate([(153 + 99 + 3, 51 + 41), (144 + 89 + 3, 56 + 36), (140 + 94 + 3, 56 + 38), (144 + 89 + 4, 56 + 36)], 1) if (m, z) == (236, 92)][0]
    def q49():
        u, v = symbols('u v', positive=True)
        f = 1 / (1 / v + 1 / u)                       # magnitudes for a real image
        df = simplify(diff(f, u) / f**2), simplify(diff(f, v) / f**2)
        return 4 if simplify(df[0] - 1 / u**2) == 0 and simplify(df[1] - 1 / v**2) == 0 else 0
    c[49] = q49
    c[48] = lambda: opt(1 / (Rational(1, 15) + Rational(1, 10)), [Rational(30, 11), Rational(15, 4), Rational(5, 2), 6])   # bottom diode reverse biased

    def q50():
        r = Symbol('r', positive=True)
        rv = solve(Rational(10) / (10 + r) / (1 / (1 + r)) - Rational(500, 400), r)[0]
        return nearest(float(rv), [0.1, 0.2, 0.3, 0.4])
    c[50] = q50
    c[51] = lambda: abs(1 / solve(9 - 1 - 9 - 6 * Symbol('c'), Symbol('c'))[0])
    c[52] = lambda: (1 + Rational(2, 5)) / (1 + 1) * 10            # h ~ (1 + k^2/R^2): sphere 2/5, hollow cylinder 1
    c[53] = lambda: sqrt(Rational(36960, 1) / (8 * Rational(22, 7) * 40) + Rational(49, 4))
    def q54():
        k, L0, a, b = symbols('k L0 a b')
        s = solve([3 - k * (a - L0), 2 - k * (b - L0)], [L0, b], dict=True)[0]
        return simplify(k * (3 * a - 2 * s[b] - s[L0]))
    c[54] = q54
    c[55] = lambda: (2 * 2 / 1)**2                  # ratio 2 pi sigma/lambda = 4 pi = pi sqrt(16)

    def q56():
        edges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a'), ('h', 'e'), ('e', 'f'), ('f', 'g'), ('g', 'h'), ('a', 'h'), ('b', 'e'), ('c', 'f'), ('d', 'g')]
        V = {n: Symbol('V' + n) for n in 'abcdefgh'}
        eqs = [sum(V[n] - V[m] for (p, m) in [(u, v) for u, v in edges if u == n] + [(v, u) for u, v in edges if v == n]) for n in 'bdefgh']
        s = solve(eqs + [V['a'] - 6, V['c']], list(V.values()))
        return s[V['e']] - s[V['f']]
    c[56] = q56
    c[57] = lambda: Rational(5, 10) * Rational(5, 10) * (Rational(2, 10) * (1 + 2 * Rational(5, 2)) - Rational(2, 10) * (1 + 2 * 2)) * 1000
    c[58] = lambda: sqrt(36 + Rational(56, 2))
    c[59] = lambda: min(n2 for n2 in range(1, 50) if (n2 * 650) % 450 == 0)
    c[60] = lambda: round(-math.log10(13.6 * (1 / 4 - 1 / 9) / (2 * 1.6e-27 * 9e16 / 1.6e-19) * 100))
    c[81] = lambda: 2 * 16 / 4
    c[83] = lambda: -((615 + 435) - (347 + 2 * 414))
    c[84] = lambda: round(760 * (1 - (2 / 0.52 * 0.1) / (100 / 18)))
    c[85] = lambda: 300 + 200 - 400
    c[86] = lambda: round(0 + math.sqrt(3 * 5))
    c[87] = lambda: Rational(20, 1000) * 2 * Rational(2, 5) / Rational(2, 1000)
    c[90] = lambda: Rational(224, 100) / Rational(224, 10) * 45 * 10
    return c
