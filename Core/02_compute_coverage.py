# 02_compute_coverage_fixed.py
"""
FIXED VERSION: Compute coverage with proper student count column
"""

import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin

# ===== BƯỚC 2: TÍNH VÙNG PHỦ CHO MỖI CAMPUS =====
print("\n" + "="*80)
print("BƯỚC 2: TÍNH VÙNG PHỦ CHO MỖI CAMPUS")
print("="*80)

# 2.1. Hàm tính khoảng cách haversine
def haversine_distance(lat1, lon1, lat2, lon2):
    """Tính khoảng cách giữa 2 điểm theo công thức haversine (km)"""
    R = 6371  # Radius of Earth in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    return R * c

# 2.2. Tính coverage cho mỗi campus
coverage_results = {}

print(f"\n📏 Coverage radius: {COVERAGE_RADIUS_KM} km")
print(f"🏫 Computing coverage for {len(campus_codes)} campuses...")

for campus_code in campus_codes:
    # Get campus info
    campus_info = campuses_df[campuses_df['Campus Code'] == campus_code].iloc[0]
    campus_lat = campus_info['lat']
    campus_lon = campus_info['lon']
    
    print(f"\n📍 {campus_code}: {campus_info['Campus Name']}")
    print(f"   Location: ({campus_lat:.6f}, {campus_lon:.6f})")
    
    # Find schools within coverage radius
    schools_in_coverage = []
    
    for idx, school in schools_df.iterrows():
        # Calculate distance
        distance_km = haversine_distance(
            campus_lat, campus_lon,
            school['lat'], school['lon']
        )
        
        # Check if within radius
        if distance_km <= COVERAGE_RADIUS_KM:
            # Create school copy with distance info
            school_copy = school.copy()
            school_copy[f'dist_to_{campus_code}'] = distance_km
            
            # IMPORTANT: Ensure student count column is included
            # Check multiple possible column names
            student_count_found = False
            for col in ['Tổng học sinh 2023', 'Số lượng', 'Số học sinh', 'Total Students']:
                if col in school:
                    school_copy['Số lượng'] = school[col]  # Standardize to 'Số lượng'
                    student_count_found = True
                    break
            
            if not student_count_found:
                # Use default from file 01
                school_copy['Số lượng'] = 500
            
            schools_in_coverage.append(school_copy)
    
    # Convert to DataFrame
    schools_in_coverage_df = pd.DataFrame(schools_in_coverage)
    
    # Store results
    coverage_results[campus_code] = {
        'campus_info': campus_info,
        'schools_df': schools_in_coverage_df,
        'num_schools': len(schools_in_coverage_df),
        'total_students': schools_in_coverage_df['Số lượng'].sum() if len(schools_in_coverage_df) > 0 else 0
    }
    
    print(f"   ✅ Found {len(schools_in_coverage_df)} schools in {COVERAGE_RADIUS_KM}km radius")
    if len(schools_in_coverage_df) > 0:
        print(f"   📊 Total students: {schools_in_coverage_df['Số lượng'].sum():,}")
        print(f"   📊 Avg distance: {schools_in_coverage_df[f'dist_to_{campus_code}'].mean():.2f}km")
        print(f"   📊 Max distance: {schools_in_coverage_df[f'dist_to_{campus_code}'].max():.2f}km")

# 2.3. Summary
print("\n" + "="*50)
print("📊 COVERAGE SUMMARY:")
print("="*50)

total_unique_schools = len(set(
    school_name 
    for data in coverage_results.values() 
    for school_name in data['schools_df']['Tên trường'] if len(data['schools_df']) > 0
))

for campus_code, data in coverage_results.items():
    print(f"\n{campus_code}:")
    print(f"  • Schools: {data['num_schools']}")
    print(f"  • Students: {data['total_students']:,}")

print(f"\n📊 Total unique schools covered: {total_unique_schools}")

# Debug: Check if student counts are correct
print("\n🔍 DEBUG: Student count verification")
for campus_code, data in coverage_results.items():
    if data['num_schools'] > 0:
        schools_df_coverage = data['schools_df']
        avg_students = schools_df_coverage['Số lượng'].mean()
        print(f"{campus_code}: Avg students/school = {avg_students:.0f}")
        
        # Show sample
        if len(schools_df_coverage) > 0:
            sample = schools_df_coverage[['Tên trường', 'Số lượng']].head(3)
            print(f"  Sample schools:")
            for _, row in sample.iterrows():
                print(f"    - {row['Tên trường']}: {row['Số lượng']} students")

print("\n✅ Hoàn thành tính vùng phủ!")