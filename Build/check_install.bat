REM check_install.bat
REM ================================
@echo off
title Campus Analysis Pro - Installation Check
echo.
echo 🔍 Checking Campus Analysis Pro Installation...
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    goto :error
) else (
    for /f "tokens=2" %%i in ('python --version 2^>nul') do echo ✅ Python %%i
)

REM Check virtual environment
echo.
echo [2/5] Checking virtual environment...
if exist campus_env (
    echo ✅ Virtual environment exists
) else (
    echo ❌ Virtual environment not found
    goto :error
)

REM Check core files
echo.
echo [3/5] Checking core files...
set "missing_files="
if not exist campus_gui.py set "missing_files=%missing_files% campus_gui.py"
if not exist main_select_campus.py set "missing_files=%missing_files% main_select_campus.py"
if not exist 01_load_data_selection.py set "missing_files=%missing_files% 01_load_data_selection.py"
if not exist requirements.txt set "missing_files=%missing_files% requirements.txt"

if defined missing_files (
    echo ❌ Missing files:%missing_files%
    goto :error
) else (
    echo ✅ All core files present
)

REM Check data files
echo.
echo [4/5] Checking sample data...
if exist Input\Campuses_with_latlon.xlsx (
    echo ✅ Campus data exists
) else (
    echo ⚠️  Campus data not found in Input/
)

if exist Input\Students_with_latlon.xlsx (
    echo ✅ Student data exists  
) else (
    echo ⚠️  Student data not found in Input/
)

if exist Input\Public_Schools_with_latlon.xlsx (
    echo ✅ School data exists
) else (
    echo ⚠️  School data not found in Input/
)

REM Check packages
echo.
echo [5/5] Checking Python packages...
call campus_env\Scripts\activate
python -c "import PyQt5; print('✅ PyQt5')" 2>nul || echo ❌ PyQt5 missing
python -c "import pandas; print('✅ Pandas')" 2>nul || echo ❌ Pandas missing  
python -c "import folium; print('✅ Folium')" 2>nul || echo ❌ Folium missing

echo.
echo ================================================
echo 🎉 Installation check completed!
echo.
echo 💡 If you see any ❌ errors above, run install.bat again
echo 💡 If you see ⚠️  warnings, copy your Excel files to Input/
echo.
goto :end

:error
echo.
echo ================================================
echo ❌ Installation issues detected!
echo.
echo 💡 Solutions:
echo   1. Run install.bat to setup everything
echo   2. Make sure you're in the correct directory
echo   3. Check if all files were extracted properly
echo.

:end
pause