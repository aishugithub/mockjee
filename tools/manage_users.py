"""
Accounts for the JEE Mock CBT server (run it on the computer or PythonAnywhere console where the database lives).

  python tools/manage_users.py add-admin <username> "<name>"    first admin: you type the password (not shown)
  python tools/manage_users.py add <username> "<name>"          a student; prints a one-time password to give them
  python tools/manage_users.py reset <username>                 new one-time password (they choose their own at login)
  python tools/manage_users.py off <username> | on <username>   switch an account off / on (their tests are kept)
  python tools/manage_users.py list
  python tools/manage_users.py assign-tests <username>          give every test saved before accounts existed to this user

Option --db PATH (default: JEE_DB_PATH or data/akil.db). Passwords are stored only as hashes.
Students can also be added and reset from the app's Students page (admins only).
"""
import argparse, getpass, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--db')
    ap.add_argument('cmd', choices=['add-admin', 'add', 'reset', 'off', 'on', 'list', 'assign-tests'])
    ap.add_argument('username', nargs='?')
    ap.add_argument('name', nargs='?')
    a = ap.parse_args()
    if a.db:
        os.environ['JEE_DB_PATH'] = a.db
    sys.path.insert(0, ROOT)
    import server   # creates the tables (and the session key in .secrets) if they don't exist yet
    from werkzeug.security import generate_password_hash

    if a.cmd != 'list' and not a.username:
        ap.error('give a username')
    with server.db() as con:
        if a.cmd == 'list':
            for u in con.execute('SELECT u.username, u.name, u.role, u.active, u.must_change, u.last_login, '
                                 '(SELECT COUNT(*) FROM attempts WHERE user_id = u.id) AS tests FROM users u ORDER BY role DESC, name'):
                state = 'off' if not u['active'] else 'one-time password' if u['must_change'] else 'ok'
                print(f"{u['username']:<20} {u['name']:<24} {u['role']:<8} {state:<18} tests {u['tests']:<4} last login {u['last_login'] or '-'}")
            n = con.execute('SELECT COUNT(*) FROM attempts WHERE user_id IS NULL').fetchone()[0]
            if n:
                print(f'\n{n} test(s) saved before accounts existed belong to nobody yet: use assign-tests <username>.')
            return

        if a.cmd in ('add-admin', 'add'):
            if not a.name:
                ap.error('give the person\'s name in quotes, e.g. "Akil"')
            if a.cmd == 'add-admin':
                pw = getpass.getpass('Choose a password for this admin (at least 8 characters): ')
                if pw != getpass.getpass('Type it again: '):
                    sys.exit('The two passwords differ; nothing was saved.')
                try:
                    server.create_user(con, a.username, a.name, pw, role='admin')
                    con.execute('UPDATE users SET must_change = 0 WHERE username = ?', (a.username.lower(),))
                except ValueError as e:
                    sys.exit(str(e))
                print(f'Admin "{a.username.lower()}" created. Sign in at the app\'s /login page.')
            else:
                try:
                    otp = server.create_user(con, a.username, a.name)
                except ValueError as e:
                    sys.exit(str(e))
                print(f'Student "{a.username.lower()}" created. One-time password: {otp}\n'
                      'Give it to them privately; they choose their own password at the first login.')
            return

        u = con.execute('SELECT id, username FROM users WHERE username = ?', (a.username.lower(),)).fetchone()
        if not u:
            sys.exit(f'No user "{a.username}".')
        if a.cmd == 'reset':
            otp = server.one_time_password()
            con.execute('UPDATE users SET pw_hash = ?, must_change = 1 WHERE id = ?', (generate_password_hash(otp), u['id']))
            print(f'New one-time password for "{u["username"]}": {otp}  (they choose their own at the next login)')
        elif a.cmd in ('off', 'on'):
            con.execute('UPDATE users SET active = ? WHERE id = ?', (int(a.cmd == 'on'), u['id']))
            print(f'"{u["username"]}" is now {"on" if a.cmd == "on" else "off (cannot sign in; tests kept)"}.')
        elif a.cmd == 'assign-tests':
            n = con.execute('UPDATE attempts SET user_id = ? WHERE user_id IS NULL', (u['id'],)).rowcount
            f = con.execute('UPDATE flags SET user_id = ? WHERE user_id IS NULL', (u['id'],)).rowcount
            s = con.execute('UPDATE analyses SET user_id = ? WHERE user_id IS NULL', (u['id'],)).rowcount
            print(f'Gave "{u["username"]}" {n} test(s), {f} concept flag(s) and {s} analysis report(s).')


if __name__ == '__main__':
    main()
