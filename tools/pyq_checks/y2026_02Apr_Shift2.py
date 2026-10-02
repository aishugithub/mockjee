"""Answer checks for JEE Main 2026 (Session 2), 2 Apr Shift 2. Each returns the option (1-4) or the value."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        a, b, r = symbols('a b r')
        s = solve([a + b - 3, a * b - r, a / 2 + 2 * b + 3], [a, b, r], dict=True)[0]
        r1, r2 = 2 * s[a] + s[b] + 2 * s[r], s[a] - 2 * s[b] - s[r] / 2
        assert r1 + r2 == -6
        return opt(-r1 * r2, [-135, -567, 135, 567])
    c[1] = q1
    c[2] = lambda: opt(12 + 10, [12, 17, 22, 24])      # r - (|c2| + 5) = 2 with |c2| = 5 -> r = 12; max = r + 10

    def q3():
        a, b = symbols('a b')
        M = Matrix([[1, 5, 6], [2, 3, 4], [1, 6, a]])
        av = solve(M.det(), a)[0]
        aug = Matrix([[1, 5, 6, 4], [2, 3, 4, 7], [1, 6, av, b]])
        bv = solve(aug[:, [0, 1, 3]].det(), b)[0]        # rank 2 for infinitely many
        lines = [lambda p, q: q - p - 3, lambda p, q: p - q - 3, lambda p, q: p + q - 11, lambda p, q: p + q - 12]
        return [i for i, f in enumerate(lines, 1) if simplify(f(av, bv)) == 0][0]
    c[3] = q3

    def q4():
        d, r = symbols('d r')
        for s in solve([1 + d + r - 1, 1 + 2 * d + r**2 - 4], [d, r], dict=True):
            if s[r] > 1:
                return opt(1 + 9 * s[d] + s[r]**4, [81, 76, 62, 55])
    c[4] = q4
    c[5] = lambda: opt(sum(Fraction(sum(k**3 for k in range(1, n + 1)), n * n) for n in range(1, 9)), [70, 71, 72, 73])
    c[6] = lambda: opt(next(m for m in range(30, 40) if all(math.comb(30, 30 - r) + 3 * math.comb(30, 31 - r) + 3 * math.comb(30, 32 - r) + math.comb(30, 33 - r) == math.comb(m, r) for r in range(3, 31))), [31, 32, 33, 34])

    def q7():
        n = next(n for n in range(3, 100) if math.comb(n + 1, 3) - math.comb(n, 3) == 66)
        return opt(sum(p for p in range(2, n + 1) if n % p == 0 and all(p % k for k in range(2, p))), [7, 8, 5, 6])
    c[7] = q7

    def q8():
        a = [Fraction(1), Fraction(1, 2)]                   # probability of ever reaching 5k points
        for k in range(2, 7):
            a.append((a[-1] + a[-2]) / 2)
        return opt(a[6].numerator + a[6].denominator, [53, 55, 107, 105])
    c[8] = q8

    def q9():
        n = symbols('n', positive=True)
        sols = [s for s in solve((8 * n - 48)**2 - (80 * n - 496), n) if s.is_integer]
        return opt(sols[0], [21, 16, 13, 7])
    c[9] = q9

    def q10():
        k = Symbol('k', real=True)
        kv = [s for s in solve(k**2 * (k - 1) + 2, k) if s.is_real][0]
        X, Y = symbols('X Y')
        cen = solve([X + (kv - 1) * Y + 3, 2 * X + kv**2 * Y - 4], [X, Y])
        r2 = cen[X]**2 + cen[Y]**2
        d2 = (cen[X] - cen[Y] + 2)**2 / 2
        return opt(4 * (r2 - d2), [10, 27, 18, 34])
    c[10] = q10

    def q11():
        a = Symbol('a')
        for x1 in solve(a * (1 - a) + 12, a):        # x1 + x2 = 1, x1 x2 = -12
            x2 = 1 - x1
            area = abs(x1 * 12 / x2 - x2 * 12 / x1) / 2
            return opt(simplify(area), [Rational(3, 2), Rational(5, 2), Rational(7, 2), Rational(9, 2)])
    c[11] = q11

    def q12():
        p = Symbol('p', real=True)
        q = -2 - p
        vy = q - p**2 / 4                                   # always negative; minimise |vy|
        pv = solve(diff(vy, p), p)[0]
        return opt(pv**2 + q.subs(p, pv)**2, [2, 4, 5, 8])
    c[12] = q12

    def q13():
        # identity: 2(cos^8 t - sin^8 t)/cos 2t = 2 - sin^2 2t (checked at sample points)
        for t in (0.1, 0.7, 1.3, 2.9, 5.0):
            assert abs(2 * (math.cos(t)**8 - math.sin(t)**8) / math.cos(2 * t) - (2 - math.sin(2 * t)**2)) < 1e-9
        # tan^2 t != 1  <=>  cos 2t != 0  <=>  sin^2 2t != 1, so the value lies in (1, 2]: a^2 in (1, 2] has no integer a
        return opt(len([a for a in range(-5, 6) if 1 < a * a <= 2]), [0, 1, 2, 3])
    c[13] = q13

    def q14():
        l, m = symbols('l m')
        cv = l * Matrix([-1, 1, 3]) + m * Matrix([1, 3, 1])
        s = solve([cv.dot(Matrix([3, -6, 2])) - 10, cv.dot(Matrix([1, 1, 1])) + 2], [l, m])
        return opt(cv.subs(s).dot(cv.subs(s)), [8, 12, 14, 15])
    c[14] = q14

    def q15():
        a, b, al, t = symbols('a b al t')
        A = Matrix([1 + 2 * t, 2 + t, al + 3 * t]); P = Matrix([a, b, 0])
        s = solve(list((A + P) / 2 - Matrix([0, Rational(3, 4), Rational(-1, 4)])) + [(A - P).dot(Matrix([2, 1, 3]))], [a, b, al, t], dict=True)[0]
        return opt(s[a]**2 + s[b]**2 + s[al]**2, [1, 2, 6, 9])
    c[15] = q15

    def q16():
        PQ, PS = Matrix([0, 1, 1]), Matrix([1, -1, 0])
        ang = math.degrees(math.acos(PQ.dot(PS) / (PQ.norm() * PS.norm())))
        al = math.radians(ang - 90)
        v = math.sin(5 * al / 2)**2 - math.sin(al / 2)**2
        return opt(nsimplify(round(v, 12), [sqrt(3)]), [Rational(1, 2), sqrt(3) / 2, sqrt(3) / 4, 2 * sqrt(3) / 5])
    c[16] = q16
    c[17] = lambda: opt(integrate(sin(x)**4 + cos(x)**4, (x, 0, 20 * pi)), [15 * pi / 2, 25 * pi, 15 * pi, 25 * pi / 2])

    def q18():
        a, b = symbols('a b')
        f = -5 * x**3 + a * x**4 + b * x**5
        s = solve([diff(f, x).subs(x, 1), diff(f, x).subs(x, -1)], [a, b])
        f = f.subs(s)
        return opt(f.subs(x, 2) - f.subs(x, -2), [0, 50, 92, 112])
    c[18] = q18

    def q19():
        F = integrate((16 * x + 24) / (x**2 + 2 * x - 15), x)
        C = 14 * log(3) - F.subs(x, 4)
        v = float(F.subs(x, 7) + C)
        al, be = next((a, b) for a in range(1, 60) for b in range(1, 60) if abs(a * math.log(2) + b * math.log(3) - v) < 1e-9)
        return opt(al + be, [31, 37, 39, 41])
    c[19] = q19

    def q20():
        y = Symbol('y', positive=True)
        X = 2 * y / (log(y) + 1)                       # from 1/v = (ln y)/2 + 1/2 with v = x/y
        assert simplify(2 * y**2 * diff(X, y) - 2 * X * y + X**2) == 0 and simplify(X.subs(y, exp(1)) - exp(1)) == 0
        return opt(simplify(X.subs(y, exp(2))), [Rational(3, 2) * exp(2), Rational(2, 3) * exp(2), exp(2), 2 * exp(2)])
    c[20] = q20
    c[21] = lambda: sum(1 for x1, y1, z1, w1 in product([2, 3, 4, 5, 6], repeat=4) if z1 % x1 == 0 and y1 <= w1)

    def q22():
        A = Matrix([[2, -2], [4, -2]]); B = Matrix([[3, 9], [1, 3]])
        P = B * A.inv(); Q = A.inv() * B
        return abs((2 * (P + Q)).trace())
    c[22] = q22
    c[23] = lambda: 72 * Rational(3, 6)**2           # |BA| + |BA'| = 12: ellipse, foci (+-3, 0), a = 6

    def q24():
        A = integrate(Rational(4, 3) * sqrt(x**2 - 9) - (8 * x - 24) / 3, (x, 3, 5))
        return simplify(3 * (A + 6 * log(3)))
    c[24] = q24
    c[25] = lambda: sum(1 for n in range(0, 30) if 2 <= (1 + math.sqrt(1 + 4 * (n + 0.5))) / 2 <= 4)   # x where x^2 - x - 1/2 = n

    # ---- Physics
    c[27] = lambda: opt(Rational(10, 25 * 4), [Rational(1, 10), Rational(1, 2), Rational(7, 10), Rational(3, 10)])
    c[28] = lambda: nearest((2 - 1) * (0.5 * (10 / 3) * 4) / 3, [3.33, 3.12, 2.22, 1.42])

    def q29():
        vx, vy = symbols('vx vy')
        F = 1e-9 * (Matrix([0, 0.4, 0]) + Matrix([vx, vy, 0]).cross(Matrix([0, 0, 4e-3])))
        s = solve(list(F - Matrix([4e-10, 2e-10, 0])), [vx, vy])
        return [i for i, v in enumerate([(50, 100), (100, 50), (-50, 100), (50, -100)], 1) if abs(s[vx] - v[0]) < 1e-6 and abs(s[vy] - v[1]) < 1e-6][0]
    c[29] = q29
    def q31():
        v, K = math.sqrt(2 * 9.8 * 6.4e6) / 1000, 9.8 * 6.4e6        # v = sqrt(2gR), K = mgR
        pairs = [(11.2, 6.27e7), (11.2, 12.54e7), (8.8, 6.27e7), (8.8, 12.54e7)]
        return [i for i, (a, b) in enumerate(pairs, 1) if abs(a - v) < 0.05 and abs(b - K) < 1e5][0]
    c[31] = q31
    c[32] = lambda: nearest(5 + 50 * 0.001 - 5 * 0.001, [5.045, 5.055, 5.450, 5.550])
    c[33] = lambda: nearest(0.03 * 2 * 4 * ((0.03)**2 - (0.01)**2) / 1e-4, [0.86, 0.64, 1.92, 7.68])

    def q34():
        n = 1e5 * 8310e-6 / (8.31 * 300)
        co2 = (13.2 - 32 * n) / 12
        return nearest(co2, [0.15, 0.25, 0.21, 0.13])
    c[34] = q34
    c[35] = lambda: nearest(2 * (1e-3)**2 * 2000 * 10 / (9 * 0.005) * 10, [0.88, 8.8, 88.8, 0.088])
    c[36] = lambda: opt(2 * 10 * Rational(1010, 100) / Rational(1, 10), [1980, 2020, 2000, 1000])   # mg(h + d) = F d
    c[38] = lambda: opt(100 * Rational(200, 400), [25, 50, Rational(666, 10), 100])   # 400 || 400 = 200 in series with 200

    def q39():
        m = 1500 * 4 / 3 * math.pi * (1e-3)**3
        V = m * 10 / 5e-9 * (0.12 / math.pi)
        return [i for i, (va, vb) in enumerate([(100, 580), (580, 100), (60, 400), (0, -200)], 1) if abs((vb - va) - V) < 1][0]
    c[39] = q39
    c[40] = lambda: opt(Rational(8, 8 - 2), [4, Rational(3, 4), Rational(4, 3), Rational(4, 5)])
    c[41] = lambda: opt(Rational(16, 10) * sqrt(3) / 2, [3 * sqrt(3) / Rational(16, 10), sqrt(3), Rational(32, 10) / sqrt(3), 4 * sqrt(3) / 5])
    c[42] = lambda: opt(2 * (1 / (300 * Rational(1, 10000))) / 300, [Rational(9, 2), Rational(2, 9), Rational(1, 3), 3])
    c[44] = lambda: nearest((83 * 1.007825 + 126 * 1.008665 - 208.980388) * 931 / 209, [7.48, 7.84, 8.79, 6.94])
    def q45():
        t1, t2 = (pi / 2 - pi / 3) / 50, (pi - pi / 3) / 50     # v = 0 when the phase is pi/2; a = 0 when it is pi
        pairs = [(pi / 300, pi / 75), (pi / 75, pi / 300), (pi / 300, pi / 25), (pi / 50, pi / 100)]
        return [i for i, (a, b) in enumerate(pairs, 1) if simplify(a - t1) == 0 and simplify(b - t2) == 0][0]
    c[45] = q45
    c[46] = lambda: round(1 / (math.acos(math.sqrt(3 / 4)) * 2 / (2 * math.pi)))    # phase pi/3 -> path lambda/6
    c[47] = lambda: (4 / 2)**5                     # B ~ v / r^2 ~ n^-5
    c[48] = lambda: 5 * (8 - 8.36 / 4.18) * 10
    c[49] = lambda: round((1 + 60 / (2 * 30)) * 10)      # biconvex, R = 60 both sides, f = 30
    c[50] = lambda: round(2 * (40 * 9 / 3) / (2 / 5 * 10))   # ML^2/3 = (2/5) m R^2 -> R^2 = alpha/2

    # ---- Chemistry
    c[51] = lambda: nearest(3.38 / 26 * 2 * 44, [5.68, 11.44, 22.74, 17.05])
    c[52] = lambda: nearest(8.1e-8 * 0.1 / 0.1, [0.1, 9.53e-6, 8.1e-8, 1.0e-13])
    def q54():
        dU = 10 - 18                       # X -> Y: q - w (w = work done by the gas)
        w = -6 - (-dU)                     # Y -> X: dU = +8 = q - w with q = -6
        texts = [('by', 18), ('by', 2), ('on', 12), ('on', 14)]
        return texts.index(('by', w) if w > 0 else ('on', -w)) + 1
    c[54] = q54
    def q55():
        pi_ = lambda grams, litres: grams / 50000 / litres * 0.083 * 300
        xyz = (pi_(1, 0.5), pi_(2, 1), pi_(3, 1.5))
        opts = [(9.96e-4,) * 3, (9.96e-4, 9.96e-4, 19.92e-4), (4.98e-4, 4.98e-4, 9.96e-4), (4.98e-4,) * 3]
        return [i for i, o in enumerate(opts, 1) if all(abs(a - b) < 1e-6 for a, b in zip(o, xyz))][0]
    c[55] = q55
    def q56():
        a = round(-math.log10(math.sqrt(5e-4 * 0.2)), 1); b = 3.3        # half-neutralised: pH = pKa
        return [(0.7, 2.0), (2.0, 3.3), (1.1, 2.2), (3.0, 2.2)].index((a, b)) + 1
    c[56] = q56
    c[62] = lambda: nearest(0.25 * 12 / 44 / 0.25 * 1000, [273, 27, 2730, 227])
    c[71] = lambda: round(6.6e-34 * 3e8 / (2.8e-20 + 2.3 * 1.6e-19) * 1e9 / 100)
    c[72] = lambda: round((300 - 600 / 2.5) / 3)
    c[73] = lambda: round(0.8 * 6 * 96500 * (1.23 - 0.02) / 1000)
    c[75] = lambda: round(1 / (7 * 12 + 8 + 80 + 14) * (108 + 80))
    return c
