"""Answer checks for JEE Main 2023 (Session 2), 8 Apr Shift 1."""
from pyq_checks.common import *
from sympy import Eq, N as N_, floor


def checks():
    c = {}

    c[1] = lambda: opt(sum(math.comb(10, k) for k in range(3, 7)), [792, 772, 752, 782])

    def q2():
        a = symbols('a', real=True)
        al = [v for v in solve((a + 2)**2 + 16 - (a + 4)**2, a) if v + 4 >= 0][0]
        be = -4
        s, p = al + be, al * be
        opts = [x**2 + 3 * x - 4, x**2 + 7 * x + 12, x**2 + 2 * x - 3, x**2 + x - 12]
        return [i for i, f in enumerate(opts, 1) if f.subs(x, s) == 0 and f.subs(x, p) == 0][0]
    c[2] = q2

    def q3():
        b, cc = 0, 1                                   # from alpha = -1 and beta*gamma = 1
        rts = Poly(x**3 + b * x + cc, x).all_roots()
        al = [r for r in rts if r == -1][0]
        be, ga = [r for r in rts if r != -1]
        assert simplify(be * ga - 1) == 0
        return opt(simplify(b**3 + 2 * cc**3 - 3 * al**3 - 6 * be**3 - 8 * ga**3), [Rational(169, 8), Rational(155, 8), 19, 21])
    c[3] = q3

    def q4():
        A = Matrix([[2, 1, 0], [1, 2, -1], [0, -1, 2]])
        B = 2 * A
        d = B.adjugate().adjugate().adjugate().det()
        n = math.log(int(d), 16)
        return opt(round(n), [10, 8, 12, 9])
    c[4] = q4

    def q5():
        P = Matrix([[sqrt(3) / 2, Rational(1, 2)], [-Rational(1, 2), sqrt(3) / 2]])
        A = Matrix([[1, 1], [0, 1]])
        assert simplify(P * P.T) == Matrix.eye(2)
        M = A**2007                                     # P^T Q^2007 P = A^2007
        a, b, cc, d = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
        return opt(2 * a + b - 3 * cc - 4 * d, [2004, 2005, 2006, 2007])
    c[5] = q5

    c[6] = lambda: opt(math.factorial(8) // (math.factorial(3) * math.factorial(2)) * (math.factorial(5) // math.factorial(4)), [14800, 33600, 16800, 18000])
    c[7] = lambda: opt(math.factorial(6) * math.perm(7, 5), [126 * math.factorial(5)**2, 7 * 360**2, 7 * 720**2, 720])

    def q8():
        for n in range(3, 100):
            for r in range(1, n):
                if math.comb(n, r) == 5 * math.comb(n, r - 1) and math.comb(n, r + 1) == 4 * math.comb(n, r):
                    return opt(math.comb(n, 3), [1827, 3654, 5481, 2436])
    c[8] = q8

    def q9():
        n = symbols('n')
        j = symbols('j')
        from sympy import summation
        s = expand(summation(((j + 1) / Rational(2))**2, (j, 1, n)) * 24)
        p = Poly(s, n)
        assert p.coeff_monomial(1) == 0
        B, C, D = p.coeff_monomial(n**3), p.coeff_monomial(n**2), p.coeff_monomial(n)
        A = 24
        assert math.gcd(math.gcd(A, B), math.gcd(C, D)) == 1   # A is least
        truth = [(A + B + C + D) % 5 == 0, (A + B) % D == 0, A + B == 5 * (D - C), (A + C + D) % B != 0]
        assert sum(truth) == 1
        return truth.index(True) + 1
    c[9] = q9

    c[10] = lambda: opt(limit((1 - cos(3 * x)**2) / cos(4 * x)**3 * sin(4 * x)**3 / log(2 * x + 1)**5, x, 0), [9, 15, 18, 24])

    def q11():
        t = symbols('t', positive=True)
        F = integrate(1 / (t * (1 + t)**2), t)
        C = -limit(F, t, oo)
        val = simplify(F.subs(t, exp(1)) + C)
        e = exp(1)
        return opt(val, [(e + 2) / (e + 1) - log(e + 1), (e + 2) / (e + 1) + log(e + 1), (e + 1) / (e + 2) - log(e + 1), (e + 1) / (e + 2) + log(e + 1)])
    c[11] = q11

    def q12():
        A = integrate(7 - x**2, (x, -1, 1)) + 2 * integrate(8 - 2 * x**2, (x, 1, 2))
        return opt(A, [18, 20, 21, 24])
    c[12] = q12

    def q13():
        X, Y = symbols('X Y')
        L = [(4, 3, 69), (-3, 4, 17), (1, 7, 61)]
        def meet(p, q):
            s = solve([p[0] * X + p[1] * Y - p[2], q[0] * X + q[1] * Y - q[2]], [X, Y])
            return Matrix([s[X], s[Y]])
        P, Q, R = meet(L[0], L[1]), meet(L[0], L[2]), meet(L[1], L[2])
        s = solve([(X - P[0])**2 + (Y - P[1])**2 - (X - Q[0])**2 - (Y - Q[1])**2,
                   (X - P[0])**2 + (Y - P[1])**2 - (X - R[0])**2 - (Y - R[1])**2], [X, Y])
        a, b = s[X], s[Y]
        return opt((a - b)**2 + a + b, [15, 16, 17, 18])
    c[13] = q13

    def q14():
        t1, t2 = symbols('t1 t2')
        for s in solve([10 * (t1 + t2) - 30, 5 * (t1**2 + t2**2) + 5 - 30], [t1, t2]):
            P, Q = (5 * s[0]**2, 10 * s[0]), (5 * s[1]**2, 10 * s[1])
            m = (Q[1] - P[1]) / (Q[0] - P[0])
            cc = P[1] - m * P[0]
            assert cc - m == 6
            return opt((Q[0] - P[0])**2 + (Q[1] - P[1])**2, [296, 325, 317, 346])
    c[14] = q14

    def q15():
        l = symbols('l')
        n = Matrix([1 + 2 * l, 2 + l, 3 - l])
        lv = solve(n.dot(Matrix([1, 1, 1]).cross(Matrix([1, -2, 3]))), l)[0]
        n = n.subs(l, lv)
        d = -4 + 5 * lv                                  # n.r + d = 0
        k = 4 / (-d)
        a, b, cc = n * k
        return opt(a - b + cc, [18, 20, 22, 24])
    c[15] = q15

    def q16():
        d1, d2 = Matrix([4, 5, 3]), Matrix([3, 4, 2])
        w = Matrix([1, 3, 4]) - Matrix([4, -2, -3])
        cr = d1.cross(d2)
        return opt(abs(w.dot(cr)) / sqrt(cr.dot(cr)), [6 * sqrt(3), 3 * sqrt(6), 2 * sqrt(6), 6 * sqrt(2)])
    c[16] = q16

    def q17():
        a, b, k = symbols('a b k')
        A, B, C = Matrix([a, 10, 13]), Matrix([6, 11, 11]), Matrix([Rational(9, 2), b, -8])
        s = solve(list(C - B - k * (B - A)), [a, b, k], dict=True)[0]
        return opt((19 * s[a] - 6 * s[b])**2, [16, 25, 36, 49])
    c[17] = q17

    c[18] = lambda: opt(Rational(50 * 2, 20 * 3 + 30 * 4 + 50 * 2), [Rational(2, 7), Rational(5, 14), Rational(3, 7), Rational(9, 28)])

    def q19():
        f = (sin(x) + cos(x) - sqrt(2)) / (sin(x) - cos(x))
        v = f.subs(x, 7 * pi / 12) * diff(f, x, 2).subs(x, 7 * pi / 12)
        return nearest(N_(v), [-2 / 3, -1 / (3 * 3**0.5), 2 / (3 * 3**0.5), 2 / 9])
    c[19] = q19

    def q20():
        imp = lambda a, b: (not a) or b
        rows = list(product([True, False], repeat=2))
        neg = [not imp(imp(p, q), imp(q, p)) for p, q in rows]
        opts = [lambda p, q: p or not q, lambda p, q: (not p) or q, lambda p, q: q and not p, lambda p, q: (not q) and p]
        return [i for i, f in enumerate(opts, 1) if [f(p, q) for p, q in rows] == neg][0]
    c[20] = q20

    def q21():
        A = [0, 3, 4, 6, 7, 8, 9, 10]
        R = {(a, b) for a in A for b in A if (a - b > 0 and (a - b) % 2 == 1) or a - b == 2}
        return len({(b, a) for a, b in R} - R)
    c[21] = q21

    def q22():
        r = 2
        assert 14 - 7 * r == 0
        return math.floor(Fraction(math.comb(7, r) * 3**(7 - r), 2**r))
    c[22] = q22

    def q23():
        a = [Fraction(n**3, n**4 + 147) for n in range(1, 100)]
        return a.index(max(a)) + 1
    c[23] = q23

    def q24():
        import mpmath
        f = lambda t: 8 * mpmath.floor(1 / mpmath.sin(t)) - 5 * mpmath.floor(mpmath.cot(t))
        pts = [mpmath.pi / 6, mpmath.pi / 4, mpmath.pi / 2, 3 * mpmath.pi / 4, 5 * mpmath.pi / 6]
        v = mpmath.quad(f, pts) * 2 / mpmath.pi
        return int(mpmath.nint(v))
    c[24] = q24

    def q25():
        C = symbols('C')
        y = (Rational(2, 3) * log(x)**Rational(3, 2) + C) / sqrt(log(x))
        assert simplify(2 * x * log(x) * diff(y, x) + y - 2 * log(x)) == 0
        Cv = solve(y.subs(x, exp(1)) - Rational(4, 3), C)[0]
        return simplify(y.subs(C, Cv).subs(x, exp(4)))
    c[25] = q25

    c[26] = lambda: sum(66 // 3**k for k in range(1, 6))

    def q27():
        # reflect (2, 1) in 2x - y + 1 = 0
        v = 2 * 2 - 1 + 1
        f, g = 2 - 2 * 2 * Rational(v, 5), 1 + 2 * 1 * Rational(v, 5)
        r2 = f**2 + g**2 - Rational(36, 5)
        alpha = r2                                       # C1 radius^2 = 4 + 1 + alpha - 5
        return alpha + sqrt(r2)
    c[27] = q27

    def q28():
        l = symbols('l')
        lams = sorted(solve(15 - 6 * l - 3, l) + solve(15 - 6 * l + 3, l))
        l1, l2 = lams[1], lams[0]
        P = Matrix([l1 - l2, l2, l1])
        AP = P - Matrix([5, 1, -7])
        d = Matrix([1, 2, 2])
        return sqrt(AP.cross(d).dot(AP.cross(d)) / d.dot(d))
    c[28] = q28

    def q29():
        al, t = symbols('al t')
        a = Matrix([6, 9, 12])
        b = Matrix([al, 11, -2])
        cv = b + t * a
        s = solve([cv.dot(Matrix([1, -2, 1])) - 5, a.dot(cv) + 12], [al, t], dict=True)[0]
        return cv.subs(s).dot(Matrix([1, 1, 1]))
    c[29] = q29

    def q30():
        u, v = symbols('u v')
        rest = [10, 12, 6, 12, 4, 8]
        for s in solve([u + v + sum(rest) - 72, u**2 + v**2 + sum(r * r for r in rest) - 8 * (Rational(925, 100) + 81)], [u, v]):
            if s[0] > s[1]:
                return 3 * s[0] - 2 * s[1]
    c[30] = q30

    c[31] = lambda: opt(400, [200, 388, 412, 400])
    c[32] = lambda: opt(Rational(10**5 + 1000 * 10 * 40, 10**5) * 1, [2, 3, 4, 5])
    c[34] = lambda: nearest(0.5 * 7e10 * (0.04e-2)**2, [2800, 5600, 8400, 11200])
    c[36] = lambda: opt(Rational(1, 2) * 6 * 1, [6, 4, 3, 2])
    c[37] = lambda: opt(sqrt(1 + Rational(1, 4)), [Rational(5, 2), sqrt(5) / 2, sqrt(5) / 4, sqrt(5) / 2 + 1])   # option 4 is dimensionally wrong (A^2); any other value
    c[38] = lambda: opt(400 * (1 - Rational(1, 2)), [0, 100, 200, 300])
    c[39] = lambda: [Rational(1), 2 / sqrt(3), Rational(4, 9), sqrt(3) / 2].index(simplify(40**2 * sin(pi / 3) / (60**2 * sin(2 * pi / 3)))) + 1
    c[40] = lambda: nearest(100 * (0.01 / 0.4 + 2 * 0.03 / 6 + 0.04 / 8), [1, 3.5, 4, 5])
    c[41] = lambda: nearest(2 * math.pi * 6400 * 0.098, [4868, 1549, 3942, 1240])

    def q42():
        A = lambda t: 1 if t >= 2 else 0
        B = lambda t: 1 if (1 <= t < 2 or 3 <= t < 4) else 0
        nand = lambda p, q: 0 if (p and q) else 1
        Y = [nand(nand(A(t), A(t)), nand(B(t), B(t))) for t in (0.5, 1.5, 2.5, 3.5)]
        shapes = {1: [0, 1, 1, 1], 2: [1, 0, 0, 0], 3: [1, 1, 1, 1], 4: [0, 0, 0, 0]}
        return [k for k, s in shapes.items() if s == Y][0]
    c[42] = q42

    def q49():
        I = Rational(4, 6 + 2 + 8)
        V1 = I * (6 + 2)
        V2 = I * (2 + 8)
        return opt(V1 / V2, [Rational(4, 5), 1, Rational(5, 4), Rational(3, 4)])
    c[49] = q49
    c[51] = lambda: 2 * 360 / 0.8
    c[52] = lambda: round(2 * (3e-3)**2 * 1750 * 10 / (9 * 0.35e-2), 6)
    c[54] = lambda: round((1.5**2 - 1) * 100)
    c[55] = lambda: round(2 * 121 * 8.1 - 242 * 7.6)

    def q56():
        a, d, o = 0, 10, 2
        imgsA = set()
        pos = [o]
        # images behind A are at negative x; generate a few reflections
        frontier = [(o, None)]
        for _ in range(4):
            new = []
            for p, last in frontier:
                if last != 'A':
                    q = 2 * a - p; new.append((q, 'A')); imgsA.add(q)
                if last != 'B':
                    q = 2 * d - p; new.append((q, 'B'))
            frontier = new
        behind = sorted(-p for p in imgsA if p < 0)
        return behind[1]
    c[56] = q56

    c[57] = lambda: round(2.7e-6 / math.sqrt(75e-3 * 1.2e-6) * 1000)
    c[58] = lambda: 1.6e3 / 800
    c[59] = lambda: round(2 / (2e28 * 1.6e-19 * 25e-6) / 1e-6)
    c[60] = lambda: round(2 * 6e-6 * 1.5e3 * 1000)
    c[61] = lambda: opt(12 - 2, [2, 10, 6, 12])
    c[81] = lambda: round((2 * 2 + 4 * 3 + 3 * 4) / (2 + 3 + 4))
    c[84] = lambda: 60 * 100 / 5

    def q86():
        pk = 10 - 2 * 0.3                             # -log(4e-10) with log 2 = 0.3 (given)
        truth = [False, abs((pk - 1) - 8.4) < 1e-9, False, True]   # A, C are false by nature of the indicator
        return sum(truth)
    c[86] = q86

    c[89] = lambda: 5 * 12 + 10 * 1
    c[90] = lambda: round(0.5 * 0.6 * 44 / 12 * 10)
    return c
