"""Answer checks for JEE Main 2023 (Session 2), 12 Apr Shift 1."""
from pyq_checks.common import *
from sympy import N as N_


def checks():
    c = {}

    def q2():
        a, b = solve(x**2 + sqrt(6) * x + 3, x)
        S = lambda n: expand(a**n + b**n)
        return opt(simplify((S(23) + S(14)) / (S(15) + S(10))), [9, 72, 81, 729])
    c[2] = q2

    def q3():
        A = Matrix([[1, Rational(1, 51)], [0, 1]])
        P, Q = Matrix([[1, 2], [-1, -1]]), Matrix([[-1, -2], [1, 1]])
        B = P * A * Q
        tot = Matrix.zeros(2)
        Bn = Matrix.eye(2)
        for _ in range(50):
            Bn = Bn * B
            tot += Bn
        return opt(sum(tot), [50, 75, 100, 125])
    c[3] = q3

    def q4():
        from itertools import permutations
        n = sum(1 for p in permutations('013579', 5) if p[0] != '0' and int(''.join(p)) > 40000 and int(''.join(p)) % 5 == 0)
        return opt(n, [72, 96, 120, 132])
    c[4] = q4

    def q5():
        s = sum((-1)**r * math.comb(100, r) for r in range(50))
        return opt(s, [math.comb(99, 49), -math.comb(99, 49), math.comb(101, 50), -math.comb(101, 50)])
    c[5] = q5

    def q6():
        n = [n for n in range(1, 30) if sum(Rational(math.comb(n, k), k + 1) for k in range(n + 1)) == Rational(1023, 10)][0]
        return opt(n, [6, 7, 8, 9])
    c[6] = q6

    def q7():
        z0, z1 = (1 + 3 * sympy_I) / 2, 1 + sympy_I
        u = (z1 - z0) / Abs_(z1 - z0)
        d = 1 / Abs_(z1 - z0)
        z2s = [z0 + d * u, z0 - d * u]
        vals = [simplify(Abs_(z)**2) for z in z2s if Abs_(z - z0) > 1]
        return opt(min(vals), [Rational(3, 2), Rational(5, 2), Rational(7, 2), Rational(13, 2)])
    from sympy import Abs as Abs_
    c[7] = q7

    def q8():
        Sn = lambda n: Rational(n * n + 3 * n, (n + 1) * (n + 2))
        a = [Sn(1)] + [Sn(n) - Sn(n - 1) for n in range(2, 11)]
        v = 28 * sum(1 / t for t in a)
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        m = [k for k in range(1, 9) if math.prod(primes[:k]) == v][0]
        return opt(m, [5, 6, 7, 8])
    c[8] = q8

    def q9():
        t = symbols('t', positive=True)
        g = t**2 * (log(sqrt(3 * exp(1)) / 2) - log(t))
        tc = [s for s in solve(diff(g, t), t) if 0 < s < 1][0]
        k = exp(g.subs(t, tc)) * exp(1)
        v = simplify((k / exp(1))**8 + k**8 / exp(5) + k**8)
        e = exp(1)
        return opt(v, [e**5 + e**6 + e**11, e**3 + e**6 + e**10, e**3 + e**5 + e**11, e**3 + e**6 + e**11])
    c[9] = q9

    c[10] = lambda: opt(integrate(3 * x + 2 - x**3, (x, -1, 2)), [Rational(19, 4), Rational(23, 4), Rational(27, 4), Rational(31, 4)])

    def q11():
        C = symbols('C')
        u = (log(x + sqrt(1 + x**2)) + C) / sqrt(1 + x**2)
        assert simplify(diff(u, x) + x * u / (1 + x**2) - 1 / (1 + x**2)) == 0
        u = u.subs(C, solve(u.subs(x, 0) - 1, C)[0])
        beta = 1 / u.subs(x, 2 * sqrt(2))
        import mpmath
        b = float(beta)
        opts = [(math.exp(1 / b), math.exp(-2) * (3 + 2 * math.sqrt(2))), (math.exp(3 / b), math.e * (5 + math.sqrt(2))),
                (math.exp(1 / b), math.exp(-2) * (5 + math.sqrt(2))), (math.exp(3 / b), math.e * (3 + 2 * math.sqrt(2)))]
        hits = [i for i, (l, r) in enumerate(opts, 1) if abs(l - r) < 1e-9]
        assert len(hits) == 1
        return hits[0]
    c[11] = q11

    def q12():
        P = Matrix([2 * sqrt(3) / sqrt(7), 6 / sqrt(7)])
        assert simplify(9 * P[0]**2 + 4 * P[1]**2 - 36) == 0
        th = atan(P[1] / P[0]) + pi / 2
        r2 = 1 / (cos(th)**2 / 4 + sin(th)**2 / 9)
        v = simplify(1 / (4 * P.dot(P)) + 1 / (4 * r2))
        return opt(v.p + v.q, [137, 143, 147, 157])
    c[12] = q12

    def q13():
        k = 7 * sqrt(3) / 3
        h = symbols('h', positive=True)
        return opt(solve(1 / h**2 + 1 / k**2 - Rational(4, 49), h)[0], [-7, -7 * sqrt(3), 7, 7 * sqrt(3)])
    c[13] = q13

    def q14():
        l = symbols('l')
        n = Matrix([4 + l, -1 + l, 1 - l])
        lv = solve(n.dot(Matrix([4, -1, 1])), l)[0]
        n = n.subs(l, lv); d = -10 - 4 * lv
        P = Matrix([2, 3, -4])
        return opt(35 * abs(n.dot(P) + d) / sqrt(n.dot(n)), [85, 90, 105, 126])
    c[14] = q14

    def q15():
        mu, al, t = symbols('mu al t')
        n = Matrix([3 + mu, 2 - 3 * mu, 1 + 2 * mu])
        mv = solve(n.dot(Matrix([3, 1, -2])), mu)[0]
        plane = lambda X, Y, Z: (3 * X + 2 * Y + Z - 2) + mv * (X - 3 * Y + 2 * Z - 13)
        av = solve(plane(-5, -4, al), al)[0]
        P = Matrix([-5 + 3 * t, -4 + t, av - 2 * t])
        tv = solve((P - Matrix([-4, -3, 2])).dot(Matrix([3, 1, -2])), t)[0]
        return opt(sum(abs(v) for v in P.subs(t, tv)), [8, 10, 12, 14])
    c[15] = q15

    def q16():
        a, b = Rational(3), Rational(5)
        cc = solve(Matrix([[a, 1, 1], [1, b, 1], [1, 1, Symbol('c')]]).det(), Symbol('c'))[0]
        return opt(1 / (1 - a) + 1 / (1 - b) + 1 / (1 - cc), [-1, 1, -2, 2])
    c[16] = q16

    def q17():
        for lam in range(-20, 21):
            a, b = Matrix([lam, 1, -1]), Matrix([3, -1, 2])
            s = a + b
            t1 = Rational(-17) / a.dot(s) if a.dot(s) != 0 else None
            if t1 is not None and t1 * b.dot(s) == -20:
                cv = t1 * s
                w = cv.cross(Matrix([lam, 1, 1]))
                return opt(w.dot(w), [46, 49, 53, 62])
    c[17] = q17

    def q18():
        vals = [a - b for a in range(1, 7) for b in range(1, 7)]
        m = Rational(sum(vals), 36)
        var = Rational(sum(v * v for v in vals), 36) - m * m
        return opt(sum(d for d in range(1, var.p + 1) if var.p % d == 0), [31, 36, 48, 72])
    c[18] = q18

    def q19():
        a, cc = 3, 7
        b = Rational(a + cc, 2)
        cA = Rational(b * b + cc * cc - a * a, 2 * b * cc)
        cB = Rational(a * a + cc * cc - b * b, 2 * a * cc)
        cC = Rational(a * a + b * b - cc * cc, 2 * a * b)
        assert cA + 2 * cB + cC == 2
        return opt(cA - cC, [Rational(3, 7), Rational(10, 7), Rational(5, 7), Rational(9, 7)])
    c[19] = q19

    def q20():
        rows = list(product([True, False], repeat=2))
        s1 = not any((((not p) or q) and (p and not q)) for p, q in rows)
        s2 = all((p and q) or ((not p) and q) or (p and not q) or ((not p) and (not q)) for p, q in rows)
        return {(True, True): 1, (False, False): 2, (True, False): 3, (False, True): 4}[(s1, s2)]
    c[20] = q20

    def q21():
        U = [(a, b) for a in (1, 2, 3) for b in (1, 2, 3)]
        cnt = 0
        for mask in range(1 << 9):
            R = {U[i] for i in range(9) if mask >> i & 1}
            if not {(1, 2), (2, 3)} <= R: continue
            if not all((k, k) in R for k in (1, 2, 3)): continue
            if not all((a, d) in R for a, b in R for c2, d in R if b == c2): continue
            if all((b, a) in R for a, b in R): continue
            cnt += 1
        return cnt
    c[21] = q21

    def q22():
        n, k = symbols('n k')
        D = Matrix([[1, 2 * k, 2 * k - 1], [n, n**2 + n + 2, n**2], [n, n**2 + n, n**2 + n + 2]]).det()
        return [v for v in range(1, 30) if sum(D.subs({k: kk, n: v}) for kk in range(1, v + 1)) == 96][0]
    c[22] = q22

    def q23():
        from itertools import permutations
        s = set(permutations('111222333'))
        return sum(1 for t in s if any(int(t[i + 1]) - int(t[i]) == int(t[i + 2]) - int(t[i + 1]) != 0 for i in range(7)))
    c[23] = q23

    def q24():
        r = symbols('r', positive=True)
        a3 = sqrt(Rational(31, 2) / Rational(31, 8))
        rv = [v for v in solve(a3 * (1 + r + r * r) - 14, r)][0]
        terms = [a3 / rv**2, a3 / rv, a3, a3 * rv, a3 * rv**2]
        assert sum(terms) / 5 == Rational(31, 10) and sum(1 / t for t in terms) / 5 == Rational(31, 40)
        var = sum(t * t for t in terms) / 5 - Rational(31, 10)**2
        return var.p + var.q
    c[24] = q24

    def q26():
        return 3000 * (2 * (integrate(1 - 100 * x**2, (x, 0, Rational(1, 10))) + integrate(100 * x**2 - 1, (x, Rational(1, 10), Rational(15, 100)))))
    c[26] = q26

    def q27():
        F = sqrt(x * (x + 7)) + 7 * log(sqrt(x) + sqrt(x + 7))
        assert all(abs(N_((diff(F, x) - sqrt((x + 7) / x)).subs(x, v))) < 1e-12 for v in (Rational(1, 3), 2, 9))
        C = (12 + 7 * log(7) - F.subs(x, 9)).simplify()
        assert abs(N_(C)) < 1e-12
        al = sqrt(8)                                    # F(1) = sqrt(8) + 7 ln(1 + sqrt(8))
        assert abs(N_(F.subs(x, 1) - al - 7 * log(1 + 2 * sqrt(2)))) < 1e-12
        return al**4
    c[27] = q27

    def q28():
        r = symbols('r', positive=True)
        r1, r2 = sorted(solve(r**2 - (2 * r - 2)**2 / 2 - 1, r))
        return r1**2 + r2**2 - r1 * r2
    c[28] = q28

    def q29():
        A, B, C = Matrix([-6, 0, 0]), Matrix([0, -2, 0]), Matrix([0, 0, 3])
        a, b, z = symbols('a b z')
        H = Matrix([a, b, z])
        s = solve([(H - A).dot(C - B), (H - B).dot(C - A), H[0] + 3 * H[1] - 2 * H[2] + 6], [a, b, z])
        assert s[z] == Rational(6, 7)
        return 98 * (s[a] + s[b])**2
    c[29] = q29

    c[30] = lambda: [n for n in range(2, 50) if Rational(n, n - 1) == Rational(n, 9)][0]
    c[36] = lambda: opt(sqrt(Rational(16, 4)), [2, 1 / sqrt(2), 4, Rational(1, 4)])

    def q37():
        k = Rational(80 - 60, 5) / (70 - 20)
        t = Rational(60 - 40) / (k * (50 - 20))
        return opt(t * 60, [Rational(25, 3), 500, 450, 420])
    c[37] = q37

    c[39] = lambda: nearest(490 * math.sqrt(70.9 / 39.9), [451.7, 551.7, 651.7, 751.7])
    c[40] = lambda: opt(Rational(1, 4) / Rational(3, 4), [Rational(1, 4), Rational(1, 3), 2, 1])
    c[42] = lambda: opt(Rational(160, 16), [10, 16, 40, 640])
    c[44] = lambda: opt(solve((x + 1) / x - Rational(150 - 30, 150 - 50), x)[0], [5, 6, 10, -5])
    c[45] = lambda: opt(sqrt(8**2 + 6**2) / 5, [2, 7, Rational(48, 10), Rational(1, 2)])
    def q46():
        m, X = symbols('m X', positive=True)
        s = solve([X / m - 12, (24 - X) / m - 4], [m, X])
        return opt(s[m], [Rational(6, 5), Rational(2, 3), Rational(4, 3), Rational(3, 2)])
    c[46] = q46
    c[47] = lambda: opt(sqrt(Rational(4 * 2 * 4, 1 * 1 * 2)), [2, 4, 8, 16])
    c[48] = lambda: opt(max(n for n in range(2, 8) if 13.6 * (1 - 1 / n**2) <= 12.5) * (max(n for n in range(2, 8) if 13.6 * (1 - 1 / n**2) <= 12.5) - 1) // 2, [1, 2, 3, 4])
    c[49] = lambda: opt(Rational(16 - 5, 1) / Rational(200 - 100, 1000), [Rational(9, 10), 9, 110, 210])

    def q51():
        r = Rational(20, 30)**2 / (cos(pi / 6) / cos(pi / 3))
        return simplify((4 / r)**2)
    c[51] = q51

    c[52] = lambda: round(0.04 * 500 * 9.8 * 4000 / 1000)
    c[53] = lambda: Rational(1, 3) / Rational(5, 6) * 5
    c[54] = lambda: round(10e-4 * math.sqrt(2 * 3 / (1250 * 3)) / 1e-5, 6)
    c[55] = lambda: round(5 * 324 / (4 * 405), 6)
    c[56] = lambda: 64 / 4 * 10
    def q57():
        a = (Rational(2, 1) / Rational(12, 10) - 1) / 100
        return 2 / (1 + 50 * a) * 1000 / 100
    c[57] = q57
    c[58] = lambda: round(0.4 * 2 * math.pi * 0.02 * 0.001 / 1e-6)
    def q59():
        v2 = 1 / (Rational(1, 20) + 1 / Rational(-(60 - 20)))
        return 60 + v2
    c[59] = q59
    c[60] = lambda: round((238.05060 - 234.04360 - 4.00260) * 931.5)
    def q61():
        M = Rational(57, 100) * 22400 / 100
        n = round(float(M * Rational(55, 100) / Rational(355, 10)))
        return opt(n, [1, 2, 3, 4])
    c[61] = q61
    c[81] = lambda: round(2 * 90 * 40 / (3 * 600))
    c[82] = lambda: sum(1 for w in (2.42, 2.3, 2.25, 3.7, 4.8, 4.3) if w < 6.6e-34 * 3e8 / 400e-9 / 1.6e-19)
    c[83] = lambda: round(8.314 * math.log(1.5))
    c[84] = lambda: round(50 * 55.51 / (55.51 + 2.6))
    c[85] = lambda: (10 - 1) * 1000
    c[87] = lambda: round(2 / 8 * 100)
    c[89] = lambda: 4 + 6
    c[90] = lambda: round(131.8 / (7 * 12 + 12 + 16) * 3 * 17)

    def q32():
        dims = {'A': (1, 0, -2), 'B': (0, 0, -1), 'C': (1, 2, -1), 'D': (1, 2, 0)}
        L2 = {1: (0, 0, -1), 2: (1, 0, -2), 3: (1, 2, 0), 4: (1, 2, -1)}
        got = tuple(next(k for k, v in L2.items() if v == dims[q]) for q in 'ABCD')
        return {(1, 3, 2, 4): 1, (2, 1, 4, 3): 2, (4, 1, 3, 2): 3, (2, 3, 1, 4): 4}[got]
    c[32] = q32

    def q34():
        fc, fm = 1000 / 2, 4 / 2
        present = {fc, fc - fm, fc + fm}
        items = {'A': 500, 'B': 2, 'C': 250, 'D': 498, 'E': 502}
        got = ''.join(k for k, v in items.items() if v in present)
        return {'ADE': 1, 'AB': 2, 'AC': 3, 'AD': 4}[got]
    c[34] = q34

    def q38():
        eta = 1 - 273 / 373
        real = eta - 0.01                               # any real engine is below Carnot
        stm = {'A': real > 0.27, 'B': real < eta, 'C': abs(real - 0.27) < 1e-9, 'D': real < 0.27}
        got = ''.join(k for k, v in stm.items() if v)
        return {'BC': 1, 'BD': 2, 'AB': 3, 'BCD': 4}[got]
    c[38] = q38

    def q88():
        # D = EtO-C6H2I2-CH2-CH(NHCOCH3)-COOEt
        C = 2 + 6 + 2 + 3 + 2
        H = 5 + 2 + 2 + 1 + 1 + 3 + 5
        assert H == 19
        return C
    c[88] = q88
    return c
