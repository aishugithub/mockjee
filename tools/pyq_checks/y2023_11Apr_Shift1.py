"""Answer checks for JEE Main 2023 (Session 2), 11 Apr Shift 1."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        e1, e2, e3 = symbols('e1 e2 e3')
        s = solve([e1 + e2 + e3 - 60, e1 + 2 * e2 + 3 * e3 - (48 + 25 + 18), e3 - 5], [e1, e2, e3])
        return opt(s[e2], [15, 9, 10, 21])
    c[1] = q1

    def q2():
        P, n = Matrix([2, 3, 5]), Matrix([2, 1, -3])
        t = (n.dot(P) - 6) / n.dot(n)
        Q = P - 2 * t * n
        return opt(sum(Q), [12, 10, 9, 5])
    c[2] = q2

    def q3():
        k = symbols('k', positive=True)
        a2, b2 = 1 / k, 1 / k**2
        inv_r2 = simplify(1 / a2 + 1 / b2)
        return opt(sum(inv_r2.subs(k, v) for v in range(1, 21)), [2870, 3080, 3210, 3320])
    c[3] = q3

    c[4] = lambda: opt(sum(1 for a in range(16) for b in range(16) if 0 <= 15 - a - b and len({a, b, 15 - a - b}) == 3), [136, 114, 92, 80])

    def q5():
        cnt = 0
        for v in range(-3, 20):
            X = Rational(v)
            base = X + Rational(7, 2)
            if base <= 0 or base == 1 or 2 * X - 3 == 0 or X == 7:
                continue
            u = ((X - 7) / (2 * X - 3))**2
            if (base > 1 and u >= 1) or (base < 1 and u <= 1):
                cnt += 1
        return opt(cnt, [8, 7, 6, 5])
    c[5] = q5

    def q6():
        al = symbols('al')
        k = 1 / (1 - al)
        sols = solve((k**2 - k)**2 - 4, al)
        sols = [s for s in sols if s.is_real and s not in (1, -1)]
        A = lambda a: Matrix.eye(2) / (1 - a)
        for s in sols:
            assert simplify(A(s).T - s * A(s) - Matrix.eye(2)) == Matrix.zeros(2)
        return opt(sum(sols), [Rational(5, 2), Rational(3, 2), 2, 0])
    c[6] = q6

    def q7():
        f = lambda t: math.floor(t * t - t) + abs(-t + math.floor(t))
        e = 1e-9
        c0 = abs(f(-e) - f(0)) < 1e-6 and abs(f(e) - f(0)) < 1e-6
        c1 = abs(f(1 - e) - f(1)) < 1e-6 and abs(f(1 + e) - f(1)) < 1e-6
        return {(False, False): 1, (True, True): 2, (True, False): 3, (False, True): 4}[(c0, c1)]
    c[7] = q7

    def q8():
        n = Matrix([2, 4, 5]).cross(Matrix([3, -2, 3]))
        d = -n.dot(Matrix([-2, 3, 5]))
        k = Rational(97, d)
        return opt(sum(n * k), [15, 16, 17, 18])
    c[8] = q8

    def q9():
        A = integrate(x**2 / 2 - 2 + sqrt(4 - x**2), (x, -2, 2))
        return opt(simplify(A), [pi - Rational(8, 3), 2 * pi - Rational(16, 3), pi + Rational(8, 3), 2 * pi + Rational(16, 3)])
    c[9] = q9

    def q11():
        n1 = Matrix([1, 1, 0]).cross(Matrix([1, 0, 1]))
        n2 = Matrix([1, -1, 0]).cross(Matrix([0, 1, -1]))
        d = n1.cross(n2)
        b = Matrix([2, -2, 1])
        a = d * 6 / d.dot(b)
        th = acos(a.dot(b) / sqrt(a.dot(a) * b.dot(b)))
        cr = a.cross(b)
        val = (th, sqrt(cr.dot(cr)))
        opts = [(pi / 4, 3 * sqrt(6)), (pi / 3, 6), (pi / 3, 3 * sqrt(6)), (pi / 4, 6)]
        return [i for i, o in enumerate(opts, 1) if simplify(o[0] - val[0]) == 0 and simplify(o[1] - val[1]) == 0][0]
    c[11] = q11

    def q13():
        d = solve(2 + Rational(99, 2) * Symbol('d') - 200, Symbol('d'))[0]
        xs = [2 + (i - 1) * d for i in range(1, 101)]
        ys = [i * (xs[i - 1] - i) for i in range(1, 101)]
        return nearest(float(sum(ys) / 100), [10051.50, 10049.50, 10101.50, 10100])
    c[13] = q13

    def q14():
        w = sympy_I * (5 + 4 * sympy_I) - (-sympy_I) * (3 + 5 * sympy_I)
        from sympy import arg
        return opt(arg(expand(w)), [pi - atan(Rational(33, 5)), -pi + atan(Rational(33, 5)), pi - atan(Rational(8, 9)), -pi + atan(Rational(8, 9))])
    c[14] = q14

    def q15():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.e**t * mpmath.log(mpmath.e**t + mpmath.sqrt(1 + mpmath.e**(2 * t))), [-mpmath.log(2), mpmath.log(2)])
        s5 = mpmath.sqrt(5)
        opts = [mpmath.log((2 + s5)**2 / mpmath.sqrt(1 + s5)) + s5 / 2,
                mpmath.log(mpmath.sqrt(2) * (2 + s5)**2 / mpmath.sqrt(1 + s5)) - s5 / 2,
                mpmath.log(2 * (2 + s5) / mpmath.sqrt(1 + s5)) - s5 / 2,
                mpmath.log(mpmath.sqrt(2) * (3 - s5)**2 / mpmath.sqrt(1 + s5)) + s5 / 2]
        return nearest(v, opts)
    c[15] = q15

    def q16():
        import mpmath
        f = lambda t: 3 * mpmath.cos(t)**4 - 5 * mpmath.cos(t)**2 - 2 * mpmath.sin(t)**6 + 2
        cs = symbols('cs')
        roots = solve(3 * cs**2 - 5 * cs - 2 * (1 - cs)**3 + 2, cs)
        th = set()
        for r in roots:
            for v in solve(cos(x)**2 - r, x):
                for k in range(-3, 4):
                    t = v + k * pi
                    if 0 <= t <= 2 * pi:
                        th.add(simplify(t))
        assert all(abs(f(float(t))) < 1e-9 for t in th)
        return opt(len(th), [8, 9, 10, 12])
    c[16] = q16

    def q17():
        inv = sum(1 for a, b, cc, d in product(range(3), repeat=4) if a * d - b * cc != 0)
        return opt(Rational(inv, 81), [Rational(47, 81), Rational(16, 27), Rational(49, 81), Rational(50, 81)])
    c[17] = q17

    def q18():
        m1, v1, m2, v2 = 5 - 3, 12, 8 + 2, 20
        m = Rational(m1 + m2, 2)
        v = Rational(v1 + v2, 2) + Rational((m1 - m)**2 + (m2 - m)**2, 2)
        return opt(m + v, [38, 32, 36, 40])
    c[18] = q18

    def q20():
        u = symbols('u')
        C = log(Rational(3)) - 2                      # ln|(1+u)/(1-u)| = 2x + C, at (1, 2): |3/(-1)| = 3
        uv = solve((1 + u) / (1 - u) + 3 * exp(2), u)[0]   # same branch (value negative) at x = 2
        assert simplify(log(3 * exp(2)) - (4 + C)) == 0
        e2 = exp(2)
        opts = [3 * e2 / (2 * (3 * e2 - 1)), (1 - 3 * e2) / (2 * (3 * e2 + 1)), (1 + 3 * e2) / (2 * (3 * e2 - 1)), 3 * e2 / (2 * (3 * e2 + 1))]
        return opt(uv / 2, opts)
    c[20] = q20

    c[21] = lambda: Rational(sum(math.comb(9, r) * 2**(9 - r) for r in range(1, 8)), 7)

    def q22():
        d = Matrix([1, 2, 3]).cross(Matrix([2, 2, 1]))
        t, l, mu = symbols('t l mu')
        s = solve(list(t * d - (Matrix([1, -11, -7]) + l * Matrix([1, 2, 3]))), [t, l])
        P = d * s[t]
        Q = Matrix([-1, 0, 1]) + mu * Matrix([2, 2, 1])
        mv = solve((Q - P).dot(Matrix([2, 2, 1])), mu)[0]
        return 9 * sum(Q.subs(mu, mv))
    c[22] = q22

    c[23] = lambda: sum(1 for p, q, r in product([True, False], repeat=3) if (not ((p or q) and (p or r))) or (q or r))

    def q24():
        a, b = solve(x**2 - 7 * x - 1, x)
        S = lambda n: a**n + b**n
        return simplify(expand(S(21) + S(17)) / expand(S(19)))
    c[24] = q24

    def q25():
        S = sum(Rational(109 - k, 5**k) for k in range(109))
        return 16 * S - Rational(1, 25**54)
    c[25] = q25

    def q26():
        F = x**11 * (1 + 3 * x)**6
        return Rational(F.subs(x, 2), 14**6)
    c[26] = q26

    c[27] = lambda: sum(1 for r in range(681) if (680 - r) % 2 == 0 and r % 4 == 0)

    def q28():
        for n in range(2, 200, 2):
            e2 = Rational(2 * (n + 2), n + 1)
            if sqrt(e2).is_rational:
                a = sqrt(1 + n); b2 = 3 + n
                return 21 * 2 * b2 / a
    c[28] = q28

    def q29():
        a, cc = symbols('a c', real=True)
        A = Matrix([[0, 1, 2], [a, 0, 3], [1, cc, 0]])
        sols = solve(list(A**3 - A), [a, cc], dict=True)
        av = [s[a] for s in sols if s[a] > 0][0]
        return math.ceil(float(av))
    c[29] = q29

    c[30] = lambda: sum(1 for p in __import__('itertools').permutations(range(5)) if all(p[i] != i for i in range(5)))
    c[31] = lambda: nearest(4000**2 / (2 * 6.4e6) / 1e-2, [1.25, 12.5, 125, 1250])

    def q34():
        h, cc, l, phi, V = symbols('h c l phi V', positive=True)
        s = solve([h * cc / l - phi - V, h * cc / (2 * l) - phi - V / 4], [phi, V], dict=True)[0]
        return opt(simplify(h * cc / s[phi] / l), [4, Rational(3, 2), 3, Rational(1, 4)])
    c[34] = q34
    c[35] = lambda: nearest(3e8 / math.sqrt(2) / 1e7, [21.2, 3.12, 5, math.sqrt(2) * 10])
    c[37] = lambda: nearest(0.5 * 8.85e-12 * 20**2 * 5e-4 / 1e-13, [8.85, 88.5, 28.5, 17.7])
    c[40] = lambda: opt(Rational(2, 1) / Rational(1, 2), [Rational(1, 4), 4, Rational(1, 2), 2])
    c[41] = lambda: opt(Rational(Rational(1, 2) * 4 * Rational(1, 4), Rational(1, 2) * 2), [Rational(1, 2), 2, Rational(2, 3), Rational(1, 4)])
    c[44] = lambda: nearest(2257 - 1e5 * (1.671 - 1e-3) / 1000, [-2090, 2090, -2426, 2476])
    c[45] = lambda: opt(32 + 180 * Rational(-95 + 15, 80), [-48, -63, -112, -148])
    c[46] = lambda: opt(Rational(1 * 1, Rational(1, 3) * 4), [Rational(3, 16), Rational(4, 3), Rational(3, 4), Rational(1, 16)])

    def q47():
        pts = [(0, 0), (5, 10), (10, 10), (15, 20), (20, 0), (25, -20)]
        dist = disp = 0
        for (t1, v1), (t2, v2) in zip(pts, pts[1:]):
            a = Rational(v1 + v2, 2) * (t2 - t1)
            disp += a; dist += abs(a)
        return opt(dist / disp, [1, Rational(1, 2), Rational(5, 3), Rational(3, 5)])
    c[47] = q47
    c[48] = lambda: opt(1 * 2**2, [1, 2, 4, 8])
    c[49] = lambda: opt(Rational(125, 1) / (Rational(1, 100) * 250), [5, 100, 50, 25])
    c[51] = lambda: round(13.6 * (1 - 1 / 16) / 4.25e-15 / 1e15, 6)
    c[52] = lambda: round((1.8 - 1) / (1.8 / 1.5 - 1), 6)
    c[53] = lambda: 4 * 2
    def q54():
        I = Rational(8 - 4) / (Rational(1, 2) + 1 + Rational(9, 2) + 2)
        return I * Rational(6, 9) * 3
    c[54] = q54
    c[55] = lambda: round(math.sqrt(9e9 * (2e-6)**2 / (2 * 0.02 * 10)) * 1000)
    c[56] = lambda: round(160 / 0.5 * 3.6)
    def q57():
        L, a = symbols('L a')
        l1, l2 = L + 100 * a, L + 120 * a
        Lv = solve(10 * l2 - 11 * l1, L)[0]
        return simplify(l1.subs(L, Lv) / Lv)
    c[57] = q57
    c[58] = lambda: round(Rational(7, 5) / (Rational(2, 5) * 10) * 100)
    c[59] = lambda: integrate(2 + 3 * x, (x, 0, 4))
    c[60] = lambda: 8 * 10 / (2 * Rational(1, 2))
    c[81] = lambda: round((0.25 * 200 + 0.40 * 500) / 700 * 100)
    c[82] = lambda: round(3.0 * 6.02e23 * (300e-10)**3 / 12)
    c[83] = lambda: round(860 / (2 * 56 + 3 * 16 + 2 * 27))
    c[84] = lambda: round((0.01 / 0.004 - 1) / 2 * 100)
    c[85] = lambda: round(0.4**2 / 0.6**2 * 100)
    def q86():
        m, n = symbols('m n')
        E42 = (4 * n - 2 * m) / 2                    # Pb4+ + 2e -> Pb2+
        val = -E42                                   # E(Pb2+/Pb4+) read as oxidation potential = m - x n
        return solve(val - (m - Symbol('X') * n), Symbol('X'))[0]
    c[86] = q86
    c[87] = lambda: round((10 - 8.8) / 1800 / 2 / 1e-6)

    def q33():
        lA, lB = symbols('lA lB', positive=True)
        sol = solve(log(2) / lA - 1 / lB, lA)[0]           # T_half(A) = mean life(B)
        opts = [lB / log(2), lB * log(2), lB, 2 * lB]          # lambda_A from each option
        return opt(sol, opts)
    c[33] = q33
    c[38] = lambda: nearest(2e-2 * 100, [2, 0.2, 1, 0.1])
    c[39] = lambda: nearest(100 * (1.25 * 1 / 1 - 1), [25, -25, 0, -50])   # S_V = S_I / R, R unchanged
    def q43():
        M = {'mono': 20.2, 'dia': 71.0, 'poly': 352.0}
        v = {k: math.sqrt(3 * 8.314 * 300 / (m / 1000)) for k, m in M.items()}
        return 1 if v['mono'] > v['dia'] > v['poly'] else 0
    c[43] = q43
    def q63():
        ag, i_ = 25 * 1, 25 * Rational(105, 100)
        excess_I = i_ - ag
        conc_I = excess_I / 50
        assert conc_I < Rational(1, 10) < Rational(1, 2)          # I- left is small; K+ (0.525 M), NO3- (0.5 M) are not
        return 2
    c[63] = q63
    return c
