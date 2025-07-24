REM activate_env.bat
REM ================================
@echo off
title Campus Analysis Pro - Development Environment
echo.
echo 🔧 Activating Campus Analysis Pro Development Environment...
echo.

if not exist campus_env (
    echo ❌ Virtual environment not found!
    echo 💡 Please run install.bat first
    pause
    exit /b 1
)

echo ✅ Activating virtual environment...
call campus_env\Scripts\activate

echo.
echo 🎯 CAMPUS ANALYSIS PRO DEVELOPMENT ENVIRONMENT
echo ================================================
echo.
echo 📋 Available commands:
echo   python campus_gui.py          - Run GUI application
echo   python main_select_campus.py  - Run console application
echo   python build_exe.py          - Build EXE file
echo   pip list                     - Show installed packages
echo   deactivate                   - Exit this environment
echo.
echo 💡 Type 'deactivate' to exit this environment
echo.

cmd /k