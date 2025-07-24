#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN CONTROLLER: Phân tích vùng phủ đa campus với CAMPUS SELECTION
Mô tả: Cho phép chọn campus cụ thể và thêm campus mới trực tiếp trong code
"""

import sys
import traceback
import os
from datetime import datetime

# ==== CẤU HÌNH HỆ THỐNG ====
PENETRATION_RATE = 0.0162  # Tỷ lệ chuyển đổi từ học sinh công thành học viên (1.62%)
COVERAGE_RADIUS_KM = 3     # Bán kính vùng phủ (km)
OVERLAP_SHARE = 0.5        # Tỷ lệ chia sẻ vùng overlap (50-50)
STUDENTS_PER_ROOM = 100    # Số học viên tối đa mỗi phòng

# ==== 🎯 CAMPUS SELECTION CONFIG ====
# Chọn campus từ 43 campus có sẵn trong Excel
SELECTED_CAMPUSES = [
    "HCM_GR",      # Campus Ho Chi Minh - Green
    "HCM_TQB",     # Campus Ho Chi Minh - Ta Quang Bưu  
    # Thêm campus codes khác từ file Excel nếu cần
    # "DN_MAIN", "CT_MAIN", "BD_MAIN", etc.
]

# Thêm campus mới (không có trong Excel)
NEW_CAMPUSES = [
    {
        "Campus Code": "HCM_New_Demo",
        "Campus Name": "Ho Chi Minh New Campus Demo", 
        "lat": 10.7769,
        "lon": 106.7009,
        "Số phòng học": 8   
    },
    # Thêm campus mới khác nếu cần
]

# ==== 🔧 CAMPUS FILTERING MODE ====
# True: Chỉ dùng campus được chọn + campus mới
# False: Dùng tất cả campus từ Excel (chế độ cũ)
USE_CAMPUS_SELECTION = True

def main():
    """Hàm main để chạy toàn bộ pipeline phân tích với campus selection"""
    
    print("🚀 BẮT ĐẦU PHÂN TÍCH VÙNG PHỦ ĐA CAMPUS (CAMPUS SELECTION MODE)")
    print("=" * 80)
    print(f"📅 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Cấu hình hệ thống:")
    print(f"   • Penetration Rate: {PENETRATION_RATE:.2%}")
    print(f"   • Bán kính phủ: {COVERAGE_RADIUS_KM} km")
    print(f"   • Overlap Share: {OVERLAP_SHARE:.0%}")
    print(f"   • Capacity/phòng: {STUDENTS_PER_ROOM} học viên")
    print("=" * 80)
    
    # Campus Selection Info
    if USE_CAMPUS_SELECTION:
        print(f"🎯 CAMPUS SELECTION MODE:")
        print(f"   📋 Campus được chọn từ Excel ({len(SELECTED_CAMPUSES)}):")
        for campus in SELECTED_CAMPUSES:
            print(f"      • {campus}")
        
        print(f"   🆕 Campus mới thêm trực tiếp ({len(NEW_CAMPUSES)}):")
        for campus in NEW_CAMPUSES:
            print(f"      • {campus['Campus Code']}: {campus['Campus Name']}")
            print(f"        📍 Tọa độ: ({campus['lat']}, {campus['lon']})")
            print(f"        🏢 Phòng học: {campus['Số phòng học']}")
        
        total_campuses = len(SELECTED_CAMPUSES) + len(NEW_CAMPUSES)
        print(f"   📊 Tổng cộng: {total_campuses} campus sẽ được phân tích")
    else:
        print(f"📋 SỬ DỤNG TẤT CẢ CAMPUS từ Excel (chế độ cũ)")
    
    print("=" * 80)
    
    print("\n📋 Pipeline gồm 6 bước:")
    print("   1️⃣ Load dữ liệu từ Excel (với campus filtering)")
    print("   2️⃣ Tính vùng phủ từng campus")
    print("   3️⃣ Tính ma trận overlap")
    print("   4️⃣ Phân tích TAM")
    print("   5️⃣ Tạo bản đồ interactive")
    print("   6️⃣ Xuất báo cáo Excel")
    print("=" * 80)
    
    # Tạo namespace global để chia sẻ biến
    global_vars = globals()
    
    # Export các biến cấu hình để các module khác sử dụng
    global_vars['PENETRATION_RATE'] = PENETRATION_RATE
    global_vars['COVERAGE_RADIUS_KM'] = COVERAGE_RADIUS_KM
    global_vars['OVERLAP_SHARE'] = OVERLAP_SHARE
    global_vars['STUDENTS_PER_ROOM'] = STUDENTS_PER_ROOM
    
    # Export campus selection config
    global_vars['SELECTED_CAMPUSES'] = SELECTED_CAMPUSES
    global_vars['NEW_CAMPUSES'] = NEW_CAMPUSES
    global_vars['USE_CAMPUS_SELECTION'] = USE_CAMPUS_SELECTION
    
    try:
        # Bước 1: Load dữ liệu với campus selection
        print("\n📂 BƯỚC 1: Load dữ liệu từ Excel với campus selection...")
        with open("01_load_data_selection.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 1")
        
        # Bước 2: Tính vùng phủ
        print("\n🗺️ BƯỚC 2: Tính vùng phủ từng campus...")
        with open("02_compute_coverage.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 2")
        
        # Bước 3: Ma trận overlap
        print("\n🔄 BƯỚC 3: Tính ma trận overlap...")
        with open("03_overlap_matrix.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 3")
        
        # Bước 4: Phân tích TAM
        print("\n📈 BƯỚC 4: Phân tích TAM...")
        with open("04_tam_analysis.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 4")
        
        # Bước 5: Tạo bản đồ
        print("\n🎨 BƯỚC 5: Tạo bản đồ interactive...")
        with open("05_generate_map.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 5")
        
        # Bước 6: Báo cáo Excel
        print("\n📊 BƯỚC 6: Xuất báo cáo Excel...")
        with open("06_export_excel.py", "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        print("✅ Hoàn thành bước 6")
        
        # Tổng kết
        print("\n" + "="*80)
        print("🎉 PHÂN TÍCH HOÀN TẤT THÀNH CÔNG!")
        print("="*80)
        
        # Thống kê tổng kết
        if 'campuses_df' in global_vars:
            num_campuses = len(global_vars['campuses_df'])
            print(f"📊 THỐNG KÊ TỔNG KẾT:")
            print(f"   🏢 Tổng số campus được phân tích: {num_campuses}")
            
            print(f"   📋 Chi tiết từng campus:")
            if 'coverage_results' in global_vars:
                coverage = global_vars['coverage_results']
                for campus_code, data in coverage.items():
                    campus_name = data.get('campus_name', campus_code)
                    print(f"      📍 {campus_code} ({campus_name})")
                    print(f"         • {data['num_schools']} trường trong {COVERAGE_RADIUS_KM}km")
                    print(f"         • {data['total_students']:,} học sinh nguồn")
                    print(f"         • {data['capacity']:,} capacity")
            
            if 'overlap_matrix' in global_vars:
                matrix = global_vars['overlap_matrix']
                total_overlaps = sum(1 for i in range(len(matrix)) for j in range(i+1, len(matrix)) if matrix.iloc[i,j] > 0)
                print(f"   🔄 Số cặp campus có overlap: {total_overlaps}")
            
            if 'tam_results' in global_vars:
                total_tam = sum(data['tam'] for data in global_vars['tam_results'].values())
                total_capacity = sum(data['capacity'] for data in global_vars['tam_results'].values())
                utilization = total_tam / total_capacity if total_capacity > 0 else 0
                print(f"   📈 Tổng TAM: {total_tam:,.0f} học viên")
                print(f"   📊 Tổng capacity: {total_capacity:,} học viên")
                print(f"   🎯 Utilization hệ thống: {utilization:.1%}")
        
        print(f"\n📁 FILES ĐÃ TẠO:")
        print(f"   📍 Map_Campus_Multi.html - Bản đồ interactive với {len(SELECTED_CAMPUSES) + len(NEW_CAMPUSES)} campus")
        print(f"   📊 Report_Campus_Multi.xlsx - Báo cáo Excel chi tiết")
        
        print(f"\n💡 HƯỚNG DẪN SỬ DỤNG:")
        print(f"   • Mở file HTML để xem bản đồ với các campus đã chọn")
        print(f"   • Click vào campus/trường để xem thông tin chi tiết") 
        print(f"   • Sử dụng Layer Control để bật/tắt hiển thị từng campus")
        print(f"   • Xem file Excel để phân tích chi tiết TAM và overlap")
        
        print(f"\n🔧 THAY ĐỔI CAMPUS:")
        print(f"   • Sửa SELECTED_CAMPUSES để chọn campus khác từ 43 campus có sẵn")
        print(f"   • Sửa NEW_CAMPUSES để thêm/sửa campus mới")
        print(f"   • Set USE_CAMPUS_SELECTION = False để dùng tất cả campus")
        print(f"   • Thay đổi COVERAGE_RADIUS_KM để điều chỉnh vùng phủ")
        
        # Hiển thị campus selection summary
        if USE_CAMPUS_SELECTION:
            print(f"\n🎯 CAMPUS ĐƯỢC PHÂN TÍCH:")
            print(f"   📋 Từ Excel: {SELECTED_CAMPUSES}")
            print(f"   🆕 Mới thêm: {[c['Campus Code'] for c in NEW_CAMPUSES]}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ LỖI: Không tìm thấy file - {e}")
        print("💡 Kiểm tra các file cần thiết:")
        required_files = [
            "01_load_data_selection.py",  # File mới với campus selection
            "02_compute_coverage.py", "03_overlap_matrix.py",
            "04_tam_analysis.py", "05_generate_map.py", "06_export_excel.py"
        ]
        print("   Python files:")
        for f in required_files:
            status = "✅" if os.path.exists(f) else "❌"
            print(f"   {status} {f}")
        print("   Excel files:")
        excel_files = [
            "Campuses_with_latlon.xlsx", "Students_with_latlon.xlsx",
            "Public_Schools_with_latlon.xlsx"
        ]
        for f in excel_files:
            full_path = f"./Input/{f}"
            status = "✅" if os.path.exists(full_path) else "❌"
            print(f"   {status} ./Input/{f}")
        return False
        
    except Exception as e:
        print(f"\n❌ LỖI KHÔNG MONG MUỐN: {e}")
        print("\n📋 STACK TRACE:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        input("\n✅ Nhấn Enter để thoát...")
    else:
        input("\n❌ Có lỗi xảy ra. Nhấn Enter để thoát...")