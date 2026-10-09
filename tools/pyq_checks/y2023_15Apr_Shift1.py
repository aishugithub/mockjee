"""Answer checks for JEE Main 2023 (Session 2), 15 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Abs, floor, Interval, Union, S as SS, solveset, Eq


def checks():
    c = {}

    def q1():
        d = (solveset((4 * x + 3) * (x + 2) > 0, x, SS.Reals)
             .intersect(Interval(-1, Rational(-1, 2)))          # -1 <= 4x+3 <= 1
             .intersect(Interval(Rational(-9, 10), Rational(-3, 10))))  # -1 <= (10x+6)/3 <= 1
        assert d == Interval.Lopen(Rational(-3, 4), Rational(-1, 2))
        return opt(36 * abs(d.inf + d.sup), [45, 54, 63, 72])
    c[1] = q1

    def q2():
        roots = []
        for lo, hi, expr in [(0, oo, x**2 - 5 * (x + 2) + 6), (-2, 0, -x**2 - 5 * (x + 2) + 6),
                             (-oo, -2, -x**2 + 5 * (x + 2) + 6)]:
            roots += [r for r in solve(expr, x) if r.is_real and (lo <= r) and (r < hi if hi != 0 else r < 0)]
        return opt(len(set(roots)), [6, 3, 5, 4])
    c[2] = q2

    def q3():
        y = Symbol('y', real=True)
        z = 3 + sympy_I * y
        re_ = simplify(((z - z.conjugate() + z * z.conjugate()) / (2 - 3 * z + 5 * z.conjugate())).as_real_imag()[0])
        assert simplify(re_ - (9 - y**2) / (8 * (1 + y**2))) == 0
        hi, lo = re_.subs(y, 0), limit(re_, y, oo)        # decreasing in y^2: max at y = 0, inf as y -> oo
        return opt(24 * (hi - lo), [27, 30, 36, 42])
    c[3] = q3

    def q4():
        m, n = symbols('m n')
        s = solve([4 * m + n - 22, 17 * m + 4 * n - 93], [m, n])
        mv, nv = s[m], s[n]
        detA = mv - nv
        d_mA = mv**mv * detA                       # order m
        d_adjadj = d_mA**((mv - 1)**2)
        total = nv**mv * d_adjadj                  # det(n M) = n^order det M
        assert total == 2**5 * 5**80 * 3**16
        c_ = 5; a_ = 16 - c_; b_ = 80
        assert 3**a_ * 5**b_ * 6**c_ == total
        return opt(a_ + b_ + c_, [84, 96, 101, 109])
    c[4] = q4

    def q5():
        X, Y, Z = symbols('X Y Z')
        s = solve([-X + 2 * Y - 9 * Z - 7, -X + 3 * Y + 7 * Z - 9, -2 * X + Y + 5 * Z - 8], [X, Y, Z])
        lam = -3 * s[X] + s[Y] + 13 * s[Z]
        d = abs(2 * s[X] - 2 * s[Y] + s[Z] - lam) / 3
        return opt(d, [7, 9, 11, 13])
    c[5] = q5

    c[6] = lambda: opt(sum(1 for t in product('1358', repeat=3) if int(''.join(t)) % 3 == 0), [18, 20, 21, 22])

    def q7():
        for a_, b_, c_ in product(range(1, 6), repeat=3):
            p = Poly(expand((a_ + b_ * x + c_ * x**2)**10), x)
            if p.coeff_monomial(x) == 20 and p.coeff_monomial(x**2) == 210:
                return opt(2 * (a_ + b_ + c_), [6, 8, 12, 15])
    c[7] = q7

    def q8():
        a, r = symbols('a r', positive=True)
        b = a * r**4
        G1, G2, G3 = a * r, a * r**2, a * r**3
        lhs = G1**4 + G2**4 + G3**4 + G1**2 * G3**2
        S_ = a + b                                    # A1 + A2
        opts = [2 * S_ * G1 * G3, S_ * G1**2 * G3**2, S_**2 * G1 * G3, 2 * S_ * G1**2 * G3**2]
        return [i for i, o in enumerate(opts, 1) if simplify(lhs - o) == 0][0]
    c[8] = q8

    def q9():
        f = lambda t: max(1 + t + math.floor(t), 2 + t, t + 2 * math.floor(t))
        pts = [Fraction(k, 1000) for k in range(0, 2001)]
        jumps = [p for p in pts[1:] if abs(f(p) - f(p - Fraction(1, 10**6))) > 1e-3]
        m_ = len(jumps)                               # only x = 2
        n_ = 0                                        # f = 2 + x on [0, 2): smooth inside (0, 2)
        assert m_ == 1 and all(f(p) == 2 + p for p in pts[:-1])
        return opt((m_ + n_)**2 + 2, [2, 3, 6, 11])
    c[9] = q9

    def q10():
        import mpmath
        val = mpmath.quad(lambda t: 1 / ((5 + 2 * t - 2 * t**2) * (1 + mpmath.e**(2 - 4 * t))), [0, 1])
        al, be = mpmath.sqrt(11), mpmath.sqrt(10)
        assert abs(val - mpmath.log((al + 1) / be) / al) < 1e-12
        return opt(Rational(121 - 100), [-21, 0, 19, 21])
    c[10] = q10

    def q11():
        t = symbols('t', positive=True)
        C = Symbol('C')
        xs = ((Rational(2, 3) * t**Rational(3, 2) - 4 * sqrt(t) + C) / sqrt(t))
        Cv = solve(xs.subs(t, 4) - 1, C)[0]
        # check it solves the ODE: 2(y+2)ln(y+2) dx/dy + x + 4 - 2 ln(y+2) = 0 with t = ln(y+2)
        y = Symbol('y', positive=True)
        X = xs.subs(C, Cv).subs(t, log(y + 2))
        assert simplify(2 * (y + 2) * log(y + 2) * diff(X, y) + X + 4 - 2 * log(y + 2)) == 0
        return opt(simplify(xs.subs({C: Cv, t: 9})), [3, Rational(10, 3), Rational(4, 9), Rational(32, 9)])
    c[11] = q11

    def q12():
        X, Y = symbols('X Y')
        A, B, C = Matrix([3, -7]), Matrix([-1, 2]), Matrix([4, 5])
        P = Matrix([X, Y])
        s = solve([(P - A).dot(C - B), (P - B).dot(C - A)], [X, Y])
        return opt(9 * s[X] - 6 * s[Y] + 60, [25, 30, 35, 40])
    c[12] = q12

    def q13():
        c1, r1 = Matrix([9, Rational(15, 2)]), sqrt(81 + Rational(225, 4) - 131)
        c2, r2 = Matrix([3, 3]), sqrt(9 + 9 + 7)
        d = sqrt((c1 - c2).dot(c1 - c2))
        n = 3 if d == r1 + r2 else (4 if d > r1 + r2 else (2 if d > abs(r1 - r2) else 1))
        return opt(n, [1, 2, 3, 4])
    c[13] = q13

    def q14():
        p1, p2, p3 = Matrix([-1, -2, -3]), Matrix([9, 3, 4]), Matrix([9, -2, 1])
        nrm = (p2 - p1).cross(p3 - p1)
        P = Matrix([3, -2, -9])
        Q = P - nrm * (nrm.dot(P - p1)) / nrm.dot(nrm)
        return opt(sqrt(Q.dot(Q)), [sqrt(35), sqrt(38), sqrt(29), sqrt(42)])
    c[14] = q14

    def q15():
        lam = Symbol('lam')
        d1, d2 = Matrix([0, 4, 1]), Matrix([3, -4, 0])
        nrm = d1.cross(d2)
        w = Matrix([-lam, 0, 6]) - Matrix([lam, 3, -6])
        sols = solve(w.dot(nrm)**2 - (13 * sqrt(nrm.dot(nrm)))**2, lam)
        return opt(8 * abs(sum(sols)), [302, 304, 306, 308])
    c[15] = q15

    def q16():
        mu = Symbol('mu')
        lam = mu + 5
        sols = solve(Matrix([[lam, -1, 1], [1, 2, mu], [3, -4, 5]]).det(), mu)
        return opt(sum(80 * ((m + 5)**2 + m**2) for m in sols), [2130, 2210, 2290, 2370])
    c[16] = q16

    def q17():
        a, b, cc, d = [Matrix(symbols(f'{p}1:3')) for p in 'abcd']
        lhs = (b - a) - (cc - b) + (d - a) - (cc - d)
        E, F = (a + cc) / 2, (b + d) / 2
        k = Symbol('k')
        return opt(solve((lhs - k * (E - F))[0], k)[0], [-4, -2, 2, 4])
    c[17] = q17

    def q18():
        from math import comb
        p = sum(Rational(1, 6) * Rational(comb(6, k), comb(10, k)) for k in range(1, 7))
        return opt(p, [Rational(1, 5), Rational(11, 50), Rational(9, 50), Rational(1, 4)])
    c[18] = q18

    def q19():
        n, s1, s2 = 10, 200, 10 * (64 + 400)
        s1, s2 = s1 - 50 + 40, s2 - 2500 + 1600
        return opt(Rational(s2, n) - Rational(s1, n)**2, [11, 12, 13, 14])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=2))
        neg = [not (p and (q and not (p and q))) for p, q in rows]
        opts = [lambda p, q: not (p or q), lambda p, q: p or q,
                lambda p, q: (not (p and q)) and q, lambda p, q: (not (p and q)) or p]
        return [i for i, f in enumerate(opts, 1) if [f(p, q) for p, q in rows] == neg][0]
    c[20] = q20

    c[21] = lambda: sum(1 for a, b, cc, d in product(range(1, 5), repeat=4) if 2 * a + 3 * b == 4 * cc + 5 * d)

    def q22():
        n = 0
        for t in product(range(8), repeat=4):
            if len(set(t)) == 4 and max(t) == 7 and t[0] + t[1] == t[2] + t[3]:
                n += 1
        return n
    c[22] = q22

    c[23] = lambda: sum(1 for n in range(10, 101) if (pow(3, n, 7) - 3) % 7 == 0)

    def q24():
        a, b = Rational(1, 2), Rational(-1, 3)
        s = (a**2 / (1 - a) - b**2 / (1 - b)) / (a - b)
        k = 50
        partial = sum(sum(a**(j - i) * b**i for i in range(j + 1)) for j in range(1, k))
        assert abs(float(partial - s)) < 1e-12
        return s.p + 3 * s.q
    c[24] = q24

    def q25():
        t = Symbol('t', real=True)
        g = sqrt(t**2 + 16) + sqrt((t - 2)**2 + 9)
        crit = [r for r in solve(diff(g, t), t) if 0 <= r <= 4]
        cands = crit + [0, 4]
        vals = {cv: g.subs(t, cv) for cv in cands}
        mx = max(vals, key=lambda k: float(vals[k])); mn = min(vals, key=lambda k: float(vals[k]))
        assert mn == Rational(8, 7)
        return 6 * mx + 21 * mn
    c[25] = q25

    def q26():
        F = atan(5 * x / (sqrt(3) * sqrt(4 - 3 * x**2))) / (5 * sqrt(3))
        assert simplify(diff(F, x) - 1 / ((3 + 4 * x**2) * sqrt(4 - 3 * x**2))) == 0 and F.subs(x, 0) == 0
        al, be = 5, sqrt(3)                           # f(1) = (1/(5 sqrt3)) tan^-1(5/sqrt3)
        assert simplify(F.subs(x, 1) - atan(al / be) / (al * be)) == 0
        return al**2 + be**2
    c[26] = q26

    def q27():
        y = Symbol('y')
        region = integrate(3 - y - Rational(2, 3) * y**2, (y, 0, Rational(3, 2)))
        A = region - pi / 4                         # quarter-of-a-half: sector of angle pi/4, radius sqrt2
        return simplify(4 * (pi + 4 * A))
    c[27] = q27

    def q28():
        b = Rational(1, 2); a = 2 * b               # ae = b sqrt3, a^2 = b^2 + a^2 e^2 -> a = 2b; LR = 2b^2/a = b
        assert 2 * b**2 / a == Rational(1, 2)
        return (2 * a + 2 * b)**2
    c[28] = q28

    def q29():
        k = Symbol('k')
        nrm = Matrix([2, 1, -1]) + k * Matrix([5, -3, 4])
        kv = solve(nrm.dot(Matrix([2, 4, 5])), k)[0]
        nrm = nrm.subs(k, kv); const = -3 + 9 * kv
        A, d = Matrix([8, -1, -19]), Matrix([-3, 4, 12])
        t = Symbol('t')
        tv = solve(nrm.dot(A + t * d) + const, t)[0]
        return abs(tv) * sqrt(d.dot(d))
    c[29] = q29

    def q30():
        # x = y = z = t: t * sum(sin A) = 18 and t * sum(sin 2A) = 9 -> sum(sin A) / sum(sin 2A) = 2
        # sum(sin A) = 4 prod cos(A/2), sum(sin 2A) = 4 prod sin A = 32 prod sin(A/2) cos(A/2)  -> prod sin(A/2) = 1/16
        A_, B_ = 1.1, 0.7                           # spot-check the two identities numerically
        C_ = math.pi - A_ - B_
        s1 = math.sin(A_) + math.sin(B_) + math.sin(C_)
        s2 = math.sin(2 * A_) + math.sin(2 * B_) + math.sin(2 * C_)
        assert abs(s1 - 4 * math.cos(A_ / 2) * math.cos(B_ / 2) * math.cos(C_ / 2)) < 1e-12
        assert abs(s2 - 4 * math.sin(A_) * math.sin(B_) * math.sin(C_)) < 1e-12
        return 80 * Rational(1, 16)
    c[30] = q30

    # Physics
    c[32] = lambda: opt(Rational(3, 2) / Rational(3, 2), [Rational(399, 20), 1, Rational(399, 10), 2])
    c[33] = lambda: opt(Rational(1, 2) * (4 - 2) * (400 - 100), [0, 200, 100, 300])
    c[34] = lambda: opt((2 * 2) / Rational(2**2), [1, 2, 4, Rational(1, 2)])        # in units of l
    g, R = symbols('g R', positive=True)

    def q35():
        v2 = 2 * g * R**2 * (1 / R - 1 / (2 * R))     # GM = gR^2
        return opt(sqrt(v2), [sqrt(2 * g * R), sqrt(4 * g * R), sqrt(g * R / 2), sqrt(g * R)])
    c[35] = q35

    def q36():
        G, m, a = symbols('G m a', positive=True)
        w = sqrt(G * m**2 / (2 * a)**2 / (m * a))
        return opt(w, [sqrt(G * m / (2 * a**3)), sqrt(G * m / (4 * a**3)), sqrt(G * m / (8 * a**3)), sqrt(G * m / a**3)])
    c[36] = q36

    def q37():
        Amag = 2 * sqrt(3) / cos(pi / 6)
        return opt(simplify(Amag * sin(pi / 6)), [2, sqrt(3), 1 / sqrt(3), 6])
    c[37] = q37

    c[38] = lambda: opt(diff(5 * x**2 - 4 * x + 5, x).subs(x, 2), [14, 16, 10, 6])

    def q39():
        a, b, cc = symbols('a b c')
        s = solve([cc, a + b - 3 * cc - 1, -2 * b + 1], [a, b, cc])    # M, L, T
        opts = [(1, 1, 0), (Rational(1, 2), 0, Rational(1, 2)), (Rational(1, 2), Rational(1, 2), 0), (1, -1, 0)]
        return [i for i, o in enumerate(opts, 1) if o == (s[a], s[b], s[cc])][0]
    c[39] = q39

    def q40():
        t = Symbol('t')
        acc = [diff(e, t, 2) for e in (10 * t, 15 * t**2, 7)]
        assert acc == [0, 30, 0]
        return 2                                    # +y
    c[40] = q40

    def q42():
        Rm = 6400e3
        d = math.sqrt(2 * Rm * 180) + math.sqrt(2 * Rm * 245)
        return opt(round(d / 1000), [48, 56, 96, 104])
    c[42] = q42

    def q43():
        # battery + terminal on the right (node B): B -D3- 10 ohm -> L, and B -10- T -D1- 10 -> L; D2 is reverse biased
        Req = Rational(10 * 20, 10 + 20)
        return opt(10 / Req, [Rational(3, 2), Rational(5, 2), 1, 2])
    c[43] = q43

    c[44] = lambda: opt(1 - Rational(1, 2)**3, [Rational(1, 4), Rational(1, 8), Rational(3, 4), Rational(7, 8)])
    c[45] = lambda: opt(1 / sqrt(Rational(1, 4)), [Rational(1, 2), 2, 1 / sqrt(2), sqrt(2)])   # in units of lambda
    c[46] = lambda: opt(Rational(600, 1000) / sin(pi / 6), [Rational(6, 10), Rational(12, 10), Rational(18, 10), 3])
    c[48] = lambda: opt(Rational(20) * Rational(1, 1000) / (Rational(12, 6)) * 1000, [5, 8, 10, 12])   # mH

    def q49():
        Rv = 50 / Rational(1, 1000) - 54            # 49946 ohm ~ 50 kOhm  -> (A)
        r = Rational(1, 1000) * 54 / (Rational(10, 1000) - Rational(1, 1000))   # 6 ohm -> (C)
        assert abs(Rv - 50000) < 100 and r == 6
        return 1                                    # (A) and (C)
    c[49] = q49

    c[51] = lambda: 2 * (Rational(18, 20)) * 50
    c[52] = lambda: 1000 * 10 * Rational(1, 10) + 2 * Rational(75, 1000) / Rational(1, 1000)
    c[53] = lambda: (2 / (sqrt(Rational(2, 5)) / sqrt(Rational(1, 2))))**2
    c[54] = lambda: integrate(5 * x, (x, 2, 4))
    c[55] = lambda: solve((2 + x + 3) * 10 - 100, x)[0]

    def q56():
        n = Symbol('n')
        r = (Rational(1, 9) - Rational(1, 16)) / (Rational(1, 4) - Rational(1, 9))   # lambda1/lambda2
        return solve(r - Rational(7, 4) / n, n)[0]
    c[56] = q56

    c[57] = lambda: 2 * asin(sqrt(2) * sin(pi / 6)) * 180 / pi - 60
    c[58] = lambda: Rational(1, 2) * Rational(2, 10) * (210 * 2 * Rational(22, 7) / 60) * Rational(2, 10)**2 * 1000

    def q59():
        v = 1e-7 * 1.6e-19 * 6.76e6 / (0.52e-10)**2
        return round(v, 6)
    c[59] = q59

    def q60():
        I = Rational(9, 6)
        return abs((9 - I * 2) - (9 - I * 4))
    c[60] = q60

    # Chemistry
    c[81] = lambda: 20 * Rational(1, 100) * 2 / Rational(1, 10)
    c[82] = lambda: round(30400 / 28.4)

    def q83():
        nw, ng = Rational(120 - 30, 18), Rational(30, 180)
        return math.floor(float(24 * nw / (nw + ng)))   # 23.23 -> 23
    c[83] = q83

    def q85():
        Ea_cat = 300 * Rational(300, 600)             # same rate: Ea/T equal
        return Ea_cat - 20
    c[85] = q85

    c[86] = lambda: 20 * Rational(1, 2) / Rational(200, 1000)          # mmol per litre of sol
    c[87] = lambda: sum(1 for z in (8 + 2, 9 + 1, 13, 12 - 2, 11 - 1, 8 - 1, 12, 13 - 3, 9) if z == 10)
    c[88] = lambda: 7 - 2
    c[90] = lambda: solve(x + 2 * (-2) + 2 * (-1), x)[0]
    return c
