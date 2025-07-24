@echo off
chcp 65001 >nul
color 0A

echo.
echo ████████╗   ████████╗   ████████╗   ██████╗
echo ██╔════██║  ██╔═══██║   ██╔═══██║   ██╔══██╗
echo ██║    ██║  ██████╔═╝   ██║   ██║   ██████╔╝
echo ██║    ██║  ██╔═══██╗   ██║   ██║   ██╔══██╗
echo ╚████████║  ██║   ██║   ╚████████║  ██║  ██║
echo  ╚═══════╝  ╚═╝   ╚═╝    ╚═══════╝  ╚═╝  ╚═╝
echo.
echo ██████╗  █████╗ ██████╗███████╗
echo ██╔══██╗██╔══██╗██╔═══█████╔══╝
echo ██████╔╝███████║██║   ████████╗
echo ██╔═══╝ ██╔══██║██║   ████╔══╝
echo ██║     ██║  ██║╚██████╔███████╗
echo ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝
echo.
echo =====================================================
echo   CAMPUS ANALYSIS PRO - ONE-CLICK INSTALLER
echo   Hệ thống phân tích vùng phủ đa campus
echo   Version 1.0 - Build %date%
echo =====================================================
echo.

REM Check if Python is installed
echo [1/6] 🔍 Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt!
    echo 💡 Vui lòng tải và cài Python từ: https://python.org
    echo    ✅ Nhớ check "Add Python to PATH"
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>nul') do echo ✅ Python %%i đã được cài đặt
)

REM Check if pip is available
echo.
echo [2/6] 🔍 Kiểm tra pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip không khả dụng!
    echo 💡 Cài đặt pip: python -m ensurepip --upgrade
    pause
    exit /b 1
) else (
    echo ✅ pip đã sẵn sàng
)

REM Create virtual environment
echo.
echo [3/6] 🛠️ Tạo virtual environment...
if exist "campus_env" (
    echo ✅ Virtual environment đã tồn tại
) else (
    python -m venv campus_env
    if %errorlevel% neq 0 (
        echo ❌ Không thể tạo virtual environment!
        pause
        exit /b 1
    ) else (
        echo ✅ Đã tạo virtual environment
    )
)

REM Activate virtual environment
echo.
echo [4/6] 🔧 Kích hoạt virtual environment...
call campus_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Không thể kích hoạt virtual environment!
    pause
    exit /b 1
) else (
    echo ✅ Virtual environment đã được kích hoạt
)

REM Install requirements
echo.
echo [5/6] 📦 Cài đặt dependencies...
echo 💡 Đang tải và cài đặt các package cần thiết...
pip install --upgrade pip
pip install PyQt5==5.15.7
pip install pandas==1.5.3
pip install numpy==1.24.3
pip install openpyxl==3.1.2
pip install xlsxwriter==3.1.2
pip install folium==0.14.0
pip install shapely==2.0.1
pip install geopy==2.3.0
pip install pyinstaller==5.13.0

if %errorlevel% neq 0 (
    echo ❌ Lỗi khi cài đặt dependencies!
    echo 💡 Thử chạy lại script với quyền Administrator
    pause
    exit /b 1
) else (
    echo ✅ Đã cài đặt tất cả dependencies
)

REM Test installation
echo.
echo [6/6] 🧪 Kiểm tra cài đặt...
python -c "import PyQt5; print('✅ PyQt5 OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ PyQt5 chưa được cài đặt đúng
    pause
    exit /b 1
)

python -c "import pandas; print('✅ Pandas OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Pandas chưa được cài đặt đúng
    pause
    exit /b 1
)

python -c "import folium; print('✅ Folium OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Folium chưa được cài đặt đúng
    pause
    exit /b 1
)

echo ✅ Tất cả dependencies đã OK!

REM Create folders
echo.
echo 📁 Tạo thư mục cần thiết...
if not exist "Input" mkdir Input
if not exist "Output" mkdir Output
echo ✅ Đã tạo thư mục Input và Output

echo.
echo =====================================================
echo 🎉 CÀI ĐẶT HOÀN TẤT THÀNH CÔNG!
echo =====================================================
echo.
echo 📋 CÁC BƯỚC TIẾP THEO:
echo.
echo 1️⃣ Đặt file Excel vào thư mục Input/:
echo    • Campuses_with_latlon.xlsx
echo    • Students_with_latlon.xlsx  
echo    • Public_Schools_with_latlon.xlsx
echo.
echo 2️⃣ Chạy ứng dụng:
echo    • Mode GUI:     python campus_gui.py
echo    • Mode Console: python main_select_campus.py
echo.
echo 3️⃣ Build EXE (tùy chọn):
echo    • python build_exe.py
echo.
echo 💡 TẬP TIN ĐÍNH KÈM:
echo    • README.txt     - Hướng dẫn chi tiết
echo    • config.json    - Cấu hình mẫu
echo.
echo ⚠️  LƯU Ý:
echo    • Kích hoạt virtual env: campus_env\Scripts\activate
echo    • Thoát virtual env: deactivate
echo.
echo ✅ SẴN SÀNG SỬ DỤNG CAMPUS ANALYSIS PRO!
echo.
pause