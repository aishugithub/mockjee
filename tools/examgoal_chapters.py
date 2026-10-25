"""
ExamGOAL's chapter list (the finer "topic" layer the owner chose on 2026-10-25), each mapped to the
NTA 2026 syllabus unit code in tools/chapters.py, so the existing chapter filters keep working.

Names are exactly as ExamGOAL / ExamSIDE print them (pdf.questions.examgoal.com/past-years/jee/jee-main).
A question's topic comes from ExamSIDE's own page for that question; only the NTA unit is derived here.

AMBIGUOUS lists ExamGOAL chapters that span two NTA units (checked against the syllabus PDF in
sources/syllabus/). For those the unit below is the usual home, and the question is marked
tag_confidence = 'low' so the owner or a teacher can review it.
"""

# subject -> {ExamGOAL chapter: NTA unit code}
MAP = {
    'Physics': {
        'Units & Measurements': 'P1',
        'Vector Algebra': 'P2',                 # syllabus unit 2 covers scalars and vectors
        'Motion in a Straight Line': 'P2',
        'Motion in a Plane': 'P2',
        'Circular Motion': 'P3',                # kinematics in unit 2, dynamics (banking, centripetal force) in unit 3
        'Laws of Motion': 'P3',
        'Work Power & Energy': 'P4',
        'Center of Mass and Collision': 'P5',   # centre of mass in unit 5, collisions in unit 4
        'Rotational Motion': 'P5',
        'Properties of Matter': 'P7',
        'Heat and Thermodynamics': 'P8',        # heat/calorimetry/expansion in unit 7, thermodynamics unit 8, kinetic theory unit 9
        'Simple Harmonic Motion': 'P10',
        'Waves': 'P10',
        'Gravitation': 'P6',
        'Electrostatics': 'P11',
        'Capacitor': 'P11',
        'Current Electricity': 'P12',
        'Magnetic Effect of Current': 'P13',
        'Magnetic Properties of Matter': 'P13',
        'Electromagnetic Induction': 'P14',
        'Alternating Current': 'P14',
        'Electromagnetic Waves': 'P15',
        'Wave Optics': 'P16',
        'Geometrical Optics': 'P16',
        'Atoms and Nuclei': 'P18',
        'Dual Nature of Radiation': 'P17',
        'Semiconductor': 'P19',
        'Communication Systems': 'PX',
    },
    'Chemistry': {
        'Some Basic Concepts of Chemistry': 'C1',
        'Structure of Atom': 'C2',
        'Redox Reactions': 'C7',
        'Gaseous State': 'CX',
        'Chemical Equilibrium': 'C6',
        'Ionic Equilibrium': 'C6',
        'Solutions': 'C5',
        'Thermodynamics': 'C4',
        'Electrochemistry': 'C7',
        'Chemical Kinetics and Nuclear Chemistry': 'C8',
        'Solid State': 'CX',
        'Surface Chemistry': 'CX',
        'Periodic Table & Periodicity': 'C9',
        'Chemical Bonding & Molecular Structure': 'C3',
        'Isolation of Elements': 'CX',
        'Hydrogen': 'CX',
        's-Block Elements': 'CX',
        'p-Block Elements': 'C10',
        'd and f Block Elements': 'C11',
        'Coordination Compounds': 'C12',
        'Salt Analysis': 'C20',
        'Environmental Chemistry': 'CX',
        'Basics of Organic Chemistry': 'C14',
        'Hydrocarbons': 'C15',
        'Haloalkanes and Haloarenes': 'C16',
        'Alcohols, Phenols and Ethers': 'C17',
        'Aldehydes, Ketones and Carboxylic Acids': 'C17',
        'Compounds Containing Nitrogen': 'C18',
        'Polymers': 'CX',
        'Biomolecules': 'C19',
        'Chemistry in Everyday Life': 'CX',
        'Practical Organic Chemistry': 'C13',   # purification/estimation in unit 13, functional-group tests in unit 20
    },
    'Mathematics': {
        'Sets and Relations': 'M1',
        'Logarithm': 'M7',                      # NTA has no logarithm unit; log functions sit in unit 7
        'Quadratic Equation and Inequalities': 'M2',
        'Sequences and Series': 'M6',
        'Mathematical Induction': 'MX',
        'Binomial Theorem': 'M5',
        'Matrices and Determinants': 'M3',
        'Permutations and Combinations': 'M4',
        'Probability': 'M13',
        'Vector Algebra': 'M12',
        '3D Geometry': 'M11',
        'Complex Numbers': 'M2',
        'Statistics': 'M13',
        'Mathematical Reasoning': 'MX',
        'Trigonometric Ratio and Identites': 'M14',
        'Trigonometric Equations': 'M14',
        'Inverse Trigonometric Functions': 'M14',
        'Properties of Triangle': 'M14',
        'Height and Distance': 'M14',
        'Straight Lines and Pair of Straight Lines': 'M10',
        'Circle': 'M10',
        'Parabola': 'M10',
        'Ellipse': 'M10',
        'Hyperbola': 'M10',
        'Functions': 'M1',
        'Limits, Continuity and Differentiability': 'M7',
        'Differentiation': 'M7',
        'Application of Derivatives': 'M7',
        'Indefinite Integrals': 'M8',
        'Definite Integration': 'M8',
        'Area Under The Curves': 'M8',
        'Differential Equations': 'M9',
    },
}

AMBIGUOUS = {
    ('Physics', 'Circular Motion'), ('Physics', 'Center of Mass and Collision'),
    ('Physics', 'Heat and Thermodynamics'), ('Chemistry', 'Practical Organic Chemistry'),
    ('Mathematics', 'Logarithm'),
}


def unit_for(subject, topic):
    """(NTA unit code, ambiguous?) for an ExamGOAL chapter; KeyError if the name is unknown."""
    return MAP[subject][topic], (subject, topic) in AMBIGUOUS
