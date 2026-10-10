# Putting the JEE Mock CBT online (PythonAnywhere, free account)

Friends open a web address like `https://<your-username>.pythonanywhere.com`, sign in with the username and
one-time password you give them, and choose their own password. Each student sees only their own tests;
you (admin) see everyone on the **Students** page.

Facts checked on 2026-10-10 (PythonAnywhere help pages and staff forum answers):
- Free account: 512 MiB disk, 1 web app, 100 CPU-seconds a day for consoles and scheduled work.
- **The free web app stops after 1 month** unless you log in and extend it on the **Web** tab (there is a button
  to run it for another month). Put a monthly reminder in your calendar. Your data is kept while it is stopped.
- Uploads on the Files page are limited to 100 MB each, so the app comes in several zip parts of at most 80 MB.
- Git cloning the repository does not fit in 512 MB (the history alone is about 350 MB), so use the zips.

Not verified: exact button names on PythonAnywhere's pages may differ slightly from the ones below.

## 1. On this computer: make the zip parts

```
python tools/make_deploy_bundle.py --with-db
```

`--with-db` includes `data/akil.db` (Akil's saved tests). Leave it out to start online with no tests.
The parts appear in `dist/` (`jee_part1.zip`, `jee_part2.zip`, ...; about 270 MB in total).

## 2. On PythonAnywhere

1. Create a free **Beginner** account at pythonanywhere.com. Your username becomes the web address.
2. Upload and unzip **one part at a time** (the zips and the unzipped files together would not fit in 512 MB):
   - **Files** tab: upload `jee_part1.zip` into your home folder `/home/<your-username>/`.
   - Open a **Bash console** (Consoles tab) and run:
     ```
     cd ~ && unzip -o -q jee_part1.zip && rm jee_part1.zip && du -sh ~/mockjee
     ```
   - Repeat for `jee_part2.zip`, `jee_part3.zip`, ... (change the number each time).
3. **Web** tab: *Add a new web app* -> *Manual configuration* (not "Flask") -> the newest Python 3 offered.
4. On the web app's page, open the **WSGI configuration file** link, delete everything in it, and paste
   (replace `<your-username>`):
   ```python
   import os, sys
   os.environ['JEE_SECURE_COOKIE'] = '1'          # the login cookie is only sent over https
   path = '/home/<your-username>/mockjee'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.chdir(path)
   from server import app as application
   ```
   Save.
5. Still on the **Web** tab:
   - **Static files**: add URL `/pyq/` with directory `/home/<your-username>/mockjee/pyq/`. The question images are
     then served without using your CPU allowance. (They are NTA's public paper images, so it does not matter that
     they bypass the login.)
   - **Security**: switch on **Force HTTPS** if it is offered.
   - Press the green **Reload** button.
6. Back in the Bash console, make your own admin account (you type your password; it is not shown):
   ```
   cd ~/mockjee && python3 tools/manage_users.py add-admin <admin-username> "<Your name>"
   ```
7. Make Akil's account and, if you uploaded his tests, give them to him:
   ```
   python3 tools/manage_users.py add akil "Akil"
   python3 tools/manage_users.py assign-tests akil
   ```
   The first command prints Akil's one-time password.
8. Open `https://<your-username>.pythonanywhere.com`, sign in as admin, open **Students**, and add each friend
   (name + username). The page shows the address, username and one-time password to send them privately.

If something fails, the **Web** tab has an **Error log** link; the last lines say what went wrong.

## 3. Day to day

- **New friend**: Students page -> Add a student. **Forgotten password**: Students page -> New password.
  **Someone should stop using it**: Turn off (their tests are kept).
- **Each month**: Web tab -> extend the web app for another month.
- **Analysis on this computer** (the jee-analysis skill): make an export key once, put it in `.secrets` on both
  sides, then download the online database:
  - On PythonAnywhere (Bash console): `echo "JEE_EXPORT_KEY=<a long random string>" >> ~/mockjee/.secrets`, then Reload.
  - On this computer, in `.secrets`: `JEE_SERVER_URL=https://<your-username>.pythonanywhere.com` and the same `JEE_EXPORT_KEY=...`.
  - `python tools/pull_db.py` downloads it to `data/`; the analysis then runs with `--user <username>`.
- **Updating the app later**: make the bundle again and upload only part 1 (it holds the app files and, with `--with-db`,
  the database: leave `--with-db` out so the online tests are not overwritten), unzip it, then Reload.

## Privacy

- Passwords are stored only as salted hashes; nobody, including you, can read them. A reset gives a new one-time password.
- The app keeps names, usernames and test answers. Friends are minors: ask their parents before you add them,
  and turn accounts off when they stop using it. (Deleting an account and its tests is not built in yet; ask Claude if a parent asks for it.)
- `/api/export` (the whole database) only works with the export key; keep `.secrets` private.
