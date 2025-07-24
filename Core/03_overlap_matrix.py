# ===== BƯỚC 3: TÍNH MA TRẬN OVERLAP (FIXED VERSION) =====

import pandas as pd
import numpy as np
from geopy.distance import geodesic

print("\n" + "="*80)
print("BƯỚC 3: TÍNH MA TRẬN OVERLAP (FIXED VERSION)")
print("="*80)

# Hàm tính khoảng cách
def haversine_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# 3.1. Tạo ma trận overlap giữa các campus
campus_list = list(coverage_results.keys())
n_campuses = len(campus_list)
overlap_matrix = np.zeros((n_campuses, n_campuses))

# 3.2. Dictionary lưu chi tiết overlap
overlap_details = {}

# 3.3. Tạo school classification với unique identifier
school_classification = {}

# Tạo dictionary mapping tên trường -> dữ liệu để tối ưu truy vấn
schools_dict = {idx: row for idx, row in schools_df.iterrows()}

for campus_code, coverage_data in coverage_results.items():
    schools_in_coverage = coverage_data['schools_df']
    
    for idx, school in schools_in_coverage.iterrows():
        school_name = school['Tên trường']
        school_lat = school['lat']
        school_lon = school['lon']
        
        # Sử dụng index làm unique identifier
        school_key = f"{school_name}_{idx}"
        
        if school_key not in school_classification:
            school_classification[school_key] = {
                'original_name': school_name,
                'lat': school_lat,
                'lon': school_lon,
                'campuses': [],
                'type': None,
                'index': idx,
                'students': school.get('Tổng học sinh 2023', 0)
            }
        
        if campus_code not in school_classification[school_key]['campuses']:
            school_classification[school_key]['campuses'].append(campus_code)

# 3.4. Phân loại trường dựa trên số campus phủ sóng
print("\n🔍 Xác định loại trường dựa trên số campus phủ sóng:")
exclusive_count = 0
shared_count = 0

for school_key, data in school_classification.items():
    num_campuses = len(data['campuses'])
    
    if num_campuses == 1:
        data['type'] = 'exclusive'
        exclusive_count += 1
    elif num_campuses > 1:
        data['type'] = 'shared'
        shared_count += 1

print(f"\n✅ Đã tạo school_classification cho {len(school_classification)} trường:")
print(f"   - Exclusive: {exclusive_count}")
print(f"   - Shared: {shared_count}")

# 3.5. Tính overlap matrix và details (SỬA LẠI để lưu số học sinh)
print("\n📊 Tính ma trận overlap (lưu số học sinh)...")

for i in range(n_campuses):
    for j in range(i+1, n_campuses):
        campus1 = campus_list[i]
        campus2 = campus_list[j]
        
        shared_students = 0
        shared_schools = []
        
        for school_key, classification in school_classification.items():
            if (campus1 in classification['campuses'] and 
                campus2 in classification['campuses']):
                shared_schools.append(classification['original_name'])
                shared_students += classification['students']
        
        # SỬA: Lưu số học sinh thay vì số trường
        overlap_matrix[i][j] = shared_students
        overlap_matrix[j][i] = shared_students
        
        overlap_key = f"{campus1}_{campus2}"
        overlap_details[overlap_key] = {
            'campus1': campus1,
            'campus2': campus2,
            'schools': shared_schools,
            'num_schools': len(shared_schools),
            'total_students': shared_students
        }
        
        if len(shared_schools) > 0:
            print(f"   • {campus1} ↔ {campus2}: {len(shared_schools)} trường, {shared_students:,} học sinh")

# 3.6. Convert to DataFrame
overlap_matrix = pd.DataFrame(
    overlap_matrix,
    index=campus_list,
    columns=campus_list
)

# 3.7. Tạo school_classification đơn giản để tương thích
school_classification_simple = {}
for school_key, data in school_classification.items():
    school_classification_simple[data['original_name']] = {
        'type': data['type'],
        'campuses': data['campuses'],
        'lat': data['lat'],
        'lon': data['lon'],
        'students': data['students']
    }

# Export kết quả
globals()["overlap_matrix"] = overlap_matrix
globals()["overlap_details"] = overlap_details
globals()["school_classification"] = school_classification_simple

print("\n✅ Hoàn thành tính ma trận overlap với UNIQUE IDENTIFIERS!")