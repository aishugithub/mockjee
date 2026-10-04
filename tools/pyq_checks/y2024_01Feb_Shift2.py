"""Answer checks for JEE Main 2024 (Session 1), 1 Feb Shift 2. Q3 and Q12 were dropped by NTA; Q35 and Q42 are disputed."""
from pyq_checks.common import *
from sympy import Function, Eq, dsolve


def checks():
    c = {}

    def q1():
        ok = [v / 10 for v in range(-200, 201) if (v / 10)**2 >= 25 and (v / 10)**2 != 4 and (v / 10)**2 + 2 * v / 10 - 15 > 0]
        assert max(w for w in ok if w < 0) == -5.1 and min(w for w in ok if w > 0) == 5.0
        return opt((-5)**2 + 5**3, [125, 140, 150, 175])
    c[1] = q1

    def q2():
        r1_reflexive = all(a * a + a * a == 1 for a in (0, 1, 0.5))
        pts = [(a, b) for a in range(1, 6) for b in range(1, 6)]
        R2 = lambda p, q: p[0] + q[1] == p[1] + q[0]
        eq2 = all(R2(p, p) for p in pts) and all(R2(q, p) for p in pts for q in pts if R2(p, q)) and \
            all(R2(p, r) for p in pts for q in pts for r in pts if R2(p, q) and R2(q, r))
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(r1_reflexive, eq2)]
    c[2] = q2

    def q4():
        k = solve(1 / Symbol('k') - Rational(3, 4), Symbol('k'))[0]
        p, q, r = 1, k, k * k
        al, be = solve(p * x**2 + q * x - r, x)
        return opt(simplify((al - be)**2), [9, Rational(80, 9), Rational(20, 3), 8])
    c[4] = q4

    def q5():
        a, b = symbols('a b')
        s = solve([a + 2 * b - 4, 2 * a + 3 * b - 3], [a, b])
        lam, mu = 3 * s[a] + s[b], 5 * s[a] + 9 * s[b]
        assert Matrix([[1, 2, 3], [2, 3, 1], [4, 3, lam]]).det() == 0
        return opt(lam + 2 * mu, [17, 22, 15, 28])
    c[5] = q5

    def q6():
        T = lambda r: math.comb(18, r) * Rational(1, 3)**(18 - r) * Rational(1, 2)**r
        return opt((T(12) / T(6))**Rational(1, 3), [Rational(1, 4), Rational(1, 9), Rational(4, 9), Rational(9, 4)])
    c[6] = q6

    def q7():
        a, d = symbols('a d')
        s = solve([5 * (2 * a + 9 * d) - 390, 7 * (a + 9 * d) - 15 * (a + 4 * d)], [a, d])
        S = lambda n: Rational(n, 2) * (2 * a + (n - 1) * d)
        return opt((S(15) - S(5)).subs(s), [690, 800, 890, 790])
    c[7] = q7

    def q8():
        f = lambda t: abs(2 * t * t + 5 * abs(t) - 3)
        h = 1e-6
        corners = [p for p in (-0.5, 0.0, 0.5) if abs((f(p + h) - f(p)) / h - (f(p) - f(p - h)) / h) > 1e-3]
        return opt(0 + len(corners), [0, 2, 3, 5])
    c[8] = q8

    def q9():
        f = lambda n: n - 1 if n % 2 == 0 else 2 * n
        a = [n for n in range(1, 200) if f(f(f(n))) == 21][0]
        return opt(limit(Abs(x)**3 / a - 0, x, a, '-'), [121, 144, 169, 225])        # [x/a] = 0 just left of a
    from sympy import Abs
    c[9] = q9

    def q10():
        v = integrate(cos(x)**4, (x, 0, pi / 3))
        a, b = v.coeff(pi), expand(v - v.coeff(pi) * pi).coeff(sqrt(3))
        return opt(9 * a + 8 * b, [3, 2, Rational(3, 2), 1])
    c[10] = q10

    def q11():
        import mpmath
        g = lambda t: 2 * t**3 - 3 * t**2 - t + 1
        v = mpmath.quad(lambda t: mpmath.sign(g(t)) * abs(g(t))**(mpmath.mpf(1) / 3), [0, 0.5, 1])
        return nearest(float(v), [-1, 0, 1, 2])
    c[11] = q11

    def q13():
        b = (3 * 2 + 4 * 3) / Rational(7)
        return opt(sqrt(1 - (b / 3)**2), [sqrt(13) / 7, Rational(11, 19), sqrt(139) / 23, Rational(13, 21)])
    c[13] = q13

    def q14():
        xs = solve(x**2 + (1 - x)**2 - (1 - x), x)
        P = [Matrix([v, 1 - v]) for v in xs]
        return opt((P[0] - P[1]).norm(), [1, sqrt(2), 1 / sqrt(2), Rational(1, 2)])
    c[14] = q14

    def q15():
        P, A, d = Matrix([3, 4, 9]), Matrix([1, -1, 2]), Matrix([3, 2, 1])
        F = A + ((P - A).dot(d) / d.dot(d)) * d
        return opt(14 * sum(2 * F - P), [102, 108, 132, 138])
    c[15] = q15

    def q16():
        s = Symbol('s')
        Pt = Matrix([-3, 4, -1]) + s * Matrix([8, 2, 2]); R = Matrix([1, 2, 3])
        s1, s2 = solve((Pt - R).dot(Pt - R) - 36, s)
        G = (Pt.subs(s, s1) + Pt.subs(s, s2) + R) / 3
        return opt(G.dot(G), [18, 24, 26, 36])
    c[16] = q16

    def q17():
        A, B, C = Matrix([1, 3, 2]), Matrix([-2, 8, 0]), Matrix([3, 6, 7])
        cl, bl = (B - A).norm(), (C - A).norm()
        D = (bl * B + cl * C) / (bl + cl)
        return opt(simplify((D - A).dot(C - A) / bl), [sqrt(19), 37 / (2 * sqrt(38)), sqrt(38) / 2, 39 / (2 * sqrt(38))])
    c[17] = q17
    c[18] = lambda: opt(Rational(5, 7) - Rational(1, 5), [Rational(3, 35), Rational(24, 35), Rational(18, 35), Rational(9, 35)])

    def q19():
        S1, S2 = 12, 10 * (Rational(84, 25) + Rational(36, 25))
        hits = [(a, b) for a in range(1, 10) for b in range(1, 10) if S1 - 10 * a == 2 and S2 - 2 * b * S1 + 10 * b * b == 40]
        a, b = hits[0]
        return opt(Rational(b, a), [1, 2, Rational(3, 2), Rational(5, 2)])
    c[19] = q19

    def q20():
        roots = [r for r in Poly(4 * x**3 + 4 * x**2 + 4 * x - 13, x).nroots() if abs(im(r)) < 1e-12 and abs(re(r)) <= 1]
        return opt(len(roots), [0, 1, 2, 3])
    from sympy import im, re
    c[20] = q20

    def q21():
        a = symbols('a', real=True)
        M = Matrix([cos(a), sin(a)])
        A = eye(2) - 2 * M * M.T
        ev = [simplify(e) for e in A.eigenvals()]
        return sum(e**2 for e in ev)
    from sympy import eye
    c[21] = q21
    c[22] = lambda: math.comb(20, 2) - math.comb(10, 2) - (math.comb(10, 2) - 1)

    def q23():
        rmax = (1 + math.sqrt(5)) / 2
        rs = [1 + k * (rmax - 1) / 100 for k in range(1, 100)]
        vals = {3 * math.floor(r) + math.floor(-r) for r in rs}
        assert len(vals) == 1
        return vals.pop()
    c[23] = q23
    c[24] = lambda: sum(2 + Rational(5, 2) * r for r in range(1, 13))

    def q25():
        y = (sqrt(x) + 1) * (x**2 - sqrt(x)) / (x * sqrt(x) + x + sqrt(x)) + Rational(1, 15) * (3 * cos(x)**2 - 5) * cos(x)**3
        return simplify(96 * diff(y, x).subs(x, pi / 6))
    c[25] = q25

    def q26():
        k, y = symbols('k y', positive=True)
        y0 = 1 / (k / 2 + 2 / k)
        A = integrate(y - k * y**2 / 2 - 2 * y**2 / k, (y, 0, y0))
        kv = [v for v in solve(diff(A, k), k) if v > 0]
        return sum(v**2 + v**2 for v in kv)              # k = 2 and, by symmetry of |c|, k = -2
    c[26] = q26

    def q27():
        Y = Symbol('Y')
        X = Function('X')
        s = dsolve(Eq(X(Y).diff(Y), (1 + X(Y) - Y**2) / Y), X(Y), ics={X(1): 1})
        return 5 * s.rhs.subs(Y, 2)
    c[27] = q27

    def q28():
        a, b = symbols('a b', positive=True)
        S1 = integrate((a - b) * x + a * b - x**2, (x, -b, a))       # chord y = (a - b)x + ab above y = x^2
        S2 = (a * b**2 + a**2 * b) / 2
        r = simplify(S1 / S2)
        m = r.subs(b, a)
        return Rational(m).p + Rational(m).q
    c[28] = q28

    def q29():
        A = Matrix([-1, 0]); B = Matrix([3, 0])
        C = A + 4 * Matrix([cos(2 * pi / 3), sin(2 * pi / 3)])
        assert (B - C).norm() == 4 * sqrt(3)
        X = Symbol('X')
        sl = (C[1] - B[1]) / (C[0] - B[0])
        al = solve(sl * (X - 3) - (X + 3), X)[0]
        be = al + 3
        return simplify(be**4 / al**2)
    c[29] = q29

    def q30():
        a, b = Matrix([1, 1, 1]), Matrix([-1, -8, 2])
        cv = b + 5 * a
        cs2 = cv.dot(Matrix([3, 4, 1]))**2 / (cv.dot(cv) * 26)
        return math.floor(1 / cs2 - 1)
    c[30] = q30
    c[32] = lambda: [i for i, v in enumerate([(-50, 30), (50, -30), (-50, -30), (-30, 50)], 1) if v == (-30 - 20, 30)][0]
    c[33] = lambda: opt(Rational(12, 100) * 25 / Rational(1, 10), [12, 25, 30, 24])
    c[34] = lambda: [i for i, v in enumerate([(2, 1, 1), (4, 2, 2), (2, 3, 3), (-2, -1, -1)], 1) if Matrix(v) == (Matrix([5, 8, 7]) + Matrix([3, -4, -3])) / 4][0]
    c[36] = lambda: [i for i, p in enumerate([3, Rational(7, 2), Rational(5, 2), Rational(3, 2)], 1) if p == 1 + Rational(3, 2)][0]
    c[37] = lambda: opt(4 * 10**2 / (1000 * 4 * Rational(1, 1)), [Rational(1, 100), Rational(1, 10), 10, 100])
    c[38] = lambda: opt(200 * Rational(14, 10) / Rational(4, 10), [600, 700, 800, 850])
    c[39] = lambda: opt(2 / sqrt(16), [Rational(1, 2), 1, Rational(3, 2), 2])
    c[40] = lambda: [i for i, (p, q) in enumerate([(2, 3), (2, 5), (3, 2), (5, 2)], 1) if Rational(p, q) == Rational(2, 2 + 3)][0]

    def q41():
        I = Rational(6, 4 + 2 + 6)
        Q1, Q2 = 4 * I * (4 + 2), 6 * I * (2 + 6)
        return opt(Q1 / Q2, [Rational(2, 3), Rational(1, 2), Rational(3, 2), 1])
    c[41] = q41
    c[43] = lambda: nearest(0.8 * 4000 / 240, [13.33, 15.1, 1.33, 1.59])
    c[44] = lambda: opt(Rational(3 * 10**8, 6 * 10**7), [10, 5, Rational(5, 2), 2])
    c[45] = lambda: opt(2 * 30, [30, 60, 15, 45])                      # sin(theta) = 2/4
    c[46] = lambda: nearest(2e-3 / (6.63e-34 * 6e14), [5e15, 7e16, 6e15, 9e18])
    c[48] = lambda: opt(Rational(66, 10) * 3 / (Rational(660, 100) * Rational(16, 10)) * 8 / 10 * 10, [11, 13, 15, 21])   # E = hc/(lambda e) eV, times 8
    c[49] = lambda: nearest((1 - 0.8 * 3 / 1 / 3) / 20, [0.01, 0.015, 0.02, 0.025])
    c[50] = lambda: opt(solve(2 / Rational(6, 5) - x / (100 - x), x)[0] - 40, [Rational(125, 2), Rational(45, 2), 65, 20])
    c[51] = lambda: simplify(4 * sqrt(x) * diff(4 * sqrt(x), x))
    c[52] = lambda: pi / ((pi / 2) / (Rational(2, 10) * Rational(15, 100) / (2 * Rational(9, 100) / 12)))
    c[53] = lambda: Rational(30, 10)
    c[54] = lambda: sqrt(9)
    c[55] = lambda: (1 / (Rational(2, 1000) * 10 * (1 / sqrt(3)) / (2 * 10**4) * 10**6))**2
    c[56] = lambda: 10 * (10 * 6 / (4 + 6))
    c[57] = lambda: 100 * Rational(1, 100) * Rational(2, 10**4) * Rational(1, 100) / Rational(5, 100) * 10**5
    c[58] = lambda: 2 * pi / (200 * Rational(2, 10) * Rational(1, 100) * pi)
    c[59] = lambda: round(5e-7 * 1 / (4 * 1e-3) * 1e6)
    c[60] = lambda: 9 * 3 * Rational(8, 9) / Rational(3, 4)
    c[64] = lambda: [i for i, (k, p) in enumerate([(7, 3), (7, 5), (5, 5), (3, 5)], 1) if p == 5 and abs(math.log10(108 * 10**5) - k) < 0.1][0]   # Ksp = 108 (10 W/M)^5
    c[81] = lambda: 4 + 2 * 5
    c[82] = lambda: round(2.303 * 8.314 * 300 / 100)
    c[83] = lambda: round(24 / 1.86 * 18.6 * 62 / 1000)
    c[84] = lambda: round(2 * 96500 / 1e5)
    c[85] = lambda: int(10 * 2.00 / 0.0591)
    c[86] = lambda: round(2.303 / 115 * math.log10(0.1 / (0.1 - (0.28 - 0.1) / 2)) * 100)
    c[87] = lambda: Rational(10, 1000) * 2 * 2 * 14 * 100
    return c
