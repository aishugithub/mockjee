# JEE Mock CBT

A browser-based mock test platform for JEE Main. Teachers or students build a paper from a previous-year-question (PYQ) bank, sit it in a screen laid out like the official computer-based test, see the score right after submitting, and download a PDF report.

Everything runs in the browser. There is no server and no login, so the app can be hosted on any static host (GitHub Pages, Netlify, Firebase Hosting, a college web server) or opened straight from the folder.

## Features

| Requirement | Where it lives |
|---|---|
| Custom duration in minutes (75, 180, anything from 1 to 600) | Setup → Test details |
| Filter by all subjects, specific subjects, or individual chapters | Setup → Subjects and chapters |
| Pick and combine PYQ years (for example 2025 + 2026) | Setup → Previous-year papers |
| Question bank source | `questions.js` (built-in) plus JSON/CSV import from **Manage bank** |
| CBT-style exam screen | Section tabs, countdown timer, candidate panel, colour-coded question palette with live counts, on-screen keypad for numericals |
| Official button set | Save & Next, Clear, Save & Mark for Review, Mark for Review & Next, Back, Next, Submit, plus the exam summary table before submitting |
| Instant score | Result screen right after submitting, with positive marks, negative marks and net score |
| Chapter diagnosis | Result screen: per-chapter attempted / correct / wrong / skipped / accuracy / marks lost to negatives / average time; strong and weak chapters (only chapters with 4+ attempted questions are judged); slow-but-correct questions and quick wrong answers (likely guesses); a **Practise next** button that ticks only the weak chapters in the setup |
| Likely traps | In the answer review, a wrong option that Claude's trap analysis links to a specific mistake shows "Likely trap (Claude's analysis)" and the mistake type. Nothing is shown where there is no trap data |
| Progress across tests | Needs `server.py`. Every saved test: chapter totals with a test-by-test trend, strong/weak chapters, his own reasons for wrong answers, matched traps, hint-ladder outcomes, timing |
| PDF report | Cover summary, subject-wise table, chapter-wise split, strong and weak chapters, then every question with the options, the student's answer, the correct answer, marks, likely trap and solution |

Palette states follow the official instructions: Not Visited, Not Answered, Answered, Marked for Review, and Answered & Marked for Review (counted for evaluation). Navigating away without **Save** does not save the answer, same as the real exam. A test in progress is saved in the browser, so a refresh or accidental tab close can be resumed; the clock keeps running meanwhile.

## Question bank

The built-in bank (`questions.js`) has 84 **original** practice questions written in JEE Main style (28 per subject, MCQ + numerical). Each carries a year tag (2023–2026) only so the year filter can be demonstrated. They are **not** official NTA questions and did not appear in those papers. The app says so on the setup page, labels each one "Practice question (year tag …)" in the review and PDF, and prints a notice on the PDF cover. For real PYQs, import your own file.

### Official NTA questions

`pyq_bank.js` holds official questions from NTA's public question papers (JEE Main 2026 Session 2, all nine B.Tech shifts so far). It is the default bank when present. Each question is shown as NTA printed it (NTA's own images). Its answer comes from NTA's **final** answer key, matched by question ID, and it carries its source, for example `JEE Main 2026 (Session 2), 2 Apr Shift 1, Q.3 (Question ID 6911213)`. Questions NTA dropped are left out. Where the final key accepts more than one answer, any of them scores.

To add a paper, save the NTA PDFs under `sources/<year>/` (with `SOURCES.md`), then:

```
pip install pymupdf pillow
python tools/extract_nta_paper.py sources/2026/<paper>.pdf sources/2026/<final_key>.pdf pyq/2026/<shift> "JEE Main 2026 (Session 2), 2 Apr Shift 1" 2026
python tools/build_pyq_bank.py
```

Check each shift's `review.csv` for flags. Serve the folder over http (below) so the images appear in the PDF report.

### Hints and worked solutions in the review

Worked solutions for NTA questions are written by Claude and checked against NTA's final key (they are never presented as NTA's). Each has two hints, short steps, a "what this question tests" line and a "if this felt hard" suggestion; the format is in `tools/SOLUTION_STYLE.md`, the files are `pyq/<year>/<shift>/solutions.csv`.

