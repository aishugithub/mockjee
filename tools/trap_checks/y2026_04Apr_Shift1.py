"""
Trap checks, JEE Main 2026 Session 2, 4 Apr Shift 1 (pyq/2026/04Apr_Shift1/traps.csv).

Each check follows the WRONG path named in traps.csv and returns (value it lands on, the option's printed value);
tools/verify_traps.py fails if they differ. For a numerical the second value is the trap value in the CSV.
"""
import math

from trap_checks.common import Matrix, Rational, Symbol, pi, simplify, solve, sqrt


def checks():
    c = {}
    c[(1, 3)] = lambda: (12 * (0 + Rational(3, 4)), 9)                       # only the n = 0 piece [0, 3/4]
    c[(4, 1)] = lambda: (3 * 2**4, 48)                                       # C(3,1)·2^4, overlap never added back
    c[(4, 3)] = lambda: (3 * 2**4 + 3, 51)                                   # overlap term added with the wrong sign
    pairs = [(b, cc) for b in range(5) for cc in range(5)]
    c[(5, 3)] = lambda: (2 * (5 + 5) + 1, 21)                                # b = 0 and c = 0 counted separately: (0,0) twice
    c[(5, 2)] = lambda: (2 * sum(1 for b, cc in pairs if b * cc == 0 and (b, cc) != (0, 0)) + 1, 17)   # b = c = 0 left out

    def q6_1():
        A = Matrix([[1, 1, 2], [-2, 0, 1], [1, 3, 5]])
        d = -A.det()                                                         # |A| taken as +4
        B = 2 * A / d                                                        # 2(adj A)^-1 = 2A/|A|
        detB = Rational(2, 1)**3 / d**3 * d                                  # |B| = (2/|A|)^3 |A|, with the slipped |A|
        return sum(detB * B), 3                                              # adj(adj B) = |B| B for 3x3
    c[(6, 1)] = q6_1
    def q7_4():
        l = [r for r in solve(Symbol('l')**3 - 15 * Symbol('l') - 50) if r.is_real][0]   # last term from S30 = l³
        return l / 29, Rational(5, 29)                                       # d = l/29: first term not subtracted
    c[(7, 4)] = q7_4
    c[(8, 1)] = lambda: (math.factorial(7), 5040)                            # all queues, condition ignored
    c[(11, 2)] = lambda: (Rational(18, 90), Rational(1, 5))                  # ratio inverted: AC^2 : BC^2
    c[(16, 1)] = lambda: (1 + 2, 3)                                          # tan(α + x): derivative +1, plus sin^-1 x term's 2
    c[(18, 1)] = lambda: (simplify((2 + pi**2 / 4) / 2), simplify(1 + pi**2 / 8))   # x ≥ 0 half only (true area 2 + π²/4)

    def q20_1():
        # (1/√3) tan^-1((2y-1)/√3) = 11/6  =>  argument of tan = 11√3/6
        return simplify(Rational(11, 6) * sqrt(3)), simplify(11 * sqrt(3) / 6)
    c[(20, 1)] = q20_1
    c[(20, 2)] = lambda: (simplify(sqrt(3) * Rational(1, 2)), simplify(sqrt(3) / 2))   # y(1) - 1/2 = (2y(1) - 1)/2: coefficient √3 halved
    c[(28, 4)] = lambda: (1 - Rational(5, 9), Rational(4, 9))               # stopped at 1 - μ = 4/9
    c[(30, 3)] = lambda: (Rational(1, 2) * Rational(7, 8) * 4 / (Rational(2, 5) * Rational(1, 8) * Rational(1, 4)), 140)   # disc MR²/2
    c[(33, 1)] = lambda: (2 - 1, 1)                                          # one gap between consecutive minima: (2 - 1)Dλ/a
    c[(33, 4)] = lambda: (3, 3)                                              # position of the 3rd minimum, 3Dλ/a
    dlA = 8 * 0.314 / (3.14 * (2e-4) ** 2 * 2e10) * 1e3                      # mm; the paper's 0.314 m means π = 3.14
    c[(34, 4)] = lambda: (round(dlA, 6), 1)                                  # string A only
    c[(34, 1)] = lambda: (round(dlA + 2 * dlA, 6), 3)                        # B's length doubled, its Y not
    c[(38, 2)] = lambda: (int('0010', 2) & int('1010', 2), int('0010', 2))   # AND (bubble missed): A'·B, as numbers
    c[(40, 3)] = lambda: (-1, -1)                                            # exponent of U = ε0AV²/2x itself
    c[(42, 2)] = lambda: (round(100 * 20e-6 * 1e3, 6), 2.0)                  # diode resistance ignored
    c[(42, 3)] = lambda: (round((100 + 5) * 20e-6 * 1e3, 6), 2.1)            # both diodes in parallel: 5 Ω
    c[(42, 4)] = lambda: (round((100 + 20) * 20e-6 * 1e3, 6), 2.4)           # both diodes in series: 20 Ω
    c[(43, 4)] = lambda: ((27, 27 / (6 + 0.75)), (27, 4))                    # EMF given as V_AB
    c[(44, 1)] = lambda: (round(1.22 * 500e-9 / 5e-7 / 2 * 100, 6), 61)      # θ = 1.22λ/2R: R taken as a radius
    c[(46, 175)] = lambda: (5 * 75 + 2 * (-100), 175)                        # 25(3î - 4ĵ) used, not 25 × unit vector
    c[(47, 132)] = lambda: (round(4 * 22 / 7 * 3.5e-2 * (4 - 1) * 1e-4 * 1e6, 6), 132)   # one surface only
    c[(51, 3)] = lambda: ((round(1.4187 / 11.2, 4), round(1.4187 / 11.2 * 6.022e23 / 1e22, 2)), (0.1267, 7.63))   # 11.2 L per mole
    c[(55, 1)] = lambda: ((2.7e-5) ** 3, (2.7e-5) ** 3)                      # cubed instead of cube root
    c[(55, 3)] = lambda: (round((2.7e-5) ** 0.5, 9), round(math.sqrt(2.7e-5), 9))   # square root instead of cube root
    c[(74, 1096)] = lambda: (round((14 - (4.74 - math.log10(250 / 5))) * 100), 1096)   # salt/base ratio upside down
    return c
