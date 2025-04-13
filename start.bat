@echo off
echo Starting Medical Chatbot System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages
    pause
    exit /b 1
)

REM Start MongoDB if not running
echo Checking MongoDB...
net start | findstr "MongoDB" >nul
if %errorlevel% neq 0 (
    echo MongoDB is not running. Starting MongoDB...
    net start MongoDB
    if %errorlevel% neq 0 (
        echo Failed to start MongoDB
        echo Please make sure MongoDB is installed and configured
        pause
        exit /b 1
    )
)

REM Start Ollama if not running
echo Checking Ollama...
netstat -ano | findstr ":11434" >nul
if %errorlevel% neq 0 (
    echo Ollama is not running. Starting Ollama...
    start /B ollama serve
    timeout /t 5
)

REM Start FastAPI backend
echo Starting FastAPI backend...
start "Medical Chatbot Backend" cmd /c "python main.py"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5

REM Start Flask frontend
echo Starting Flask frontend...
start "Medical Chatbot Frontend" cmd /c "python frontend.py"

REM Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 5

echo.
echo Medical Chatbot System is running!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5000
echo.
echo Press any key to stop all services...
pause >nul

REM Stop all services
echo Stopping services...
taskkill /F /FI "WINDOWTITLE eq Medical Chatbot Backend" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Medical Chatbot Frontend" >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1

echo All services stopped.
pause 