In the answer review, a wrong or skipped question that has hints opens with the answer hidden. The student can have another go (practice only, the score never changes), open hint 1 and hint 2, ask for the solution, or skip it; skipping is fine and is recorded as a choice. Each step is saved with the attempt (`practice` table in `data/akil.db`): solved without a hint, after hint 1, after hint 2, looked at the solution, or skipped. Questions answered correctly keep their solution folded away.

The `jee-analysis` skill (`.claude/skills/jee-analysis/`) turns those records into a diagnosis: `tools/analysis_data.py` collects the counts, Claude writes the report and concept flags, `tools/save_analysis.py` stores them.

### How the sample answers were checked

`verify_answers.py` recomputes the 65 calculation-based answers independently (SymPy and plain arithmetic) and confirms each one matches the key stored in `questions.js`:

```
pip install sympy
python3 verify_answers.py
# 65 computed checks, 0 failed
# 65 answer keys cross-checked, 0 mismatched
```

The remaining 19 questions test facts or concepts (for example the shape of XeF₄ or the peroxide effect). They cannot be computed and were reviewed by hand against NCERT content. The script lists them so a subject teacher can review them too.

### Marking defaults

Defaults per subject are 20 MCQs + 5 numericals, +4 / −1 in both sections. Coaching-site summaries of recent NTA information bulletins describe this pattern. Check the official bulletin for the session you are preparing for, and change the marking on the setup page if it differs.

### CSV format

```
id,subject,chapter,year,type,question,option_a,option_b,option_c,option_d,answer,solution
P101,Physics,Kinematics,2025,MCQ,"A car accelerates ...",2 m/s^{2},4 m/s^{2},5 m/s^{2},10 m/s^{2},B,"a = 20/5"
C101,Chemistry,Atomic Structure,2026,NUM,"Angular nodes in a 4d orbital ____.",,,,,2,"l = 2"
```

- `type`: `MCQ` or `NUM` (also accepts `numerical`, `integer`).
- `answer`: `A`–`D` (or `1`–`4`) for MCQs; a number or a range such as `2.4-2.6` for numericals.
- `^{..}` gives superscript and `_{..}` subscript. Unicode symbols (², √, π, ⇌) work directly.
- An optional `source` column (for example `JEE Main 2025, 22 Jan Shift 1`) is printed with each question in the review and PDF. Without it, imported questions show as `JEE Main <year>`.
- An optional `image` column accepts a `data:` URI or an `https://` URL for figures.

A Google Sheet exported as CSV works. The **Download CSV template** button gives a starter file.

### JSON format

An array of objects with the same fields as `questions.js` (`options` as an array, `answer` as a 0-based index for MCQs).

## Running it

With accounts and saved progress (the normal way):

```
python server.py
```

then open http://localhost:8000 and sign in. The first time, make your own admin account:
`python tools/manage_users.py add-admin <username> "<your name>"` (you type the password; it is not shown).

**Accounts.** There is no public sign-up. The admin adds each student (Students page, or
`python tools/manage_users.py add <username> "<name>"`) and gives them a one-time password; at the first sign-in
they choose their own. A student sees only their own tests and progress; the admin sees everyone and can open any
student's progress, make a new one-time password, or switch an account off. Passwords are stored only as hashes.

**Online for friends:** see [DEPLOY.md](DEPLOY.md) (PythonAnywhere free account).

Without the server, `index.html` still works opened as a file (no accounts; results stay in that browser).
PDF generation loads `html2canvas` and `jsPDF` from cdnjs, so it needs an internet connection.

## Files

- `index.html`: the whole app (UI, exam engine, scoring, PDF report, Students page for admins)
- `server.py`: serves the app, accounts and sign-in, saves every test to SQLite (`data/akil.db`)
- `login.html`: sign-in and choose-your-password page
- `tools/manage_users.py`: accounts from the command line; `tools/make_deploy_bundle.py`: zips for PythonAnywhere
- `questions.js`: built-in sample bank and schema notes
- `verify_answers.py`: independent check of the sample answer keys
