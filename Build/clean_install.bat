REM clean_install.bat
REM ================================
@echo off
title Campus Analysis Pro - Clean Install
echo.
echo 🧹 Campus Analysis Pro - Clean Installation...
echo.

echo ⚠️  WARNING: This will delete the existing virtual environment
echo    and reinstall everything from scratch.
echo.
set /p confirm="Are you sure? (y/n): "
if /i not "%confirm%"=="y" (
    echo ❌ Installation cancelled
    pause
    exit /b 0
)

echo.
echo 🗑️  Cleaning up existing installation...

REM Remove virtual environment
if exist campus_env (
    echo Removing virtual environment...
    rmdir /s /q campus_env
    echo ✅ Removed campus_env/
)

REM Remove build artifacts
if exist dist (
    echo Removing dist folder...
    rmdir /s /q dist
    echo ✅ Removed dist/
)

if exist build (
    echo Removing build folder...
    rmdir /s /q build
    echo ✅ Removed build/
)

REM Remove spec file
if exist campus_analysis.spec (
    del campus_analysis.spec
    echo ✅ Removed campus_analysis.spec
)

REM Remove compiled Python files
for /r %%i in (*.pyc) do del "%%i" 2>nul
for /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul
echo ✅ Removed Python cache files

echo.
echo 🔧 Starting fresh installation...
call install.bat

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Clean installation completed successfully!
) else (
    echo ❌ Clean installation failed
)

pause