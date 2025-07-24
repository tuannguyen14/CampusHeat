#!/usr/bin/env python3
"""
Script để build file EXE cho Campus Analysis GUI
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Kiểm tra các package cần thiết"""
    print("🔍 Kiểm tra requirements...")
    
    required_packages = [
        "PyQt5", "pandas", "numpy", "openpyxl", 
        "xlsxwriter", "folium", "shapely", "geopy", "pyinstaller"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Thiếu packages: {', '.join(missing_packages)}")
        print("Chạy: pip install -r requirements.txt")
        return False
    
    return True

def create_spec_file():
    """Tạo file .spec cho PyInstaller"""
    print("\n📝 Tạo file .spec...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['campus_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('01_load_data_selection.py', '.'),
        ('02_compute_coverage.py', '.'),
        ('03_overlap_matrix.py', '.'),
        ('04_tam_analysis.py', '.'),
        ('05_generate_map.py', '.'),
        ('06_export_excel.py', '.'),
        ('campus_icon.png', '.'),
    ],
    hiddenimports=[
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.missing',
        'folium.plugins',
        'shapely.geometry',
        'geopy.distance',
        'xlsxwriter.workbook',
        'openpyxl.chart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CampusAnalysisPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='campus_icon.ico'
)
'''
    
    with open('campus_analysis.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("  ✅ Đã tạo campus_analysis.spec")

def create_icon():
    """Tạo icon mặc định nếu không có"""
    icon_path = Path("campus_icon.png")
    ico_path = Path("campus_icon.ico")
    
    if not icon_path.exists():
        print("\n🎨 Tạo icon mặc định...")
        # Tạo icon đơn giản bằng PIL nếu có
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Tạo image 64x64
            img = Image.new('RGBA', (64, 64), (52, 152, 219, 255))
            draw = ImageDraw.Draw(img)
            
            # Vẽ biểu tượng campus đơn giản
            draw.rectangle([10, 20, 54, 50], fill=(255, 255, 255, 255))
            draw.rectangle([20, 25, 25, 35], fill=(52, 152, 219, 255))
            draw.rectangle([30, 25, 35, 35], fill=(52, 152, 219, 255))
            draw.rectangle([40, 25, 45, 35], fill=(52, 152, 219, 255))
            draw.rectangle([25, 40, 40, 45], fill=(52, 152, 219, 255))
            
            img.save("campus_icon.png")
            print("  ✅ Đã tạo campus_icon.png")
            
            # Convert to ICO
            img.save("campus_icon.ico", format='ICO')
            print("  ✅ Đã tạo campus_icon.ico")
            
        except ImportError:
            # Tạo file placeholder
            with open("campus_icon.png", "w") as f:
                f.write("")
            with open("campus_icon.ico", "w") as f:
                f.write("")
            print("  ⚠️  Tạo placeholder icon (cần PIL để tạo icon thật)")

def build_exe():
    """Build file EXE"""
    print("\n🔨 Bắt đầu build EXE...")
    
    # Tạo thư mục dist nếu cần
    os.makedirs("dist", exist_ok=True)
    
    # Chạy PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm", 
        "campus_analysis.spec"
    ]
    
    print(f"Chạy: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build thành công!")
            
            # Kiểm tra file exe
            exe_path = Path("dist/CampusAnalysisPro.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 File EXE: {exe_path} ({size_mb:.1f} MB)")
                return True
            else:
                print("❌ Không tìm thấy file EXE sau khi build")
                return False
        else:
            print("❌ Build thất bại!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi build: {e}")
        return False

def copy_required_files():
    """Copy các file cần thiết vào thư mục dist"""
    print("\n📂 Copy files cần thiết...")
    
    dist_path = Path("dist")
    
    # Tạo thư mục Input trong dist
    input_dir = dist_path / "Input"
    input_dir.mkdir(exist_ok=True)
    
    # Copy sample data files (nếu có)
    sample_files = [
        "Campuses_with_latlon.xlsx",
        "Students_with_latlon.xlsx", 
        "Public_Schools_with_latlon.xlsx"
    ]
    
    source_input = Path("Input")
    if source_input.exists():
        for file in sample_files:
            src = source_input / file
            dst = input_dir / file
            if src.exists():
                import shutil
                shutil.copy2(src, dst)
                print(f"  ✅ {file}")
            else:
                print(f"  ⚠️  {file} - không tìm thấy")
    
    # Tạo thư mục Output
    output_dir = dist_path / "Output"
    output_dir.mkdir(exist_ok=True)
    print(f"  ✅ Tạo thư mục Output")
    
    # Copy README
    readme_content = """
# Campus Analysis Pro

## Hướng dẫn sử dụng:

1. Đặt các file Excel vào thư mục Input/:
   - Campuses_with_latlon.xlsx
   - Students_with_latlon.xlsx  
   - Public_Schools_with_latlon.xlsx

2. Chạy CampusAnalysisPro.exe

3. Cấu hình tham số và campus

4. Nhấn "Bắt đầu phân tích"

5. Xem kết quả trong thư mục Output/

## Lưu ý:
- Cần có đủ 3 file Excel đầu vào
- Kết quả sẽ được lưu trong thư mục Output
- Có thể lưu/load cấu hình bằng file JSON

## Liên hệ hỗ trợ:
- Email: support@campusanalysis.com
- Website: www.campusanalysis.com
"""
    
    with open(dist_path / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"  ✅ README.txt")

def main():
    """Hàm main"""
    print("🚀 CAMPUS ANALYSIS PRO - BUILD EXE")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Create icon
    create_icon()
    
    # Create spec file
    create_spec_file()
    
    # Build EXE
    if not build_exe():
        return False
    
    # Copy required files
    copy_required_files()
    
    print("\n" + "=" * 50)
    print("🎉 BUILD HOÀN TẤT!")
    print("=" * 50)
    
    print("\n📁 Các file đã tạo:")
    print("  • dist/CampusAnalysisPro.exe - File thực thi chính")
    print("  • dist/Input/ - Thư mục cho file Excel đầu vào")
    print("  • dist/Output/ - Thư mục cho kết quả")
    print("  • dist/README.txt - Hướng dẫn sử dụng")
    
    print("\n💡 Hướng dẫn triển khai:")
    print("  1. Copy toàn bộ thư mục dist/ cho người dùng")
    print("  2. Đặt file Excel vào dist/Input/")
    print("  3. Chạy dist/CampusAnalysisPro.exe")
    
    print("\n✅ Sẵn sàng sử dụng!")
    
    return True

if __name__ == "__main__":
    success = main()
    input(f"\n{'✅ Nhấn Enter để thoát...' if success else '❌ Có lỗi. Nhấn Enter để thoát...'}")
