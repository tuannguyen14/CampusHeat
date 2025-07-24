# import pandas as pd
# import numpy as np

# print("📈 Đang phân tích TAM (Total Addressable Market)...")

# # TAM Formula: (Exclusive students + 50% Competition students) × Penetration Rate

# print(f"\n📊 Công thức tính TAM:")
# print(f"   TAM = (Học sinh exclusive + {OVERLAP_SHARE:.0%} × Học sinh cạnh tranh) × {PENETRATION_RATE:.2%}")
# print("=" * 70)

# # Dictionary lưu kết quả TAM
# tam_results = {}

# # Tính TAM cho từng campus
# for campus_code in campus_codes:
#     campus_name = coverage_results[campus_code]['campus_name']
    
#     # Lấy số liệu cơ bản
#     total_students = coverage_results[campus_code]['total_students']
#     exclusive = exclusive_students[campus_code]
#     competition = total_students - exclusive
    
#     # Tính addressable market
#     addressable_market = exclusive + (competition * OVERLAP_SHARE)
    
#     # Tính TAM
#     tam = addressable_market * PENETRATION_RATE
    
#     # Tính % capacity utilization nếu đạt TAM
#     capacity = coverage_results[campus_code]['capacity']
#     utilization = tam / capacity if capacity > 0 else 0
    
#     # Lưu kết quả
#     tam_results[campus_code] = {
#         'campus_name': campus_name,
#         'total_students': total_students,
#         'exclusive_students': exclusive,
#         'competition_students': competition,
#         'addressable_market': int(addressable_market),
#         'tam': int(tam),
#         'capacity': capacity,
#         'utilization': utilization,
#         'gap': int(capacity - tam) if capacity > tam else 0,
#         'overflow': int(tam - capacity) if tam > capacity else 0
#     }
    
#     print(f"\n📍 {campus_code} - {campus_name}:")
#     print(f"   • Tổng học sinh trong vùng: {total_students:,}")
#     print(f"   • Học sinh exclusive: {exclusive:,} ({exclusive/total_students:.1%})")
#     print(f"   • Học sinh cạnh tranh: {competition:,} ({competition/total_students:.1%})")
#     print(f"   • Addressable market: {addressable_market:,.0f}")
#     print(f"   • TAM: {tam:.0f} học viên")
#     print(f"   • Capacity: {capacity:,} học viên")
#     print(f"   • Utilization: {utilization:.1%}")
    
#     if tam > capacity:
#         print(f"   ⚠️  OVERFLOW: {tam - capacity:.0f} học viên")
#     else:
#         print(f"   ✅ GAP: {capacity - tam:.0f} học viên")

# # Phân tích tổng thể
# print("\n" + "="*70)
# print("📊 PHÂN TÍCH TỔNG THỂ:")

# # Tổng TAM
# total_tam = sum(data['tam'] for data in tam_results.values())
# total_capacity = sum(data['capacity'] for data in tam_results.values())
# total_utilization = total_tam / total_capacity if total_capacity > 0 else 0

# print(f"\n📈 Tổng quan hệ thống:")
# print(f"   • Tổng TAM: {total_tam:,.0f} học viên")
# print(f"   • Tổng capacity: {total_capacity:,} học viên")
# print(f"   • Utilization trung bình: {total_utilization:.1%}")

# # Phân loại campus theo utilization
# print(f"\n🎯 Phân loại theo mức độ utilization:")

# underutilized = []  # < 70%
# optimal = []        # 70-90%
# nearfull = []       # 90-100%
# overflow = []       # > 100%

# for campus_code, data in tam_results.items():
#     util = data['utilization']
#     if util < 0.7:
#         underutilized.append((campus_code, util))
#     elif util < 0.9:
#         optimal.append((campus_code, util))
#     elif util <= 1.0:
#         nearfull.append((campus_code, util))
#     else:
#         overflow.append((campus_code, util))

# if underutilized:
#     print(f"\n🟡 Underutilized (<70%):")
#     for campus, util in underutilized:
#         print(f"   • {campus}: {util:.1%} - Cần tăng cường marketing")

# if optimal:
#     print(f"\n🟢 Optimal (70-90%):")
#     for campus, util in optimal:
#         print(f"   • {campus}: {util:.1%} - Mức độ tốt")

# if nearfull:
#     print(f"\n🟠 Near Full (90-100%):")
#     for campus, util in nearfull:
#         print(f"   • {campus}: {util:.1%} - Gần đạt capacity")

# if overflow:
#     print(f"\n🔴 Overflow (>100%):")
#     for campus, util in overflow:
#         print(f"   • {campus}: {util:.1%} - Cần mở rộng hoặc mở campus mới")

# # Phân tích cơ hội mở rộng
# print(f"\n🚀 CƠ HỘI MỞ RỘNG:")

# # Tìm khu vực có overflow cao
# high_overflow_areas = [(c, d['overflow']) for c, d in tam_results.items() if d['overflow'] > 0]
# if high_overflow_areas:
#     high_overflow_areas.sort(key=lambda x: x[1], reverse=True)
#     print(f"\n📍 Khu vực cần mở rộng capacity:")
#     for campus, overflow_amount in high_overflow_areas:
#         rooms_needed = overflow_amount / STUDENTS_PER_ROOM
#         print(f"   • {campus}: Thiếu {overflow_amount:,.0f} chỗ (cần thêm {rooms_needed:.0f} phòng)")

# # Tìm khu vực underutilized có thể tối ưu
# low_util_areas = [(c, d['gap']) for c, d in tam_results.items() if d['utilization'] < 0.5]
# if low_util_areas:
#     low_util_areas.sort(key=lambda x: x[1], reverse=True)
#     print(f"\n📍 Khu vực cần tối ưu hóa:")
#     for campus, gap in low_util_areas:
#         util = tam_results[campus]['utilization']
#         print(f"   • {campus}: Chỉ đạt {util:.1%} capacity (còn trống {gap:,.0f} chỗ)")

