@echo off
echo =======================================================
echo Starting MediZentrum Hospital Management System
echo =======================================================
echo.

:: Start Redis (Requires Docker running on Windows)
echo [1/5] Starting Redis via Docker...
start cmd /k "title Redis Server && docker run --rm -p 6379:6379 redis"

:: Start Backend Server
echo [2/5] Starting Flask Backend Database API...
start cmd /k "title Flask API && cd /d %~dp0Backend && call venv\Scripts\activate.bat && python app.py"

:: Start Celery Worker
echo [3/5] Starting Celery Worker (Asynchronous Jobs)...
start cmd /k "title Celery Worker && cd /d %~dp0Backend && call venv\Scripts\activate.bat && python run_celery.py"

:: Start Celery Beat
echo [4/5] Starting Celery Beat (Scheduled Jobs - Daily Reminders)...
start cmd /k "title Celery Beat && cd /d %~dp0Backend && call venv\Scripts\activate.bat && celery -A celery_config.celery_app beat --loglevel=info"

:: Start Frontend Server
echo [5/5] Starting Vue Frontend UI...
start cmd /k "title Vue Frontend && cd /d %~dp0Frontend && npm run dev"

echo.
echo All processes have been launched in separate terminal windows!
echo If your Redis crashes, ensure Docker Desktop is running and active.
pause
