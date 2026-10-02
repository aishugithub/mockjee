---
name: jee-analysis
description: Analyse Akil's JEE Main mock-test attempts from the progress database (data/akil.db). Finds strong and weak chapters, why he loses marks (his own reasons, how far he got with hints in the review, timing, guesses, traps), writes concept flags and a report for the owner, and saves them to the database. Use when the owner asks to analyse Akil's tests, check his progress, or find what he should practise next.
---

# jee-analysis

The site exists to diagnose Akil: which chapters are strong or weak, and WHY he gets questions wrong.
This skill turns his recorded attempts into that diagnosis. Everything it writes is Claude's analysis
and must be labelled that way. Never present a guess as a fact.

## 1. Get the data
- The database is `data/akil.db`. If the owner uses the online copy (PythonAnywhere), first run
  `python tools/pull_db.py`. It uses `JEE_SERVER_URL` / `JEE_EXPORT_KEY` from `.secrets`. Never ask for the PythonAnywhere password.
- Run `python tools/analysis_data.py --out <scratchpad>/facts.json`. Add `--since YYYY-MM-DD` or
  `--attempts id1,id2` when the owner asks about specific tests. Default is all attempts.
- Read facts.json. It holds the counts. Do the reasoning yourself, and never recount by hand what the script already counted.
- To see a question itself, open the image at `pyq/<year>/<shift>/img/<question_id>.png` (the source line names the shift).
  Read the worked solution and hints in `pyq/<year>/<shift>/solutions.csv`.

## 2. What the signals mean
For every wrong or skipped question you may have up to four signals. Combine them; don't rely on one.

| Signal | Field | Reading |
|---|---|---|
| His own reason | `his_reason` | concept = didn't know it; approach = knew it, wrong method; calc = arithmetic slip; recall = forgot a formula/fact; misread; rushed |
| Review outcome (hint ladder) | `review_outcome` | `solved_no_hint`: he can do it, so the loss was a slip, time or nerves. `solved_hint1`: knows the concept, couldn't see where to start (approach). `solved_hint2`: needed the formula or key step (recall / formula). `saw_solution`: real gap for now. `skipped`: chose not to try, which is allowed (see below). `open`: not reviewed yet. |
| Time | `secs`, `slow_correct`, `fast_wrong` | under 30 s and wrong suggests a guess; correct but over 2× his median suggests a shaky area |
| Answer changes | `answer_changes` | changed away from the right answer means low confidence |
| Trap | `option_traps`, `mistake_type` | only when present in the bank (step 3 of the plan). Name the mistake only if the trap data says so. |

Skipping is allowed and expected. Akil cannot score 100% in JEE Main, and choosing what to leave is a skill.
- Never treat a skip as a failure. Count skips separately.
- A chapter where he skips most questions, both in the test and in review, is a chapter he avoids. Report it as "not attempted yet", not as "weak".
- Skipped in the test but solved in review (`in_test: skipped` with a solved outcome) is good news: he knows more than he risked in the test. Mention it, because it is a confidence issue.
- Negative marks from fast wrong answers are worth pointing out: skipping those would have scored more.

## 3. Rules for conclusions
- Minimum evidence: call a chapter **weak** or **strong** only with at least 4 attempted questions in it across the analysed tests. With fewer, say "too few questions to judge (n = …)".
- A **flag** is one specific idea, e.g. "capacitor with a dielectric layer: series vs parallel", never "Electrostatics is weak". It needs at least 2 pieces of evidence, or 1 if the review outcome was `saw_solution` and his reason was `concept`.
- Flag `kind`: concept_gap | formula_misapplied | calculation | units | misread | ncert_fact | speed.
  Map: saw_solution or reason concept means concept_gap; solved_hint2 or reason recall means formula_misapplied (or ncert_fact for chemistry facts); reason calc or solved_no_hint after a wrong test answer means calculation; misread means misread; rushed or fast_wrong means speed.
- Update earlier flags (`open_flags` in facts.json) instead of adding duplicates.
  - Mark one `improving` when he has since got questions on that idea right, or solved them with fewer hints.
  - Mark it `resolved` only after 2 or more later correct answers on that idea in the timed test.
- Severity: high = several marks lost and the idea recurs in JEE; medium = recurring but small; low = one-off.
- Be kind and specific. Write for a parent and a student, not for an examiner.

## 4. The report (Markdown, for the owner)
Keep it short enough to read in three minutes:
1. **Snapshot**: tests covered, score trend, accuracy, marks lost to negatives.
2. **Strong chapters** and **weak chapters** (each with n), and chapters with too little data.
3. **Why marks were lost**: counts of mistake kinds, e.g. "calculation slips: 6 of 14 wrong answers", using his reasons and the review outcomes together.
4. **What the review showed**: how many he solved alone, after 1 hint, after 2 hints, needed the solution, or skipped, plus what that says.
5. **Guessing and time**: fast wrong answers and the marks they cost; slow-but-correct questions.
6. **Practise next**: 3–5 concrete items: chapter + idea + what to do. For example: "Revise series/parallel dielectric layers, then the 6 capacitor PYQs from 2024". The app can build a test from chosen chapters.
7. **Not verified / caveats**: small samples, untagged questions, anything you inferred.
End with: "Analysis written by Claude from Akil's recorded attempts."

## 5. Save
- Write `<scratchpad>/result.json` in the format documented at the top of `tools/save_analysis.py`
  (`attempts`, `summary` = the report, `flags`).
- Run `python tools/save_analysis.py <scratchpad>/result.json`. Flags then show in the app (`/api/flags`).
- If the owner uses PythonAnywhere, the saved flags live only in the local copy until the database is uploaded back. Say so; don't upload it yourself.
- Show the owner the report in the chat and offer to publish it as a page.
