"""
Facts for the jee-analysis skill: reads Akil's attempt database and the question bank and prints
one JSON document with everything the analysis needs, already counted. Read-only.

Usage:  python tools/analysis_data.py --user akil [--db data/akil.db] [--attempts ID,ID] [--since 2026-10-01] [--out facts.json]
        (--user picks the student; databases from before accounts existed have one student and need no --user)

What it contains
  attempts     one row per test (score, counts, time, date)
  chapters     per subject + chapter, over the chosen attempts: attempted, correct, wrong, skipped,
               accuracy, marks lost to negatives, average seconds per attempted question,
               Akil's own reasons for wrong answers, and the review outcomes (hint ladder)
  questions    every wrong or skipped question with what happened: his answer, time, answer changes,
               his reason, the review outcome (solved without a hint / after hint 1 / after hint 2 /
               looked at the solution / skipped), current chapter tag, and Claude's concept line
  slow_correct correct answers that took much longer than his own median (shaky areas)
  fast_wrong   wrong answers given quickly (likely guesses)
  open_flags   flags written by earlier analyses, to update instead of duplicating
"""
import argparse, json, os, sqlite3, statistics, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTCOMES = ['solved_no_hint', 'solved_hint1', 'solved_hint2', 'saw_solution', 'skipped', 'open']


def load_bank():
    s = open(os.path.join(ROOT, 'pyq_bank.js'), encoding='utf-8').read()
    bank = json.loads(s[s.index('['):s.rindex(']') + 1])
    return {q['id']: q for q in bank}


