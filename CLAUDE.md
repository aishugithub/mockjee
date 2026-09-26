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
- Done: JEE Main 2026 Session 2, all 9 B.Tech shifts (673 questions). The final key's India pages match the public papers' question IDs.
- Not possible with public docs: 2025 papers (only shown inside candidate login). 2026 Session 1 papers are also not in the public Question Papers menu.
- Chapters are "Not tagged yet"; needs tagging (by reading the images) before chapter filters are useful.
- Images load from `pyq/`, so serve the folder over http (`python -m http.server`) for the PDF report. The claude.ai Artifact copy does not include the PYQ images.

## Why this site exists (owner, 2026-09-26)
Plenty of sites already run PYQ mocks. This one exists to diagnose Akil: which chapters he is strong or weak in, and WHY he gets questions wrong. Many wrong options in JEE are traps, meaning they are exactly what you get by making a specific mistake. When Akil picks one, the site should name that mistake (e.g. "used the full-plate formula for a half-filled capacitor"). Every feature should serve this diagnosis.

## Next planned steps (in order)
Work in batches of one shift (75 questions). Have the owner review the first batch before doing the rest, as with the extraction.

1. **Chapter tagging (Claude reads the images).** Claude can read the question images (Q3 and Q68 of 2026 were read and checked this way). For each question, record in the shift's `questions.json` (and carry it through `build_pyq_bank.py`):
   - `chapter`: from the official NTA JEE Main syllabus chapter list (download the current syllabus PDF from jeemain.nta.nic.in into `sources/`, and use its unit names exactly, so tags are consistent)
   - `subtopic` (a short concept name)
   - `secondary_chapter` when a question really mixes two chapters
   - `tag_confidence` (high/low); low-confidence tags go to the owner for review
2. **Worked solution + key check.** Claude solves each question. If Claude's answer disagrees with NTA's final key, do NOT change the key: flag it for the owner. Where computable, verify with SymPy as `verify_answers.py` does. Label every solution "Solution written by Claude, checked against NTA's final key", never as NTA's.
3. **Trap (distractor) analysis.** For each wrong MCQ option, record `option_traps[k]` = the specific mistake that leads to it (wrong formula, sign or factor error, unit slip, misread "incorrect statement", etc.), plus a `mistake_type` from a fixed list (concept gap, formula misapplied, calculation slip, units, misread question, NCERT fact not known). Only write a trap when the path is really derivable. Otherwise write "no clear mistake path" and never invent one. For numericals, record known trap values where a common slip gives a specific number. Label all of this as Claude's analysis. A subject teacher should spot-check it.
4. **Analysis in the app** (result screen, PDF, and a new "Akil's progress" view across all attempts in history):
   - per chapter: attempted, correct, wrong, skipped, accuracy, marks lost to negatives, time per question
   - strong/weak chapter lists, only with a minimum number of attempts shown (don't call a chapter weak from 1 question)
   - each wrong answer: the trap he fell into, and his recurring mistake types across tests (e.g. "calculation slips: 6 of 14 errors")
   - slow-but-correct questions (shaky areas) and guessing pattern (wrong attempts that cost negative marks)
   - "practise next": build a test from his weak chapters
5. **Keep attempt history safe.** History is only in this browser's localStorage (`jeecbt.history.v1`). It is lost if browser data is cleared, and is not shared across devices. Add export/import of history (JSON file) at minimum.
6. Later: 2024 and 2023 papers (below).

## 2024 and 2023 papers
2024 and 2023: jeemain.nta.nic.in's archive has final answer keys, and nta.ac.in hosts NTA papers at `/Download/ExamPaper/Paper_<timestamp>.pdf`, but there is no public index page for them (nta.ac.in/Downloads redirects home). Identify which of those files are JEE Main B.Tech shifts, confirm each one's question IDs match an NTA final key, then run the same two tools. The old site jeemain.nta.ac.in has an expired certificate; don't bypass it.

## Testing
Open `index.html` in a browser, or serve the folder (`python -m http.server`). Check the full flow: setup, instructions, answering (Save & Next, Mark for Review, numerical keypad), submit, result, PDF.
