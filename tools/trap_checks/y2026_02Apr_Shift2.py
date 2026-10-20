"""
Trap checks, JEE Main 2026 Session 2, 2 Apr Shift 2 (pyq/2026/02Apr_Shift2/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
import math

from trap_checks.common import Fraction, Rational, expand, log, pi, simplify, solve, sqrt, symbols, x


def checks():
    c = {}
    c[(1, 2)] = lambda: ((2 * 6 - 3 + 2 * (-18)) * (6 + 6 + 9), -567)        # product of the roots taken as m
    c[(2, 1)] = lambda: (2 + 10, 12)                                         # r from min = r - 10 = 2, given as the answer
    c[(2, 2)] = lambda: ((2 + 10) + 5, 17)                                   # max taken as r + 5
    c[(4, 1)] = lambda: (3**4, 81)                                           # g5 alone
    c[(7, 1)] = lambda: (2 + 2 + 3, 7)                                       # 12 = 2*2*3 with repetition
    c[(7, 4)] = lambda: (2 * 3, 6)

    def q8_1():
        p = [Fraction(1), Fraction(1, 2)]
        for _ in range(5): p.append((p[-1] + p[-2]) / 2)
        return p[5].numerator + p[5].denominator, 53
    c[(8, 1)] = q8_1

    def q12_3():
        p = symbols('p')
        q = -1 - p                                                            # 1 dropped from 1 + p + q = -1
        pv = solve(simplify(q - p**2 / 4).diff(p), p)[0]
        return pv**2 + q.subs(p, pv)**2, 5
    c[(12, 3)] = q12_3
    c[(13, 3)] = lambda: (len({a for a in range(-5, 6) if a * a == 1}), 2)   # value 1 allowed once tan^2 = 1 is ignored
    c[(17, 1)] = lambda: (Rational(3, 8) * 20 * pi, 15 * pi / 2)

    def q19_2():
        C = symbols('C')
        f = 9 * log(x + 5) + 7 * log(x - 3) + C                               # coefficients swapped
        Cv = solve(f.subs(x, 4) - 14 * log(3), C)[0]
        v = simplify(f.subs({C: Cv, x: 7}) - (32 * log(2) + 5 * log(3)))
        assert v == 0
        return 32 + 5, 37
    c[(19, 2)] = q19_2
    c[(20, 1)] = lambda: (Rational(1) + Rational(1, 2), Rational(3, 2))      # 1/v = 3/2 left uninverted: coefficient of e^2
    c[(21, 80)] = lambda: (8 * math.comb(5, 2), 80)
    c[(27, 2)] = lambda: (Rational(10, 5 * 4), Rational(1, 2))
    c[(31, 2)] = lambda: (round(2 * 9.8 * 6.4e6 / 1e7, 2), 12.54)
    c[(32, 2)] = lambda: (Fraction('5.050') + Fraction('0.005'), Fraction('5.055'))
    c[(32, 3)] = lambda: (5 + 50 * Fraction('0.01') - 5 * Fraction('0.01'), Fraction('5.45'))
    c[(33, 4)] = lambda: (Fraction('0.03') * 8 * (36 - 4), Fraction('7.68'))
    c[(35, 1)] = lambda: (math.floor(2 * 1e-6 * 2000 * 10 / (9 * 0.005) * 100) / 100, 0.88)
    c[(36, 1)] = lambda: (Rational(2 * 10 * 99, 10) / Rational(1, 10), 1980)
    c[(36, 3)] = lambda: (2 * 10 * 10 / Rational(1, 10), 2000)
    c[(37, 1)] = lambda: (3 * 10**8 * Rational(2, 10**7), 60)                # size right; option +60 k has the wrong sign
    c[(38, 3)] = lambda: (math.floor(100 * 400 / 600 * 10) / 10, 66.6)
    c[(40, 2)] = lambda: (Fraction(8 - 2, 8), Fraction(3, 4))
    c[(40, 4)] = lambda: (Fraction(8, 8 + 2), Fraction(4, 5))
    c[(41, 3)] = lambda: (Rational(16, 10) / (sqrt(3) / 2), Rational(32, 10) / sqrt(3))

    def q43_3():
        mu, I, L, R = symbols('mu I L R', positive=True)
        B = 4 * mu * I * sqrt(2) / 2 / (4 * pi * L / 2)                       # one sin 45 per side
        return simplify(B * pi * R**2 / I), sqrt(2) * mu * R**2 / L
    c[(43, 3)] = q43_3
    c[(45, 2)] = lambda: ((pi - pi / 3) / 50, pi / 75)                       # t1 taken at the mean position
    c[(46, 12)] = lambda: (Rational(1) / (Rational(1, 6) / 2), 12)          # cos^2(phi) = 3/4: phi = pi/6, path = lambda/12
    c[(47, 8)] = lambda: (Rational(4, 2)**3, 8)
    c[(48, 400)] = lambda: (5 * 8 * 10, 400)
    c[(49, 30)] = lambda: ((1 + Rational(60, 30)) * 10, 30)
    c[(54, 2)] = lambda: (-6 - (-8), 2)                                      # w = q - dU with dU kept at -8
    c[(55, 2)] = lambda: (2 * Fraction('9.96'), Fraction('19.92'))           # z = x + y (units of 1e-4 bar)
    c[(73, 701)] = lambda: (round(6 * 96500 * 1.21 / 1000), 701)
    return c
