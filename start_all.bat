@echo off
echo =======================================================
echo Starting MediZentrum Hospital Management System
echo =======================================================
echo.

:: [1] Start Redis via Docker
echo [1/6] Starting Redis via Docker...
start cmd /k "title Redis Server && docker run --rm -p 6379:6379 redis"

:: [2] Start Flask Backend
echo [2/6] Starting Flask Backend (API Server on port 5000)...
start cmd /k "title Flask API && cd /d %~dp0Backend && call venv\Scripts\activate.bat && python app.py"

:: [3] Start Celery Worker
echo [3/6] Starting Celery Worker (handles async jobs)...
start cmd /k "title Celery Worker && cd /d %~dp0Backend && call venv\Scripts\activate.bat && python run_celery.py"

:: [4] Start Celery Beat
echo [4/6] Starting Celery Beat (scheduled jobs - daily reminders, monthly reports)...
start cmd /k "title Celery Beat && cd /d %~dp0Backend && call venv\Scripts\activate.bat && celery -A celery_config.celery_app beat --loglevel=info"

:: [5] Start Vue Frontend
echo [5/6] Starting Vue Frontend (on port 5173)...
start cmd /k "title Vue Frontend && cd /d %~dp0Frontend && npm run dev"

:: [6] Wait for Flask to be ready, then run Daily Reminder Test
echo [6/6] Waiting 8 seconds for Flask to start, then triggering Daily Reminder...
timeout /t 8 /nobreak > nul
start cmd /k "title Daily Reminder Test && cd /d %~dp0Backend && call venv\Scripts\activate.bat && python test_celery_jobs.py && echo. && echo Done! Check your Google Chat Space! && pause"

echo.
echo =======================================================
echo All services launched! Here is what is running:
echo   [1] Redis      - Message broker for Celery jobs
echo   [2] Flask API  - Backend REST API on http://localhost:5000
echo   [3] Celery Worker - Executes background jobs (CSV export alert)
echo   [4] Celery Beat   - Sends daily reminders and monthly reports on schedule
echo   [5] Vue Frontend  - Patient/Doctor UI on http://localhost:5173
echo   [6] Job Test   - Fires today's appointment reminders to Google Chat
echo =======================================================
pause
