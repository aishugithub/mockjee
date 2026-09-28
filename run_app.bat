@echo off
rem Double-click to start the JEE mock app with the progress database.
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 >nul & start http://localhost:8000"
python server.py
pause
