REM update_packages.bat
REM ================================
@echo off
title Campus Analysis Pro - Update Packages
echo.
echo 🔄 Updating Campus Analysis Pro packages...
echo.

if not exist campus_env (
    echo ❌ Virtual environment not found!
    echo 💡 Please run install.bat first
    pause
    exit /b 1
)

call campus_env\Scripts\activate

echo 📦 Updating pip...
python -m pip install --upgrade pip

echo.
echo 📦 Updating core packages...
pip install --upgrade PyQt5 pandas numpy openpyxl xlsxwriter folium shapely geopy

echo.
echo 📦 Installing optional packages...
pip install --upgrade matplotlib seaborn plotly

echo.
echo ✅ Package update completed!
echo.
echo 📋 Current package versions:
pip list | findstr "PyQt5\|pandas\|numpy\|folium"

pause