"""
Official chapter (unit) names for tagging, from NTA's JEE Main 2026 syllabus
(sources/syllabus/JEE_Main_2026_syllabus.pdf, jeemain.nta.nic.in). Every question's
`chapter` must be one of these, so filters and chapter analysis stay consistent.

Names follow the syllabus unit titles in title case. Two spelling slips in NTA's PDF are
corrected: "INTEGRAL CALCULAS" -> Integral Calculus, "DIFFRENTIAL EQUATIONS" -> Differential Equations.

Questions from older papers (2023) on topics NTA removed from the syllabus are tagged
OUTSIDE instead of being forced into a unit; their `subtopic` names the old topic.
"""

OUTSIDE = 'Not in current syllabus'

CHAPTERS = {
    'Mathematics': [
        'Sets, Relations and Functions',
        'Complex Numbers and Quadratic Equations',
        'Matrices and Determinants',
        'Permutations and Combinations',
        'Binomial Theorem',
        'Sequence and Series',
        'Limit, Continuity and Differentiability',
        'Integral Calculus',
        'Differential Equations',
        'Co-ordinate Geometry',
        'Three Dimensional Geometry',
        'Vector Algebra',
        'Statistics and Probability',
        'Trigonometry',
    ],
    'Physics': [
        'Units and Measurements',
        'Kinematics',
        'Laws of Motion',
        'Work, Energy and Power',
        'Rotational Motion',
        'Gravitation',
        'Properties of Solids and Liquids',
        'Thermodynamics',
        'Kinetic Theory of Gases',
        'Oscillations and Waves',
        'Electrostatics',
        'Current Electricity',
        'Magnetic Effects of Current and Magnetism',
        'Electromagnetic Induction and Alternating Currents',
        'Electromagnetic Waves',
        'Optics',
        'Dual Nature of Matter and Radiation',
        'Atoms and Nuclei',
        'Electronic Devices',
        'Experimental Skills',
    ],
    'Chemistry': [
        'Some Basic Concepts in Chemistry',
        'Atomic Structure',
        'Chemical Bonding and Molecular Structure',
        'Chemical Thermodynamics',
        'Solutions',
        'Equilibrium',
        'Redox Reactions and Electrochemistry',
        'Chemical Kinetics',
        'Classification of Elements and Periodicity in Properties',
        'p-Block Elements',
        'd- and f-Block Elements',
        'Coordination Compounds',
        'Purification and Characterisation of Organic Compounds',
        'Some Basic Principles of Organic Chemistry',
        'Hydrocarbons',
        'Organic Compounds Containing Halogens',
        'Organic Compounds Containing Oxygen',
        'Organic Compounds Containing Nitrogen',
        'Biomolecules',
        'Principles Related to Practical Chemistry',
    ],
}

# Short codes used in tags.json to keep hand-written tag files compact and typo-proof.
CODES = {}
for _subj, _names in CHAPTERS.items():
    for _i, _n in enumerate(_names, 1):
        CODES[f'{_subj[0]}{_i}'] = (_subj, _n)      # M1..M14, P1..P20, C1..C20
for _s in 'MPC':
    CODES[f'{_s}X'] = ({'M': 'Mathematics', 'P': 'Physics', 'C': 'Chemistry'}[_s], OUTSIDE)

if __name__ == '__main__':
    for k, (s, n) in CODES.items():
        print(k, s, n, sep='\t')
