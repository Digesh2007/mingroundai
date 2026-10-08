@echo off
title MindGuard AI - Flask Server
color 0A

cd /d "C:\Users\digesh kg\OneDrive\Desktop\myworkings\mindground"

echo.
echo  ==========================================
echo    MindGuard AI - Starting Flask Server
echo  ==========================================
echo.

set VENV_PYTHON=mindguard-ai\venv\Scripts\python.exe

echo [1/3] Checking virtual environment...
if not exist "%VENV_PYTHON%" (
    echo Creating virtual environment...
    python -m venv mindguard-ai\venv
)
echo Done.

echo [2/3] Installing dependencies...
"%VENV_PYTHON%" -m pip install flask google-generativeai python-dotenv --quiet --disable-pip-version-check
echo Done.

echo [3/3] Starting Flask server...
echo.
echo  ------------------------------------------
echo   Open in browser: http://127.0.0.1:5000
echo   Keep this window OPEN while using the app
echo   Press Ctrl+C to stop the server
echo  ------------------------------------------
echo.

"%VENV_PYTHON%" app.py

echo.
echo Server stopped. Press any key to close.
pause
