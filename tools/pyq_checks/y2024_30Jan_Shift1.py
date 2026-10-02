"""Answer checks for JEE Main 2024 (Session 1), 30 Jan Shift 1."""
from pyq_checks.common import *
from sympy import Abs, Function, summation


def checks():
    c = {}

    def q1():
        xs = [k / 100 for k in range(-1000, 1001)]
        ok = [v for v in xs if -1 <= (2 - abs(v)) / 4 <= 1 and v < 3 and abs(math.log(3 - v)) > 1e-12]
        assert min(ok) == -6 and max(ok) < 3 and 2 not in ok
        return opt(6 + 3 + 2, [8, 9, 11, 12])
    c[1] = q1

    def q2():
        X, Y = symbols('X Y', real=True)
        z = X + sympy_I * Y
        e = expand(z**2 + sympy_I * (X - sympy_I * Y))
        sols = [s for s in solve([e.as_real_imag()[0], e.as_real_imag()[1]], [X, Y], dict=True) if s[X] * s[Y] != 0]
        vals = {simplify(Abs((s[X] + sympy_I * s[Y])**2)) for s in sols}
        assert len(vals) == 1
        return opt(vals.pop(), [Rational(1, 4), 1, 4, 9])
    c[2] = q2

    def q3():
        l, m = symbols('l m')
        A = Matrix([[1, 1, 1], [1, 2, 2 * l], [1, 3, 4 * l**2]])
        assert factor(A.det()) == (2 * l - 1)**2
        def kind(lv, mv):
            Aa = A.subs(l, lv); b = Matrix([4 * mv, 10 * mv, mv**2 + 15])
            r1, r2 = Aa.rank(), Aa.row_join(b).rank()
            return 'unique' if r1 == 3 else ('inf' if r1 == r2 else 'none')
        # statement 2: 'inconsistent if l = 1/2 and m != 1' fails at m = 15
        assert kind(Rational(1, 2), 15) == 'inf' and kind(Rational(1, 2), 2) == 'none'
        assert kind(2, 1) == 'unique' and kind(2, 15) == 'unique'
        return 2
    c[3] = q3

    def q4():
        c4, s4, s2 = 2 * cos(x)**4, 2 * sin(x)**4, sin(2 * x)**2
        f = Matrix([[c4, s4, 3 + s2], [3 + c4, s4, s2], [c4, 3 + s4, s2]]).det()
        return opt(simplify(diff(f, x).subs(x, 0) / 5), [0, 1, 2, 6])
    c[4] = q4
    c[5] = lambda: opt(Rational(sum(1 for a in range(11) for b in range(11) if abs(a - b) > 5), 121),
                       [Rational(60, 121), Rational(30, 121), Rational(62, 121), Rational(31, 121)])

    def q6():
        a, d = symbols('a d')
        S = lambda n: Rational(n, 2) * (2 * a + (n - 1) * d)
        s = solve([S(20) - 790, S(10) - 145], [a, d])
        return opt((S(15) - S(5)).subs(s), [405, 395, 390, 410])
    c[6] = q6

    def q7():
        A = x * (54 - 2 * x**2)
        xv = [r for r in solve(diff(A, x), x) if r > 0][0]
        return opt(A.subs(x, xv), [92, 108, 88, 122])
    c[7] = q7

    def q8():
        t = Symbol('t')
        f = Rational(1, 2) + t / 3 + t**2          # any smooth f with f(0) = 1/2
        al = limit(x * integrate(f, (t, 0, x)) / (exp(x**2) - 1), x, 0)
        return opt(8 * al**2, [1, 2, 4, 16])
    c[8] = q8

    def q9():
        g = sin(2 * math.pi * x) + x**3 * 0          # a sample g: g'(1/2) = g'(3/2)
        gp = diff(g, x)
        assert simplify(gp.subs(x, Rational(1, 2)) - gp.subs(x, Rational(3, 2))) == 0
        f = (g + g.subs(x, 2 - x)) / 2
        fp = diff(f, x)
        zeros = [v for v in (Rational(1, 2), 1, Rational(3, 2)) if simplify(fp.subs(x, v)) == 0]
        assert len(zeros) == 3                    # so f'' vanishes at least twice in (0, 2) by Rolle
        return 1
    c[9] = q9

    def q10():
        t = Symbol('t')
        v = integrate(1 / ((1 + t**2) * (1 + 3 * t**2)), (t, 0, 1))
        return opt(simplify(v), [13 * (2 * sqrt(3) - 3) * pi / 8, (2 * sqrt(3) + 3) * pi / 24, pi / (8 * (2 * sqrt(3) + 3)), 13 * pi / (8 * (4 * sqrt(3) + 3))])
    c[10] = q10

    def q11():
        y = Symbol('y')
        r = solve(y**2 - 2 * y - 8, y)
        return opt(integrate((y + 8) / 2 - (y**2 / 4 + 2), (y, min(r), max(r))), [6, 7, 8, 9])
    c[11] = q11

    def q12():
        y = -x * (2 - x) * sin(x) + 2
        ode = diff(y, x) / cos(x) + 2 * (1 - x) * tan(x) + x * (2 - x)
        assert simplify(ode) == 0 and y.subs(x, 0) == 2
        return opt(y.subs(x, 2), [1, 2, 2 * (sin(2) + 1), 2 * (1 - sin(2))])
    c[12] = q12

    def q13():
        m = tan(pi / 12)                         # 30 deg rotated 15 deg clockwise
        Y = Symbol('Y')
        line = Y - m * (x - 9)
        cands = [Y / (sqrt(3) - 2) + x - 9, x / (sqrt(3) - 2) + Y - 9, Y / (sqrt(3) + 2) + x - 9, x / (sqrt(3) + 2) + Y - 9]
        return [i for i, e in enumerate(cands, 1) if simplify(solve(e, Y)[0] - solve(line, Y)[0]) == 0][0]
    c[13] = q13

    def q14():
        d = sqrt((2 + 1)**2 + (2 + 2)**2)
        r2 = sqrt(4 + 4 - 4)
        lo, hi = d - r2, d + r2
        return [i for i, (a, b) in enumerate([(Rational(1, 2), 7), (0, 7), (3, 7), (5, 9)], 1) if (a, b) == (lo, hi)][0]
    c[14] = q14

    def q15():
        e = Symbol('e', positive=True)
        return opt([v for v in solve(1 - e**2 - e**2 / 4, e) if v < 1][0], [2 / sqrt(5), 1 / sqrt(3), sqrt(5) / 3, sqrt(3) / 2])
    c[15] = q15

    def q16():
        t = Symbol('t')
        Q = Matrix([-3 + 5 * t, 1 + 2 * t, -4 + 3 * t])
        tv = solve((Q - Matrix([1, 2, 3])).dot(Matrix([5, 2, 3])), t)[0]
        return opt(19 * sum(Q.subs(t, tv)), [99, 100, 101, 102])
    c[16] = q16
    c[17] = lambda: opt((Matrix([-3, 4, -2]) - Matrix([2, 3, 5])).cross(Matrix([1, 2, 3])).norm() / 2,
                        [sqrt(474) / 2, sqrt(306) / 2, sqrt(410) / 2, sqrt(586) / 2])

    def q18():
        # a sample pair with |a| = 1, a.b = 2, |b| = 4
        a = Matrix([1, 0, 0]); b = Matrix([2, sqrt(12), 0])
        assert a.norm() == 1 and a.dot(b) == 2 and b.norm() == 4
        cv = 2 * a.cross(b) - 3 * b
        return opt(simplify(b.dot(cv) / (b.norm() * cv.norm())), [-sqrt(3) / 2, 2 / sqrt(3), Rational(2, 3), -1 / sqrt(3)])
    c[18] = q18

    def q19():
        M = 8 + Rational(18 - 12, 10) * 4
        return opt(20 * M, [52, 104, 208, 416])
    c[19] = q19

    def q20():
        s = Symbol('s')
        sv = solve(2 * s**3 + 2 * s * (1 - s**2) + 4 * s - 4, s)
        assert sv == [Rational(2, 3)]
        a0 = math.asin(2 / 3)
        sols = sorted([a0 + 2 * k * math.pi for k in range(4)] + [math.pi - a0 + 2 * k * math.pi for k in range(4)])
        n = next(n for n in range(1, 20) if sum(1 for v in sols if v <= n * math.pi / 2) == 3)
        roots = solve(x**2 + n * x + (n - 3), x)
        assert all(r < 0 for r in roots)
        return 3
    c[20] = q20
    c[21] = lambda: 2 + int(math.log2((2**6)**7))

    def q22():
        lam = min(a * (70 - a) for a in range(1, 70) if (a * (70 - a)) % 2 and (a * (70 - a)) % 3)
        al = [a for a in range(1, 70) if a * (70 - a) == lam]
        a, b = al[0], 70 - al[0]
        return (sqrt(a - 1) + sqrt(b - 1)) * (lam + 35) / abs(a - b)
    c[22] = q22
    c[23] = lambda: sum(1 for r in range(825) if (824 - r) % 2 == 0 and r % 6 == 0)

    def q24():
        T = [1]
        d = 3
        while len(T) < 10:
            T.append(T[-1] + d); d += 1
        al = sum(t * t for t in T); be = sum(n**4 for n in range(1, 11))
        return Rational(4 * al - be - 40, 55)
    c[24] = q24

    def q25():
        v = (Rational(2, 3) - Rational(1, 9)) * 1 + (9 - Rational(2, 3)) * 2      # [.] = 1 on [1/9, 2/3), 2 on [2/3, 9)
        import mpmath
        num = mpmath.quad(lambda u: mpmath.floor(mpmath.sqrt(10 * u / (u + 1))), [0, mpmath.mpf(1) / 9, mpmath.mpf(2) / 3, 9])
        assert abs(num - float(v)) < 1e-9
        return 9 * v
    c[25] = q25

    def q26():
        y = Function('y')
        sol = (sqrt(3) * (x**4 / 4 + 2 * x)) / sqrt(1 - x**2)
        ode = (1 - x**2) * diff(sol, x) - (x * sol + (x**3 + 2) * sqrt(3 * (1 - x**2)))
        assert simplify(ode) == 0 and sol.subs(x, 0) == 0
        v = Rational(sol.subs(x, Rational(1, 2)))
        return v.p + v.q
    c[26] = q26

    def q27():
        B = Symbol('B', positive=True)
        Bv = solve(B**2 - 27 * (1 + B / 9), B)[0]
        assert simplify(Bv - Rational(3, 2) * (1 + sqrt(13))) == 0
        a, e = 3, sqrt(1 + Bv / 9)
        assert simplify((Bv / a) / (a * e) - 1 / sqrt(3)) == 0
        return 9 + 4 + 169
    c[27] = q27

    def q28():
        def sd(A, d1, B, d2):
            n = d1.cross(d2)
            return abs((B - A).dot(n)) / n.norm()
        d1 = sd(Matrix([-1, 0, 0]), Matrix([12, 6, -1]), Matrix([0, -2, 1]), Matrix([6, 6, 1]))
        d2 = sd(Matrix([1, -8, 4]), Matrix([2, -7, 5]), Matrix([1, 2, 6]), Matrix([2, 1, -3]))
        return simplify(32 * sqrt(3) * d1 / d2)
    c[28] = q28

    def q29():
        best = 0
        for mp in range(0, 12):
            for pc in range(0, 16):
                for mc in range(0, 16):
                    for t in range(0, min(mp, pc, mc) + 1):
                        if 20 + 25 + 16 - mp - pc - mc + t != 40: continue
                        if 20 - mp - mc + t < 0 or 25 - mp - pc + t < 0 or 16 - pc - mc + t < 0: continue
                        best = max(best, t)
        return best
    c[29] = q29

    def q30():
        a, b = symbols('a b')
        s = solve([4 * a + 2 * b - Rational(1, 2), 4 * a + Rational(1, 4)], [a, b])
        return 48 * (s[a] + s[b])
    c[30] = q30
    c[32] = lambda: opt(sqrt(3) / 2 * Rational(1, 8), [sqrt(3) / 2, 0, sqrt(3) / 16, 1 / sqrt(2)])     # coefficients of m u^3/g (option 1 is mu^2/g)

    def q33():
        return nearest(0.1 * (math.sqrt(2 * 9.8 * 10) + math.sqrt(2 * 9.8 * 5)), [2.39, 43.2, 23.9, 4.32])
    c[33] = q33

    def q34():
        a, T, g = symbols('a T g', positive=True)
        s = solve([T - 2 * g * Rational(1, 2) - 2 * a, 4 * g - 2 * T - 4 * a / 2], [a, T], dict=True)[0]
        return opt(simplify(s[a] / g), [Rational(1, 3), Rational(1, 4), Rational(1, 2), 1])
    c[34] = q34
    c[35] = lambda: opt(sqrt(2 * 10 * Rational(1, 2)), [10, sqrt(10), 2 * sqrt(10), 20])
    c[36] = lambda: nearest(5.12e7 / 6.4 / 1000 - 6400, [1600, 1000, 540, 1200])
    c[39] = lambda: nearest(2 * 320 / 32, [20, 80, -73, 4])
    c[41] = lambda: nearest(27 + (220 / 2.75 / 60 - 1) / 2e-4, [694, 1667, 1694, 1235])
    c[42] = lambda: opt(sqrt(2) / 2, [1 / sqrt(2), sqrt(2), 2, Rational(1, 2)])            # coefficient of mu0 I / a
    c[43] = lambda: opt(1 / sqrt(1 + 2**2), [1 / sqrt(2), 1 / sqrt(3), 1 / sqrt(5), 1 / sqrt(7)])
    c[45] = lambda: nearest(400e-9 * 1 / 0.2e-3 * 1000, [2, 0.2, 0.02, 20])               # in mm
    c[46] = lambda: nearest(6.626e-34 * 3e8 / (3.0 * 1.602e-19) * 1e9, [400, 414, 200, 215])
    c[48] = lambda: nearest(((20 - 10) / 200 - 10 / 500) * 1000, [0, 20, 30, 50])
    c[49] = lambda: nearest(4 / (3300 + 700) * 500, [0.012, 0.002, 0.5, 4])
    c[50] = lambda: nearest(220 * 10 / 100 * 7 / 22, [22, 7, 15, 44])
    c[51] = lambda: (125 - 50 / 2 + 50) + 50 / 2
    c[52] = lambda: Rational(1, 2) * 10 * 100 - Rational(1, 2) * 20 * 25
    c[53] = lambda: Rational(6 * 30, 9) / (Rational(5, 10**7) * 2 * 10**11) * 10**4
    c[54] = lambda: (Rational(330, 120) - Rational(330, 440)) * 100 * 2
    c[55] = lambda: 3 * (Rational(2, 3) * Rational(1, 2)) / Rational(1, 2)                  # loss = (2/3)(1/2)CV^2 over E = (1/2)CV^2, times 3
    c[56] = lambda: 2 + (8 - 2) / (2 + 4) * 4
    c[57] = lambda: round(math.sqrt(2) * 3.5e-5 * math.sin(math.pi / 4) * 1e6)
    c[58] = lambda: round(0.5 * 0.5e-4 * 0.5 * (1200 * 2 * math.pi / 60) * 0.8**2 / (math.pi * 1e-5))
    c[59] = lambda: Rational(15 * 30, 45)

    def q60():
        n = round(math.sqrt(13.6 / 0.85))
        return n * (n - 1) // 2
    c[60] = q60
    c[81] = lambda: round(0.35 * 0.250 * 82.02)
    c[82] = lambda: 2 * (1 + 3)
    c[83] = lambda: Rational(1, 2) * 20 * 20                    # kPa x dm^3 = J
    c[84] = lambda: 14 + math.log10(math.sqrt(1e-11 / 0.10))
    def q85():
        b, cc, xx, y, z = symbols('b cc xx y z')
        eqs = [2 - y,                       # Mn
               8 + cc - 2 * y - z,          # O
               2 * cc - z,                  # H
               b - 2 * xx,                  # I
               -2 - b + z]                  # charge
        return solve(eqs, [b, cc, xx, y, z])[z]
    c[85] = q85
    c[86] = lambda: round(500 * 0.05 * 7.9 / 108 * 6.022e23 / 1e23)
    c[87] = lambda: round(10 * 0.3010 / (2 * 0.3010 - 0.4771))
    c[89] = lambda: Rational(35, 50) * 10
    return c
