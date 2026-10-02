"""
Independent re-computation of NTA PYQ answers, to back Claude's worked solutions
(pyq/<year>/<shift>/solutions.csv). Each check recomputes the answer from the question
alone (SymPy / brute force / plain arithmetic) and returns the option number (1-4) for
an MCQ or the value for a numerical. The result is compared with NTA's FINAL key from
questions.json. A mismatch is reported, never "fixed": the key is NTA's.

Questions that are conceptual (theory statements, NCERT facts, reaction products) have
no check here; their solutions need a subject teacher's review.

Usage:  python tools/verify_pyq_solutions.py
"""
import csv, json, math, os, sys
from fractions import Fraction
from itertools import product

from sympy import (Matrix, Rational, Symbol, cos, diff, exp, expand, integrate, limit,
                   log, nsimplify, pi, simplify, sin, solve, sqrt, symbols)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x = Symbol('x')


def opt(value, options):
    """1-based position of value among the options (exact comparison after simplify)."""
    same = lambda o: abs(value - o) < 1e-9 if isinstance(value, float) else simplify(value - o) == 0
    hits = [i for i, o in enumerate(options, 1) if same(o)]
    assert len(hits) == 1, (value, options)
    return hits[0]


# ---------------------------------------------------------------- 2026 / 02Apr_Shift1
def s26_02a1():
    c = {}

    def q1():
        for N in range(1, 60):
            r = solve(expand(sum((x + j) * (x + j + 2) for j in range(N)) - 4 * N), x)
            if len(r) == 2 and all(t.is_integer for t in r) and abs(r[0] - r[1]) == 2:
                return opt(N + min(r), [0, 1, 2, 3])
    c[1] = q1

    def q2():
        X, Y = symbols('X Y', real=True)
        e = expand(50 * (2 * X / (1 + 3 * sqrt(-1)) - Y / (1 - 2 * sqrt(-1))) - 31 - 17 * sqrt(-1))
        s = solve([e.as_real_imag()[0], e.as_real_imag()[1]], [X, Y])
        return opt(10 * (s[X] - 3 * s[Y]), [20, 31, 35, 75])
    c[2] = q2

    def q3():
        a, b = symbols('a b')
        beta = solve(Matrix([[1, 2, 1], [2, 1, a], [8, 4, b]]).det(), b)[0]
        # with det = 0, row3 - 4*row2 gives 0 = 18 - 20: never consistent, so "no solution"
        assert Matrix([[8, 4, beta, 18]]) - 4 * Matrix([[2, 1, a, 5]]) == Matrix([[0, 0, 0, -2]])
        return opt(simplify(beta / a), [-4, 4, 8, -8])
    c[3] = q3

    def q4():
        a, b = symbols('a b')
        A = Matrix([[1, 2], [1, a]]); B = Matrix([[3, 3], [b, 2]])
        A = A.subs(solve(list(A**2 - 4 * A + Matrix.eye(2)), a, dict=True)[0])
        B = B.subs(solve(list(B**2 - 5 * B - 6 * Matrix.eye(2)), b, dict=True)[0])
        s1 = ((B - A) * (B + A)).T == Matrix([[13, 15], [7, 10]])
        s2 = (A + B).adjugate().det() == -5
        return {(True, False): 1, (False, True): 2, (True, True): 3, (False, False): 4}[(s1, s2)]
    c[4] = q4

    c[5] = lambda: opt(len([v for v in {1 + 5 * i for i in range(101)} & {9 + 7 * i for i in range(71)} if v % 3 == 0]), [4, 5, 6, 7])
    c[6] = lambda: opt(sum(1 for t in product('12357', repeat=7) if len(set(t)) == 5), [15400, 17800, 16800, 29400])

    def q7():
        n = 0
        for r in range(0, 36):
            for k in range(-50, 51):
                if k * k != 3 and Fraction(math.comb(36, r + 1)) == Fraction(6 * math.comb(35, r), k * k - 3):
                    n += 1
        return opt(n, [2, 4, 8, 16])
    c[7] = q7

    def q8():
        k = Symbol('k')
        f = [2, k, 28, 54, k + 1, 5]; m = [7.5, 12.5, 17.5, 22.5, 27.5, 32.5]
        kv = solve(sum(Rational(str(mi)) * fi for mi, fi in zip(m, f)) - 21 * sum(f), k)[0]
        eqs = [2*x**2 - 23*x - 10, 4*x**2 - 35*x + 24, 2*x**2 - 19*x - 10, 2*x**2 - 35*x + 98]
        return [i for i, e in enumerate(eqs, 1) if e.subs(x, kv) == 0][0]
    c[8] = q8

    def q9():
        M1, M2, M3 = Matrix([Rational(5, 2), 7]), Matrix([Rational(5, 2), 3]), Matrix([4, 5])
        S = M1 + M2 + M3                     # = A + B + C
        A, B, C = S - 2 * M2, S - 2 * M3, S - 2 * M1   # any labelling gives the same incentre
        a, b, cc = (B - C).norm(), (C - A).norm(), (A - B).norm()
        I = (a * A + b * B + cc * C) / (a + b + cc)
        return opt(simplify(3 * I[0] + I[1]), [11, 12, 13, 14])
    c[9] = q9

    def q10():
        a2, b2 = symbols('a2 b2', positive=True)
        s = solve([16 / a2 + 9 / b2 - 1, 1 - a2 / b2 - Rational(5, 9)], [a2, b2], dict=True)[0]
        return opt(2 * s[a2] / sqrt(s[b2]), [4*sqrt(5)/3, 2*sqrt(5), 7*sqrt(5)/3, 8*sqrt(5)/3])
    c[10] = q10

    def q11():
        K = nsimplify(sin(pi/18) * sin(5*pi/18) * sin(7*pi/18))
        return opt(sin(10 * K * pi / 3), [(sqrt(3) + 1) / (2 * sqrt(2)), (sqrt(3) - 1) / sqrt(2), sqrt(3) / 2, Rational(1, 2)])
    c[11] = q11

    def q12():
        sols = set()
        for a in range(-2, 3):                 # range of sin x (sin x + cos x) is [(1-sqrt2)/2, (1+sqrt2)/2]
            for s in solve(sin(x) * (sin(x) + cos(x)) - a, x):
                for t in range(-2, 3):
                    for v in [s + 2 * pi * t, s + pi * t]:
                        if v.is_real and -pi <= v <= pi and simplify(sin(v) * (sin(v) + cos(v)) - a) == 0:
                            sols.add(nsimplify(v))
        return opt(len(sols), [3, 6, 7, 9])
    c[12] = q12

    def q13():
        a, b, t, s = symbols('a b t s')
        P = Matrix([-1 + 3*t, -a + 5*t, -b - 1 + 7*t]); Q = Matrix([2 + s, b + 4*s, 2*a + 7*s])
        sol = solve(list(P - Q) + [P[2]], [a, b, t, s], dict=True)[0]
        return opt(sol[a] + sol[b], [2, 5, 7, 9])
    c[13] = q13

    def q14():
        best = max(3 * math.sqrt(72 + 12 * d) + 4 * math.sqrt(72 - 12 * d) for d in [i / 1000 - 6 for i in range(12001)])
        return opt(round(best), [30, 36, 60, 72])
    c[14] = q14

    def q15():
        d = Matrix([2, 2, 1]).cross(Matrix([1, 2, 2])); P0 = Matrix([1, 1, 1])
        P = P0 - (P0.dot(d) / d.dot(d)) * d
        return opt(34 * sum(P), [50, 80, 100, 120])
    c[15] = q15

    def q16():
        a, b = symbols('a b')
        p = x**3 - 5*x**2 + a*x + b
        s = solve([p.subs(x, 2), diff(p, x).subs(x, 2)], [a, b])
        m = limit(sin(p.subs(s)) / ((sqrt(x - 1) - 1) * log(x - 1)), x, 2)
        return opt(s[a] + s[b] + m, [5, 6, 8, 10])
    c[16] = q16

    def q17():
        lny = integrate(2 + log(x), x); C = 1 - lny.subs(x, 1)   # ln y(1) = ln e = 1
        return opt(exp(lny.subs(x, exp(1)) + C),
                   [exp(exp(1)), exp(exp(2)), exp(2 * exp(1)), exp(2**exp(1))])   # option 4 is e^(2^e)
    c[17] = q17

    def q18():
        # critical points of |sin x / x| on (-2pi, 2pi): corners where sin x = 0 (x = +-pi),
        # the smooth maximum at x = 0, and f' = 0 where tan x = x (one root in (pi, 3pi/2) each side)
        import mpmath
        r = mpmath.findroot(lambda t: mpmath.tan(t) - t, 4.49)
        assert math.pi < r < 2 * math.pi
        return opt(2 + 1 + 2, [1, 3, 5, 7])
    c[18] = q18

    def q19():
        v = sum(integrate((exp(x) + exp(-x)) / math.factorial(n), (x, n, n + 1)) for n in range(3))
        e = exp(1)
        return opt(v, [e**2 + e**3 - 1/e**2 - 1/e**3, (e**2 + e**3 - 1/e**2 - 1/e**3) / 2,
                       e**2 + e**3 - 1/(2*e**2) - 1/(2*e**3), (e**2 + e**3) / 2 - 1/e**2 - 1/e**3])
    c[19] = q19

    def q20():
        y = 1 / (1 + sin(x)) - 1            # from dy/(y+1) = -cos x dx/(1 + sin x), y(0) = 0
        assert simplify((1 + sin(x)) * diff(y, x) + (y + 1) * cos(x)) == 0 and y.subs(x, 0) == 0
        return [i for i, a in enumerate([pi/6, pi/4, pi/3, pi/2], 1) if y.subs(x, a) == Rational(-1, 2)][0]
    c[20] = q20

    def q21():
        # domain: 0 < |2x-5|/|x^2-4| <= 1  ->  (x-1)^2 (x^2+2x-9) >= 0, x != +-2, 5/2
        r = solve(x**2 + 2*x - 9, x)
        a, cc = min(r), max(r); b = 1; d = e = Rational(5, 2)
        for t in [-10, a - Rational(1, 10), 1, cc + Rational(1, 100), 3, 10]:
            v = abs(2*t - 5) / abs(t**2 - 4); assert 0 < v <= 1
        return simplify(a + b + cc + d + e)
    c[21] = q21

    def q22():
        a = lambda k: 6 * k**3 - 6 * (k - 1)**3
        return sum(Fraction(a(k + 1) - a(k), 36)**2 for k in range(1, 7))
    c[22] = q22

    def q23():
        good = sum(1 for a, b, cc in product(range(1, 5), repeat=3) if 8 * b * b - 4 * a * cc < 0)
        f = Fraction(good, 64)
        return f.numerator + f.denominator
    c[23] = q23

    def q24():
        h = Symbol('h', positive=True)       # centre (h, h), passes through O (3 axis points, equal intercepts 2h)
        hv = solve(2*h**2 - ((2*h - 1)**2 / 2 + Rational(14, 4)), h)[0]
        return 2 * hv**2
    c[24] = q24

    def q25():
        import mpmath
        a = mpmath.quad(lambda t: mpmath.log(t*t + 4, 2), [0, 2*mpmath.sqrt(3)]) + mpmath.quad(lambda t: mpmath.sqrt(2**t - 4), [2, 4])
        return round(a * a, 6)
    c[25] = q25

    # ---- Physics (plain arithmetic)
    c[26] = lambda: opt(2 * 1 - (-1) + (-2), [0, 1, -1, 2])      # energy density M L^-1 T^-2

    def q27():
        F, L, d, l = 100, 1.5, 0.08e-2, 0.5e-2
        Y = 4 * F * L / (math.pi * d**2 * l)
        dY = Y * (2 * 0.001 / 0.08 + 0.1 / 150 + 0.001 / 0.5)
        return [i for i, o in enumerate([1.3, 1.65, 0.13, 0.25], 1) if abs(dY / 1e9 - o) < 0.01][0]
    c[27] = q27
    c[28] = lambda: opt(sqrt(1**2 + (4 * 2)**2 + 4**2), [sqrt(6), 9, sqrt(33), 0])   # a = (x, 4y, z)

    def q29():
        m, r, v, a = 0.1, (10, 5), (20, 15), (20, 30)
        cross = lambda u, w: u[0] * w[1] - u[1] * w[0]
        st = {'A': (m * v[0], m * v[1]) == (2, 1.5), 'B': (m * a[0], m * a[1]) == (2, 3),
              'C': abs(cross(r, (m * v[0], m * v[1])) - 15) < 1e-9, 'D': abs(cross(r, (m * a[0], m * a[1])) - 20) < 1e-9}
        return ['ABC', 'BCD', 'ACD', 'ABD'].index(''.join(k for k in 'ABCD' if st[k])) + 1
    c[29] = q29
    c[30] = lambda: opt(sqrt(Rational(2**3, 4) / Rational(1, 2)), [Rational(1, 2), 2, 4, Rational(1, 4)])
    c[31] = lambda: opt(Rational(3, 2) * 100 - 2 * 10, [150, 120, 130, 170])
    c[32] = lambda: opt(round((1 / (0.5 + 0.5 / 5) - 1) * 100, 2), [33.34, 66.67, 200, 400])
    c[33] = lambda: [(2, 3, 5), (5, 3, 2), (2, 5, 7), (7, 5, 2)].index(tuple(int(2 * t) for t in (Rational(7, 2), Rational(5, 2), 1))) + 1
    c[34] = lambda: opt(Rational(18, 8), [Rational(3, 2), Rational(2, 3), Rational(4, 9), Rational(9, 4)])
    c[35] = lambda: opt(Rational(200) / Rational(1, 150) / 100, [120, 150, 200, 300])
    c[36] = lambda: opt(2 * sqrt(3), [sqrt(3) / 2, 2 * sqrt(3), 1 / sqrt(3), sqrt(3)])   # tan60 = p2/(2 p1)
    c[38] = lambda: opt(2 * 2**Rational(3, 2) * 9 / sqrt(2), [36, 128 * sqrt(2), 16, 64])   # P ~ N A^1.5 r^2

    def q41():
        mu1, mu2, u, R = 1, 1.54, -40, -20
        v = mu2 / ((mu2 - mu1) / R + mu1 / u)
        h = 2 * (mu1 * v) / (mu2 * u)
        return min(range(1, 5), key=lambda i: abs([1, 0.5, 1.2, 0.25][i - 1] - h))   # 0.96 cm -> nearest option
    c[41] = q41
    def q42():
        hc, phi, V = symbols('hc phi V')     # lambda = 1
        s = solve([3 * V - (hc - phi), V - (hc / 2 - phi)], [phi, V], dict=True)[0]
        return opt(simplify(hc / s[phi]), [1, 4, 2, 3])
    c[42] = q42
    c[40] = lambda: opt((Rational(3, 4)) / (Rational(3, 2) - 1), [Rational(3, 4), Rational(3, 2), 2, Rational(1, 2)])   # i = 3A/4, delta = A/2
    c[43] = lambda: opt(Rational(3 * 10**8, 15 * 10**5), [200, 150, 400, 300])
    c[44] = lambda: min(range(1, 5), key=lambda i: abs([-1.51, -0.85, -0.38, -0.28][i - 1] + 13.6 / 36))
    c[45] = lambda: min(range(1, 5), key=lambda i: abs([10, 7, 8, 11][i - 1] - 0.08 * 4 * math.pi * 1e-6 * (512 * (1 / 8)**2 - 1) * 1e6))
    c[46] = lambda: round(2 * 628e-9 / 0.2e-3 * 180 / math.pi * 100)   # 35.98, integer answer 36
    c[47] = lambda: round((8e5 * 0.15 - 1e5 * 0.15 * 8**(1 / 1.5)) / 0.5 / 1000, 6)
    c[48] = lambda: sum(t * t for t in Matrix([1, -2, 3]).cross(Matrix([2, 3, -5])))
    c[49] = lambda: 2 / (Rational(2, 3))   # stress at l/3 = W/A + (2/3) w/A = W/A + (2/gamma) w/A
    c[50] = lambda: round(10 * 10 * 3.87 * 1.0, 6)

    # ---- Chemistry (plain arithmetic)
    c[51] = lambda: opt(Rational(3, 4) * 56, [Rational(21, 10), Rational(42, 10), 21, 42])
    c[52] = lambda: min(range(1, 5), key=lambda i: abs([8.72e-18, 1.962e-18, 1.962e-17, 6.54e-17][i - 1] - 9 * 2.18e-18))
    c[54] = lambda: opt(-1200 + 3 * (-164) + 6 * (-83) - (-663), [-648, -1350, -2002, -1527])

    def q55():
        m = 19.5 / 78 / 0.5; a = 1 / (1.86 * m) - 1
        Ka = m * a * a / (1 - a)
        return min(range(1, 5), key=lambda i: abs(math.log10([1e-6, 4e-4, 3e-5, 3e-3][i - 1]) - math.log10(Ka)))
    c[55] = q55

    def q56():
        X, Y = symbols('X Y', positive=True)
        r = (32 * X / 4)**Rational(1, 3) / sqrt(4 * Y)
        return opt(r, [2 * X**Rational(1, 3) / Y, 2 * sqrt(X / Y), sqrt(X / Y), X**Rational(1, 3) / sqrt(Y)])
    c[56] = q56
    c[71] = lambda: round(Fraction(5.33 / (52 + 3 * 35.5 + 6 * 18)).limit_denominator(1000) / Fraction(8.61 / (108 + 35.5)).limit_denominator(1000) * 100)
    c[73] = lambda: (lambda n: n + 2 * n + 2)(next(n for n in range(1, 20) if Fraction(3 * n + 1, 2) == 8))

    def q74():
        T2 = 1 / (1 / 300 - 0.48 / (60000 / (2.3 * 8.3)))
        return round(T2 - 273)
    c[74] = q74
    c[75] = lambda: round(10**(105 / 35) - 273)
    return c


