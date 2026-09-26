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

## Next planned step
Download the NTA final answer key and the matching question paper for one session (start with JEE Main 2025, January Shift 1). Save them under `sources/` with their original URL and download date. Extract the questions into the CSV import format, matched to the key by NTA question ID. Flag anything that can't be extracted reliably (figures, heavy equations) for manual checking. Have the owner review that batch before scaling up.

## Testing
Open `index.html` in a browser, or serve the folder (`python -m http.server`). Check the full flow: setup, instructions, answering (Save & Next, Mark for Review, numerical keypad), submit, result, PDF.
