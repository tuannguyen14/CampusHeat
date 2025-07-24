REM run_console.bat  
REM ================================
@echo off
title Campus Analysis Pro - Console Mode
echo.
echo 🚀 Starting Campus Analysis Pro Console...
echo.

if not exist campus_env (
    echo ❌ Virtual environment not found!
    echo 💡 Please run install.bat first
    pause
    exit /b 1
)

call campus_env\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

if not exist main_select_campus.py (
    echo ❌ main_select_campus.py not found!
    echo 💡 Please check if you're in the correct directory
    pause
    exit /b 1
)

echo ✅ Launching console application...
python main_select_campus.py
echo.
echo 👋 Console application finished
pause