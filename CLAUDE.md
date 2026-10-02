# JEE Mock CBT: project notes for Claude

A static browser app (no server) for JEE Main mock tests: setup page (duration, PYQ years, subjects/chapters, marking), a CBT exam screen modelled on the official NTA layout, instant results, and a PDF report. See README.md for features and the question-bank format.

## Files
- `index.html`: the whole app (UI, exam engine, scoring, PDF via html2canvas + jsPDF from cdnjs)
- `questions.js`: built-in sample bank (`window.JEE_SAMPLE_BANK`)
- `verify_answers.py`: recomputes the sample answer keys with SymPy and cross-checks `questions.js`
- A copy of `index.html` with the doctype/html/head/body/meta tags stripped is published as a claude.ai Artifact: https://claude.ai/artifact/T3WdQnV6aBoco1DfS9AY1R

## Credibility rules (the owner's top priority)
- Never present a question as a real PYQ unless it came from an official NTA paper. The 84 built-in questions are ORIGINAL practice items. Their years are demo tags only. The UI labels them "Practice question (year tag N)", and the setup page and PDF cover say they are not official.
- Every real PYQ must carry a `source` (e.g. "JEE Main 2025, 22 Jan Shift 1, Q.ID …") and its answer must come from NTA's FINAL answer key, not the provisional key or coaching sites. Mark questions NTA dropped or gave bonus marks for.
- Only use public NTA documents. Never use a candidate's login.
- Don't state facts about the exam pattern, other products or papers without checking a source. Say what was not verified.
- After editing any answer key, run `python3 verify_answers.py`. Conceptual questions it can't compute need a subject teacher's review.

## Official PYQ bank (status 2026-09-26)
- `sources/<year>/`: NTA PDFs exactly as downloaded, with `SOURCES.md` (URL, date, hash). Downloaded from the owner's own computer.
- NTA papers print every question and option as an image; only question/option IDs are text. `tools/extract_nta_paper.py` saves NTA's own images (unchanged pixels) to `pyq/<year>/<shift>/img/`, maps the final key's correct option ID to the option position, and writes `questions.json` + `review.csv` (flags) per shift.
- `tools/build_pyq_bank.py` bundles all shifts into `pyq_bank.js` (`window.JEE_PYQ_BANK`), the app's default bank. Dropped questions and "any answer" keys are left out; "41 or 42" and two-correct-option keys use `accept`.
- Done: JEE Main 2026 Session 2 (9 shifts), 2024 Sessions 1 and 2 (17 shifts), 2023 Session 2 (12 shifts): 3,264 questions. The final key's India pages match the public papers' question IDs.
- Not possible with public docs: 2025 papers (only shown inside candidate login). 2026 Session 1 papers are also not in the public Question Papers menu.
- Chapters are tagged for every question (see step 1 below).
- Images load from `pyq/`, so serve the folder over http (`python -m http.server`) for the PDF report. The claude.ai Artifact copy does not include the PYQ images.

## Why this site exists (owner, 2026-09-26)
Plenty of sites already run PYQ mocks. This one exists to diagnose Akil: which chapters he is strong or weak in, and WHY he gets questions wrong. Many wrong options in JEE are traps, meaning they are exactly what you get by making a specific mistake. When Akil picks one, the site should name that mistake (e.g. "used the full-plate formula for a half-filled capacitor"). Every feature should serve this diagnosis.

## Next planned steps (in order)
Work in batches of one shift (75 questions). Have the owner review the first batch before doing the rest, as with the extraction.

