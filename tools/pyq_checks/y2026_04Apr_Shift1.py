"""Answer checks for JEE Main 2026 (Session 2), 4 Apr Shift 1 (Q36 dropped by NTA)."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        lo, hi = None, None
        for k in range(-400000, 400001):          # scan x on a fine grid
            t = k / 100000
            if -1 <= (4 * t + 2 * math.floor(t)) / 3 <= 1:
                lo = t if lo is None else lo; hi = t
        return opt(round(12 * (lo + hi)), [6, 8, 9, 4])
    c[1] = q1

    def q2():
        ok = [t / 1000 for t in range(-10000, 10001) if abs(abs((t / 1000)**2 + t / 1000 - 9) - (abs(t / 1000) + abs((t / 1000)**2 - 9))) < 1e-9]
        # solution set [-3, 0] U [3, inf): alpha = -3, beta = 0, gamma = 3
        assert min(ok) == -3 and 0 in ok and 0.001 not in ok and 3 in ok and 2.999 not in ok
        return opt(9 + 0 + 9, [9, 18, 36, 72])
    c[2] = q2

    def q3():
        y = Symbol('y', real=True)
        w = (3 + sympy_I * y) / (sympy_I * y - sympy_I)
        re_, im_ = simplify(w.as_real_imag()[0]), simplify(w.as_real_imag()[1])
        sols = [s for s in solve(re_ - im_, y) if re_.subs(y, s) > 0]
        return opt(sols[0]**2, [9, 4, 5, 1])
    c[3] = q3
    c[4] = lambda: opt(3**4 - sum(1 for f in product('abc', repeat=4) if len(set(f)) == 3), [48, 45, 51, 35])

    def q5():
        n = 0
        for a, b, cc, d in product(range(5), repeat=4):
            if a + d != 4: continue
            A = Matrix([[a, b], [cc, d]])
            if A**2 - 4 * A + 3 * Matrix.eye(2) == Matrix.zeros(2): n += 1
        return opt(n, [20, 17, 21, 19])
    c[5] = q5

    def q6():
        A = Matrix([[1, 1, 2], [-2, 0, 1], [1, 3, 5]])
        M = (2 * A.adjugate().inv()).adjugate().adjugate()
        return opt(sum(M), [3, 4, -4, -3])
    c[6] = q6

    def q7():
        d = Symbol('d')
        a = Rational(10, 3)
        for s in solve(15 * (2 * a + 29 * d) - (a + 29 * d)**3, d):
            if s.is_real and a + 29 * s >= 0:
                return opt(s, [Rational(5, 87), Rational(25, 83), Rational(15, 29), Rational(5, 29)])
    c[7] = q7
    c[8] = lambda: opt(math.factorial(7) - math.factorial(5) * math.factorial(3), [5040, 3050, 3410, 4320])

    def q9():
        base = sum(math.comb(r, 3) for r in range(3, 100))
        for k in range(2, 100):
            coef = base + math.comb(100, 3) * k**3
            n = (Fraction(coef, math.comb(100, 3)) - Fraction(101, 4)) / 43
            if n.denominator == 1 and n >= 1:
                return opt(k + int(n), [10, 11, 12, 13])
    c[9] = q9

    def q10():
        a, b = symbols('a b')
        known = [21, 8, 17, 51, 103, 13, 67]
        s = solve([a + b - 80, (a - 21) + (21 - b) + sum(abs(v - 21) for v in known) - 234], [a, b])
        vals = sorted(known + [s[a], s[b]])
        assert vals[4] == 21 and s[a] > s[b]
        return opt(2 * s[a], [109, 117, 161, 131])
    c[10] = q10

    def q11():
        A, B = Matrix([-3, -3]), Matrix([-3, 9])
        u2, u3 = Matrix([1, 1]) / sqrt(2), Matrix([1, -3]) / sqrt(10)
        # the two bisector directions through O: u2 + u3 and u2 - u3; the obtuse-angle bisector bisects the pair forming the obtuse angle
        for d, (p, q) in ((u2 + u3, (u2, u3)), (u2 - u3, (u2, -u3))):
            if p.dot(q) < 0:          # p and q make an obtuse angle: this d bisects it
                t = -3 / d[0]; C = d * t
                return opt(simplify((B - C).dot(B - C) / (A - C).dot(A - C)), [5, Rational(1, 5), Rational(2, 3), Rational(3, 2)])
    c[11] = q11

    def q12():
        A = Matrix([1, 2]); B = 2 * Matrix([5, -1]) - A; C = 3 * Matrix([3, 4]) - A - B
        X, Y = symbols('X Y')
        P = Matrix([X, Y])
        s = solve([(P - A).dot(P - A) - (P - B).dot(P - B), (P - A).dot(P - A) - (P - C).dot(P - C)], [X, Y])
        return opt(21 * (s[X] + s[Y]), [309, 403, 497, 524])
    c[12] = q12

    def q13():
        t = Symbol('t')
        ends = [Matrix([-1, 2 * tv - 2]) for tv in solve(1 + (2 * t - 2)**2 - 1 - 3 * (2 * t - 2), t)]
        M = (ends[0] + ends[1]) / 2
        return opt(6 * (M[0] + M[1]), [1, 3, 4, 6])
    c[13] = q13

    def q14():
        s, t, l = symbols('s t l')
        P = Matrix([2 * s, 3 * s, 3 * s - 1]); Q = Matrix([-1 - t, 2 + t, 4 * t])
        sol = solve(list(Q - P - l * Matrix([1, -1, 2])), [s, t, l], dict=True)[0]
        D = (Q - P).subs(sol)
        return opt(225 * D.dot(D), [1024, 1014, 1104, 1204])
    c[14] = q14

    def q15():
        s, t = symbols('s t')
        P0 = Matrix([-2, -8, 6]); R = P0 + s * Matrix([1, -1, 2]); L = Matrix([1 + t, 1 + 2 * t, -t])
        sol = solve(list(R - L), [s, t], dict=True)[0]
        D = R.subs(sol) - P0
        return opt(D.dot(D), [3, 6, 8, 12])
    c[15] = q15

    def q16():
        y = atan((3 * cos(x) - 4 * sin(x)) / (4 * cos(x) + 3 * sin(x))) + 2 * atan(x / (1 + sqrt(1 - x**2)))
        return opt(nsimplify(round(float(diff(y, x).subs(x, sqrt(3) / 2)), 10)), [3, -1, 1, 2])
    c[16] = q16

    def q17():
        a, b, cc, d = symbols('a b cc d')
        f = a * x**3 + b * x**2 + cc * x + d
        sols = [s for s in solve(Poly(expand(f - diff(f, x) * diff(f, x, 2)), x).all_coeffs() + [d], [a, b, cc, d], dict=True) if s.get(a, a) != 0]
        f = f.subs(sols[0])
        return opt(36 * (diff(f, x).subs(x, 2) + diff(f, x, 2).subs(x, 2) + integrate(f, (x, 0, 2))), [42, 46, 56, 66])
    c[17] = q17

    def q18():
        A = 2 * (integrate(x * sin(x), (x, 0, pi / 2)) + integrate(pi - x, (x, pi / 2, pi)))
        assert all((k * math.pi / 200) * math.sin(k * math.pi / 200) <= math.pi - k * math.pi / 200 + 1e-12 for k in range(0, 101))
        return opt(A, [1 + pi**2 / 8, 2 + pi**2 / 4, pi**2 / 8 - 1, 4 + pi**2 / 2])
    c[18] = q18

    def q19():
        import mpmath
        x0 = mpmath.findroot(lambda t: t * mpmath.sin(t) - 1, 1.1)
        total = mpmath.quad(lambda t: abs(mpmath.sin(t)) + mpmath.floor(t * mpmath.sin(t)), [-2, -x0, 0, x0, 2])
        beta = total - 2 * (3 - mpmath.cos(2))
        return opt(round(float(beta * mpmath.sin(beta / 2)), 9), [1, 2, 4, 8])
    c[19] = q19

    def q20():
        y = Symbol('y')
        # integral of dy/(y^2 - y + 1) = (2/sqrt3) atan((2y-1)/sqrt3); RHS integral 0..1 of (1 + x + x^2) = 11/6
        val = sqrt(3) * tan(Rational(11, 6) * sqrt(3) / 2)
        return opt(val, [sqrt(3) * tan(11 * sqrt(3) / 6), sqrt(3) / 2 * tan(11 * sqrt(3) / 12), sqrt(3) * tan(11 * sqrt(3) / 12), sqrt(3) / 2 * tan(11 * sqrt(3) / 6)])
    c[20] = q20
    c[21] = lambda: 96 * Fraction(sum(1 for s in product((0, 1), repeat=8) if sum(s[:6]) == 4 and sum(s[3:]) == 3), 256)

    def q22():
        e = Symbol('e', positive=True)
        return simplify(solve(e**2 + 2 * e - 1, e)[0]**2 + 2 * sqrt(2))
    c[22] = q22
    c[23] = lambda: round((math.tan(math.radians(81)) - math.tan(math.radians(3))) /
                          sum(math.sin(math.radians(a)) / math.cos(math.radians(3 * a)) for a in (3, 9, 27)), 9)

    def q24():
        n = 7
        th = [2**(k - 1) * math.pi / (2**n + 1) for k in range(1, n + 1)]
        return round(sum(1 / math.cos(t)**2 for t in th) / sum(1 / math.sin(t)**2 for t in th), 9)
    c[24] = q24

    def q25():
        # max{6x, 2+3x^2} has corners where the two pieces cross with different slopes;
        # |x-1| cos|x^2 - 1/4| has a corner at x = 1 because cos(3/4) != 0 (cos|u| = cos u is smooth)
        cross = [r for r in solve(6 * x - (2 + 3 * x**2), x) if -math.pi < float(r) < math.pi and 6 != float(diff(2 + 3 * x**2, x).subs(x, r))]
        corner_at_1 = abs(math.cos(0.75)) > 1e-9 and all(abs(float(r) - 1) > 1e-9 for r in cross)
        return len(cross) + int(corner_at_1)
    c[25] = q25

    # ---- Physics
    c[26] = lambda: opt(Rational(25, 10) / 5 / 100, [Rational(1, 100), Rational(1, 1000), Rational(5, 100), Rational(5, 1000)])
    c[27] = lambda: opt(Rational(63, 10) * 10**7 / (Rational(21, 10) * 10**9) * 100, [2, 3, 6, 4])
    c[28] = lambda: opt(1 - Rational(1, 1) / Rational(9, 4), [Rational(3, 4), Rational(2, 3), Rational(5, 9), Rational(4, 9)])   # a_s/a_r = 1.5^2
    c[29] = lambda: opt(abs(10 * Rational(61, 10) - (2 * 3 * Rational(56, 10) + 4 * Rational(74, 10))), [Rational(69, 10), Rational(79, 10), Rational(22, 10), Rational(43, 10)])
    c[30] = lambda: opt((Rational(1, 4) * Rational(7, 8) * 4) / (Rational(2, 5) * Rational(1, 8) * Rational(1, 4)), [35, 70, 140, 210])
    c[31] = lambda: opt(sin(pi / 3) / sin(pi / 6), [sqrt(2), sqrt(3), 2 * sqrt(3), 1 / sqrt(2)])
    c[33] = lambda: opt(3 - 1, [1, Rational(3, 2), 2, 3])
    c[34] = lambda: nearest(2 * 8 * 0.314 / (math.pi * (2e-4)**2 * 2e10) * 1000, [3, 2, 1.9, 1])
    c[37] = lambda: [('series', 0.5), ('parallel', 0.5), ('series', 1), ('parallel', 2)].index(('series', 30 / (20 / 1) - 1)) + 1   # x = 1: Ig = 20/x, need 30/Ig - x in series
    c[38] = lambda: ['1101', '0010', '0111', '1000'].index(''.join(str(int(a == '1' or b == '0')) for a, b in zip('1101', '1010'))) + 1   # Y = (A'B)' = A + B'

    def q39():
        f = -10
        img = lambda u: 1 / (1 / f - 1 / u)
        return opt(abs(img(-20) - img(-30)), [Rational(5, 2), 5, Rational(15, 2), 7])
    c[39] = q39
    c[40] = lambda: opt(diff(1 / x, x).as_powers_dict()[x], [-2, 1, -1, 2])          # U = eps A V^2 / (2x), dU/dt ~ x^-2
    c[41] = lambda: nearest(0.02 * math.pi * 200 / 0.03 * ((0.06)**3 - (0.03)**3) / 3 * 100, [4.4, 2.64, 3.25, 1.2])
    c[42] = lambda: nearest((100 + 10) * 20e-6 * 1000, [2.2, 2.0, 2.1, 2.4])

    def q43():
        r = Rational(3, 4); E = 27; R = 6        # four identical 27 V / 3 ohm branches in parallel, 6 ohm load
        I = E / (r + R)
        return [i for i, (v, a) in enumerate([(24, 12), (24, 4), (18, 12), (27, 4)], 1) if v == I * R and a == I][0]
    c[43] = q43
    c[44] = lambda: nearest(1.22 * 500e-9 / 5e-7 * 100, [61, 122, 244, 305])
    c[46] = lambda: Matrix([5, 2, 2]).dot(Matrix([3, -4, 0]) * 5)
    c[47] = lambda: round(2 * 3.5e-2 * 4 * Fraction(22, 7) * ((0.02)**2 - (0.01)**2) * 1e6)
    c[48] = lambda: 7 * 2 * Fraction(22, 7)       # omega = 1
    c[49] = lambda: Matrix([4, 24]).dot(Matrix([Rational(4, 2), 8]))     # F(2) . v(2), v = (t^2/2, t^3)
    c[50] = lambda: round(math.tan(math.acos(0.5)) * 100 / math.sqrt(3))

    # ---- Chemistry
    c[51] = lambda: min(range(4), key=lambda i: abs([0.1266, 0.0633, 0.1266, 0.0633][i] - 1.4187 / 22.4) * 1e3 + abs([3.812e22, 3.812e22, 7.6238e22, 7.6238e22][i] - 1.4187 / 22.4 * 6.022e23) / 1e21) + 1
    c[52] = lambda: nearest(5 / ((1 / 4 - 1 / 9) / (1 / 16 - 1 / 25)), [1, 0.81, 1.75, 27])
    c[55] = lambda: nearest((2.7e-5)**(1 / 3), [(2.7e-5)**3, 6e-2, math.sqrt(2.7e-5), 3e-2])
    c[56] = lambda: opt(Rational(3 + 6 + 1 + 0, 5), [3, 2, 5, 7])
    c[72] = lambda: round(0.5 * (7 * 12 + 5 + 35.5 + 32))     # 78.25 g, integer answer 78
    def q73():
        br = 3.36 * 80 / 188 / 2.0 * 100; cpc = 26.7; h = 100 - br - cpc
        mol = [cpc / 12, h / 1, br / 80]
        r = [m / min(mol) for m in mol]
        k = next(k for k in range(1, 7) if all(abs(v * k - round(v * k)) < 0.08 for v in r))
        return round(r[0] * k)
    c[73] = q73
    c[74] = lambda: round((14 - 4.74 - math.log10(25 / 0.5)) * 100)

    def q75():
        m = 0.5 / 0.3
        ns = m * 0.040
        return round(ns * (760 / 10) - ns)          # n_solute/(n_solute + N) = 10/760
    c[75] = q75
    return c
