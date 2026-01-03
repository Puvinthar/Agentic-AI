@echo off
REM Production startup script for Agentic AI (Windows)

setlocal enabledelayedexpansion

REM Set environment variables
set ENVIRONMENT=production
set BACKEND_URL=%BACKEND_URL:http://localhost:8000%
set FLASK_ENV=production
set FLASK_DEBUG=0

echo.
echo ============================================================
echo 🚀 Starting Agentic AI Frontend (Production)
echo ============================================================
echo 📡 Backend URL: !BACKEND_URL!
echo 🌐 Listening on 0.0.0.0:5000
echo ============================================================
echo.

REM Run with Gunicorn
C:\Python313\python.exe -m gunicorn -w 4 -b 0.0.0.0:5000 --timeout 60 --access-logfile - server:app

pause
