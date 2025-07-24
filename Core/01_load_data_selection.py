import pandas as pd
import numpy as np
import os
import math

print("📂 Đang load dữ liệu từ các file Excel với CAMPUS SELECTION...")

# Lấy cấu hình từ main.py
STUDENTS_PER_ROOM = globals().get('STUDENTS_PER_ROOM', 100)
USE_CAMPUS_SELECTION = globals().get('USE_CAMPUS_SELECTION', False)
SELECTED_CAMPUSES = globals().get('SELECTED_CAMPUSES', [])
NEW_CAMPUSES = globals().get('NEW_CAMPUSES', [])

print(f"🔧 Campus selection mode: {'✅ ENABLED' if USE_CAMPUS_SELECTION else '❌ DISABLED'}")

# Kiểm tra và tạo thư mục Input nếu cần
input_dir = "./Input"
if not os.path.exists(input_dir):
    input_dir = "."
    print("⚠️  Không tìm thấy thư mục Input, sử dụng thư mục hiện tại")

# ============================================================================
# LOAD DỮ LIỆU CAMPUS VỚI SELECTION
# ============================================================================

try:
    # Load toàn bộ campus từ Excel
    full_campuses_df = pd.read_excel(f"{input_dir}/Campuses_with_latlon.xlsx")
    full_campuses_df['Campus Code'] = full_campuses_df['Campus Code'].astype(str).str.strip()
    print(f"📋 Loaded {len(full_campuses_df)} campus từ Excel")
    
    # Hiển thị danh sách campus có sẵn
    available_campuses = sorted(full_campuses_df['Campus Code'].unique())
    print(f"   Available campus codes: {available_campuses}")
    
    if USE_CAMPUS_SELECTION:
        print(f"\n🎯 CAMPUS SELECTION MODE:")
        
        # ===== FILTER CAMPUS TỪ EXCEL =====
        selected_from_excel = []
        if SELECTED_CAMPUSES:
            print(f"📋 Filtering campus từ Excel...")
            for campus_code in SELECTED_CAMPUSES:
                campus_data = full_campuses_df[full_campuses_df['Campus Code'] == campus_code]
                if not campus_data.empty:
                    selected_from_excel.append(campus_data.iloc[0])
                    print(f"   ✅ Found: {campus_code}")
                else:
                    print(f"   ❌ Not found: {campus_code}")
                    print(f"      Available: {available_campuses}")
        
        # Convert to DataFrame
        if selected_from_excel:
            selected_campuses_df = pd.DataFrame(selected_from_excel)
        else:
            selected_campuses_df = pd.DataFrame(columns=full_campuses_df.columns)
        
        print(f"   📊 Selected from Excel: {len(selected_campuses_df)} campus")
        
        # ===== THÊM CAMPUS MỚI =====
        new_campuses_list = []
        if NEW_CAMPUSES:
            print(f"🆕 Adding new campus...")
            for campus_info in NEW_CAMPUSES:
                # Validate required fields
                required_fields = ['Campus Code', 'Campus Name', 'lat', 'lon', 'Số phòng học']
                if all(field in campus_info for field in required_fields):
                    # Tạo campus record
                    new_campus = {
                        'Campus Code': str(campus_info['Campus Code']).strip(),
                        'Campus Name': campus_info['Campus Name'],
                        'lat': float(campus_info['lat']),
                        'lon': float(campus_info['lon']),
                        'Số phòng học': int(campus_info['Số phòng học'])
                    }
                    
                    # Copy other columns from template (if exists)
                    if not full_campuses_df.empty:
                        template = full_campuses_df.iloc[0].to_dict()
                        for col in template:
                            if col not in new_campus:
                                new_campus[col] = template[col] if pd.notna(template[col]) else None
                    
                    new_campuses_list.append(new_campus)
                    print(f"   ✅ Added: {new_campus['Campus Code']} - {new_campus['Campus Name']}")
                    print(f"      📍 Coordinates: ({new_campus['lat']}, {new_campus['lon']})")
                    print(f"      🏢 Rooms: {new_campus['Số phòng học']}")
                else:
                    missing = [f for f in required_fields if f not in campus_info]
                    print(f"   ❌ Invalid campus config: missing {missing}")
        
        # Convert new campuses to DataFrame
        if new_campuses_list:
            new_campuses_df = pd.DataFrame(new_campuses_list)
        else:
            new_campuses_df = pd.DataFrame(columns=full_campuses_df.columns)
        
        print(f"   📊 New campus added: {len(new_campuses_df)} campus")
        
        # ===== KẾT HỢP CAMPUS =====
        if not selected_campuses_df.empty and not new_campuses_df.empty:
            campuses_df = pd.concat([selected_campuses_df, new_campuses_df], ignore_index=True)
        elif not selected_campuses_df.empty:
            campuses_df = selected_campuses_df
        elif not new_campuses_df.empty:
            campuses_df = new_campuses_df
        else:
            print("❌ Không có campus nào được chọn!")
            campuses_df = pd.DataFrame(columns=full_campuses_df.columns)
        
        print(f"\n📊 FINAL CAMPUS LIST ({len(campuses_df)} campus):")
        for _, campus in campuses_df.iterrows():
            source = "📋 Excel" if campus['Campus Code'] in SELECTED_CAMPUSES else "🆕 New"
            print(f"   {source}: {campus['Campus Code']} - {campus['Campus Name']}")
    
    else:
        # Sử dụng tất cả campus (chế độ cũ)
        campuses_df = full_campuses_df.copy()
        print(f"📋 Using ALL campus from Excel: {len(campuses_df)} campus")
    
    # Chuẩn hóa dữ liệu campus
    campuses_df['Campus Code'] = campuses_df['Campus Code'].astype(str).str.strip()
    campus_codes = [str(code).strip() for code in campuses_df['Campus Code'].unique()]
    
    print(f"✅ Final campus codes: {campus_codes}")
    
    # Đảm bảo có các cột cần thiết
    required_cols = ['Campus Code', 'Campus Name', 'lat', 'lon']
    missing_cols = [col for col in required_cols if col not in campuses_df.columns]
    if missing_cols:
        print(f"⚠️  Thiếu cột: {missing_cols}")
    
    # Tính capacity từ số phòng học
    if 'Số phòng học' in campuses_df.columns:
        campuses_df['capacity'] = campuses_df['Số phòng học'].fillna(8) * STUDENTS_PER_ROOM
    else:
        print("⚠️  Không có cột 'Số phòng học', sử dụng default 8 phòng/campus")
        campuses_df['capacity'] = 8 * STUDENTS_PER_ROOM
    
    print(f"✅ Campus capacity calculated based on {STUDENTS_PER_ROOM} students/room")
    
