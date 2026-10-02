"""Answer checks for JEE Main 2026 (Session 2), 6 Apr Shift 1. Q50 is disputed (see solutions.csv)."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        xs = [k / 1000 for k in range(-5000, 5001) if -3 <= (k / 1000 + math.floor(k / 1000)) <= 3]
        assert min(xs) == -1 and max(xs) < 2 and max(xs) > 1.99
        return opt(1 + 4, [2, 5, 10, 13])
    c[1] = q1

    def q2():
        k = Symbol('k')
        D = k**2 - 15 * k + 27
        kv = solve(2 * (9 * (k - 1))**2 / 9 - 18 * D, k)            # roots r, 2r: 2(sum/3)^2 = product
        kv = [v for v in kv if D.subs(k, v) != 0]
        return opt(6 * kv[0], [4, 6, 8, 12])
    c[2] = q2

    def q3():
        both, mixed = [], []
        for k in range(0, 60001):
            a = k / 10000
            if a * a - 8 <= 0: continue
            r1, r2 = (a - math.sqrt(a * a - 8)) / 2, (a + math.sqrt(a * a - 8)) / 2
            if r1 > 1: both.append(a)
            if 0 < r1 < 1 < r2: mixed.append(a)
        al, be, ga = min(both), max(both), min(mixed)
        return nearest(al**2 + be**2 + ga**2, [18, 22, 26, 34])
    c[3] = q3

    def q4():
        k = Symbol('k')
        r = solve(36 * k**2 + 40 * k - 25, k)
        return opt(9 * sum(r), [-10, -8, 10 * sqrt(13), 8 * sqrt(13)])
    c[4] = q4
    c[5] = lambda: opt(sum((-1)**(n + 1) * n**3 for n in range(1, 16)), [1706, 1856, 1982, 2403])

    def q6():
        g = Symbol('g')
        return opt(sum(solve(g * (1 + (32 - 9 * g) / 2) - 8, g)), [Rational(34, 9), Rational(34, 13), Rational(32, 9), Rational(32, 13)])
    c[6] = q6
    c[7] = lambda: opt(math.comb(len(set('IOEUA')), 2) * math.comb(len(set('NCSQTL')), 2) * 24, [2670, 2840, 2920, 3600])
    c[8] = lambda: opt(Rational(math.comb(26, 13), math.comb(28, 14)), [1, Rational(14, 13), Rational(27, 7), Rational(7, 27)])

    def q9():
        S1 = Rational(2500 - 100, 20); mean = S1 / 20
        S2 = 2500 - 10 * S1 - 500
        return [(2, 1), (3, 1), (3, 2), (4, 1)].index((int(mean / sqrt(S2 / 20 - mean**2)), 1)) + 1
    c[9] = q9
    c[10] = lambda: opt(next(n for n in range(1, 20) if Fraction(n + 2, 2 * (n + 1)) == Fraction(9, 16)), [5, 7, 8, 9])

    def q11():
        e = Rational(5, 3)
        a2 = 36 - 48 / (e**2 - 1)          # 36/a^2 - 48/(a^2 (e^2 - 1)) = 1
        b2 = a2 * (e**2 - 1)
        return opt(2 * (2 * (a2 + 1)) / sqrt(b2), [10, 20, 25, 30])
    c[11] = q11

    def q12():
        t = Symbol('t', positive=True)
        tv = solve(9 * (4 * t**2 - t**2)**2 + 36 * t**2 - 117, t)[0]
        F, P, Q = Matrix([3, 0]), Matrix([3 * tv**2, 6 * tv]), Matrix([12 * tv**2, 12 * tv])
        u, v = P - F, Q - F
        return opt(abs(u[0] * v[1] - u[1] * v[0]) / (u.norm() * v.norm()), [Rational(3, 5), Rational(4, 5), Rational(5, 13), Rational(12, 13)])
    c[12] = q12

    def q13():
        a = Symbol('a')
        for av in solve(6 * a**2 - 7 * a + 2, a):           # from 2 - 2(a + b) + ab = 0 with ab = 1/3
            bv = 1 / (3 * av)
            if 0 < av < 1 and abs(math.atan(1 - av) + math.atan(1 - bv) - math.pi / 4) < 1e-12:
                return opt(6 * (av + bv), [6, 7, 8, 9])
    c[13] = q13

    def q14():
        sols = set()
        for k in range(-3, 3):
            for th in (math.pi / 3 + 2 * k * math.pi, math.pi + 2 * k * math.pi):
                if -2 * math.pi < th < 2 * math.pi and abs(math.cos(th) + 1 - math.sqrt(3) * math.sin(th)) < 1e-9:
                    sols.add(round(th, 9))
        return nearest(sum(sols), [-2 * math.pi / 3, -4 * math.pi / 3, 2 * math.pi / 3, 4 * math.pi / 3])
    c[14] = q14

    def q15():
        a, b, cc, t = symbols('a b cc t')
        P = Matrix([1, 6, a]); I = Matrix([a / 3, 0, a + cc]); M = (P + I) / 2
        eqs = [M[0] - t, M[1] - 1 - 2 * t, M[2] - (a - 1 + b * t), (P - I).dot(Matrix([1, 2, b]))]
        for s in solve(eqs, [a, b, cc, t], dict=True):
            if s[b] > 0:
                F = Matrix([1, 3, s[a] - 1 + s[b]])
                d = Matrix([1, 2, s[b]]) / Matrix([1, 2, s[b]]).norm()
                for S in (F + 2 * sqrt(14) * d, F - 2 * sqrt(14) * d):
                    if S[0] > 0:
                        return opt(sum(S), [19, 20, 21, 22])
    c[15] = q15

    def q16():
        d1 = Matrix([3, 5, 7]).cross(Matrix([1, 4, 7])); d2 = Matrix([2, 1, 2])
        cs = abs(d1.dot(d2)) / (d1.norm() * d2.norm())
        return opt(simplify(sqrt(1 - cs**2) / cs), [3 * sqrt(2) / 2, 5 * sqrt(2) / 2, 5 * sqrt(2) / 3, 4 * sqrt(2) / 3])
    c[16] = q16
    c[17] = lambda: opt(limit(x**2 * sin(x)**2 / (x**2 - sin(x)**2), x, 0), [2, 3, 4, 6])
    c[18] = lambda: opt(integrate(32 * cos(x)**4, (x, 0, pi / 4)), [4 * pi + 2, 3 * pi + 8, 3 * pi + 4, 4 * pi + 3])

    def q19():
        y = Symbol('y')
        return opt(integrate((y**2 + 3) / 4, (y, 0, 3)) + integrate(6 - y, (y, 3, 6)), [8, 9, 12, 15])
    c[19] = q19
    c[20] = lambda: opt(integrate(2**x - x**2, (x, 0, 1)), [(3 - log(2)) / (3 * log(2)), 1 / (3 * log(2)), 3 + log(2), (3 + log(2)) / (2 + log(3))])

    def q21():
        A = Matrix([[-1, 1, -1], [1, 0, 1], [0, 0, 1]])
        a, b = symbols('a b')
        M = A**2 + a * A.adjugate().adjugate() + b * A.adjugate() * A.adjugate().adjugate() - Matrix([[2, -2, 2], [-2, 0, -1], [0, 0, -1]])
        s = solve(list(M), [a, b], dict=True)[0]
        return (s[a] - s[b])**2
    c[21] = q21

    def q22():
        h = Symbol('h', positive=True)
        hv = [v for v in solve(h**2 + (2 * h - 4)**2 - 61, h) if 2 * v - 4 > 0][0]
        return 4 * (36 - (hv - 1)**2)
    c[22] = q22

    def q23():
        a, b = Matrix([1, 1, 1]), Matrix([0, 1, -1])
        cv = (3 * a - a.cross(b)) / 3
        assert a.cross(cv) == b and a.dot(cv) == 3
        return cv.dot(a - 2 * b)
    c[23] = q23

    def q24():
        r, a = Rational(1, 2), 2                  # 2 sqrt(alpha beta) = alpha -> alpha = 4 beta
        s = sum(Fraction(a) * Fraction(1, 2)**k for k in range(10))
        return s.numerator + s.denominator
    c[24] = q24

    def q25():
        C = 1 - Rational(1, 3)
        v = (5 * sqrt(5) / 3 + Rational(8, 3) + C) / sqrt(5)
        return math.floor(float(v))
    c[25] = q25

    # ---- Physics
    c[26] = lambda: nearest((0.02 / 97.42 + 0.05 / 8.35 + 2 * 0.02 / 20.20) * 100, [0.63, 0.82, 0.72, 0.25])
    c[27] = lambda: [(1, Rational(5, 2)), (Rational(3, 2), Rational(5, 2)), (1, 2), (1, Rational(7, 2))].index((1, 2 + Rational(1, 2) + 1)) + 1   # A = E L^(1/2) -> M L^(5/2) T^-2; B = L
    c[28] = lambda: nearest(0.5 * 0.001 * 25 - 0.001 * 10 * 1000, [-8.75, -8.35, -9.55, -9.98])
    c[29] = lambda: nearest((1.5 * 10 - 2 * 5) / (1.5 * 5), [0.33, 0.67, 1, 0.5])
    c[30] = lambda: nearest(4e8 * 3.14 * (4e-3)**2 / 1600 - 10, [2.56, 3.89, 4.32, 5.16])

    def q31():
        I = Rational(2, 5) * 5 * Rational(4, 100)**2; w = 40 * pi
        tau = I * w / 10; turns = w * 10 / 2 / (2 * pi)
        return [(Rational(128, 1000) * pi, 100), (Rational(128, 10000) * pi, 50), (Rational(128, 1000) * pi, 50), (Rational(128, 10000) * pi, 100)].index((simplify(tau), turns)) + 1
    c[31] = q31
    c[32] = lambda: opt(2 + Rational(4, 2), [2, 4, 3, 6])

    def q33():
        h = 10 * cos(pi / 3); half = 10 * sin(pi / 3)
        pts = [(15, Matrix([0, h / 2])), (2, Matrix([-half, -h / 2])), (3, Matrix([half, -h / 2]))]
        G = sum((m * p for m, p in pts), Matrix([0, 0])) / 20
        return [(sqrt(3) / 4, Rational(5, 4)), (sqrt(3) / 4, 1), (0, 0), (Rational(5, 4), 0)].index((simplify(G[0]), G[1])) + 1
    c[33] = q33
    c[34] = lambda: nearest(2.2 * 11 / 20, [1.1, 2.22, 1.21, 4.44])
    c[35] = lambda: opt(2 * Rational(90, 400) / (Rational(1, 400) + Rational(1, 500)), [100, 120, 90, 105])
    c[36] = lambda: opt(cos(pi / 3)**2 / cos(pi / 6)**2, [3, 4, Rational(1, 3), Rational(1, 4)])
    c[37] = lambda: opt(nsimplify(acos(1 / sqrt(2)) / (2 * pi / 5)), [Rational(1, 4), Rational(5, 4), Rational(5, 8), Rational(3, 8)])
    c[38] = lambda: nearest(100 * 2 * math.pi**2 * 8.85e-12 * 0.35**2 * 1e9, [2.14, 2.44, 3.25, 0.7])
    c[39] = lambda: opt((5 - Rational(2, 1) / Rational(1, 2)) / Rational(1, 2), [6, 2, 4, 5])      # V_LED = 2 mW / 0.5 mA = 4 V
    c[41] = lambda: nearest(abs((1.4 / (0.4 - 1 / 4)) / (1.4 * -4)), [1.66, 2.33, 2.66, 1.33])
    c[42] = lambda: nearest((4 * math.pi * 1e-7 * 2 / 0.2)**2 / (2 * 4 * math.pi * 1e-7) * 1e-9 / 1e-14, [6.28, 6.28e-6, 628, 6.28e-4])
    c[43] = lambda: opt((1 - Rational(2, 10)) / (1 - Rational(4, 10)), [Rational(4, 3), Rational(3, 4), Rational(5, 3), Rational(3, 5)])
    c[44] = lambda: [(27, 20), (3, 16), (5, 36), (20, 27)].index((lambda f: (f.numerator, f.denominator))(Fraction(5, 36) / Fraction(3, 16))) + 1
    c[45] = lambda: nearest(80 / math.hypot(80, 60), [0.8, 0.64, 0.9, 0.5])

    def q46():
        V = Symbol('V')
        Vs = solve((2 - V) / 3 - V / 4 - (V - 3) / 6, V)[0]
        I6 = (Vs - 3) / 6
        return round(float(6 * I6**2 * 100 * 100))
    c[46] = q46
    c[47] = lambda: round(math.degrees(math.acos(math.sqrt(3 / 4))))
    c[48] = lambda: round(7000 / 17.13 / 7 * 6e23 * (7.0183 + 1.008 - 2 * 4.004) * 931e6 / 1e32)
    c[49] = lambda: 3 * (25 - 0 + (1 - (-8)) + 4 * (2 - (-5)))
    c[71] = lambda: round(3.5e-3 / 7 * (520 + 7297))
    c[72] = lambda: round(3 * 14 / (12 * 12 + 11 + 3 * 14) * 100)
    c[73] = lambda: round(4.7 / 94 * 0.6 * 100)
    c[74] = lambda: round(100 * 0.5**(6 / 3))
    c[75] = lambda: round(abs((28400 - (-8.3 * 300 * 2.3 * (0.30 + 2 * 0.48 - 1 - 7))) / 300))

    # ---- Chemistry MCQs
    c[51] = lambda: ['FeO', 'Fe2O3', 'Fe3O4', 'FeO3'].index({(1, 1): 'FeO', (2, 3): 'Fe2O3', (3, 4): 'Fe3O4'}[
        (lambda r: next((a, b) for a in range(1, 5) for b in range(1, 5) if abs(b / a - r) < 0.03))((30.1 / 16) / (69.9 / 56))]) + 1
    c[52] = lambda: opt(1 / (4 * (Rational(1, 4) - Rational(1, 9))), [Rational(9, 5), Rational(36, 5), Rational(1, 4), Rational(5, 9)])
    c[56] = lambda: opt(100 * (1 - Rational(25, 125)), [50, 60, 70, 80])
    c[57] = lambda: [(3.28, 2.624), (2.624, 3.28), (3.28, 0.656), (0.656, 6.56)].index((round(0.082 * 400 / 10, 3), round(0.8 * 0.082 * 400 / 10, 3))) + 1
    return c
