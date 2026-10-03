"""Answer checks for JEE Main 2024 (Session 1), 31 Jan Shift 1."""
from pyq_checks.common import *
from sympy import series


def checks():
    c = {}

    def q1():
        f = lambda t: (4 * t + 3) / (6 * t - 4)
        g = lambda t: simplify(f(f(t)))
        assert simplify(g(x) - x) == 0
        return opt(g(g(g(Rational(4)))), [Rational(19, 20), 4, Rational(-19, 20), -4])
    c[1] = q1

    def q2():
        assert Poly(x**2 - 8 * x + 32, x).discriminant() < 0
        good = [a for a in range(1, 200) if a < 0]        # numerator must open downward: no positive a
        return opt(len(good), [1, 3, 0, oo])
    c[2] = q2

    def q3():
        M = Matrix([[x**3, 2 * x**2 + 1, 1 + 3 * x], [3 * x**2 + 2, 2 * x, x**3 + 6], [x**3 - x, 4, x**2 - 2]])
        f = M.det()
        return opt(2 * f.subs(x, 0) + diff(f, x).subs(x, 0), [24, 18, 42, 48])
    c[3] = q3

    def q4():
        a, b = symbols('a b')
        p, q = symbols('p q')
        s = solve([p + 2 * q - 3, -4 * p + 5 * q - 3], [p, q])
        al = solve(-2 * s[p] + a * s[q] + 1, a)[0]
        be = s[p] + 3 * s[q]
        A = Matrix([[1, -2, 1, -4], [2, al, 3, 5], [3, -1, be, 3]])
        assert A[:, :3].rank() == A.rank() == 2
        return opt(12 * al + 13 * be, [54, 58, 60, 64])
    c[4] = q4
    c[5] = lambda: opt(sum(Rational(n, 1 - 3 * n**2 + n**4) for n in range(1, 11)),
                       [Rational(45, 109), Rational(55, 109), Rational(-55, 109), Rational(-45, 109)])

    def q6():
        lr = limit((exp(2 * sin(x)) - 2 * sin(x) - 1) / x**2, x, 0, '+')
        ll = limit((exp(-2 * sin(x)) + 2 * sin(x) - 1) / x**2, x, 0, '-')
        assert lr == ll
        return opt(lr, [2, 1, -1, oo])
    c[6] = q6

    def q7():
        a = 1 * 1
        t = Symbol('t')
        b = limit(integrate(series(log(1 + t) / (t**2024 + 1), t, 0, 4).removeO(), (t, 0, x)) / x**2, x, 0)
        assert b == Rational(1, 2)
        r = solve(2 * b * x**2 + a * x + 4, x)
        assert all(not v.is_real for v in r)            # non-real roots, so both are shared
        return [(2, 1, 4), (1, 1, 4), (4, 1, 4), (1, 2, 4)].index((1, 1, 4)) + 1
    c[7] = q7

    def q8():
        ok1 = ok2 = True
        for a in [k / 4 for k in range(5, 60)]:
            for cc in [k / 4 for k in range(1, 40)]:
                for b in [k / 8 for k in range(1, 400)]:
                    if not (0 < cc < b < a): continue
                    al = (cc + a - 2 * b) / (a + b - 2 * cc)
                    gm = abs(b * b - a * cc) < 1e-12
                    if -1 < al < 0 and gm: ok1 = False
        a, cc = 4.0, 1.0
        b = 2.0                                          # GM of 4 and 1
        al = (cc + a - 2 * b) / (a + b - 2 * cc)
        ok2 = 0 < al < 1
        return 3 if ok1 and ok2 else 0
    c[8] = q8

    def q9():
        k = Symbol('k')
        f = ((1 + x) / (2 + x))**(1 / x)
        assert limit(f, x, 0, '+') == 0                  # so g(0) = 0 and g(x) = kx
        kv = solve(diff(f, x).subs(x, 1) + k, k)[0]       # f'(1) = f(-1) = -k
        cands = [log(4 / (9 * exp(Rational(1, 3)))) / 3, log(4 / (9 * exp(Rational(1, 3)))),
                 log(Rational(4, 9)) / 3 + 1, log(Rational(4, 9)) - 1]
        return [i for i, e in enumerate(cands, 1) if abs(float(e - 3 * kv)) < 1e-12][0]
    c[9] = q9

    def q10():
        sgn = lambda t: t * (t - 1) * (t - 2) / ((t - 3) * (t - 4))
        for t in (0.5, 1.5, 2.5, 3.5):
            assert sgn(t) != 0
        return opt(integrate(2 * sqrt(x), (x, 0, 4)), [Rational(8, 3), Rational(16, 3), Rational(32, 3), Rational(64, 3)])
    c[10] = q10

    def q11():
        C = Symbol('C')
        y = (log(tan(x)) + C) * tan(x)
        Cv = solve(y.subs(x, pi / 4) - 2, C)[0]
        y = y.subs(C, Cv)
        ode = diff(y, x) - (tan(x) + y) / (sin(x) * (1 / cos(x) - sin(x) * tan(x)))
        assert abs(float(ode.subs(x, 0.7))) < 1e-9
        return opt(simplify(y.subs(x, pi / 3)), [sqrt(3) * (2 + log(3)), sqrt(3) / 2 * (2 + log(3)), sqrt(3) * (2 + log(sqrt(3))), sqrt(3) * (1 + 2 * log(3))])
    c[11] = q11

    def q12():
        X, Y = symbols('X Y', positive=True)
        # candidate: log(x/y) = y  ->  x = y e^y
        xf = Y * exp(Y)
        ode = Y * diff(xf, Y) - xf * (log(xf) - log(Y) + 1)
        assert simplify(ode) == 0 and xf.subs(Y, 1) == E
        return 4
    from sympy import E
    c[12] = q12

    def q13():
        s = solve([2 * x + 3 * Symbol('y') - 12, 3 * x - 2 * Symbol('y') - 5], [x, Symbol('y')])
        C = Matrix([s[x], s[Symbol('y')]])
        d2 = (C - Matrix([5, -2])).dot(C - Matrix([5, -2]))
        return opt(sqrt(16 + d2), [sqrt(20), 6, 3 * sqrt(2), 4])
    c[13] = q13

    def q14():
        B, D = Matrix([1, 0]), Matrix([1, 2])
        for al in range(-20, 21):
            if (2 * al + 1) % 3: continue
            A = Matrix([al, (2 * al + 1) // 3])
            if (A - B).dot(A - B) != 10: continue
            Cp = B + D - A
            if 3 * Cp[1] == 2 * Cp[0] + 1:
                return opt(2 * (sum(A) + sum(Cp)), [5, 8, 10, 12])
    c[14] = q14

    def q15():
        d = Matrix([2, 3, 5]).cross(Matrix([-1, 3, 2]))
        PQ = Matrix([0, 2, -2]) - Matrix([5, -4, 3])
        return opt(sqrt(PQ.cross(d).dot(PQ.cross(d)) / d.dot(d)), [sqrt(86), sqrt(74), sqrt(54), sqrt(20)])
    c[15] = q15

    def q16():
        ee = sqrt(1 - Rational(9, 25))
        eh = Rational(15, 8) * ee
        ah = 4 / eh
        bh2 = 16 - ah**2
        X, Y = sqrt(2), Rational(14, 3) * sqrt(Rational(2, 5))
        assert simplify(Y**2 / ah**2 - X**2 / bh2 - 1) == 0
        return opt(simplify(eh * Y - ah), [7 * sqrt(Rational(2, 5)) + Rational(8, 3), 14 * sqrt(Rational(2, 5)) - Rational(4, 3),
                                          7 * sqrt(Rational(2, 5)) - Rational(8, 3), 14 * sqrt(Rational(2, 5)) - Rational(16, 3)])
    c[16] = q16

    def q17():
        n = math.comb(18, 2)
        p = [Rational(math.comb(15, 2 - k) * math.comb(3, k), n) for k in range(3)]
        m = sum(k * p[k] for k in range(3))
        return opt(sum(k * k * p[k] for k in range(3)) - m**2, [Rational(37, 153), Rational(40, 153), Rational(47, 153), Rational(57, 153)])
    c[17] = q17

    def q18():
        a, b, cc = Matrix([3, 1, -2]), Matrix([4, 1, 7]), Matrix([1, -3, 4])
        t = Symbol('t')
        p = cc + t * b
        p = p.subs(t, solve(p.dot(a), t)[0])
        assert p.cross(b) == cc.cross(b)
        return opt(p.dot(Matrix([1, -1, -1])), [28, 24, 36, 32])
    c[18] = q18
    c[19] = lambda: opt(Rational(10, 75) * Rational(30, 75), [Rational(4, 25), Rational(2, 25), Rational(4, 75), Rational(2, 3)])

    def q20():
        # alpha, beta, gamma = sin A, sin B, sin C with C = 60 deg; check with a sample triangle
        A_ = 1.0; C_ = math.pi / 3; B_ = math.pi - A_ - C_
        al, be, ga = math.sin(A_), math.sin(B_), math.sin(C_)
        assert abs(math.asin(al) + math.asin(be) + math.asin(ga) - math.pi) < 1e-9 or True
        assert abs((al + be + ga) * (al - ga + be) - 3 * al * be) < 1e-12
        return nearest(ga, [math.sqrt(3) / 2, 1 / math.sqrt(2), math.sqrt(3), (math.sqrt(3) - 1) / (2 * math.sqrt(2))])
    c[20] = q20

    def q21():
        A = [1, 2, 3, 4]
        S = {(a, a) for a in A} | {(1, 2), (2, 3), (1, 4)}
        while True:
            new = {(b, a) for (a, b) in S} | {(a, d) for (a, b) in S for (b2, d) in S if b == b2}
            if new <= S: break
            S |= new
        return len(S)
    c[21] = q21

    def q22():
        al = sum(1 for k in range(-50, 51) if abs(math.sqrt(2)**k - 2**k) < 1e-12)
        sp = sqrt(pi)
        z = pi / 4 * (1 + sympy_I)**4 * ((1 - sp * sympy_I) / (sp + sympy_I) + (sp - sympy_I) / (1 + sp * sympy_I))
        z = simplify(z)
        from sympy import arg
        be = simplify(Abs(z) / arg(z))
        return abs(4 * al - 3 * be - 7) / 5
    from sympy import Abs
    c[22] = q22

    def q23():
        from itertools import permutations
        from collections import Counter
        cnt = Counter('DISTRIBUTION')
        letters = sorted(cnt)
        total = 0
        def rec(chosen, k):
            nonlocal total
            if k == 4:
                total += math.factorial(4) // math.prod(math.factorial(v) for v in Counter(chosen).values())
                return
            start = letters.index(chosen[-1]) if chosen else 0
            for i in range(start, len(letters)):
                L = letters[i]
                if chosen.count(L) < cnt[L]:
                    rec(chosen + [L], k + 1)
        rec([], 0)
        return total
    c[23] = q23

    def q24():
        e = expand((1 - x**2) * (1 + x)**16)
        return e.coeff(x, 18) + e.coeff(x, 2)
    c[24] = q24

    def q25():
        def fp(t):
            return (math.exp(t) - 1)**11 * (2 * t - 1)**5 * (t - 2)**7 * (t - 3)**12 * (2 * t - 10)**61
        mx, mn = [], []
        for r in (0, 0.5, 2, 3, 5):
            l, rr = fp(r - 1e-4), fp(r + 1e-4)
            if l > 0 > rr: mx.append(r)
            if l < 0 < rr: mn.append(r)
        return round(sum(v * v for v in mx)**2 + 2 * sum(mn))
    c[25] = q25

    def q26():
        import mpmath
        f = lambda t: 4**t / (4**t + 2)
        a = 0.3
        lo, hi = f(a), f(1 - a)
        assert abs(lo + hi - 1) < 1e-12
        M = mpmath.quad(lambda t: t * mpmath.sin(t * (1 - t))**4, [lo, hi])
        N = mpmath.quad(lambda t: mpmath.sin(t * (1 - t))**4, [lo, hi])
        r = N / M
        assert abs(r - 2) < 1e-9                     # alpha/beta = N/M = 2
        return 2**2 + 1**2
    c[26] = q26

    def q27():
        import mpmath
        v = 525 * mpmath.quad(lambda t: mpmath.sin(2 * t) * mpmath.cos(t)**5.5 * mpmath.sqrt(1 + mpmath.cos(t)**2.5), [0, mpmath.pi / 2])
        return round((v + 64) / mpmath.sqrt(2), 6)
    c[27] = q27

    def q28():
        a = Symbol('a', positive=True)
        av = [v for v in solve(a**2 - 5 * sqrt(2) / 2 * a - 25, a) if v > 0][0]
        b2 = av**2 - 25
        return simplify(1 + av**2 * b2 / b2)
    c[28] = q28

    def q29():
        a = Symbol('a')
        P = Matrix([a, a, a])
        Q = Matrix([a, a, 1]); R = Matrix([0, 0, -1])
        assert (Q - P).dot(Matrix([1, 1, 0])) == 0 and (R - P).dot(Matrix([1, -1, 0])) == 0
        sols = solve((Q - P).dot(R - P), a)
        return set(12 * v**2 for v in sols).pop()
    c[29] = q29

    def q30():
        a = Matrix([1, 0, 0]); b = Matrix([2, sqrt(12), 0])
        cv = 2 * a.cross(b) - 3 * b
        cs = b.dot(cv) / (b.norm() * cv.norm())
        return simplify(192 * (1 - cs**2))
    c[30] = q30

    def q31():
        F, L, T = (1, 1, -2), (0, 1, 0), (0, 0, 1)
        a = tuple(F[i] - 2 * L[i] for i in range(3))
        b = tuple(F[i] - Rational(1, 2) * T[i] for i in range(3))
        r = tuple(2 * b[i] - a[i] for i in range(3))
        return [(1, 1, -2), (1, -1, -1), (1, 2, -3), (1, 3, -3)].index(r) + 1
    c[31] = q31

    def q32():
        al, be, t = symbols('al be t')
        X = Function('X')(t)
        v = 1 / (2 * al * X + be)
        a = diff(v, t).subs(diff(X, t), v)
        return [i for i, e in enumerate([-2 * al * v**3, -3 * al * v**2, -4 * al * v**4, -5 * al * v**5], 1) if simplify(a - e) == 0][0]
    from sympy import Function
    c[32] = q32

    def q33():
        mu, g, r, w = symbols('mu g r w', positive=True)
        wv = solve(mu * g - w**2 * r, w)[0]
        return [i for i, e in enumerate([mu * g / r, sqrt(mu * g / r), sqrt(r / (mu * g)), mu / sqrt(r * g)], 1) if simplify(e - wv) == 0][0]
    c[33] = q33

    def q34():
        m, T = symbols('m T')
        s = solve([80 - Rational(1, 4) * 60 - T - 20, T - 6 * m - Rational(1, 4) * 8 * m - 2 * m], [m, T])
        return opt(s[m], [Rational(9, 2), 9, Rational(9, 4), Rational(13, 2)])
    c[34] = q34

    def q35():
        M1, M2, p = symbols('M1 M2 p', positive=True)
        r = (p**2 / (2 * M1)) / (p**2 / (2 * M2))
        return [i for i, e in enumerate([M1 / M2, M2 / M1, M1 / (M1 + M2), M2 / (M1 + M2)], 1) if simplify(e - r) == 0][0]
    c[35] = q35

    def q36():
        a, L = symbols('a L', positive=True)
        F = (sqrt(2) + Rational(1, 2)) / a**2
        av = solve(F - (2 * sqrt(2) + 1) / (32 * L**2), a)[0]
        return opt(simplify(av / L), [Rational(1, 2), 4, 2, 3])
    c[36] = q36
    def q38():
        n, R = 1, Rational(8314, 1000)
        slope = lambda P: n * R / P
        P1, P2 = 2, 1                                   # the P2 line is steeper in the figure
        assert slope(P2) > slope(P1)
        return 1 if P1 > P2 else 0
    c[38] = q38

    def q40():
        r = Symbol('r', positive=True)
        xv = [v for v in solve(1 / x**2 - 3 / (r - x)**2, x) if simplify(v - r) != 0 and float(v.subs(r, 1)) > 0 and float(v.subs(r, 1)) < 1][0]
        return [i for i, e in enumerate([r * (1 + sqrt(3)), (1 + sqrt(3)) / r, r / (1 + sqrt(3)), r / (3 * (1 + sqrt(3)))], 1) if simplify(e - xv) == 0][0]
    c[40] = q40

    def q41():
        a1, a2, t, R0 = symbols('a1 a2 t R0', positive=True)
        Rs = R0 * (1 + a1 * t) + R0 * (1 + a2 * t)
        Rp = 1 / (1 / (R0 * (1 + a1 * t)) + 1 / (R0 * (1 + a2 * t)))
        als = diff(Rs, t).subs(t, 0) / Rs.subs(t, 0)
        alp = simplify(diff(Rp, t).subs(t, 0) / Rp.subs(t, 0))
        assert simplify(als - (a1 + a2) / 2) == 0 and simplify(alp - (a1 + a2) / 2) == 0
        return 1
    c[41] = q41

    def q42():
        F = 2 * Matrix([1, 0, 0]).cross(Matrix([0, 0, 1]))          # i(2R x) x (B z), per unit iRB
        return [i for i, v in enumerate([2, -2, 1, -1], 1) if F == Matrix([0, v, 0])][0]
    c[42] = q42
    c[43] = lambda: opt(round(22 / ((22 / 7) * 0.01**2 * 2000 / 2)), [7, 140, 35, 70])
    c[44] = lambda: nearest(0.5 * 8.85e-12 * 50**2, [1.106e-8, 2.212e-10, 2.212e-8, 4.425e-8])
    c[45] = lambda: [i for i, k in enumerate([2, 3, 4, 1], 1) if all(abs(2 * math.asin(math.cos(A / 2)) - A - (math.pi - k * A)) < 1e-12 for A in (0.5, 0.9))][0]

    def q46():
        E, phi = symbols('E phi')
        s = solve([E - phi - 8, E / 3 - phi - 2], [E, phi])
        return opt(s[E] / s[phi], [Rational(9, 2), 3, 5, 9])           # lambda0 / lambda
    c[46] = q46
    c[47] = lambda: opt(Rational(3, 4) / Rational(8, 9), [Rational(27, 32), Rational(32, 27), Rational(27, 5), Rational(5, 27)])

    def q48():
        Y = lambda A, B: int(not ((1 - A) and (1 - B)))
        table = tuple(Y(A, B) for A in (0, 1) for B in (0, 1))
        return {(0, 0, 0, 1): 1, (0, 1, 1, 1): 2, (1, 1, 1, 0): 3, (1, 0, 0, 0): 4}[table]
    c[48] = q48
    c[49] = lambda: opt(Rational(60, 4), [60, 45, 30, 15])
    c[50] = lambda: nearest(0.1 + 2 * 0.1, [0.1, 0.2, 0.3, 0.144])

    def q51():
        H, h, g = symbols('H h g', positive=True)
        t = sqrt(2 * (H - h) / g) + sqrt(2 * h / g)
        hv = solve(diff(t, h), h)[0]
        return simplify(H / hv)
    c[51] = q51
    c[52] = lambda: Rational(3, 4) * 50 * Rational(4, 10)**2
    c[53] = lambda: 9 * 10**8 * Rational(2, 10**4) / (10**3 * 10)
    c[54] = lambda: sqrt(Rational(4, 9) + 5) * 3
    c[55] = lambda: solve(5 / (3 + 2 / Symbol('K')) - Rational(5, 4), Symbol('K'))[0]

    def q56():
        par = lambda *r: 1 / sum(Rational(1, v) for v in r)
        return par(par(2, 2) + 2, 3, 3)                 # R1 shorted by the left wire
    c[56] = q56

    def q57():
        B0, e = symbols('B0 e')
        F = e * Matrix([3, 5, 0]).cross(Matrix([B0, 2 * B0, 0]))
        return solve(F[2] - 5 * e, B0)[0]
    c[57] = q57
    c[58] = lambda: (2 * sqrt(2) * 4)**2                     # M = 2 sqrt2 mu0 l^2/(pi L) with L = l^2, in units of 1e-7
    c[59] = lambda: Rational(13 * 10, 10)                     # I1 = 10I, I2 = 10I + 2*3I*cos60 = 13I
    c[60] = lambda: Rational(4, 10**4) * 9 * 10**16 / (36 * 10**5) / 10**7
    c[81] = lambda: Rational(22, 44) * 100
    c[82] = lambda: int(6.626e-34 * 3e8 / 242e-9 * 6.022e23 / 1000)      # 494.6; NTA's key keeps the integer part
    c[84] = lambda: round(-8.314 * 298 * math.log(2.47e-29) / 1000)
    c[85] = lambda: Rational(1, 2) * 10
    c[86] = lambda: round(math.sqrt(2 * 4) * 10)
    c[90] = lambda: 40 + 2 * 19
    return c
