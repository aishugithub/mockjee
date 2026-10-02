# How worked solutions are written (for Akil)

Every PYQ gets one row in `pyq/<year>/<shift>/solutions.csv`:

| column | what goes in it |
|---|---|
| `q` | question number in the paper (1–75) |
| `claude_answer` | option number 1–4 (MCQ) or the value (numerical) Claude got. Must equal NTA's final key; if it does not, stop and flag it to the owner. Never change the key. |
| `check` | `sympy` or `arithmetic` = the answer is recomputed in `tools/verify_pyq_solutions.py`; `conceptual` = theory, needs a teacher. |
| `hint1` | A nudge towards the idea, usually a question. Names what to notice or which concept applies. Gives away no number and no option. |
| `hint2` | The key formula, relation or first step, written out. Still stops before the answer. |
| `solution` | Short numbered steps (1. 2. 3. …), one idea per step, plain words, then `Answer: (k)` or `Answer: value`. Written for a student, not for a checker. Say why a tempting wrong option is wrong when that is quick. |
| `concept` | One line: what the question tests (chapter idea, not the chapter name alone). |
| `revise` | One or two kind sentences: which part was probably hard and what to revise (topic, NCERT chapter name). Never "you didn't understand"; we don't know why he missed it. Suggest, don't judge. |
| `note` | For the owner/teacher only: figure readings, rounding, NCERT-dependent statements. Shown in small print. |

Rules
- The app shows hints one by one, then the solution, so hint 1 must not contain hint 2's formula, and neither may contain the answer.
- Tone: warm, direct, encouraging. "Notice…", "Ask yourself…", "A common slip here is…".
- Markup: `x^{2}`, `H_{2}O`, `\n` for a new line. Do not use a bare `^` or `_`.
- Everything is labelled in the app as written by Claude and checked against NTA's final key.
- After a shift: `python tools/verify_pyq_solutions.py`, `python tools/build_pyq_bank.py`, `python tools/make_solution_review.py pyq/<year>/<shift>`.
