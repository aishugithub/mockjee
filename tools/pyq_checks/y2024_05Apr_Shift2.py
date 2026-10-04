"""Answer checks for JEE Main 2024 (Session 2), 5 Apr Shift 2. Q63 is disputed (not checked here)."""
from pyq_checks.common import *
from sympy import Function, Eq, N, dsolve, floor, Abs, im, re


def checks():
    c = {}
    c[1] = lambda: opt(math.comb(9, 3) * math.comb(6, 3), [1710, 1520, 1680, 1640])

    def q3():
        n = 800; cnt = 0
        for i in range(n):
            for j in range(n):
                X, Y = -5 + (i + .5) * 10 / n, -5 + (j + .5) * 10 / n
                z = complex(X, Y)
                if abs(z) <= 5 and X >= 0 and ((z + 1 - 3**.5 * 1j) / (1 - 3**.5 * 1j)).imag >= 0:
                    cnt += 1
        return nearest(cnt * (10 / n)**2, [125 * math.pi / 24, 125 * math.pi / 4, 125 * math.pi / 6, 125 * math.pi / 12])
    c[3] = q3

    def q4():
        m, n = symbols('m n')
        M = Matrix([[1, 1, 1], [2, 5, 5], [1, 2, m]])
        mv = solve(M.det(), m)[0]
        aug = M.subs(m, mv).row_join(Matrix([4, 17, n]))
        nv = solve(aug[:, [0, 1, 3]].det(), n)[0]
        assert aug.subs(n, nv).rank() == 2
        e = [mv**2 + nv**2 + mv * nv - 68, mv**2 + nv**2 - mv * nv - 39, mv**2 + nv**2 + mv + nv - 64, mv**2 + nv**2 - mv - nv - 46]
        return [i for i, v in enumerate(e, 1) if v == 0][0]
    c[4] = q4

    def q5():
        a, b = symbols('a b')
        A = Matrix([[b, a, 3], [a, a, b], [-b, a, 2 * a]])
        B = Matrix([[3 * a, -9, 3 * a], [-a, 7, -2 * a], [-2 * a, 5, -2 * b]])
        C = A.adjugate().T
        sols = [s for s in solve([C[0, 0] - B[0, 0], C[0, 1] - B[0, 1]], [a, b], dict=True) if s[a] * s[b] != 0]
        s = [s for s in sols if C.subs(s) == B.subs(s)][0]
        return opt((A * B).subs(s).det(), [125, 64, 216, 343])
    c[5] = q5

    def q6():
        from itertools import permutations
        words = sorted(set(''.join(p) for p in permutations('BHBJO')))
        assert len(words) == 60
        return [i for i, w in enumerate(['OBBHJ', 'OBBJH', 'HBBJO', 'JBBOH'], 1) if w == words[49]][0]
    c[6] = q6
    c[7] = lambda: opt(sum(1 for a in range(1, 7) for b in range(1, 7) for cc in range(1, 7) if b * b > 4 * a * cc), [19, 38, 57, 76])

    def q8():
        K = lambda t: 4 ** (1 + t) + 4 ** (1 - t) + 16 ** t + 16 ** (-t)
        return nearest(min(K(i / 1000) for i in range(0, 3000)), [10, 8, 4, 16])
    c[8] = q8

    def q9():
        e = expand((Rational(3)**Rational(1, 5) / x + 2 * x / Rational(5)**Rational(1, 3))**12)
        const = e.as_independent(x)[0]
        al = simplify(const / (2**8 * Rational(3)**Rational(1, 5)))
        return opt(25 * al, [742, 639, 724, 693])
    c[9] = q9

    def q10():
        f = lambda t: 2 * t * t + t + math.floor(t * t + 1e-12) - math.floor(t + 1e-12)
        pts = [-1, 0, 1, math.sqrt(2), math.sqrt(3), 2]
        bad = 0
        for p in pts:
            vals = [f(p)]
            if p > -1: vals.append(f(p - 1e-9))
            if p < 2: vals.append(f(p + 1e-9))
            if max(vals) - min(vals) > 1e-6: bad += 1
        return opt(bad, [6, 5, 4, 3])
    c[10] = q10

    def q11():
        import mpmath
        lhs = mpmath.quad(lambda t: (1 - t**10)**20, [0, 1])
        assert abs(lhs - mpmath.beta(0.1, 21) / 10) < 1e-12
        return opt(100 * (Rational(1, 10) + Rational(1, 10) + 21), [2120, 2012, 1021, 1120])
    c[11] = q11
    c[12] = lambda: opt(integrate(-x**2 - 2 * x, (x, -2, 0)), [1, Rational(2, 3), Rational(4, 3), Rational(8, 3)])

    def q13():
        g, y, p = symbols('g y p')                  # p = y'
        F = x**2 + y**2 + 2 * g * (x + y)
        gv = solve(diff(F.subs(y, Function('Y')(x)), x).subs(Function('Y')(x).diff(x), p).subs(Function('Y')(x), y), g)[0]
        de = simplify(numer(together(F.subs(g, gv))))
        opts = [((x**2 - y**2 + 2 * x * y), (x**2 - y**2 - 2 * x * y)), ((x**2 + y**2 - 2 * x * y), (x**2 + y**2 + 2 * x * y)),
                ((x**2 - y**2 + 2 * x * y), (x**2 - y**2 + 2 * x * y)), ((x**2 + y**2 + 2 * x * y), (x**2 + y**2 - 2 * x * y))]
        return [i for i, (P, Q) in enumerate(opts, 1) if simplify(de.subs(p, P / Q)) == 0][0]
    from sympy import numer, together
    c[13] = q13

    def q14():
        r = Symbol('r', positive=True)
        rv = [v for v in solve(2 * (2 - r)**2 - r**2, r) if v < 2][0]
        return [i for i, e in enumerate([r - 1, r**2 - 8 * r + 8, 2 * r**2 - 8 * r + 7, 2 * r**2 - 4 * r + 1], 1) if simplify(e.subs(r, rv)) == 0][0]
    c[14] = q14

    def q15():
        y = Symbol('y')
        chord = expand((x**2 + y**2 - 2 * (x + y) + 1) - ((x + 1)**2 + y**2 - 4))
        Py = solve(chord.subs(x, 0), y)[0]
        return opt(1 + (Py - 1)**2, [1, 2, 4, 6])
    c[15] = q15

    def q16():
        X, Y = symbols('X Y')
        area2 = (2 + 1) * (Y - 1) - (3 - 1) * (X + 1)
        assert area2.subs({X: 0, Y: 10}) > 0                        # points above AB give + sign
        line = expand((area2 - 20) * Rational(15, 25))              # a X + b Y = 15 after scaling
        a, b = line.coeff(X), line.coeff(Y)
        assert line.subs({X: 0, Y: 0}) == -15
        return opt(5 * a + 2 * b, [4, 6, Rational(-6, 5), Rational(-12, 5)])
    c[16] = q16

    def q17():
        A, d, P = Matrix([1, -1, 2]), Matrix([2, 3, 5]), Matrix([8, 5, 7])
        F = A + d * (P - A).dot(d) / d.dot(d)
        return opt(sum(2 * F - P), [20, 18, 16, 14])
    c[17] = q17

    def q18():
        l = Symbol('l')
        a, b, i = Matrix([2, 5, -1]), Matrix([2, -2, 2]), Matrix([1, 0, 0])
        cc = l * (2 * a + b + i) - i
        assert simplify((cc + i).cross(a + b + i) - a.cross(cc + i)) == Matrix([0, 0, 0])
        lv = solve(a.dot(cc) + 29, l)[0]
        return opt(cc.subs(l, lv).dot(Matrix([-2, 1, 1])), [15, 12, 10, 5])
    c[18] = q18

    def q19():
        best = min(27 * ((2 / (3 * math.sin(t)))**2 + 4) for t in [k / 10000 * math.pi / 3 for k in range(1, 10001)])
        return nearest(best, [105, 124, 110, 121])
    c[19] = q19

    def q20():
        t = Symbol('t')
        y = (2 * cos(t) + cos(2 * t)) / (cos(3 * t) + 4 * cos(2 * t) + 5 * cos(t) + 2)
        v = (diff(y, t, 2) + diff(y, t) + y).subs(t, pi / 2)
        return opt(simplify(v), [Rational(1, 2), 1, Rational(3, 2), 2])
    c[20] = q20

    def q21():
        import mpmath
        g = lambda t: mpmath.sin(t)**2 + (2 + 2 * t - t * t) * mpmath.sin(t) - 3 * (t - 1)**2
        xs = [-math.pi + k * 2 * math.pi / 20000 for k in range(20001)]
        return sum(1 for u, v in zip(xs, xs[1:]) if g(u) * g(v) < 0)
    c[21] = q21

    def q22():
        import mpmath
        mpmath.mp.dps = 30
        r = (mpmath.sqrt(3) - mpmath.sqrt(2)) / mpmath.sqrt(3)
        terms = [1, (mpmath.sqrt(3) - mpmath.sqrt(2)) / (2 * mpmath.sqrt(3)), (5 - 2 * mpmath.sqrt(6)) / 18,
                 (9 * mpmath.sqrt(3) - 11 * mpmath.sqrt(2)) / (36 * mpmath.sqrt(3)), (49 - 20 * mpmath.sqrt(6)) / 180]
        assert all(abs(terms[n] - r**n / (n * (n + 1))) < 1e-25 for n in range(1, 5))
        S_ = 1 + mpmath.nsum(lambda n: r**n / (n * (n + 1)), [1, mpmath.inf])
        a, b = [(a, b) for a in range(1, 10) for b in range(1, 10) if math.gcd(a, b) == 1
                and abs(2 + (mpmath.sqrt(mpmath.mpf(b) / a) + 1) * mpmath.log(mpmath.mpf(a) / b) - S_) < 1e-20][0]
        return 11 * a + 18 * b
    c[22] = q22

    def q23():
        a = [v for v in solve(2 * x**2 + x - 2, x) if v > 0][0]
        import mpmath
        mpmath.mp.dps = 40
        av = mpmath.mpf(str(N(a, 50)))
        t = 1 / av + mpmath.mpf('1e-12')
        L = 16 * (1 - mpmath.cos(2 + t - 2 * t * t)) / (1 - av * t)**2
        hits = [(al, be) for al in range(0, 300) for be in range(0, 40) if abs(al + be * mpmath.sqrt(17) - L) < 1e-6]
        return sum(hits[0])
    c[23] = q23

    def q24():
        vals = [(math.sqrt(max(0, 8 * t - t * t - 12)) - 4)**2 + (t - 7)**2 for t in [2 + 4 * k / 400000 for k in range(400001)]]
        M, m = max(vals), min(vals)
        return round(M * M - m * m, 3)
    c[24] = q24

    def q25():
        import mpmath
        f = lambda t: mpmath.quad(lambda u: 2 * u / (1 - mpmath.cos(t)**2 * mpmath.sin(u)**2), [0, mpmath.pi / 2, mpmath.pi])
        assert abs(f(1) - mpmath.pi**2 / mpmath.sin(1)) < 1e-9
        return integrate(sin(Symbol('t')), (Symbol('t'), 0, pi / 2))
    c[25] = q25

    def q26():
        y = Function('y')
        s = dsolve(Eq(y(x).diff(x) + 2 * x / (1 + x**2)**2 * y(x), x * exp(1 / (1 + x**2))), y(x), ics={y(0): 0})
        f = simplify(s.rhs * exp(-1 / (1 + x**2)))
        r = solve(f - x - 4, x)
        return integrate(x + 4 - f, (x, min(r), max(r)))
    c[26] = q26

    def q27():
        m = Rational(-1, 2)
        P = Matrix([9 + 1 / m**2, 2 / m])
        y = Symbol('y')
        assert P[1]**2 == 4 * (P[0] - 9)
        return (P - Matrix([7, 4])).norm()
    c[27] = q27

    def q28():
        s, t = symbols('s t')
        P1 = Matrix([-2 - 3 * s, 2 + 4 * s, 5 + 2 * s]); P2 = Matrix([-2 - t, -6 + 2 * t, 1])
        sol = solve([(P1 - P2).dot(Matrix([-3, 4, 2])), (P1 - P2).dot(Matrix([-1, 2, 0]))], [s, t])
        A, B = P1.subs(sol), P2.subs(sol)
        k = (-1 - A[0]) / (B[0] - A[0])
        Q = A + k * (B - A)
        return (Q[1] - Q[2])**2
    c[28] = q28

    def q29():
        al = Symbol('al')
        K = 1 - Rational(1, 3) - Rational(1, 6) - Rational(1, 4)
        mu = al / 3 + K - Rational(3, 4)
        var = al**2 / 3 + K + Rational(9, 4) - mu**2
        sols = [v for v in solve(var - (mu + 2)**2, al) if v != 0]
        return (sqrt(var) + mu).subs(al, sols[0])
    c[29] = q29

    def q30():
        roots = set()
        for lo, hi, e in [(-5, oo, x * (x + 5) + 2 * (x + 7) - 2), (-7, -5, -x * (x + 5) + 2 * (x + 7) - 2), (-oo, -7, -x * (x + 5) - 2 * (x + 7) - 2)]:
            for r in solve(e, x):
                if r.is_real and lo <= r <= hi:
                    roots.add(r)
        return len(roots)
    c[30] = q30

    c[32] = lambda: opt((2 * pi * 120 / 180)**2 * 9, [0, 4 * pi**2, 16 * pi**2, 57600 * pi**2])
    c[33] = lambda: nearest(0.3 * 50 * 9.8, [1.47, 14.7, 147, 1470])
    c[36] = lambda: opt(Rational(1, 10) * 20, [5, 2, 1, Rational(1, 2)])
    c[37] = lambda: nearest(4.2e4 * ((6 / 24)**2 * (1 / 4))**(1 / 3), [1.4e4, 8.4e4, 1.05e4, 1.68e5])
    c[41] = lambda: nearest(31.4 / (2 * math.pi * 50 * 0.01), [10, 0.01, 63, 68])
    c[42] = lambda: opt(Rational(10, 5), [Rational(1, 2), 2, 1, 4])
    c[46] = lambda: nearest(0.02 * 100 / (10 - 0.02) * 100, [20, 2, 200, 800])
    c[49] = lambda: opt(solve(Symbol('g') / (Symbol('g') - 1) - 3, Symbol('g'))[0], [Rational(3, 2), Rational(5, 3), Rational(7, 5), Rational(9, 7)])
    c[51] = lambda: 64 / 4
    c[52] = lambda: Rational(1, 3) / (Rational(1, 2) + Rational(1, 3)) * 5
    c[53] = lambda: round(550e-9 * 1 / 0.2e-3 / 1e-5, 6)
    c[54] = lambda: round(10 * (14 / 1.4)**2, 6)
    c[55] = lambda: 90 * 400 / 600
    c[56] = lambda: 5 * (2 * 2 / (2 + 2))
    c[57] = lambda: round(6.28e-3 * 0.5 / (4 * math.pi * 1e-7 * 5))
    c[58] = lambda: Rational(2, 1) / Rational(1, 8)
    c[59] = lambda: 12 / 3
    c[60] = lambda: Rational(36 * 915, 5)
    c[61] = lambda: opt(Rational(11, 44), [Rational(1, 4), Rational(1, 2), Rational(3, 4), Rational(35, 100)])
    c[64] = lambda: 2 if 0.34 - 0.46 < 0 else 1
    c[71] = lambda: opt(sum(1 for n in (0, 0, 2, 5, 7) if n <= 2), [4, 3, 2, 1])   # e set holds 2 electrons in tetrahedral high spin
    c[81] = lambda: sum(1 for l in range(4) for m in range(-l, l + 1) if abs(m) == 1)
    c[83] = lambda: -2 * (6 * -393.5 + 3 * -286 - 48.5)
    c[84] = lambda: round(1.86 * 0.1 * (1 + math.sqrt(6.25e-5 / 0.1)) * 100)
    c[85] = lambda: round(1.5**2 * 0.7 / (0.5**2 * 0.2) * 10)
    c[86] = lambda: round(0 + math.sqrt(5 * 7))
    c[87] = lambda: round(351 / (17 * 12 + 14 + 16) * 2 * 106)
    c[88] = lambda: round(5 / 12.5 / (10 / 12.5) * 100)
    c[90] = lambda: round(0.2 * 45, 6)

    def q35():
        t, P, m = symbols('t P m', positive=True)
        v = sqrt(2 * P * t / m)
        xx = integrate(v, (t, 0, t))
        return opt(simplify(diff(log(xx), t) * t), [1, Rational(3, 2), Rational(2, 3), 2])
    c[35] = q35
    return c
