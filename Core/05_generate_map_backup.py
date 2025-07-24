#!/usr/bin/env python3
"""Generate interactive map with COMPLETE VALIDATION"""

import folium
from folium import plugins
import pandas as pd
import numpy as np
from shapely.geometry import MultiPoint
from geopy.distance import geodesic
import os

# ===============================================================================
# IMPORT VALIDATION MODULE (ĐÃ SỬA)
# ===============================================================================

def calculate_distance_strict(lat1, lon1, lat2, lon2):
    """Tính khoảng cách chặt chẽ"""
    try:
        if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
            return float('inf')
        return geodesic((float(lat1), float(lon1)), (float(lat2), float(lon2))).km
    except:
        return float('inf')

def validate_and_clean_school_classification(school_classification, campuses_df, schools_df, radius_km):
    """Validation 1: ĐÃ SỬA để bao gồm thông tin vị trí"""
    print("🔍 VALIDATION 1: Lọc school_classification...")
    
    cleaned_classification = {}
    stats = {'removed': 0, 'reclassified': 0, 'kept': 0}
    
    # Tạo dictionary mapping để tối ưu truy vấn
    school_coords = {row['Tên trường']: (row['lat'], row['lon'], row.get('Tổng học sinh 2023', 0)) 
                    for _, row in schools_df.iterrows()}
    
    for school_name, classification in school_classification.items():
        if school_name not in school_coords:
            stats['removed'] += 1
            continue
            
        school_lat, school_lon, school_students = school_coords[school_name]
        
        if pd.isna(school_lat) or pd.isna(school_lon):
            stats['removed'] += 1
            continue
        
        # Kiểm tra khoảng cách đến từng campus
        assigned_campuses = classification.get('campuses', [])
        valid_campuses = []
        
        for campus_code in assigned_campuses:
            campus_data = campuses_df[campuses_df['Campus Code'] == campus_code]
            if campus_data.empty:
                continue
            
            campus = campus_data.iloc[0]
            distance = calculate_distance_strict(
                school_lat, school_lon,
                campus['lat'], campus['lon']
            )
            
            if distance <= radius_km:
                valid_campuses.append(campus_code)
        
        # Xác định loại trường
        old_type = classification.get('type', 'unknown')
        
        if len(valid_campuses) == 0:
            stats['removed'] += 1
        else:
            new_type = 'exclusive' if len(valid_campuses) == 1 else 'shared'
            
            if old_type != new_type:
                stats['reclassified'] += 1
            else:
                stats['kept'] += 1
            
            # THÊM THÔNG TIN VỊ TRÍ VÀ HỌC SINH
            cleaned_classification[school_name] = {
                'type': new_type,
                'campuses': valid_campuses,
                'lat': school_lat,
                'lon': school_lon,
                'students': school_students
            }
    
    print(f"   📊 Removed: {stats['removed']}, Reclassified: {stats['reclassified']}, Kept: {stats['kept']}")
    return cleaned_classification

# ===============================================================================
# MAIN VALIDATION & MAP CREATION (ĐÃ SỬA)
# ===============================================================================

# ... (phần khởi tạo bản đồ giữ nguyên)

# Thêm school markers (ĐÃ TỐI ƯU)
print("🏫 Thêm school markers (validated only)...")
schools_added = 0
validation_errors = 0

for school_name, classification in school_classification.items():
    school_type = classification['type']
    covering_campuses = classification['campuses']
    lat, lon = classification['lat'], classification['lon']
    students = classification.get('students', 0)
    
    # SAFETY CHECK: Verify logic consistency
    if len(covering_campuses) == 1 and school_type != 'exclusive':
        validation_errors += 1
        school_type = 'exclusive'
    elif len(covering_campuses) > 1 and school_type != 'shared':
        validation_errors += 1
        school_type = 'shared'
    
    # Xử lý giá trị học sinh bị thiếu
    if pd.isna(students):
        students = 0
    
    # Tạo marker size (ĐÃ THÊM KIỂM TRA GIÁ TRỊ)
    marker_size = max(4, min(12, students / 300 if students > 0 else 6))
    
    # Tạo popup content
    popup_content = f"""
    <div style="width: 340px;">
        <h4 style="margin: 0; color: {'orange' if school_type == 'shared' else 'blue'};">{school_name}</h4>
        <hr style="margin: 5px 0;">
        <b>Trạng thái:</b> {school_type.title()}<br>
        <b>Số học sinh:</b> {students:,.0f}<br>
        <b>Thuộc campus:</b> {', '.join(covering_campuses)}<br>
    </div>
    """
    
    # Thêm vào nhóm phù hợp
    if school_type == 'exclusive':
        campus_code = covering_campuses[0]
        target_group = exclusive_schools_groups[campus_code]
        marker_color = get_campus_color(campus_code)
    else:
        target_group = shared_schools_group
        marker_color = 'orange'
    
    folium.CircleMarker(
        location=[float(lat), float(lon)],
        radius=marker_size,
        color=marker_color,
        fillColor=marker_color,
        weight=2,
        fill=True,
        fillOpacity=0.7,
        popup=folium.Popup(popup_content, max_width=360)
    ).add_to(target_group)
    
    schools_added += 1

print(f"\n📊 VALIDATED SCHOOL MARKERS:")
print(f"   • Schools added: {schools_added}")
print(f"   • Validation errors: {validation_errors}")

# ... (phần còn lại giữ nguyên)