except FileNotFoundError:
    print("❌ Không tìm thấy file Campuses_with_latlon.xlsx")
    exit()
except Exception as e:
    print(f"❌ Lỗi khi load campus data: {e}")
    exit()

# ============================================================================
# LOAD DỮ LIỆU HỌC VIÊN (KHÔNG THAY ĐỔI)
# ============================================================================

try:
    students_df = pd.read_excel(f"{input_dir}/Students_with_latlon.xlsx")
    # Chuẩn hóa studycampuscode
    if 'studycampuscode' in students_df.columns:
        students_df['studycampuscode'] = students_df['studycampuscode'].astype(str).str.strip()
    print(f"✅ Students: {len(students_df)} records")
except FileNotFoundError:
    print("❌ Không tìm thấy file Students_with_latlon.xlsx")
    exit()

# ============================================================================
# LOAD DỮ LIỆU TRƯỜNG CÔNG (KHÔNG THAY ĐỔI)
# ============================================================================

try:
    schools_df = pd.read_excel(f"{input_dir}/Public_Schools_with_latlon.xlsx")
    schools_df['Tên trường'] = schools_df['Tên trường'].astype(str)
    print(f"✅ Public Schools: {len(schools_df)} records")
    
    # Đảm bảo có cột số học sinh
    if 'Tổng học sinh 2023' not in schools_df.columns:
        print("⚠️  Không có cột 'Tổng học sinh 2023', tạo giá trị mặc định")
        schools_df['Tổng học sinh 2023'] = 500
        
except FileNotFoundError:
    print("❌ Không tìm thấy file Public_Schools_with_latlon.xlsx")
    exit()

# ============================================================================
# TẠO TRANSFER SUGGESTION CHO CAMPUS ĐÃ CHỌN
# ============================================================================

