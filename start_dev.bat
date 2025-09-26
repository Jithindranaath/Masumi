@echo off
echo Starting AI Budget Planner Development Environment...
echo.

echo Starting Backend Server...
start "Backend" cmd /k "python main.py api"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
cd frontend
start "Frontend" cmd /k "npm run dev"

echo.
echo Development servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
pause