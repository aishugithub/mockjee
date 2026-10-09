"""
Shared definitions for the trap (distractor) analysis, step 3 in CLAUDE.md.

A trap row names the specific mistake that leads to one wrong option (MCQ) or to a known slip value
(numerical). Rows live in pyq/<year>/<shift>/traps.csv; they are Claude's analysis, not NTA's.
"""

COLS = ['q', 'option', 'trap', 'mistake_type', 'check', 'note']

# The fixed list of mistake types (code -> label shown to Akil). Keep it short; add a code only with the owner.
MISTAKE_TYPES = {
    'concept_gap': 'Concept gap',
    'formula_misapplied': 'Formula misapplied',
    'calc_slip': 'Calculation slip',
    'units': 'Units',
    'misread': 'Misread the question',
    'ncert_fact': 'NCERT fact not known',
    'none': 'No clear mistake path',
}

# sympy / arithmetic = a script in tools/trap_checks recomputes the wrong path and confirms it lands on this
# option's value; conceptual = the path is a misconception, not a computation (a teacher should spot-check it).
CHECKS = ('sympy', 'arithmetic', 'conceptual')

NO_PATH = 'No clear mistake path'