# # Export kết quả
# globals()["tam_results"] = tam_results

# print("\n✅ Hoàn thành phân tích TAM!")
# 04_tam_analysis_fixed.py
"""
FIXED VERSION: Tính toán TAM với proper variable initialization
"""

import pandas as pd

# ===== BƯỚC 4: PHÂN TÍCH TAM (TOTAL ADDRESSABLE MARKET) =====
print("\n" + "="*80)
print("BƯỚC 4: PHÂN TÍCH TAM (TOTAL ADDRESSABLE MARKET)")
print("="*80)

print("\n📈 Đang phân tích TAM (Total Addressable Market)...")

# 4.1. Tính số học sinh exclusive và shared cho mỗi campus
tam_analysis = {}

for campus_code in campus_codes:
    # Initialize counters
    exclusive_students = 0
    shared_students = 0
    exclusive_schools = []
    shared_schools = []
    
    # Get coverage data for this campus
    coverage_data = coverage_results.get(campus_code, {})
    schools_in_coverage = coverage_data.get('schools_df', pd.DataFrame())
    
    # Process each school in coverage
    for idx, school in schools_in_coverage.iterrows():
        school_name = school['Tên trường']
        
        # Try multiple column names for student count
        student_count = 0
        for col in ['Tổng học sinh 2023', 'Số lượng', 'Số học sinh']:
            if col in school:
                value = school.get(col, 0)
                if pd.notna(value):
                    try:
                        student_count = int(value)
                        break
                    except:
                        pass
        
        # Default if no valid count found
        if student_count == 0:
            student_count = 500  # Default value from your file 01
        
        # Find school classification
        # Handle both simple and unique key formats
        school_class = None
        
        # Try direct name lookup first (for backward compatibility)
        if school_name in school_classification:
            school_class = school_classification[school_name]
        else:
            # Try with unique key format
            school_key = f"{school_name}_{idx}"
            if school_key in school_classification:
                school_class = school_classification[school_key]
                # Extract the classification data
                school_class = {
                    'campuses': school_class.get('campuses', []),
                    'type': school_class.get('type', 'unknown')
                }
            else:
                # Fallback: search through all classifications
                for key, data in school_classification.items():
                    if isinstance(data, dict) and data.get('original_name') == school_name:
                        if data.get('index') == idx:
                            school_class = data
                            break
        
        if school_class:
            # Check if this school is exclusive to this campus
            if school_class.get('type') == 'exclusive' and campus_code in school_class.get('campuses', []):
                exclusive_students += student_count
                exclusive_schools.append(school_name)
            elif school_class.get('type') == 'shared' and campus_code in school_class.get('campuses', []):
                shared_students += student_count
                shared_schools.append(school_name)
    
    # Store results
    tam_analysis[campus_code] = {
        'exclusive_students': exclusive_students,
        'shared_students': shared_students,
        'exclusive_schools': len(exclusive_schools),
        'shared_schools': len(shared_schools),
        'total_students': exclusive_students + shared_students
    }

# 4.2. Calculate TAM for each campus
print("\n📊 Công thức tính TAM:")
print("   TAM = (Học sinh exclusive + 50% × Học sinh shared) × Penetration Rate")
print("\n📊 Chi tiết TAM cho từng campus:")

penetration_rate = 0.0162  # 1.62%

for campus_code, data in tam_analysis.items():
    exclusive = data['exclusive_students']
    shared = data['shared_students']
    
    # TAM calculation
    tam = (exclusive + 0.5 * shared) * penetration_rate
    
    # Store TAM
    data['tam'] = tam
    data['tam_base'] = exclusive + 0.5 * shared
    
    # Print details
    print(f"\n📍 {campus_code}:")
    print(f"   • Exclusive: {exclusive:,} học sinh ({data['exclusive_schools']} trường)")
    print(f"   • Shared: {shared:,} học sinh ({data['shared_schools']} trường)")
    print(f"   • TAM Base: {data['tam_base']:,.0f} học sinh")
    print(f"   • TAM (1.62%): {tam:,.0f} học sinh")

# 4.3. Summary statistics
total_tam = sum(data['tam'] for data in tam_analysis.values())
total_exclusive = sum(data['exclusive_students'] for data in tam_analysis.values())
total_shared = sum(data['shared_students'] for data in tam_analysis.values())

print("\n📊 TỔNG KẾT TAM:")
print(f"   • Tổng học sinh exclusive: {total_exclusive:,}")
print(f"   • Tổng học sinh shared: {total_shared:,}")
print(f"   • Tổng TAM (all campuses): {total_tam:,.0f} học sinh")

# 4.4. Overlap analysis
print("\n📊 Phân tích overlap:")
for overlap_key, overlap_data in overlap_details.items():
    if overlap_data['num_schools'] > 0:
        campus1 = overlap_data['campus1']
        campus2 = overlap_data['campus2']
        print(f"   • {campus1} ↔ {campus2}: {overlap_data['num_schools']} trường, {overlap_data['total_students']:,} học sinh")

# 4.5. Export TAM results to dataframe for later use
tam_df = pd.DataFrame.from_dict(tam_analysis, orient='index')
tam_df.index.name = 'Campus'
tam_df = tam_df.reset_index()

print("\n✅ Hoàn thành phân tích TAM!")

# Make variables available globally
globals()['tam_analysis'] = tam_analysis
globals()['tam_df'] = tam_df
# Also export as tam_results for compatibility
globals()['tam_results'] = tam_analysis