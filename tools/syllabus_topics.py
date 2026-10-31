"""
Sub-topics within each NTA unit, so Akil can practise one narrow topic (owner's request 2026-10-31: "still
finer topics" than ExamGOAL's chapter names). Built from the items NTA lists under each unit of the JEE Main
2026 syllabus (sources/syllabus/JEE_Main_2026_syllabus.pdf), grouped into a handful per unit; the wording
follows the syllabus. NTA itself does not tag questions by topic: the tags in pyq/<year>/<shift>/syllabus_topics.csv
(columns q,syllabus_topic) are Claude's, made by reading each question.

A few groups are named for how questions are usually set rather than a single syllabus phrase (for example
"Area under curves", which the syllabus lists under definite integrals); every one still sits inside its unit.
Questions on topics outside the current syllabus get no sub-topic. Not in the 2026 wording but kept because
older papers (2021-2025) ask them inside the same unit: Remainders and approximations, Properties of
triangles, Planes, Radioactivity, Electrolysis and Faraday's laws.
"""

SYLLABUS_TOPICS = {
    # ---------------- Mathematics ----------------
    'Sets, Relations and Functions': [
        'Sets, union, intersection and power set',
        'Relations and equivalence relations',
        'Functions: domain and range',
        'One-one, onto and composite functions',
    ],
    'Complex Numbers and Quadratic Equations': [
        'Algebra of complex numbers',
        'Modulus, argument and Argand plane',
        'Roots and coefficients of quadratics',
        'Nature of roots and location of roots',
    ],
    'Matrices and Determinants': [
        'Algebra and types of matrices',
        'Evaluating determinants and their properties',
        'Adjoint and inverse of a matrix',
        'System of linear equations: consistency',
    ],
    'Permutations and Combinations': [
        'Fundamental principle of counting',
        'Permutations: arrangements and words',
        'Combinations: selections and distributions',
    ],
    'Binomial Theorem': [
        'General term and specific coefficients',
        'Middle term and greatest term',
        'Sums of binomial coefficients',
        'Remainders and approximations',
    ],
    'Sequence and Series': [
        'Arithmetic progressions',
        'Geometric progressions',
        'AM, GM and their relation',
        'Special series and sums of terms',
    ],
    'Limit, Continuity and Differentiability': [
        'Functions and their graphs',
        'Limits',
        'Continuity and differentiability',
        'Differentiation techniques',
        'Rate of change and tangents',
        'Increasing and decreasing functions',
        'Maxima and minima',
    ],
    'Integral Calculus': [
        'Indefinite integrals',
        'Definite integrals and their properties',
        'Area under curves',
    ],
    'Differential Equations': [
        'Order and degree; forming equations',
        'Variable separable equations',
        'Homogeneous equations',
        'Linear first-order equations',
    ],
    'Co-ordinate Geometry': [
        'Points, distance, section formula and locus',
        'Straight lines',
        'Centroid, orthocentre and circumcentre',
        'Circle',
        'Parabola',
        'Ellipse',
        'Hyperbola',
    ],
    'Three Dimensional Geometry': [
        'Direction cosines and ratios; angle between lines',
        'Equation of a line in space',
        'Skew lines and shortest distance',
        'Planes',
    ],
    'Vector Algebra': [
        'Addition and components of vectors',
        'Scalar (dot) product',
        'Vector (cross) product and triple products',
    ],
    'Statistics and Probability': [
        'Mean, median and mode',
        'Variance, standard deviation and mean deviation',
        'Probability: addition and multiplication theorems',
        'Conditional probability and Bayes theorem',
        'Random variables and probability distributions',
    ],
    'Trigonometry': [
        'Trigonometric identities and values',
        'Trigonometric equations',
        'Inverse trigonometric functions',
        'Properties of triangles',
    ],
    # ---------------- Physics ----------------
    'Units and Measurements': [
        'Units and dimensional analysis',
        'Errors, least count and significant figures',
    ],
    'Kinematics': [
        'Motion in a straight line and graphs',
        'Relative velocity',
        'Projectile motion',
        'Uniform circular motion',
    ],
    'Laws of Motion': [
        "Newton's laws, momentum and impulse",
        'Equilibrium of forces and connected bodies',
        'Friction',
        'Circular motion dynamics: banked roads',
    ],
    'Work, Energy and Power': [
        'Work by constant and variable forces',
        'Work-energy theorem and power',
        'Spring potential energy and conservation of energy',
        'Motion in a vertical circle',
        'Collisions',
    ],
    'Rotational Motion': [
        'Centre of mass',
        'Moment of inertia and axes theorems',
        'Torque and angular momentum conservation',
        'Rolling motion and rotational dynamics',
        'Equilibrium of rigid bodies',
    ],
    'Gravitation': [
        'Law of gravitation and gravitational field',
        'Acceleration due to gravity: altitude and depth',
        "Kepler's laws",
        'Gravitational potential energy and escape velocity',
        'Satellites: orbital velocity, period and energy',
    ],
    'Properties of Solids and Liquids': [
        "Elasticity: stress, strain and Young's modulus",
        "Fluid pressure, Pascal's law and buoyancy",
        "Viscosity and Stokes' law",
        "Bernoulli's principle and flow",
        'Surface tension and capillarity',
        'Thermal expansion',
        'Calorimetry and latent heat',
        'Heat transfer: conduction, convection, radiation',
    ],
    'Thermodynamics': [
        'Zeroth and first law; heat and work',
        'Isothermal and adiabatic processes',
        'Second law, heat engines and refrigerators',
    ],
    'Kinetic Theory of Gases': [
        'Ideal gas equation',
        'Kinetic theory: pressure, rms speed and temperature',
        'Degrees of freedom and specific heats',
        'Mean free path',
    ],
    'Oscillations and Waves': [
        'SHM: equation, phase and energy',
        'Spring-mass systems and pendulums',
        'Travelling waves and wave speed',
        'Superposition and standing waves: strings and pipes',
        'Beats',
    ],
    'Electrostatics': [
        "Coulomb's law and superposition",
        'Electric field and dipoles',
        "Electric flux and Gauss's law",
        'Electric potential and potential energy',
        'Conductors and capacitance',
        'Capacitor combinations, dielectrics and energy',
    ],
    'Current Electricity': [
        'Drift velocity, resistivity and Ohm\'s law',
        'Resistor combinations and temperature dependence',
        'Cells, emf and internal resistance',
        "Kirchhoff's laws and circuits",
        'Wheatstone bridge and metre bridge',
        'Electrical energy and power',
    ],
    'Magnetic Effects of Current and Magnetism': [
        'Biot-Savart law',
        "Ampere's law: wires and solenoids",
        'Force on moving charges and currents',
        'Torque on current loops and galvanometers',
        'Magnetic dipoles and bar magnets',
        'Magnetic materials',
    ],
    'Electromagnetic Induction and Alternating Currents': [
        "Faraday's and Lenz's laws; motional emf",
        'Self and mutual inductance',
        'AC: rms values, reactance and impedance',
        'LCR circuits, resonance and power',
        'AC generator and transformer',
    ],
    'Electromagnetic Waves': [
        'Displacement current and properties of EM waves',
        'Electromagnetic spectrum',
    ],
    'Optics': [
        'Reflection and spherical mirrors',
        'Refraction and total internal reflection',
        'Lenses and lens combinations',
        'Prism and dispersion',
        'Optical instruments',
        "Wavefronts and Huygens' principle",
        "Interference: Young's double slit",
        'Diffraction',
        'Polarisation',
    ],
    'Dual Nature of Matter and Radiation': [
        'Photoelectric effect',
        'Matter waves: de Broglie relation',
    ],
    'Atoms and Nuclei': [
        'Rutherford scattering and Bohr model',
        'Hydrogen spectrum',
        'Nuclear size, mass defect and binding energy',
        'Radioactivity',
        'Nuclear fission and fusion',
    ],
    'Electronic Devices': [
        'Semiconductors and p-n junction',
        'Diodes and rectifiers',
        'Zener diode, LED, photodiode and solar cell',
        'Logic gates',
    ],
    'Experimental Skills': [
        'Vernier calipers and screw gauge',
        'Mechanics and properties-of-matter experiments',
        'Heat and sound experiments',
        'Electricity experiments',
        'Optics experiments',
        'Semiconductor experiments',
    ],
    # ---------------- Chemistry ----------------
    'Some Basic Concepts in Chemistry': [
        'Laws of chemical combination',
        'Mole concept and molar mass',
        'Empirical and molecular formulae',
        'Stoichiometry and limiting reagent',
        'Concentration terms',
    ],
    'Atomic Structure': [
        'Electromagnetic radiation and photoelectric effect',
        'Bohr model and hydrogen spectrum',
        'de Broglie relation and uncertainty principle',
        'Quantum numbers and orbitals',
        'Electronic configuration',
    ],
    'Chemical Bonding and Molecular Structure': [
        'Ionic bonding and lattice enthalpy',
        "Electronegativity, Fajans' rule and dipole moment",
        'VSEPR theory and shapes',
        'Hybridisation and resonance',
        'Molecular orbital theory and bond order',
        'Hydrogen bonding',
    ],
    'Chemical Thermodynamics': [
        'System, state functions and processes',
        'First law: work, heat, internal energy, enthalpy',
        "Enthalpies of reaction and Hess's law",
        'Entropy, Gibbs energy and spontaneity',
    ],
    'Solutions': [
        'Concentration of solutions',
        "Vapour pressure, Raoult's law and ideal solutions",
        'Colligative properties',
        "van 't Hoff factor and abnormal molar mass",
    ],
    'Equilibrium': [
        "Physical equilibria and Henry's law",
        'Equilibrium constants Kp and Kc',
        "Le Chatelier's principle",
        'Acids, bases, pH and ionisation constants',
        'Salt hydrolysis and buffers',
        'Solubility product and common ion effect',
    ],
    'Redox Reactions and Electrochemistry': [
        'Oxidation number and balancing redox reactions',
        "Conductance and Kohlrausch's law",
        'Electrode potentials and cells',
        'Nernst equation and Gibbs energy',
        "Electrolysis and Faraday's laws",
        'Batteries and fuel cells',
    ],
    'Chemical Kinetics': [
        'Rate, order and molecularity',
        'Integrated rate laws and half-life',
        'Arrhenius equation and activation energy',
    ],
    'Classification of Elements and Periodicity in Properties': [
        'Periodic table and electronic configuration',
        'Atomic and ionic radii',
        'Ionisation enthalpy and electron gain enthalpy',
        'Electronegativity, valence and oxidation states',
    ],
    'p-Block Elements': [
        'Group 13: boron family',
        'Group 14: carbon family',
        'Group 15: nitrogen family',
        'Group 16: oxygen family',
        'Group 17: halogens',
        'Group 18: noble gases',
    ],
    'd- and f-Block Elements': [
        'Transition elements: trends and properties',
        'Colour, magnetism and catalytic behaviour',
        'K2Cr2O7 and KMnO4',
        'Lanthanoids and actinoids',
    ],
    'Coordination Compounds': [
        "Werner's theory, ligands and nomenclature",
        'Isomerism in complexes',
        'Valence bond theory and magnetism',
        'Crystal field theory and colour',
        'Applications of complexes',
    ],
    'Purification and Characterisation of Organic Compounds': [
        'Purification methods and chromatography',
        'Detection of elements',
        'Quantitative estimation of elements',
    ],
    'Some Basic Principles of Organic Chemistry': [
        'IUPAC nomenclature',
        'Structural isomerism',
        'Stereoisomerism',
        'Reactive intermediates and their stability',
        'Inductive, resonance and hyperconjugation effects',
        'Types of organic reactions',
    ],
    'Hydrocarbons': [
        'Alkanes and conformations',
        'Alkenes',
        'Alkynes',
        'Aromaticity and benzene',
        'Electrophilic aromatic substitution',
    ],
    'Organic Compounds Containing Halogens': [
        'Preparation of haloalkanes and haloarenes',
        'SN1 and SN2 reactions',
        'Elimination reactions',
        'Haloarenes and polyhalogen compounds',
    ],
    'Organic Compounds Containing Oxygen': [
        'Alcohols',
        'Phenols',
        'Ethers',
        'Aldehydes and ketones: nucleophilic addition',
        'Aldehydes and ketones: named reactions and tests',
        'Carboxylic acids and their derivatives',
    ],
    'Organic Compounds Containing Nitrogen': [
        'Amines: preparation and reactions',
        'Basicity of amines',
        'Diazonium salts',
    ],
    'Biomolecules': [
        'Carbohydrates',
        'Amino acids and proteins',
        'Vitamins and hormones',
        'Nucleic acids',
    ],
    'Principles Related to Practical Chemistry': [
        'Detection of elements and functional groups',
        'Preparation of compounds',
        'Titrations and indicators',
        'Salt analysis: cations and anions',
        'Physical chemistry experiments',
    ],
}

if __name__ == '__main__':
    print(sum(len(v) for v in SYLLABUS_TOPICS.values()), 'sub-topics in', len(SYLLABUS_TOPICS), 'units')