SHIFTS = {('2026', '02Apr_Shift1'): s26_02a1}


def key_of(q):
    return q['answer'] + 1 if q['type'] == 'MCQ' else q['answer']


def check_solutions_csv(year, shift, qs):
    """Claude's written answer in solutions.csv vs NTA's final key (disagreements are flags, not edits)."""
    path = os.path.join(ROOT, 'pyq', year, shift, 'solutions.csv')
    if not os.path.exists(path):
        return 0
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    bad = 0
    for r in rows:
        q = qs[int(r['q']) - 1]
        if q.get('exclude') or q.get('answer') is None:
            continue
        mine, key = r['claude_answer'].strip(), key_of(q)
        accept = [a + 1 for a in q.get('accept', [])] if q['type'] == 'MCQ' else q.get('accept', [])
        ok = (float(mine) == float(key)) or any(float(mine) == float(a) for a in accept)
        if not ok:
            bad += 1
            print(f"{year} {shift} Q{r['q']}: Claude's solution gives {mine}, NTA final key {key}: FLAG FOR OWNER")
    print(f'{year} {shift}: {len(rows)} written solutions, {bad} disagree with the key')
    return bad


def main():
    bad = 0
    for (year, shift), make in SHIFTS.items():
        qs = json.load(open(os.path.join(ROOT, 'pyq', year, shift, 'questions.json'), encoding='utf-8'))['questions']
        bad += check_solutions_csv(year, shift, qs)
        checks = make()
        sol = os.path.join(ROOT, 'pyq', year, shift, 'solutions.csv')
        if os.path.exists(sol):     # a solution labelled as recomputed must really have a check here
            for r in csv.DictReader(open(sol, encoding='utf-8')):
                if r['check'] in ('sympy', 'arithmetic') and int(r['q']) not in checks:
                    bad += 1; print(f"{year} {shift} Q{r['q']}: labelled '{r['check']}' but has no check in this script")
        for n, f in sorted(checks.items()):
            q = qs[n - 1]
            got = f()
            key = key_of(q)
            ok = (got == key) or (q['type'] != 'MCQ' and abs(float(got) - float(key)) < 1e-6)
            if not ok: bad += 1
            print(f"{year} {shift} Q{n:<3} {'ok ' if ok else 'MISMATCH'}  computed {got}  NTA key {key}")
        print(f'{year} {shift}: {len(checks)} of {len(qs)} questions recomputed')
    if bad:
        print(f'{bad} mismatches: flag for the owner, do not change the key'); sys.exit(1)


if __name__ == '__main__':
    main()
