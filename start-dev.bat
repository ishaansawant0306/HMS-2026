@echo off
rem Start backend and frontend servers from the repo root.
cd /d "%~dp0Backend"
start "Backend" cmd /k "cd /d "%~dp0Backend" && python app.py"
start "Frontend" cmd /k "cd /d "%~dp0Frontend" && npm install && npm run dev"

ntimeout /t 3 /nobreak > nul
nstart "" "http://localhost:3000"