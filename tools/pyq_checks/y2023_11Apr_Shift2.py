"""Answer checks for JEE Main 2023 (Session 2), 11 Apr Shift 2."""
from pyq_checks.common import *


def checks():
    c = {}

    def q1():
        A, B = [1, 3, 4, 6, 9], [2, 4, 5, 8, 10]
        n = sum(1 for a1, b1, a2, b2 in product(A, B, A, B) if a1 <= b2 and b1 <= a2)
        return opt(n, [26, 52, 160, 180])
    c[1] = q1

    def q2():
        ok = lambda t: math.floor(t)**2 - 3 * math.floor(t) - 10 > 0
        pts = [-2.0001, -2, 5.999, 6, 5.5]
        res = [ok(p) for p in pts]
        # (-inf,-2) U [6,inf): -2.0001 in, -2 out, 5.999 out, 6 in, 5.5 out
        return 1 if res == [True, False, False, True, False] else 0
    c[2] = q2

    def q3():
        p, q, X = 1, 2, Rational(-10)               # example a = 1 + 2i; real z = -10
        s1 = (p + X) > (0 - q)                       # A: Re(a + conj z) > Im(conj a + z)
        p2, q2 = -1, -2
        X2 = Rational(10)
        s2 = (p2 + X2) < (0 - q2)                    # B
        return 2 if (not s1 and not s2) else 0
    c[3] = q3

    def q4():
        al, be, m, n = symbols('al be m n')
        s = solve([7 * m + 5 * n - 175, 11 * m + 4 * n - 194], [m, n])
        av = solve(al * s[m] + 7 * s[n] - 57, al)[0]
        bv = solve(13 * s[m] + be * s[n] - 361, be)[0]
        return opt(av + bv + 2, [3, 4, 5, 6])
    c[4] = q4

    def q5():
        l = symbols('l', positive=True)
        M = Matrix([[x + 1, x, x], [x, x + l, x], [x, x, x + l**2]])
        lv = solve(M.det().subs(x, 0) - Rational(9, 8) * 81, l)[0]
        assert simplify(M.det().subs(l, lv) - Rational(9, 8) * (103 * x + 81)) == 0
        r1, r2 = lv, lv / 3
        opts = [4 * x**2 + 24 * x - 27, 4 * x**2 - 24 * x - 27, 4 * x**2 + 24 * x + 27, 4 * x**2 - 24 * x + 27]
        return [i for i, f in enumerate(opts, 1) if f.subs(x, r1) == 0 and f.subs(x, r2) == 0][0]
    c[5] = q5

    def q6():
        from itertools import permutations
        w = sorted(''.join(p) for p in permutations('MATHS'))
        return opt(w.index('THAMS') + 1, [101, 102, 103, 104])
    c[6] = q6

    def q8():
        for N in range(3, 40):
            for r in range(1, N):
                a, b, cc = math.comb(N, r - 1), math.comb(N, r), math.comb(N, r + 1)
                if 3 * a == b and 5 * a == cc:
                    return opt(a + b + cc, [25, 41, 63, 92])
    c[8] = q8

    c[9] = lambda: opt(Rational(5**5 * 3**3 * 2**2, 3750), [55, 90, 108, 110])

    def q10():
        def gf(t):
            f = t + 1 if t < 0 else abs(t - 1)
            return f + 1 if f < 0 else 1
        h = 1e-6
        bad = []
        for p in [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]:
            l = (gf(p) - gf(p - h)) / h; r = (gf(p + h) - gf(p)) / h
            if abs(l - r) > 1e-3 or abs(gf(p - h) - gf(p + h)) > 1e-3:
                bad.append(p)
        return 4 if bad == [-1] and abs(gf(-1 - h) - gf(-1 + h)) < 1e-3 else 0
    c[10] = q10

    def q11():
        assert all(min(t * t, t) == t * t for t in [0.1, 0.5, 0.9])
        assert all(math.floor(t - math.log(t)) == 1 for t in [1, 1.5, 2])
        v = integrate(x * exp(x**2), (x, 0, 1)) + integrate(x * exp(1), (x, 1, 2))
        e = exp(1)
        return opt(v, [1 + 3 * e / 2, 2 * e - 1, 2 * e - Rational(1, 2), (e - 1) * (e**2 + Rational(1, 2))])
    c[11] = q11

    def q12():
        import mpmath
        f = lambda u: u**2 + 3 * u + 1               # any test function
        I1 = mpmath.quad(lambda t: f(mpmath.sin(2 * t)) * mpmath.sin(t), [0, mpmath.pi / 2])
        I2 = mpmath.quad(lambda t: f(mpmath.cos(2 * t)) * mpmath.cos(t), [0, mpmath.pi / 4])
        return nearest(-I1 / I2, [-math.sqrt(2), math.sqrt(2), -math.sqrt(3), math.sqrt(3)])
    c[12] = q12

    def q13():
        C = symbols('C')
        y = (x**4 / 4 - 1 / x + C) * (x**5 + 1) / x**5
        assert simplify(diff(y, x) + 5 * y / (x * (x**5 + 1)) - (x**5 + 1)**2 / x**7) == 0
        y = y.subs(C, solve(y.subs(x, 1) - 2, C)[0])
        return opt(y.subs(x, 2), [Rational(637, 128), Rational(679, 128), Rational(693, 128), Rational(697, 128)])
    c[13] = q13

    def q14():
        cs = symbols('cs')
        d2 = 27 * cs**2 - 24 * cs + 13
        cm = solve(diff(d2, cs), cs)[0]
        return opt(12 * d2.subs(cs, cm), [69, 72, 92, 115])
    c[14] = q14

    def q15():
        P1, P2, P3 = Matrix([5, 3, 0]), Matrix([13, 3, -2]), Matrix([1, 6, 2])
        n = (P2 - P1).cross(P3 - P1)
        dist = lambda Q: abs(n.dot(Q - P1)) / sqrt(n.dot(n))
        al = [a for a in range(1, 50) if dist(Matrix([3, 4, a])) == 2][0]
        e = n.dot(Matrix([2, al, x]) - P1)
        a = [v for v in solve(e - 3 * sqrt(n.dot(n)), x) + solve(e + 3 * sqrt(n.dot(n)), x) if v > 0]
        return opt(a[0], [3, 4, 5, 6])
    from sympy import Abs as Abs_
    c[15] = q15

    def q16():
        t, s = symbols('t s')
        R = Matrix([2, -1, 2]) + t * Matrix([3, 4, 2])
        R = R.subs(t, solve(R[0] - R[1] + R[2] - 4, t)[0])
        Q = R + s * Matrix([2, 2, 1])
        sv = solve(Q[0] + 2 * Q[1] + 3 * Q[2] + 2, s)[0]
        d = (Q.subs(s, sv) - R)
        return opt(sqrt(d.dot(d)), [3, sqrt(31), sqrt(61), sqrt(189)])
    c[16] = q16

    def q17():
        import random
        random.seed(1)
        a, b, cc = [Matrix([random.randint(-5, 5) for _ in range(3)]) for _ in range(3)]
        d = a + 2 * (b - a) + 3 * (cc - a)          # coplanar with a, b, c
        T = lambda u, v, w: Matrix.hstack(u, v, w).det()
        lhs = T(a, b, cc)
        opts = [T(d, b, a) + T(a, cc, d) + T(d, b, cc), T(d, cc, a) + T(b, d, a) + T(cc, d, b),
                T(a, d, b) + T(d, cc, a) + T(d, b, cc), T(b, cc, d) + T(d, a, cc) + T(d, b, a)]
        hits = [i for i, o in enumerate(opts, 1) if o == lhs]
        assert len(hits) == 1
        return hits[0]
    c[17] = q17

    def q18():
        u, v = symbols('u v')
        for s in solve([u + v - 18, u**2 + v**2 - (6 * 35 - 46)], [u, v]):
            data = [1, 2, 4, 5, s[0], s[1]]
            return opt(Rational(sum(abs(d - 5) for d in data), 6), [Rational(7, 3), Rational(8, 3), 3, Rational(10, 3)])
    c[18] = q18

    c[19] = lambda: opt(sqrt(5**2 + (5 * sqrt(3))**2), [5, 5 * sqrt(5), Rational(5, 2) * sqrt(5), 10])

    def q20():
        rows = list(product([True, False], repeat=3))
        imp = lambda a, b: (not a) or b
        conv = [imp(r, (not p) and q) for p, q, r in rows]
        opts = [lambda p, q, r: imp(p or not q, not r), lambda p, q, r: imp((not p) or q, r),
                lambda p, q, r: imp(not r, p and q), lambda p, q, r: imp(not r, (not p) and q)]
        return [i for i, f in enumerate(opts, 1) if [f(*t) for t in rows] == conv][0]
    c[20] = q20

    def q21():
        a = symbols('a', real=True)
        from sympy import im
        z = a - Rational(13, 11) * sympy_I
        r = expand_complex((z**2 + 8 * sympy_I * z - 15) / (z**2 - 3 * sympy_I * z - 2))
        sols = [s for s in solve(simplify(im(r)), a) if s != 0]
        return 242 * sols[0]**2
    from sympy import expand_complex
    c[21] = q21

    c[22] = lambda: sum(1 for f in product(range(1, 7), repeat=5) if f[0] + f[1] == f[3] - 1)

    def q23():
        k = symbols('k', positive=True)
        S = k * (k**2 + k - 1) / (k - 1)**3
        n = symbols('n')
        assert all(Rational(m * m + 5 * m + 2, 2) == [1, 4, 8, 13, 19][m] for m in range(5))
        return [v for v in solve(S - 10, k) if v.is_integer][0]
    c[23] = q23

    def q24():
        t = symbols('t', positive=True)
        return len([r for r in solve(t**4 - t**3 - 3 * t**2 - t + 1, t) if r.is_real and r > 0])
    c[24] = q24

    def q25():
        A = integrate(2 * x**2 + 1, (x, 0, 1)) - integrate(1 - x, (x, 0, Rational(2, 5))) - integrate(4 * x - 1, (x, Rational(2, 5), 1))
        return 60 * A
    c[25] = q25

    def q26():
        P = Matrix([-1, 0])
        n = Matrix([2, -3]); cst = 3                  # l1: 2x - 3y + 3 = 0
        t = (n.dot(P) + cst) / n.dot(n)
        Pi = P - 2 * t * n
        V = Matrix([0, 1])
        d = Pi - V
        al, be = d[1], -d[0]                          # normal to direction
        k = 17 / -(al * V[0] + be * V[1])
        al, be = al * k, be * k
        return al**2 + be**2 - al - be
    c[26] = q26

    def q27():
        al = [a for a in (6, -6) if Rational(6, a) == 1][0]
        x1, y1 = al - 1, al + 2
        assert al**2 * x1**2 - 9 * y1**2 == 9 * al**2
        a2, b2 = 9, al**2
        # normal: a2 x / x1 + b2 y / y1 = a2 + b2
        A_, B_, C_ = Rational(a2, x1), Rational(b2, y1), -(a2 + b2)
        return (A_ * 6 + B_ * -4 + C_)**2 / (A_**2 + B_**2)
    c[27] = q27

    def q28():
        l, t = symbols('l t')
        d = Matrix([1, 2, l]); n = Matrix([1, 2, 3])
        lv = [v for v in solve((n.dot(d))**2 * 14 - 9 * n.dot(n) * d.dot(d), l)]
        lv = [v for v in lv if simplify(sqrt(1 - (n.dot(d.subs(l, v)))**2 / (n.dot(n) * d.subs(l, v).dot(d.subs(l, v)))) - sqrt(Rational(5, 14))) == 0][0]
        P = Matrix([0, 1, 3]) + t * d.subs(l, lv)
        P = P.subs(t, solve(n.dot(P) - 4, t)[0])
        return P[0] + 2 * P[1] + 6 * P[2]
    c[28] = q28

    def q29():
        a, b = Matrix([1, 2, 3]), Matrix([1, 1, -1])
        c1, c2, c3 = symbols('c1 c2 c3')
        cv = Matrix([c1, c2, c3])
        s = solve([a.dot(cv) - 11, b.dot(a.cross(cv)) - 27, b.dot(cv) + sqrt(3) * sqrt(b.dot(b))], [c1, c2, c3])
        w = a.cross(cv.subs(s))
        return w.dot(w)
    c[29] = q29

    def q30():
        p = sum(Rational(3, 4)**(n - 1) * Rational(1, 4) for n in range(1, 50) if 25 * n * n - 256 < 0)
        return p.q - p.p
    c[30] = q30

    c[31] = lambda: nearest(400 * (360 + 40) / (360 + 20), [514, 421, 485, 471])
    c[32] = lambda: nearest(math.sqrt(3 * 1.4e-23 * 300 / 4.6e-26), [27.4, 91, 523, 1260])
    c[33] = lambda: opt(sqrt(10 * 6400 * 1000) / 1000 * (sqrt(2) - 1), [Rational(112, 10) * (sqrt(2) - 1), Rational(74, 10) * (sqrt(2) - 1), 8 * (sqrt(2) - 1), Rational(79, 10) * (sqrt(2) - 1)])
    c[35] = lambda: opt(Rational(1, 2) * 10 * 5, [5, 25, 125, 166])
    c[36] = lambda: opt(10 * 2**2, [5, 10, 16, 40])
    c[39] = lambda: opt(sqrt((40 * cos(pi / 6))**2 + (40 * sin(pi / 6) - 20)**2), [0, 20 * sqrt(3), 20, 40 * sqrt(3)])

    def q40():
        # density = F^a V^b T^c: M: a = 1; L: a + b = -3; T: -2a - b + c = 0
        a, b, cc = symbols('a b c')
        s = solve([a - 1, a + b + 3, -2 * a - b + cc], [a, b, cc])
        opts = [(2, -2, 6), (1, 4, -6), (1, -4, -2), (1, -2, 2)]
        return opts.index((s[a], s[b], s[cc])) + 1
    c[40] = q40

    c[43] = lambda: opt(180 - 2 * 30, [110, 120, 130, 140])
    c[44] = lambda: opt(Rational(-136, 10) * 4 / 4, [Rational(-544, 10), Rational(-136, 10), Rational(-34, 10), Rational(-272, 10)])
    c[45] = lambda: opt(1 / sqrt(1849), [Rational(2, 43), Rational(1, 62), Rational(1, 30), Rational(1, 43)])

    def q49():
        I = 8 / Rational(2 + 2)                       # R5 in series with (D-A block = 2 ohm)
        VDA = I * 2
        I4 = VDA / (3 + 3)
        return opt(I4 / 2, [Rational(1, 2), Rational(1, 4), Rational(1, 3), Rational(2, 3)])
    c[49] = q49

    c[51] = lambda: round(math.sqrt(8e10 * 3.2e-4 / 0.5 / 8e3) / (2 * 0.5))
    c[52] = lambda: round(3.5e-2 * 2 * 4 * 22 / 7 * (0.2**2 - 0.1**2) / 1e-4)
    c[54] = lambda: (5 * 10 * 0.5 + 5 * 1) * 1 * 10
    c[56] = lambda: 50 + (50 - (8 - 8 / (4 / 3)))
    c[57] = lambda: round(0.5 * 2 * (10 / 4)**2 * 100)
    c[58] = lambda: round(0.5 * 2 * 0.15 * 1000)
    c[59] = lambda: round((3 / (1.5 / 10) - 10) / 2)

    def q60():
        right = 1 / (Rational(1, 2) + Rational(1, 4) + Rational(1, 2))
        mid = right + Rational(2, 10)
        tot = 1 / (Rational(1, 2) + 1 / mid + Rational(1, 2))
        Q = tot * 10
        return Q / mid * right
    c[60] = q60

    c[62] = lambda: nearest(0.2 / 54.2 * 100 / 18 * 180, [3.69, 4.69, 2.59, 3.59])

    def q63():
        k = Rational(10, 100) / (20 * Rational(5, 10))
        xv = Rational(40, 100) / (k * Rational(5, 10))
        yv = Rational(80, 100) / (k * 40)
        return [(80, 2), (40, 4), (160, 4), (80, 4)].index((xv, yv)) + 1
    c[63] = q63

    c[64] = lambda: opt(Rational(2, 2 + 18) * 100, [2, 5, 10, 20])
    c[69] = lambda: [i for i, (a, b) in enumerate([(6.92, 6.92), (4.89, 6.92), (5.92, 1.732), (3.87, 1.732)], 1) if abs(a - math.sqrt(35)) < 0.01 and abs(b - math.sqrt(3)) < 0.01][0]
    c[81] = lambda: round(2.4 / 24 * 22.4 * 100)
    c[85] = lambda: round(3**2 / ((4.5 - 1.5) * (4.5 - 1.5)))
    return c
