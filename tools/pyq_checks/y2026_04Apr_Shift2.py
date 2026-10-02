"""Answer checks for JEE Main 2026 (Session 2), 4 Apr Shift 2."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        # increasing f: f(x) = f^-1(x) iff f(x) = x on [1, inf)
        s1 = [r for r in solve((x - 1)**4 + 1 - x, x) if r.is_real and r >= 1]
        # II: (x-1)^4 + 1 = 1 + x^(1/4) has a root in (2, 3) by sign change
        g = lambda t: (t - 1)**4 - t**0.25
        s2_nonempty = g(2) < 0 < g(3)
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(len(s1) == 2, not s2_nonempty)]
    c[1] = q1

    def q2():
        z = Symbol('z')
        return opt(sum(simplify(abs(r + sqrt(3) * sympy_I)**2) for r in solve(z**2 + 4 * z + 16, z)), [42, 23, 27, 38])
    c[2] = q2

    def q3():
        l, m = symbols('l m')
        lv = solve(Matrix([[1, 1, 1], [1, 2, 3], [1, 3, l]]).det(), l)[0]
        mv = solve(Matrix([[1, 1, 5], [1, 2, 9], [1, 3, m]]).det(), m)[0]
        return opt(lv + mv, [16, 18, 19, 21])
    c[3] = q3

    def q4():
        p = expand((x - 1) * (x - 1 - sqrt(2) * sympy_I) * (x - 1 + sqrt(2) * sympy_I))
        return opt(integrate(p, (x, -1, 1)), [-2, -4, -8, -10])
    c[4] = q4

    def q5():
        n = 0
        for l in range(-50, 51):
            if l == -2: continue
            a, b, cc = l + 2, -3 * l, 4 * l
            D = b * b - 4 * a * cc
            if D > 0 and -b / a > 0 and cc / a > 0:
                n += 1
        return opt(n, [1, 2, 3, 4])
    c[5] = q5

    def q6():
        A = Matrix([[1, 2, 7], [4, -2, 8], [3, 8, -7]])
        p = max(e for e in A.eigenvals() if e.is_real)
        X = Symbol('X')
        pts = {(xv, 0) for xv in solve((X - p)**2 + (2 * p)**2 - 320, X) if xv.is_real} |               {(0, yv) for yv in solve(p**2 + (X - 2 * p)**2 - 320, X) if yv.is_real}
        return opt(len(pts), [1, 2, 3, 4])          # distinct points: the circle passes through O
    c[6] = q6
    c[7] = lambda: opt(nsimplify(0.2**(math.log(0.5) / math.log(math.sqrt(5))) + 0.04**(math.log(0.5) / math.log(5))), [4, 5, 8, 25])

    def q8():
        S1, S2 = symbols('S1 S2')
        s = solve([S2 + 4 * S1 + 40 - 180, S2 - 2 * S1 + 10 - 90], [S1, S2])
        return opt(sqrt(s[S2] / 10 - (s[S1] / 10)**2), [2, sqrt(3), 2 * sqrt(2), 3])
    c[8] = q8

    def q9():
        r = next(r for r in range(19) if 18 - r - Rational(r, 2) == 0)
        term = math.comb(18, r) * Rational(9)**(18 - r) * Rational(-1, 3)**r
        return opt(term / 221, [84, 78, 168, 198])
    c[9] = q9

    def q10():
        # Q + R = (6, 9); Q on (x-7)^2 + (y-7)^2 = 16 with R on x + y = 5  ->  Q on x + y = 10
        X = Symbol('X')
        ys = [9 - (10 - xv) for xv in solve((X - 7)**2 + (10 - X - 7)**2 - 16, X)]
        return opt(sum(ys), [6, 2, 4, 8])
    c[10] = q10

    def q11():
        a, e = symbols('a e', positive=True)
        s = solve([a * e - 3, a / e - Rational(4, 3)], [a, e], dict=True)[0]
        b2 = s[a]**2 * (s[e]**2 - 1)
        t = Symbol('t', positive=True)       # t = alpha^2
        tv = [v for v in solve(t * b2 * (t / s[a]**2 - 1) - 16 * 15, t) if v > 0][0]
        return opt(tv, [12, 16, 24, 25])
    c[11] = q11

    def q12():
        best = max(16 * math.sin(k * math.pi / 200000 / 2) * math.cos(k * math.pi / 200000 / 2)**3 for k in range(200001))
        return opt(nsimplify(round(best, 9), [sqrt(3)]), [3 * sqrt(3) / 2, 3 * sqrt(3), 4 * sqrt(3), 6 * sqrt(3)])
    c[12] = q12

    def q13():
        a1, b1 = Matrix([Rational(1, 3), 2, Rational(8, 3)]), Matrix([2, -5, 6])
        a2, b2 = Matrix([Rational(-2, 3), 0, Rational(-1, 3)]), Matrix([0, 1, -1])
        n = b1.cross(b2)
        return opt(abs((a2 - a1).dot(n)) / n.norm(), [sqrt(5), 3, 2 * sqrt(3), sqrt(15)])
    c[13] = q13

    def q14():
        al = Symbol('al')
        P = Matrix([al, 2 * al, 1]); Q = Matrix([2 * al + 1, al**2 - 3 * al, (al - 1) / 2])
        M = (P + Q) / 2; d = Matrix([3, 2, 1])
        eq1 = (Q - P).dot(d)
        sols = set()
        for v in solve(eq1, al):
            Mv = M.subs(al, v)
            if simplify((Mv[0] - 2) / 3 - (Mv[1] - 1) / 2) == 0 and simplify((Mv[1] - 1) / 2 - Mv[2]) == 0:
                sols.add(v)
        opts = [{3}, {3, -1}, {3, Rational(1, 4), -1}, {3, Rational(1, 4)}]
        return opts.index(sols) + 1
    c[14] = q14

    def q15():
        lam = Symbol('lam')
        uv = Rational(1, 2)                      # acute angle with |u x v| = sqrt3/2
        Au, Av = lam + uv, lam * uv + 1
        exprs = [Rational(4, 3) * Au - Rational(2, 3) * Av, Rational(2, 3) * Au - Rational(1, 3) * Av,
                 Rational(4, 3) * Au + Rational(2, 3) * Av, Au - Av / 2]
        return [i for i, e in enumerate(exprs, 1) if simplify(e - lam) == 0][0]
    c[15] = q15

    def q16():
        f = lambda t: 2 * t * t + t - 1          # put x = 0: f(y) = f(0) + 2y^2 + y
        a = Symbol('a'); X, Y = symbols('X Y')
        av = solve(expand(f(X + Y) - (f(X) + 2 * Y**2 + Y + a * X * Y)).coeff(X).coeff(Y), a)[0]
        assert f(1) == 2
        return opt(sum(av + f(n) for n in range(1, 6)), [110, 140, 150, 170])
    c[16] = q16
    c[17] = lambda: opt(sum(1 for a in range(23) for b in range(23) for cc in range(12) if a + b + 2 * cc == 22), [121, 124, 144, 169])

    def q18():
        y = Symbol('y')
        return opt(integrate((1 - 4 * y**2) - (-3 * y**2), (y, -1, 1)), [Rational(1, 3), Rational(2, 3), Rational(4, 3), Rational(5, 3)])
    c[18] = q18

    def q19():
        # integrating factor (x^3 + 2)/(2 + e^-2x): d/dx[y IF] = x^3 + 2
        IF = (x**3 + 2) / (2 + exp(-2 * x))
        P = (6 * x**2 + (3 * x**2 + 2 * x**3 + 4) * exp(-2 * x)) / ((x**3 + 2) * (2 + exp(-2 * x)))
        assert simplify(diff(IF, x) / IF - P) == 0
        C = Rational(3, 2) * IF.subs(x, 0)
        y1 = (Rational(1, 4) + 2 + C) / IF.subs(x, 1)
        return opt(simplify(y1 / (2 + exp(-2))), [Rational(13, 8), Rational(6, 13), Rational(12, 13), Rational(13, 12)])
    c[19] = q19

    def q20():
        import mpmath
        v = mpmath.quad(lambda t: mpmath.acot(1 + t + t * t), [0, 1])
        L = math.log(5 / 4)
        opts = [2 * math.atan(2) + L / 2 + math.pi / 2, 2 * math.atan(2) + L / 2 - math.pi / 2,
                2 * math.atan(2) - L / 2 + math.pi / 2, 2 * math.atan(2) - L / 2 - math.pi / 2]
        return nearest(float(v), opts)
    c[20] = q20

    def q21():
        aps = sum(1 for a in range(1, 32) for d in range(1, 16) if a + 2 * d <= 31)
        f = Fraction(aps, math.comb(31, 3))
        return f.numerator + f.denominator
    c[21] = q21

    def q22():
        f = lambda t: math.exp(t - 1) if t < 0 else t * t - 5 * t + 6
        g = lambda t: f(abs(t)) + abs(f(t))
        disc = [t for t in (0,) if abs(g(-1e-9) - g(1e-9)) > 1e-6]
        # corners of |f| for x >= 0 at roots 2 and 3; f(|x|) is smooth away from 0
        kinks = [t for t in (2, 3) if abs((g(t + 1e-6) - g(t)) / 1e-6 - (g(t) - g(t - 1e-6)) / 1e-6) > 1e-3]
        return len(disc) + len(disc) + len(kinks)      # a discontinuity is also a non-differentiable point
    c[22] = q22

    def q23():
        # half-lines through P(alpha, 0) at +-30 deg: triangle PAB is equilateral with side alpha
        al = Rational(9, 2) / (sqrt(3) / 2)
        R = al / sqrt(3)
        return simplify(al**2 / R)
    c[23] = q23

    def q24():
        s, X, Y = symbols('s X Y')
        p = -5 - s                               # (t1+1)(t2+1) = -4
        cx = (4 + 4 * (s**2 - 2 * p)) / 3; cy = (8 + 8 * s) / 3
        locus = expand(cx.subs(s, solve(cy - Y, s)[0]))      # x as a function of y: x = A y^2 + B
        A = locus.coeff(Y, 2)
        return 3 * (1 / A)                       # y^2 = (1/A)(x - B): latus rectum 1/A
    c[24] = q24

    def q25():
        f = cos(x) - 1                           # from f' = -tan x (1 + f), f(0) = 0
        t = Symbol('t')
        assert simplify(diff(f, x) - diff(log(cos(x)), x) + f * tan(x)) == 0
        return simplify(diff(f, x, 2).subs(x, pi / 6) + 12 * diff(f, x).subs(x, -pi / 6) + f.subs(x, pi / 6))
    c[25] = q25

    # ---- Physics
    c[27] = lambda: opt(18 + 100 - 80, [18, 28, 38, 48])              # relative to A: 80 + v - 100 = 18 km/h
    c[28] = lambda: [(1, 2), (2, 5), (5, 2), (5, 4)].index(tuple(int(v) // math.gcd(50, 40) for v in (0.5 * 50 * 4 / 2, 0.5 * 100 * 4 / 5))) + 1
    c[29] = lambda: opt(round(math.degrees(math.atan((43.6 - 9.8 * 2) / 24))), [60, 45, 30, 75])
    c[30] = lambda: opt(3 - 1, [sqrt(3), 2 * sqrt(2), 2, Rational(4, 9)])
    c[31] = lambda: opt(Rational(3, 2) * 2 / Rational(1, 2), [1, 4, 8, 6])
    c[32] = lambda: nearest(30e-4 * 0.5 / (10 * 15e-6), [100, 10, 1000, 1500])
    c[35] = lambda: opt(sqrt((Rational(1, 4) + 1) / 1), [sqrt(Rational(5, 4)), sqrt(Rational(2, 3)), sqrt(Rational(3, 2)), sqrt(3)])   # T = 2 pi sqrt(I/(M g R)) with I = 5MR^2/4
    c[36] = lambda: nearest((math.sqrt(Matrix([1, 2, 2]).norm()) - 1) * 100, [73, 63, 83, 53])
    c[37] = lambda: opt(1 / (1 / Rational(2) + 1 / Rational(2)) + 1, [2, Rational(7, 2), Rational(7, 3), Rational(5, 2)])
    c[39] = lambda: opt(1 / (4 * pi * Rational(1, 10**7) * 400) / 10**5, [25 / pi, 1 / (16 * pi), 1 / pi, 1 / (4 * pi)])
    c[41] = lambda: opt(1 / (Rational(4, 10) * 2), [Rational(1, 2), Rational(5, 2), Rational(4, 5), Rational(5, 4)])
    c[42] = lambda: opt((cos(pi / 6)**2 * cos(pi / 6)**2) / cos(pi / 3)**2, [Rational(3, 4), Rational(4, 3), Rational(9, 4), Rational(4, 9)])
    c[46] = lambda: (25 - 10) / (0.5 / 10)
    c[47] = lambda: math.sqrt(6.4 * 10)
    c[48] = lambda: round(math.hypot(1e-7 * 2 * 3 * math.sqrt(5) / 0.05**3, 1e-7 * 3 * math.sqrt(5) / 0.05**3) * 1e3, 6)
    c[49] = lambda: round(125 * 1 * 3.14 * 0.02**2 * 0.4 * 0.5 * 1e4, 6)
    c[50] = lambda: round(7 * 450 / 0.56, 6)

    # ---- Chemistry
    c[51] = lambda: [('C', 'A', 'B'), ('C', 'B', 'A'), ('B', 'C', 'A'), ('B', 'A', 'C')].index(tuple(sorted(
        {'A': 2 * 18, 'B': 684 / 342 * 45, 'C': 90.8 / 22.7 * 2}, key=lambda k: -{'A': 2 * 18, 'B': 684 / 342 * 45, 'C': 90.8 / 22.7 * 2}[k]))) + 1
    c[52] = lambda: ['AC', 'AE', 'BE', 'CD'].index(''.join(sorted(k for k, (n, z) in {'A': (1, 1), 'B': (1, 2), 'C': (2, 2), 'D': (1, 3), 'E': (2, 4)}.items()
                                                              if Fraction(n * n, z) == 1))) + 1
    c[55] = lambda: opt(Rational(475, 100) + nsimplify(math.log10((14.2 * 0.1) / (28.4 * 0.1 - 14.2 * 0.1))), [7, Rational(475, 100), Rational(35, 10), Rational(482, 100)])   # half-neutralised: pH = pKa
    c[64] = lambda: opt(9 * 12 + 10, [90, 118, 160, 125])      # trans-1-phenylpropene C9H10

    def q71():
        n = 3.365 / 46
        dU = -99.472 / n
        dH = dU + (-1) * 8.314e-3 * 298.15
        hf = 2 * -393.5 + 3 * -285.8 - dH
        return round(abs(hf) / 100)
    c[71] = q71

    def q72():
        p = [0.5 / 1.25 * 2, 0.5 / 1.25 * 2, 0.25 / 1.25 * 2]     # N2O5, N2O4, O2 at 50 % dissociation, 2 atm
        Kp = p[1]**2 * p[2] / p[0]**2
        assert abs(Kp - 0.4) < 1e-12
        return round(-8.314 * 323 * 2.303 * (2 * 0.30 - 1))      # log 0.4 = 2 log 2 - 1
    c[72] = q72

    def q73():
        E0 = 0.15 + 0.036
        n = round(0.059 * 2 / (0.2057 - E0))              # E = E0 - (0.059/n) log Q with Q = 1e-2
        return next(xv for xv in range(1, 5) if math.lcm(xv, 3) == n)
    c[73] = q73
    c[74] = lambda: round(20 * 1 / 3)                      # 0.65 -> 0.00065 is three decades; 0.065 is one
    c[75] = lambda: round(0.4813 / 233 * 32 / (2.0e-3 * 76) * 1000)
    return c
