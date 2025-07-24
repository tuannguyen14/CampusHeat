REM build_exe.bat
REM ================================
@echo off
title Campus Analysis Pro - Build EXE
echo.
echo 🔨 Building EXE for Campus Analysis Pro...
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

if not exist build_exe.py (
    echo ❌ build_exe.py not found!
    echo 💡 Please check if you're in the correct directory
    pause
    exit /b 1
)

echo ✅ Starting EXE build process...
echo 💡 This may take 5-10 minutes...
python build_exe.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 EXE build completed successfully!
    echo 📁 Check dist/ folder for CampusAnalysisPro.exe
    echo.
    if exist dist\CampusAnalysisPro.exe (
        set /p choice="Do you want to test the EXE? (y/n): "
        if /i "%choice%"=="y" (
            echo 🧪 Testing EXE...
            cd dist
            CampusAnalysisPro.exe
            cd ..
        )
    )
) else (
    echo ❌ EXE build failed!
    echo 💡 Check the error messages above
)

pause