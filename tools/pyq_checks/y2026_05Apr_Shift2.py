"""Answer checks for JEE Main 2026 (Session 2), 5 Apr Shift 2."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        for r in (2, -2):                         # r^2 = 4 from (gamma + delta)/(alpha + beta)
            a = Rational(1, 1 + r)
            p, q = a * a * r, a * a * r**5
            if p.is_integer and q.is_integer:
                return opt(abs(p + q), [16, 32, 34, 38])
    c[1] = q1

    def q2():
        z = Symbol('z')
        return opt(sum(simplify(abs(r)**2) for r in solve(z**2 + 4 * z - (1 + 12 * sympy_I), z)), [18, 22, 29, 34])
    c[2] = q2

    def q3():
        n, k = symbols('n k', positive=True, integer=True)
        for kv in range(1, 10):
            tot = sum(Matrix([[m, -1, -5], [-2 * m**2, 3 * (2 * kv + 1), 2 * kv + 1], [-3 * m**3, 3 * kv * (2 * kv + 1), 3 * kv * (kv + 2) + 1]]).det()
                      for m in range(1, kv + 1))
            if tot == 98:
                return opt(kv, [3, 4, 5, 6])
    c[3] = q3

    def q4():
        M = Matrix([[1, 0, -1], [2, 1, 1], [3, 2, 1]])
        v = M.inv() * Matrix([1, 7, 11])
        return opt(sum(v), [4, 5, 7, 11])
    c[4] = q4

    def q5():
        s = sum(Fraction(n, 1 + 4 * n**4) for n in range(1, 11))
        return opt(s.numerator + s.denominator, [256, 264, 276, 284])
    c[5] = q5
    c[6] = lambda: opt(sum(59 + Rational(100, 40) * k for k in (25, 28, 31, 36)) / 4, [129, 136, Rational(26300, 200), 134])
    c[7] = lambda: opt(next(math.comb(10, r) * 2**(10 - r) for r in range(11) if 20 - 3 * r == 2), [3240, 3360, 3480, 3600])
    c[8] = lambda: nearest(0.6 * 0.8 + 0.4 * 0.7, [0.74, 0.76, 0.72, 0.78])
    c[9] = lambda: opt(sum(math.comb(5, b) * math.comb(6, y) * math.comb(4, r) for b in range(2, 6) for y in range(2, 7) for r in range(2, 5) if b + y + r == 8),
                       [4100, 4140, 4230, 4290])

    def q10():
        n = next(n for n in range(2, 40) if Fraction(sum(r * (r - 1) * math.comb(n, r) for r in range(n + 1)), 2**n) == 60)
        cum, half = 0, 2**n / 2
        for r in range(n + 1):
            cum += math.comb(n, r)
            if cum >= half:
                return opt(r * (r - 1), [56, 42, 72, 90])
    c[10] = q10

    def q11():
        P, C, r2 = Matrix([3, 3]), Matrix([1, 2]), 2
        return opt((2 * sqrt((P - C).dot(P - C)))**2, [10, 20, 25, 5])     # PR + PS = 2 sqrt(PC^2 - p^2), max at p = 0
    c[11] = q11

    def q12():
        t = Symbol('t')
        tv = [s for s in solve(4 * t / (2 * t**2 + 2) - Rational(3, 5), t) if 2 * s**2 > 1][0]
        A, B, C = Matrix([-2, 0]), Matrix([2 * tv**2, 4 * tv]), Matrix([2 / tv**2, -4 / tv])
        area = abs((B - A)[0] * (C - A)[1] - (B - A)[1] * (C - A)[0]) / 2
        return opt(6 * area, [80, 160, 174, 192])
    c[12] = q12

    def q13():
        e = max(solve(6 * x**2 - 11 * x + 3, x))
        a = Rational(9, 2) / e
        return opt(2 * a**2 * (e**2 - 1) / a, [Rational(11, 3), Rational(17, 3), Rational(15, 2), Rational(17, 2)])
    c[13] = q13

    def q14():
        t = Symbol('t')
        P = Matrix([-3 + 8 * t, 4 + 2 * t, -1 + 2 * t]); R = Matrix([1, 2, 3])
        F = P.subs(t, solve((R - P).dot(Matrix([8, 2, 2])), t)[0])
        assert (R - F).dot(R - F) < 36
        G = (2 * F + R) / 3
        return opt(sum(G), [4, 5, 6, 8])
    c[14] = q14

    def q15():
        t, a = symbols('t a')
        P = Matrix([1, 2, 7]); L = Matrix([t, 1 + t, 2 + 2 * t])
        F = L.subs(t, solve((P - L).dot(Matrix([1, 1, 2])), t)[0])
        I = 2 * F - P
        return opt(sum(solve((Matrix([a, 2, 5]) - I).dot(Matrix([a, 2, 5]) - I) - 16, a)), [11, 9, 6, 4])
    c[15] = q15

    def q17():
        y = Symbol('y')
        f = limit((1 - cos(x * y)) * tan(x * y) / y**3, y, 0)
        assert simplify(f - x**3 / 2) == 0
        g = lambda t: t**3 / 2 - math.sin(t)
        roots = {0.0}
        for k in range(-400, 400):
            a, b = k / 100 + 1e-7, (k + 1) / 100 + 1e-7
            if g(a) * g(b) < 0:
                roots.add(round(a, 1))
        return opt(len(roots), [0, 2, 3, 1])
    c[17] = q17

    def q18():
        al = 3                                     # min of [2(2^a + 2^-a) + 3^a + 3^-a]/2 at a = 0
        assert min((2**(1 - a) + 2**(1 + a) + 3**a + 3**(-a)) / 2 for a in [k / 100 for k in range(-300, 301)]) == 3
        v = integrate(1 / (exp(2 * x) - exp(-2 * x)), (x, log(al - 1), log(al)))
        return nearest(float(v), [0.5 * math.log(4 / 3), 0.25 * math.log(4 / 3), 0.5 * math.log(8 / 5), 0.25 * math.log(8 / 5)])
    c[18] = q18

    def q19():
        f = log(x) + exp(x)
        F = integrate(f.subs(x, Symbol('t')), (Symbol('t'), 1, x)) + (1 - x) * (log(x) - 1) + exp(1)
        assert simplify(F - f) == 0
        return opt(simplify(f.subs(x, f.subs(x, 1))), [1 + exp(exp(1)), 1 + exp(1), 1 + exp(1) + exp(exp(1)), 1 + 2 * exp(1)])
    c[19] = q19
    c[20] = lambda: opt((4 - 2) * 25 + ((3 - 9) - (4 - 2) * 2), [20, 40, -20, -40])
    c[21] = lambda: sum(1 for a1, b1, a2, b2 in product([1, 4, 7], [2, 3, 8], [1, 4, 7], [2, 3, 8]) if (a2 + b1) % (a1 + b2) == 0)

    def q22():
        I = Matrix([-1, -1]) - 2 * Rational(-1 - 2 - 1, 5) * Matrix([1, 2])
        lines = []
        for H in (Matrix([-1, 1]), Matrix([3, -1])):        # where x = -1 and y = -1 hit x + 2y = 1
            d = I - H
            a_, b_ = d[1], -d[0]; c_ = a_ * H[0] + b_ * H[1]
            lines.append((a_, b_, c_))
        out = {}
        for a_, b_, c_ in lines:
            k = 9 / c_ if c_ in (9, -9) or (9 / c_).is_integer else None
            for target in (9, 7):
                kk = Rational(target, c_)
                if (a_ * kk).is_integer and (b_ * kk).is_integer:
                    out[target] = (a_ * kk, b_ * kk)
        (a, b), (cc, d) = out[9], out[7]
        return a * d + b * cc
    c[22] = q22

    def q23():
        sols = set()
        for k in range(-9, 10):
            for th in (2 * k * math.pi / 9, k * math.pi / 6):
                if -math.pi - 1e-12 <= th <= math.pi + 1e-12 and abs(math.cos(th) * math.cos(2.5 * th) - math.cos(7 * th) * math.cos(3.5 * th)) < 1e-9:
                    sols.add(round(th, 9))
        return len(sols)
    c[23] = q23

    def q24():
        al2 = Rational(10, 64)                    # f = (3 cos x - sin x)/8, max sqrt10/8
        b = Symbol('b', positive=True)
        A = integrate(x**2 - b * x**3, (x, 0, 1 / b))
        return 30 * solve(A - al2, b)[0]**3
    c[24] = q24

    def q25():
        t = Symbol('t', positive=True)
        F = integrate((1 + t**2) / sqrt(t), t)
        C = Rational(6, 5) * sqrt(2) * sqrt(2) - F.subs(t, 1)
        y = (F.subs(t, sqrt(3)) + C) / 2
        return simplify((y * Rational(5, 4))**4)
    c[25] = q25

    # ---- Physics
    c[27] = lambda: opt(Rational(10, 5) * (Rational(1, 2) / 10 + Rational(2, 10) / 5), [Rational(1, 4), 2, Rational(5, 2), Rational(18, 100)])
    c[28] = lambda: opt(1 * 10 * Rational(1, 2) * 8 * Rational(1, 2), [20, 25, 30, 10])      # f = mg sin30 along the incline; displacement 8 m vertical, angle 60 deg
    c[29] = lambda: [(25, 0), (50, 0), (100, 0), (100, 2.5)].index((Rational(1, 2) * 20 * 5 * 2, 0)) + 1
    c[30] = lambda: opt(Rational(4**2 - 2**2, 2**2), [6, 3, 4, Rational(1, 3)])
    c[31] = lambda: ['cylinder', 'ring', 'disc', 'sphere'].index({Rational(1, 2): 'cylinder', 1: 'ring', Rational(2, 5): 'sphere'}[Rational(7, 5) - 1]) + 1
    c[32] = lambda: opt(1 - Rational(1, 3), [Rational(1, 2), Rational(3, 4), Rational(1, 4), Rational(2, 3)])
    c[33] = lambda: opt(8 * 4 - 4 * 2**2, [8, 16, 64, 4])          # in units of pi r^2 S
    c[34] = lambda: opt(diff(x**4, x) / x**4 * x, [2, 1, 4, 3])    # V ~ T^4: (1/V) dV/dT = 4/T, times T
    def q36():
        B0, w, l, L, r = symbols('B0 w l L r', positive=True)
        emf = integrate(B0 * exp(-l * r) * w * r, (r, 0, L))
        opts = [B0 * w * (1 / l**2 - exp(-l * L) * (1 / l**2 + L / l)), B0 * w * (1 / l**2 + exp(-l * L) * (1 / l**2 + L / l)),
                B0 * w * (4 / l**2 - exp(-2 * l * L) * (1 / l**2 + 2 * L / l)), B0 * w * (3 / l**2 - exp(-3 * l * L) * (3 / l**2 + L / l))]
        return opt(emf, opts)
    c[36] = q36
    c[37] = lambda: opt(Rational(2, 2 + 6) * 2, [Rational(1, 2), Rational(3, 2), 0, 2])

    def q38():
        q_, E0, l, L = symbols('q E0 l L', positive=True)
        W = integrate(q_ * E0 * exp(-l * x), (x, 0, L))
        return opt(simplify(W), [q_ * E0 / l * (1 - exp(-l * L)), symbols('v0') * q_ * symbols('B0') / (2 * l) * (2 - exp(-2 * l * L)),
                                 q_ * E0 / l * (1 + exp(-l * L)), q_ * (E0 + symbols('v0') * symbols('B0')) / l * (1 - exp(-l * L / 2))])
    c[38] = q38

    def q41():
        v1 = 1 / (Rational(1, 10) - Rational(1, 15)); u2 = v1 - 15          # P's image is 15 cm beyond Q (virtual object)
        v2 = 1 / (Rational(1, 15) + 1 / u2)
        m = (v1 / -15) * (v2 / u2)
        assert v2 == Rational(15, 2) and abs(m) == 1
        return 2
    c[41] = q41
    def q42():
        lam = 1; d = 5 * lam; D = 10 * d; y = d / 2          # opposite one slit
        phase = 2 * pi * Rational(y * d, D) / lam
        return opt(cos(phase / 2)**2, [Rational(1, 4), Rational(1, 2), 1, Rational(3, 4)])
    c[42] = q42
    c[43] = lambda: opt(1 / Rational(8, 10), [Rational(12, 10), 1, Rational(125, 100), Rational(75, 100)])
    c[44] = lambda: nearest((6 * 1.00727 + 6 * 1.00866 - 12) * 931.5, [127.5, 89.03, 272.0, 92.0])
    c[46] = lambda: round(0.5 * 1.1e11 * (3e-3 / 3)**2 * 600e-6, 6)

    def q47():
        X = Symbol('X')
        return round(solve(X * 4.2 * 50 - (1000 - X) * (4.2 * 50 + 2256), X)[0])
    c[47] = q47
    c[48] = lambda: round(1.6 / math.sqrt(1.6 * 40e-6))
    c[49] = lambda: solve(Rational(1, 4) * (5 + x) - Rational(1, 2) * (2 + x), x)[0]
    c[50] = lambda: round(Fraction(22, 7) * Fraction(4, 100) * 14 / 2 * 50)

    # ---- Chemistry
    c[51] = lambda: nearest(min(50 * 1.3 * 0.5 / 98, 20 / 65) * 22.4, [5.824, 7.428, 6.892, 8.375])
    c[54] = lambda: opt(Rational(2 * 42 - 8 - 80) - 600 * Rational(2 * 200 - 140 - 250, 1000), [-21000, -10, -1000, Rational(-9012, 1000)])

    def q56():
        a, x_, p = symbols('a x p', positive=True)
        Kp = (x_ / (a + x_) * p)**2 / ((a - x_) / (a + x_) * p)
        return opt(simplify(Kp), [x_**2 / (a**2 + x_**2) * p, x_**2 / (a**2 - x_**2) * p, (a + x_**2) / x_**2 * p, (a**2 - x_**2) / x_**2 * p])
    c[56] = q56
    c[57] = lambda: opt(nsimplify((Rational(160, 100) - Rational(156, 100)) / Rational(59, 1000)), [Rational(2, 39) * 10, Rational(40, 59), Rational(29, 20), Rational(59, 40)])
    c[71] = lambda: 3 + 2 + 5 + 4 + 1
    c[72] = lambda: (lambda M: {16: 2 * 12 + 6}[M])(round(22.4 / 1.4))     # RH = CH4 -> CH3I -> C2H6
    c[73] = lambda: round(20 / ((1000 * 10 * 0.08 / 1000) * 1 / (8.3 * 300)) / 1000)
    c[74] = lambda: round(1.9e-3 * 1.3 * 1000 / 123.5 * 75 / 1000 * 100 * 100)
    c[75] = lambda: round(240 * 1.5 / 4)
    return c
