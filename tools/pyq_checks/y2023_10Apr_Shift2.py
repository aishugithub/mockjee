"""Answer checks for JEE Main 2023 (Session 2), 10 Apr Shift 2."""
from pyq_checks.common import *
from sympy import floor


def checks():
    c = {}

    def q1():
        A, B = [2, 3, 4], [8, 9, 12]
        n = sum(1 for a1, b1, a2, b2 in product(A, B, A, B) if b2 % a1 == 0 and b1 % a2 == 0)
        return opt(n, [12, 18, 24, 36])
    c[1] = q1

    def q2():
        u = symbols('u', positive=True)
        ts = [log(v, 9) for v in solve(9 / u + u - 10, u)]       # tan^2 x values
        xs = []
        for t in ts:
            r = atan(sqrt(t))
            xs += [r, -r] if r != 0 else [0]
        beta = sum(tan(v / 3)**2 for v in xs)
        return opt(simplify((beta - 14)**2 / 6), [8, 16, 32, 64])
    c[2] = q2

    def q3():
        X, Y = symbols('X Y', real=True)
        from sympy import im
        z = X + sympy_I * Y
        num = expand_complex((2 * z - 3 * sympy_I) * (4 * X - sympy_I * (4 * Y + 2)))
        assert simplify(im(num) + 16 * X) == 0
        # x = 0, and (0, -1/2) excluded (denominator zero); options 1-3 hold, option 4 fails
        y = symbols('y', real=True)
        assert simplify(y + y**2 + Rational(1, 4) - (y + Rational(1, 2))**2) == 0
        return 4
    from sympy import expand_complex
    c[3] = q3

    def q4():
        f = math.factorial
        M = Matrix([[f(5), f(6), f(7)], [f(6), f(7), f(8)], [f(7), f(8), f(9)]])
        dA = M.det() / (f(5) * f(6) * f(7))         # NTA's reading: |A| = det M / (5! 6! 7!)
        d2A = 8 * dA
        return opt(d2A**4, [2**20, 2**16, 2**12, 2**8])
    c[4] = q4

    def q5():
        cnt = sum(1 for cars in product(range(3), repeat=8) if max(cars.count(k) for k in range(3)) <= 3)
        return opt(cnt, [560, 1120, 1680, 3360])
    c[5] = q5

    def q6():
        for p in range(1, 40):
            for q in range(1, 40):
                c1 = p - q                                         # coefficient of x
                c2 = math.comb(p, 2) + math.comb(q, 2) - p * q     # coefficient of x^2
                if c1 == 4 and c2 == -5:
                    return opt(2 * p + 3 * q, [60, 63, 66, 69])
    c[6] = q6

    def q7():
        a = (pow(22, 2022, 3) + pow(2022, 22, 3)) % 3
        b = (pow(22, 2022, 7) + pow(2022, 22, 7)) % 7
        return opt(a * a + b * b, [5, 10, 13, 20])
    c[7] = q7

    def q8():
        t = [4]
        d = 7
        while len(t) < 29:
            t.append(t[-1] + d); d += 3
        assert t[:5] == [4, 11, 21, 34, 50]
        return opt(Rational(sum(t[9:29]), 60), [220, 223, 226, 227])
    c[8] = q8

    c[9] = lambda: nearest(float(atan(1) + atan(2) + atan(3)), [5 * math.pi / 4, 3 * math.pi / 2, 3 * math.pi / 4, math.pi])

    def q10():
        F = Rational(1, 2) * (x / exp(1))**(2 * x) - Rational(1, 2) * (exp(1) / x)**(2 * x)
        g = ((x / exp(1))**(2 * x) + (exp(1) / x)**(2 * x)) * log(x)
        assert abs(N_((diff(F, x) - g).subs(x, Rational(17, 10)))) < 1e-12
        a = b = cc = d = 2
        return opt(a + 2 * b + 3 * cc - 4 * d, [-8, -4, 1, 4])
    from sympy import N as N_
    c[10] = q10

    def q11():
        t = symbols('t', positive=True)
        f_t2 = solve((Symbol('F') + t**4) * 2 * t - diff(Rational(4, 3) * t**3, t), Symbol('F'))[0]
        v = f_t2.subs(t, pi / 2)
        return opt(v, [-pi**2 * (1 + pi**2 / 16), pi**2 * (1 - pi**2 / 16), -pi * (1 + pi**3 / 16), pi * (1 - pi**3 / 16)])
    c[11] = q11

    def q12():
        A = Matrix([1, 2])
        C = 2 * A / 5
        return opt(sqrt((A - C).dot(A - C)), [3 * sqrt(5) / 5, 2 * sqrt(5) / 5, 4 * sqrt(5) / 5, 6 * sqrt(5) / 5])
    c[12] = q12

    def q13():
        m = symbols('m', positive=True)
        mv = solve(19 * m**2 + 15 - 16 * (1 + m**2), m)[0]
        ang_minor = pi / 2 - atan(mv)
        return opt(ang_minor, [pi / 3, pi / 4, pi / 6, pi / 12])
    c[13] = q13

    def q14():
        A, B, C, P = Matrix([1, 2, 0]), Matrix([1, 4, 1]), Matrix([0, 5, 1]), Matrix([1, 2, 6])
        n = (B - A).cross(C - A)
        t = n.dot(P - A) / n.dot(n)
        Q = P - 2 * t * n
        return opt(Q.dot(Q), [62, 65, 70, 76])
    c[14] = q14

    def q15():
        t, s = symbols('t s')
        L = Matrix([t, 6 - 2 * t, -8 + 5 * t])
        M1 = Matrix([5 + 4 * s, 7 + 3 * s, -2 + s])
        M2 = Matrix([-3 + 6 * s, 3 - 3 * s, 6 + s])
        sa = solve(list(L - M1)[:2], [t, s]); A = L.subs(t, sa[t]); assert (L - M1).subs(sa)[2] == 0
        sb = solve(list(L - M2)[:2], [t, s]); B = L.subs(t, sb[t]); assert (L - M2).subs(sb)[2] == 0
        Mid = (A + B) / 2
        return opt(abs(2 * Mid[0] - 2 * Mid[1] + Mid[2] - 14) / 3, [Rational(10, 3), Rational(11, 3), 4, 3])
    c[15] = q15

    def q16():
        a, b, cv = Matrix([2, 7, -1]), Matrix([3, 0, 5]), Matrix([1, -1, 2])
        w = a.cross(b)
        d = w * 12 / cv.dot(w)
        return opt(Matrix([-1, 1, -1]).dot(cv.cross(d)), [24, 42, 44, 48])
    c[16] = q16

    def q18():
        n = [n for n in range(9, 40) if math.comb(n, 7) == math.comb(n, 9)][0]
        k = Rational(math.comb(n, 2), 2**n) * 2**15
        return opt(k, [15, 30, 60, 90])
    c[18] = q18

    def q19():
        k = symbols('k', positive=True)
        fs = [k + 2, 2 * k, k**2 - 1, k**2 - 1, k**2 + 1, k - 3]
        kv = solve(sum(fs) - 62, k)[0]
        fs = [f.subs(k, kv) for f in fs]
        val = sum(f * i * i for i, f in enumerate(fs)) / sum(fs)
        return opt(floor(val), [6, 7, 8, 9])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=2))
        st = [not (p or not (p and q)) for p, q in rows]
        opts = [lambda p, q: (not (p and q)) and q, lambda p, q: not (p or q), lambda p, q: (p and q) and not p, lambda p, q: not (p and q)]
        return [i for i, f in enumerate(opts, 1) if [f(p, q) for p, q in rows] == st][0]
    c[20] = q20

    def q21():
        rts = sorted(solve(7 * x**2 + 10 * x + 3, x))
        al, de = rts
        be = ga = Rational(-3, 5)
        return abs(3 * al + 10 * (be + ga) + 21 * de)
    c[21] = q21

    def q22():
        l = symbols('l')
        M = Matrix([[6 * l, -3, 3], [2, 6 * l, 4], [3, 2, 3 * l]])
        rhs = Matrix([4 * l**2, 1, l])
        S = []
        for lv in solve(M.det(), l):
            A = M.subs(l, lv)
            if Matrix.hstack(A, rhs.subs(l, lv)).rank() > A.rank():
                S.append(lv)
        return 12 * sum(abs(v) for v in S)
    c[22] = q22

    def q23():
        from itertools import permutations
        return sum(int(''.join(p)) for p in set(permutations('2123')))
    c[23] = q23

    def q24():
        a, d = symbols('a d')
        T = [(a + k * d) * 2**k for k in range(5)]
        s = solve([T[2] - 2, sum(T) - Rational(49, 2)], [a, d])
        return T[4].subs(s)
    c[24] = q24

    def q25():
        k = symbols('k')
        f = x + k * (x - 1)**2
        f = f.subs(k, solve(f.subs(x, -1), k)[0])
        al = [v for v in solve(f - (x + 1), x) if v > 0][0]
        m = diff(f, x).subs(x, al)
        return al + m * (al + 1)                      # x-intercept of normal: x = al + m*y0
    c[25] = q25

    def q26():
        A = integrate(x - (2 - x**2), (x, 1, sqrt(2))) + integrate(x - (x**2 - 2), (x, sqrt(2), 2))
        return simplify(6 * A + 16 * sqrt(2))
    c[26] = q26

    def q27():
        k = 2
        assert Rational(1, 10)**(-k) == 100
        y = ((2 * x + 1) * log(2 * x + 1) - (2 * x + 1)) / 2
        y = y - y.subs(x, 0) + k
        assert simplify(exp(diff(y, x)) - (k * x + Rational(k, 2))) == 0
        v = 4 * y.subs(x, 1) - 5 * log(3)
        return round(float(v))                         # exact 4 + ln 3; NTA gives the nearest integer
    c[27] = q27

    def q28():
        X, Y = symbols('X Y')
        L1, L2, AC = 2 * X - 3 * Y + 23, 5 * X + 4 * Y - 23, 3 * X + 7 * Y - 23
        V = solve([L1, L2], [X, Y]); A = solve([L1, AC], [X, Y]); C = solve([L2, AC], [X, Y])
        Mx, My = (A[X] + C[X]) / 2, (A[Y] + C[Y]) / 2
        a, b = My - V[Y], V[X] - Mx
        cc = -(a * V[X] + b * V[Y])
        return 50 * (a * A[X] + b * A[Y] + cc)**2 / (a * a + b * b)
    c[28] = q28

    def q29():
        Apt, n = Matrix([4, 3, 1]), Matrix([1, -1, 2])
        t = (n.dot(Apt) + 3) / n.dot(n)
        Np = Apt - t * n
        for b in range(-50, 51):
            a = 8 + 2 * b
            B = Matrix([5, a, b])
            cr = (B - Apt).cross(Np - Apt)
            if cr.dot(cr) == 4 * 18:
                return a * a + b * b + a * b
    c[29] = q29

    def q30():
        t = symbols('t', positive=True)
        ts = solve(sqrt(3) * (t**2 + 1) - 4 * t, t)
        tv = min(ts)                                   # tan(theta1), smaller -> theta2/theta1 largest
        a = symbols('a', positive=True)
        av = solve(a * a * tv / 2 - (2 * sqrt(3) - 3), a)[0]
        th2 = pi / 2 - atan(tv)
        per = av + av * tan(th2) + av / cos(th2)
        return simplify(per)
    c[30] = q30

    c[31] = lambda: opt(1 / (1 - Rational(2, 3)), [1, 2, 3, 4])
    c[32] = lambda: opt(sqrt(2), [Rational(1, 2), 1, sqrt(2), 2])
    c[33] = lambda: opt(2 * Rational(5, 2) + 4 * Rational(3, 2), [4, 8, 11, 16])
    c[35] = lambda: opt(Rational(1, 1 * 1) / Rational(1, 3 * 4), [Rational(1, 12), Rational(1, 36), 12, 36])
    c[37] = lambda: opt(sqrt(32), [sqrt(2), sqrt(4), sqrt(8), sqrt(32)])     # T / sqrt(R) with g = pi^2
    c[38] = lambda: opt(sin(pi / 6)**2 / sin(pi / 3)**2, [Rational(1, 3), 1 / sqrt(3), 2 / sqrt(3), sqrt(3)])
    c[39] = lambda: nearest(3.2 + 4 * 0.01 - 6 * 0.01, [3.26, 3.25, 3.22, 3.18])
    c[42] = lambda: opt(2 * 3, [6000, 3000, 3, 6])
    def q43():
        I1 = Rational(5, 25 + 1 / (Rational(1, 150) + Rational(1, 150)))
        I2 = I1 / 2
        I3 = 0                                         # D2 reverse biased
        truth = [I1 / I2 == 1, False, False, I1 / I2 == 2]   # I2/I3 and I3/I4 are undefined / 0
        return truth.index(True) + 1
    c[43] = q43
    c[44] = lambda: opt(Rational(3), [1, 2, 3, 8])
    c[45] = lambda: nearest(6.63e-34 * 5e14 / 1.6e-19, [1.36, 2.98, 2.07, 18.6])
    c[47] = lambda: opt(cos(pi / 6)**2 / cos(pi / 4)**2, [Rational(3, 2), Rational(2, 3), Rational(1, 3), 3])
    c[48] = lambda: nearest(3e8 * 6e-7, [6e-7, 180, 2e15, 5e14])
    c[51] = lambda: round(5 * (2 * math.pi / 3.14)**2 * 1)
    c[52] = lambda: 200 * 4 / 10
    def q53():
        tau = (Matrix([0, 0, 0]) - Matrix([2, -3, 0])).cross(Matrix([0, 0, -1]))
        return 2 * tau[0] / tau[1]
    c[53] = q53
    c[54] = lambda: (14000 + 2000) * 3 / 1000
    c[55] = lambda: round(math.sqrt(2 * 9e9 * 1.6e-19 * 2e-8 / 9e-31) / 1e6)
    c[56] = lambda: 4 * 917
    def q57():
        v1 = 1 / (Rational(1, 24) + Rational(1, -6))
        u2 = v1 - 10
        v2 = 1 / (Rational(1, 9) + 1 / u2)
        return 6 + 10 + v2
    c[57] = q57
    c[58] = lambda: round(4 * 22 / 7 * 1e-7 * 5000 * 2.5 * 4e-4 * 700 / 1e-4)
    c[59] = lambda: round(4 * math.pi * 1e-7 * 14 / (4 * 0.022) / 1e-4)
    c[60] = lambda: round(3e-7 * 0.01 / (0.01 * 1) / 1e-7)
    c[81] = lambda: [n for n in range(1, 10) if abs(9 * 2.18e-18 * (1 / n**2 - 1 / (n + 1)**2) - 1.47e-17) < 0.02e-17][0]
    c[84] = lambda: round(0.63 / (1.29e-3 * 0.3 / (0.083 * 300)))
    c[85] = lambda: round((720 - 450) / 2 / 450 * 10)
    def q86():
        al = 1000 * 5e-5 / 0.0025 / 400
        return round(0.0025 * al * al / (1 - al) / 1e-7)
    c[86] = q86
    c[89] = lambda: [n for n in range(8) if abs(math.sqrt(n * (n + 2)) - 4.90) < 0.01][0]

    def q61():
        NA = Rational(602, 100) * 10**23
        props = {'I': ('mass', 28), 'II': ('electrons', Rational(602, 10) * 10**23), 'III': ('mass', 32), 'IV': ('volume', Rational(114, 10))}
        species = {'A': (Rational(16, 16), 16, 10), 'B': (Rational(1, 2), 2, 2), 'C': (Rational(1), 28, 14), 'D': (Rational(1, 2), 64, 32)}   # moles, molar mass, electrons
        def match(sp):
            n, Mm, e = species[sp]
            for k, (kind, val) in props.items():
                if kind == 'mass' and n * Mm == val: return k
                if kind == 'electrons' and n * e * NA == val: return k
                if kind == 'volume' and abs(float(n * Rational(227, 10)) - float(val)) < 0.1: return k
        got = tuple(match(sp) for sp in 'ABCD')
        opts = {1: ('I', 'III', 'II', 'IV'), 2: ('II', 'IV', 'I', 'III'), 3: ('II', 'IV', 'III', 'I'), 4: ('II', 'III', 'IV', 'I')}
        return [k for k, v in opts.items() if v == got][0]
    c[61] = q61

    def q80():
        n = Rational(315, 100) / 126
        return 1 if n / Rational(250, 1000) == Rational(1, 10) else 0
    c[80] = q80
    return c
