REM run_gui.bat
REM ================================
@echo off
title Campus Analysis Pro - GUI Mode
echo.
echo 🚀 Starting Campus Analysis Pro GUI...
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

if not exist campus_gui.py (
    echo ❌ campus_gui.py not found!
    echo 💡 Please check if you're in the correct directory
    pause
    exit /b 1
)

echo ✅ Launching GUI application...
python campus_gui.py
echo.
echo 👋 GUI application closed
pause