1. **Chapter tagging: DONE (2026-09-28).** All 3,264 questions (2023 S2, 2024 S1+S2, 2026 S2) are tagged in `pyq/<year>/<shift>/tags.csv` (columns `q,chapter,subtopic,confidence,secondary`; chapter codes from `tools/chapters.py`, which follows the NTA 2026 syllabus units). `build_pyq_bank.py` checks every code and subject. 2023 topics dropped from the current syllabus (communication systems, solid state, surface chemistry, s-block, polymers, etc.) are tagged `PX/CX/MX` = "Not in current syllabus" and are unticked by default in the app. 90 tags are `low` confidence; `pyq/low_confidence_tags.csv` lists them for the owner or a teacher to review. Tags were made by Claude reading the question images.
2. **Worked solution + key check: owner approved the approach (2026-10-02) and asked for ALL shifts, written for Akil with hints.** Format and tone: `tools/SOLUTION_STYLE.md` (columns `q,claude_answer,check,hint1,hint2,solution,concept,revise,note`). Progress (update after every shift): DONE 2026: 02Apr_Shift1, 02Apr_Shift2, 04Apr_Shift1, 04Apr_Shift2, 05Apr_Shift1, 05Apr_Shift2. NEXT: 2026 06Apr_Shift1, 06Apr_Shift2, 08Apr_Shift2, then 2024 (17 shifts), then 2023 (12 shifts). Disputed so far (held back, owner/teacher to decide): 2026 04Apr_Shift2 Q61.
   Per shift: `python tools/make_sheets.py pyq/<y>/<shift> <scratch>` to read the images; solve; write `tools/pyq_checks/y<year>_<shift>.py` (checks() -> {q: fn} returning option 1-4 or value) for every computable question; write the hint-style data file and run `python tools/write_solutions_csv.py <data.py> pyq/<y>/<shift>`; then `python tools/finish_shift.py <data.py> pyq/<y>/<shift>` (writes the CSV, runs every check, builds the bank and the review page; commit and push only when it prints "OK: ready to commit").
   Hint ladder in the review (owner's request, 2026-10-02): wrong/skipped questions with hints open with the answer hidden; Akil can retry (practice only), open hint 1, hint 2, see the solution, or skip (allowed: he can't score 100%, choosing what to leave is fine). Every step is logged in `exam.practice[i].events` and saved to the `practice` table (outcome solved_no_hint / solved_hint1 / solved_hint2 / saw_solution / skipped / open). The server rebuilds missing practice rows from `raw_json` on startup.
   **jee-analysis skill: DONE** (`.claude/skills/jee-analysis/SKILL.md`, `tools/analysis_data.py`, `tools/save_analysis.py`).
   Earlier status: FIRST BATCH DONE (2026-10-01). 2026 / 02Apr_Shift1: all 75 solved in `pyq/2026/02Apr_Shift1/solutions.csv` (columns `q,claude_answer,check,solution,note`; `check` = `sympy` | `arithmetic` (both recomputed in `tools/verify_pyq_solutions.py`) | `conceptual` (needs a teacher)). All 75 agree with NTA's final key; 57 are recomputed by script, 18 are conceptual. `build_pyq_bank.py` bundles solutions as `solution`, `solution_by: "claude"`, `solution_check`, `solution_note` and refuses to build if a solution's answer differs from the key. The app labels them "written by Claude, checked against NTA's final key" in the review and PDF. `tools/make_solution_review.py <shift folder>` writes `solutions_review.html` for the owner/teacher. Notes worth a look: Q37 and Q39 depend on reading loose figures; Q41's exact answer is 0.96 cm (key 1); Q63 is NCERT-based. Run `python tools/verify_pyq_solutions.py` after adding a shift (needs `pip install sympy mpmath`). Next: the remaining shifts, after the owner approves this batch.
   Original brief: Claude solves each question. If Claude's answer disagrees with NTA's final key, do NOT change the key: flag it for the owner. Where computable, verify with SymPy as `verify_answers.py` does. Label every solution "Solution written by Claude, checked against NTA's final key", never as NTA's.
3. **Trap (distractor) analysis.** For each wrong MCQ option, record `option_traps[k]` = the specific mistake that leads to it (wrong formula, sign or factor error, unit slip, misread "incorrect statement", etc.), plus a `mistake_type` from a fixed list (concept gap, formula misapplied, calculation slip, units, misread question, NCERT fact not known). Only write a trap when the path is really derivable. Otherwise write "no clear mistake path" and never invent one. For numericals, record known trap values where a common slip gives a specific number. Label all of this as Claude's analysis. A subject teacher should spot-check it.
4. **Analysis in the app** (result screen, PDF, and a new "Akil's progress" view across all attempts in history):
   - per chapter: attempted, correct, wrong, skipped, accuracy, marks lost to negatives, time per question
   - strong/weak chapter lists, only with a minimum number of attempts shown (don't call a chapter weak from 1 question)
   - each wrong answer: the trap he fell into, and his recurring mistake types across tests (e.g. "calculation slips: 6 of 14 errors")
   - slow-but-correct questions (shaky areas) and guessing pattern (wrong attempts that cost negative marks)
   - "practise next": build a test from his weak chapters
5. **Attempt history: DONE (2026-09-28).** `server.py` (Flask) serves the app and saves every submitted exam to SQLite at `data/akil.db` (tables `attempts`, `responses`, `flags`, `analyses`; schema in `server.py`). Per question it stores the final and first answer, answer changes, visits, time, mark-for-review, and Akil's own reason for each wrong answer (`concept` didn't know / `approach` silly concept mistake / `calc` silly calculation mistake / `recall` forgot a formula or fact / `misread` / `rushed`), tapped inside the answer review. Marks are recomputed on the server. Results made while the server was unreachable wait in localStorage (`jeecbt.unsynced.v1`) and are sent on the next load. Start with `run_app.bat` or `python server.py` (port 8000). `data/` and `.secrets` are gitignored. Online copy (PythonAnywhere, planned): `tools/pull_db.py` downloads the database via `/api/export` using `JEE_SERVER_URL` / `JEE_EXPORT_KEY` from `.secrets`; never ask the owner for the PythonAnywhere password.
   The `jee-analysis` skill now exists (see step 2).
6. Later: 2024 and 2023 papers (below).

## 2024 and 2023 papers
2024 and 2023: jeemain.nta.nic.in's archive has final answer keys, and nta.ac.in hosts NTA papers at `/Download/ExamPaper/Paper_<timestamp>.pdf`, but there is no public index page for them (nta.ac.in/Downloads redirects home). Identify which of those files are JEE Main B.Tech shifts, confirm each one's question IDs match an NTA final key, then run the same two tools. The old site jeemain.nta.ac.in has an expired certificate; don't bypass it.

## Testing
Run `python server.py` and open http://localhost:8000 (set `JEE_DB_PATH` to a scratch file so tests don't write into Akil's real database). Check the full flow: setup, instructions, answering (Save & Next, Mark for Review, numerical keypad), submit, result, PDF.