print("⚠️  Bỏ qua tạo transfer suggestion - sẽ tạo on-demand nếu cần")
transfer_df = pd.DataFrame()  # Empty for now

# ============================================================================
# HIỂN thị THÔNG TIN CẤU TRÚC DỮ LIỆU
# ============================================================================

print("\n📋 Cấu trúc dữ liệu:")
print("=" * 70)

# Thông tin campus được chọn
print(f"\n🏫 CAMPUSES ({len(campuses_df)} campus được chọn):")
print(f"Columns: {list(campuses_df.columns)}")

for idx, row in campuses_df.iterrows():
    campus_code = row.get('Campus Code', 'N/A')
    campus_name = row.get('Campus Name', 'N/A')
    capacity = row.get('capacity', 0)
    rooms = capacity // STUDENTS_PER_ROOM
    source = "📋 Excel" if campus_code in SELECTED_CAMPUSES else "🆕 New"
    
    print(f"  {source} {campus_code}: {campus_name}")
    print(f"    📍 Tọa độ: ({row.get('lat', 'N/A')}, {row.get('lon', 'N/A')})")
    print(f"    📚 Capacity: {capacity:,} học viên ({rooms} phòng)")

# Thống kê học viên theo campus được chọn
print(f"\n👨‍🎓 STUDENTS DISTRIBUTION (filtered by selected campus):")
if 'studycampuscode' in students_df.columns:
    # Chỉ thống kê học viên thuộc campus được chọn
    valid_student_counts = students_df[students_df['studycampuscode'].isin(campus_codes)]['studycampuscode'].value_counts()
    print(f"  Học viên thuộc campus được chọn ({len(valid_student_counts)} campus):")
    for campus_code, count in valid_student_counts.items():
        campus_name = campuses_df[campuses_df['Campus Code'] == campus_code]['Campus Name'].iloc[0] if len(campuses_df[campuses_df['Campus Code'] == campus_code]) > 0 else 'Unknown'
        print(f"  - {campus_code} ({campus_name}): {count:,} học viên")
    
    # Thống kê học viên NOT thuộc campus được chọn  
    invalid_students = students_df[~students_df['studycampuscode'].isin(campus_codes)]
    if len(invalid_students) > 0:
        print(f"\n  Học viên thuộc campus khác (không được chọn): {len(invalid_students)}")
        invalid_counts = invalid_students['studycampuscode'].value_counts()
        for campus_code, count in invalid_counts.head(5).items():
            print(f"  - {campus_code}: {count:,} học viên")
        if len(invalid_counts) > 5:
            print(f"  - ... và {len(invalid_counts) - 5} campus khác")
    
    total_selected_students = valid_student_counts.sum() if len(valid_student_counts) > 0 else 0
    total_other_students = len(invalid_students)
    print(f"\n  📊 Summary:")
    print(f"     • Students in selected campus: {total_selected_students:,}")
    print(f"     • Students in other campus: {total_other_students:,}")
    print(f"     • Total students: {len(students_df):,}")
    
else:
    print("  ⚠️ Không có thông tin campus của học viên")

# Thông tin trường công (không thay đổi)
print(f"\n🏫 PUBLIC SCHOOLS: {len(schools_df)} trường")
total_public_students = schools_df['Tổng học sinh 2023'].sum()
print(f"  - Tổng học sinh: {total_public_students:,}")
print(f"  - Trung bình: {schools_df['Tổng học sinh 2023'].mean():.0f} học sinh/trường")

# Kiểm tra tính hợp lệ của dữ liệu campus được chọn
print("\n🔍 Kiểm tra dữ liệu campus được chọn:")

# Kiểm tra tọa độ campus
invalid_campus_coords = campuses_df[
    campuses_df['lat'].isna() | campuses_df['lon'].isna() |
    (campuses_df['lat'] == 0) | (campuses_df['lon'] == 0)
]
if len(invalid_campus_coords) > 0:
    print(f"  ⚠️ {len(invalid_campus_coords)} campus thiếu tọa độ hợp lệ:")
    for _, campus in invalid_campus_coords.iterrows():
        print(f"     - {campus['Campus Code']}: ({campus.get('lat', 'N/A')}, {campus.get('lon', 'N/A')})")
else:
    print("  ✅ Tất cả campus được chọn có tọa độ hợp lệ")