def user_id(con, username):
    """users.id for a username; None for databases made before accounts existed (one student only)."""
    if not con.execute("SELECT 1 FROM sqlite_master WHERE name = 'users'").fetchone():
        if username:
            sys.exit('This database has no accounts yet; leave out --user.')
        return None
    if not username:
        names = [r[0] for r in con.execute("SELECT username FROM users WHERE role = 'student' ORDER BY username")]
        sys.exit('Say whose tests to use with --user <username>. Students: ' + (', '.join(names) or 'none yet'))
    row = con.execute('SELECT id FROM users WHERE username = ?', (username.lower(),)).fetchone()
    if not row:
        sys.exit(f'No user "{username}".')
    return row[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', default=os.environ.get('JEE_DB_PATH', os.path.join(ROOT, 'data', 'akil.db')))
    ap.add_argument('--user', help='username of the student to analyse')
    ap.add_argument('--attempts', help='comma-separated attempt ids (default: all)')
    ap.add_argument('--since', help='only attempts submitted on or after this date (YYYY-MM-DD)')
    ap.add_argument('--out', help='write to this file instead of stdout')
    a = ap.parse_args()
    if not os.path.exists(a.db):
        sys.exit(f'No database at {a.db}. Run tools/pull_db.py for the online copy, or take a test first.')
    con = sqlite3.connect(a.db); con.row_factory = sqlite3.Row
    bank = load_bank()

    uid = user_id(con, a.user)
    where, args = ([], []) if uid is None else (['user_id = ?'], [uid])
    if a.attempts:
        ids = a.attempts.split(','); where.append(f"id IN ({','.join('?' * len(ids))})"); args += ids
    if a.since:
        where.append('submitted_at >= ?'); args.append(a.since)
    attempts = [dict(r) for r in con.execute(
        'SELECT id, student, test_name, submitted_at, duration_min, time_used_s, score, max_score, n_questions, '
        'n_correct, n_wrong, n_skipped FROM attempts' + (' WHERE ' + ' AND '.join(where) if where else '') +
        ' ORDER BY submitted_at', args)]
    ids = [x['id'] for x in attempts]
    if not ids:
        sys.exit('No attempts match.')
    ph = ','.join('?' * len(ids))
    resp = [dict(r) for r in con.execute(f'SELECT * FROM responses WHERE attempt_id IN ({ph}) ORDER BY attempt_id, q_index', ids)]
    has_practice = con.execute("SELECT 1 FROM sqlite_master WHERE name = 'practice'").fetchone()
    prac = {(r['attempt_id'], r['q_index']): dict(r) for r in con.execute(f'SELECT * FROM practice WHERE attempt_id IN ({ph})', ids)} if has_practice else {}
    flags = [dict(r) for r in con.execute("SELECT * FROM flags WHERE status != 'resolved'" + ('' if uid is None else ' AND user_id = ?'),
                                          () if uid is None else (uid,))]
    when = {x['id']: x['submitted_at'] for x in attempts}

    times = [r['time_ms'] / 1000 for r in resp if r['attempted'] and r['time_ms']]
    med = statistics.median(times) if times else 0
    chap = defaultdict(lambda: dict(n=0, attempted=0, correct=0, wrong=0, skipped=0, neg_marks=0.0, secs=[],
                                    reasons=Counter(), review=Counter()))
    questions, slow, fast = [], [], []
    for r in resp:
        q = bank.get(r['question_id'], {})
        subj, ch = q.get('subject', r['subject']), q.get('chapter', r['chapter'])   # current tag wins
        c = chap[(subj, ch)]
        c['n'] += 1
        secs = round((r['time_ms'] or 0) / 1000)
        if r['attempted']:
            c['attempted'] += 1; c['secs'].append(secs)
            if r['correct']:
                c['correct'] += 1
                if med and secs > 2 * med and secs > 120:
                    slow.append(dict(attempt=r['attempt_id'], q=r['q_index'] + 1, question_id=r['question_id'], subject=subj, chapter=ch, secs=secs))
            else:
                c['wrong'] += 1; c['neg_marks'] += -(r['marks'] or 0)
                if r['reason']: c['reasons'][r['reason']] += 1
                if secs < 30:
                    fast.append(dict(attempt=r['attempt_id'], q=r['q_index'] + 1, question_id=r['question_id'], subject=subj, chapter=ch, secs=secs))
        else:
            c['skipped'] += 1
        p = prac.get((r['attempt_id'], r['q_index']))
        if p: c['review'][p['outcome']] += 1
        if not r['correct']:
            questions.append({k: v for k, v in dict(
                attempt=r['attempt_id'], date=(when[r['attempt_id']] or '')[:10], q=r['q_index'] + 1,
                question_id=r['question_id'], source=r['source'], subject=subj, chapter=ch, subtopic=q.get('subtopic'),
                type=r['qtype'], in_test='wrong' if r['attempted'] else 'skipped',
                his_answer=(int(r['given']) + 1 if r['qtype'] == 'MCQ' and r['given'] is not None else r['given']),
                key=(q.get('answer') + 1 if q.get('type') == 'MCQ' and q.get('answer') is not None else q.get('answer')),
                secs=secs, answer_changes=r['answer_changes'], visits=r['visits'], his_reason=r['reason'],
                review_outcome=p['outcome'] if p else None, review_hints=p['hints_used'] if p else None,
                review_wrong_tries=p['wrong_tries'] if p else None, review_secs=round(p['practice_ms'] / 1000) if p else None,
                skipped_then_reopened=bool(p) and '"skip"' in p['events'] and '"reopen"' in p['events'],
                concept=q.get('concept'), option_traps=q.get('option_traps'), mistake_type=q.get('mistake_type'),
            ).items() if v not in (None, '', [], {})})

    chapters = []
    for (subj, ch), c in sorted(chap.items()):
        chapters.append(dict(subject=subj, chapter=ch, questions=c['n'], attempted=c['attempted'], correct=c['correct'],
                             wrong=c['wrong'], skipped=c['skipped'],
                             accuracy=round(c['correct'] / c['attempted'], 2) if c['attempted'] else None,
                             neg_marks=c['neg_marks'], avg_secs=round(statistics.mean(c['secs'])) if c['secs'] else None,
                             his_reasons=dict(c['reasons']), review={k: c['review'][k] for k in OUTCOMES if c['review'][k]}))
    out = open(a.out, 'w', encoding='utf-8') if a.out else sys.stdout
    if not a.out: sys.stdout.reconfigure(encoding='utf-8')
    json.dump(dict(db=a.db, median_secs_per_attempted=round(med), attempts=attempts, chapters=chapters,
                   questions=questions, slow_correct=slow, fast_wrong=fast, open_flags=flags),
              out, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
