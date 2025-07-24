#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN CONTROLLER: Phân tích vùng phủ đa campus với CAMPUS SELECTION và DEBUG MODE
Mô tả: Cho phép chọn campus cụ thể, thêm campus mới và chạy từng bước để debug
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
SELECTED_CAMPUSES = [
    "HCM_GR",      # Campus Ho Chi Minh - Green
    "HCM_TQB",     # Campus Ho Chi Minh - Ta Quang Bưu  
]

NEW_CAMPUSES = [
    {
        "Campus Code": "HCM_New_Demo",
        "Campus Name": "Ho Chi Minh New Campus Demo", 
        "lat": 10.7769,
        "lon": 106.7009,
        "Số phòng học": 8
    },
]

USE_CAMPUS_SELECTION = True

# ==== 🔧 DEBUG & STEP CONTROL ====
DEBUG_MODE = True  # Bật debug chi tiết
STEP_BY_STEP = True  # Pause sau mỗi bước

# Điều khiển từng bước (True = chạy, False = bỏ qua)
STEPS_TO_RUN = {
    'step1_load_data': True,
    'step2_compute_coverage': True,
    'step3_overlap_matrix': True,
    'step4_tam_analysis': True,
    'step5_generate_map': True,
    'step6_export_excel': True
}

# Điều khiển debug từng bước
DEBUG_STEPS = {
    'step1_data_validation': True,
    'step2_coverage_debug': True,
    'step3_overlap_debug': True,
    'step2_distance_verification': True,
    'step3_shared_schools_check': True,
    'step5_validation_debug': True
}

def print_step_header(step_num, step_name):
    """In header cho mỗi bước"""
    print(f"\n{'='*80}")
    print(f"📋 BƯỚC {step_num}: {step_name}")
    print(f"{'='*80}")

def print_debug_section(section_name):
    """In header cho debug section"""
    print(f"\n🔍 DEBUG: {section_name}")
    print(f"{'-'*60}")

def wait_for_user():
    """Chờ user nhấn Enter để tiếp tục"""
    if STEP_BY_STEP:
        input("⏸️  Nhấn Enter để tiếp tục...")

def run_step_with_debug(step_name, file_name, step_num, global_vars):
    """Chạy một bước với debug"""
    if not STEPS_TO_RUN.get(step_name, True):
        print(f"⏭️  Bỏ qua {step_name}")
        return True
    
    print_step_header(step_num, step_name.replace('_', ' ').title())
    
    try:
        # Chạy file
        with open(file_name, "r", encoding="utf-8") as f:
            exec(f.read(), global_vars)
        
        print(f"✅ Hoàn thành {step_name}")
        
        # Debug sau mỗi bước
        if DEBUG_MODE:
            run_step_debug(step_name, global_vars)
        
        wait_for_user()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi trong {step_name}: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return False

def run_step_debug(step_name, global_vars):
    """Chạy debug cho từng bước"""
    
    if step_name == 'step1_load_data' and DEBUG_STEPS.get('step1_data_validation', False):
        print_debug_section("STEP 1 - Data Validation")
        
        if 'campuses_df' in global_vars:
            campuses_df = global_vars['campuses_df']
            print(f"📊 Campuses loaded: {len(campuses_df)}")
            
            for _, campus in campuses_df.iterrows():
                code = campus['Campus Code']
                lat, lon = campus['lat'], campus['lon']
                print(f"   📍 {code}: ({lat}, {lon})")
                
                # Verify coordinates
                if pd.isna(lat) or pd.isna(lon):
                    print(f"      ❌ Invalid coordinates!")
        
        if 'schools_df' in global_vars:
            schools_df = global_vars['schools_df']
            print(f"📊 Schools loaded: {len(schools_df)}")
            
            # Check for invalid coordinates
            invalid_coords = schools_df[schools_df['lat'].isna() | schools_df['lon'].isna()]
            print(f"   ⚠️  Schools with invalid coordinates: {len(invalid_coords)}")
    
    elif step_name == 'step2_compute_coverage' and DEBUG_STEPS.get('step2_coverage_debug', False):
        print_debug_section("STEP 2 - Coverage Debug")
        
        if 'coverage_results' in global_vars:
            coverage_results = global_vars['coverage_results']
            campuses_df = global_vars['campuses_df']
            
            print(f"📊 Coverage computed for {len(coverage_results)} campuses")
            
            # Debug specific problematic cases
            for campus_code, coverage_data in coverage_results.items():
                print(f"\n📍 {campus_code} Coverage Analysis:")
                schools_in_coverage = coverage_data.get('schools_df', pd.DataFrame())
                
                if len(schools_in_coverage) > 0:
                    print(f"   • Schools in coverage: {len(schools_in_coverage)}")
                    
                    # Check distances
                    distance_col = f'dist_to_{campus_code}'
                    if distance_col in schools_in_coverage.columns:
                        distances = schools_in_coverage[distance_col]
                        max_dist = distances.max()
                        min_dist = distances.min()
                        avg_dist = distances.mean()
                        
                        print(f"   • Distance range: {min_dist:.2f}km - {max_dist:.2f}km (avg: {avg_dist:.2f}km)")
                        
                        # Check for violations
                        violations = schools_in_coverage[distances > COVERAGE_RADIUS_KM]
                        if len(violations) > 0:
                            print(f"   ❌ VIOLATIONS: {len(violations)} schools > {COVERAGE_RADIUS_KM}km")
                            for _, school in violations.iterrows():
                                school_name = school['Tên trường']
                                dist = school[distance_col]
                                print(f"      • {school_name}: {dist:.2f}km")
                        else:
                            print(f"   ✅ All schools within {COVERAGE_RADIUS_KM}km radius")
    
    elif step_name == 'step2_compute_coverage' and DEBUG_STEPS.get('step2_distance_verification', False):
        print_debug_section("STEP 2 - Distance Verification")
        
        # Verify distance calculation manually
        if 'coverage_results' in global_vars:
            coverage_results = global_vars['coverage_results']
            campuses_df = global_vars['campuses_df']
            schools_df = global_vars['schools_df']
            
            # Test with specific schools
            test_schools = ['Tiểu học Bùi Minh Trực', 'Tiểu học Lam Sơn']
            
            for school_name in test_schools:
                school_data = schools_df[schools_df['Tên trường'] == school_name]
                if not school_data.empty:
                    school = school_data.iloc[0]
                    school_lat, school_lon = school['lat'], school['lon']
                    
                    print(f"\n🔍 Testing {school_name} ({school_lat}, {school_lon}):")
                    
                    for _, campus in campuses_df.iterrows():
                        campus_code = campus['Campus Code']
                        campus_lat, campus_lon = campus['lat'], campus['lon']
                        
                        # Manual distance calculation
                        from geopy.distance import geodesic
                        distance = geodesic((school_lat, school_lon), (campus_lat, campus_lon)).km
                        
                        print(f"   📍 {campus_code}: {distance:.2f}km")
                        
                        # Check if in coverage
                        in_coverage = school_name in coverage_results.get(campus_code, {}).get('schools_df', pd.DataFrame())['Tên trường'].values
                        should_be_in = distance <= COVERAGE_RADIUS_KM
                        
                        if in_coverage != should_be_in:
                            print(f"      ❌ MISMATCH: In coverage={in_coverage}, Should be={should_be_in}")
                        else:
                            print(f"      ✅ CORRECT: In coverage={in_coverage}")
    
    elif step_name == 'step3_overlap_matrix' and DEBUG_STEPS.get('step3_shared_schools_check', False):
        print_debug_section("STEP 3 - Shared Schools Check")
        
        if 'school_classification' in global_vars:
            school_classification = global_vars['school_classification']
            
            # Check shared schools
            shared_schools = {name: data for name, data in school_classification.items() 
                            if data['type'] == 'shared'}
            
            print(f"📊 Found {len(shared_schools)} shared schools")
            
            for school_name, data in list(shared_schools.items())[:5]:  # Top 5
                campuses = data['campuses']
                print(f"\n🔍 {school_name}:")
                print(f"   • Assigned to: {campuses}")
                
                # Verify distances manually
                if 'schools_df' in global_vars and 'campuses_df' in global_vars:
                    schools_df = global_vars['schools_df']
                    campuses_df = global_vars['campuses_df']
                    
                    school_data = schools_df[schools_df['Tên trường'] == school_name]
                    if not school_data.empty:
                        school = school_data.iloc[0]
                        school_lat, school_lon = school['lat'], school['lon']
                        
                        for campus_code in campuses:
                            campus_data = campuses_df[campuses_df['Campus Code'] == campus_code]
                            if not campus_data.empty:
                                campus = campus_data.iloc[0]
                                campus_lat, campus_lon = campus['lat'], campus['lon']
                                
                                from geopy.distance import geodesic
                                distance = geodesic((school_lat, school_lon), (campus_lat, campus_lon)).km
                                
                                print(f"   📍 Distance to {campus_code}: {distance:.2f}km")
                                
                                if distance > COVERAGE_RADIUS_KM:
                                    print(f"      ❌ VIOLATION: {distance:.2f}km > {COVERAGE_RADIUS_KM}km")
    
    elif step_name == 'step5_generate_map' and DEBUG_STEPS.get('step5_validation_debug', False):
        print_debug_section("STEP 5 - Validation Debug")
        
        if 'school_classification' in global_vars:
            school_classification = global_vars['school_classification']
            
            # Check validation results
            exclusive_count = sum(1 for d in school_classification.values() if d['type'] == 'exclusive')
            shared_count = sum(1 for d in school_classification.values() if d['type'] == 'shared')
            
            print(f"📊 Post-validation results:")
            print(f"   • Exclusive schools: {exclusive_count}")
            print(f"   • Shared schools: {shared_count}")
            
            # Check for any remaining violations
            violations_found = 0
            if 'schools_df' in global_vars and 'campuses_df' in global_vars:
                schools_df = global_vars['schools_df']
                campuses_df = global_vars['campuses_df']
                
                for school_name, classification in school_classification.items():
                    school_data = schools_df[schools_df['Tên trường'] == school_name]
                    if not school_data.empty:
                        school = school_data.iloc[0]
                        school_lat, school_lon = school['lat'], school['lon']
                        
                        for campus_code in classification['campuses']:
                            campus_data = campuses_df[campuses_df['Campus Code'] == campus_code]
                            if not campus_data.empty:
                                campus = campus_data.iloc[0]
                                campus_lat, campus_lon = campus['lat'], campus['lon']
                                
                                from geopy.distance import geodesic
                                distance = geodesic((school_lat, school_lon), (campus_lat, campus_lon)).km
                                
                                if distance > COVERAGE_RADIUS_KM:
                                    print(f"   ❌ STILL VIOLATION: {school_name} → {campus_code}: {distance:.2f}km")
                                    violations_found += 1
            
            if violations_found == 0:
                print("   ✅ No violations found after validation!")
            else:
                print(f"   ❌ Found {violations_found} violations after validation!")

def main():
    """Main function với step-by-step control"""
    
    print("🚀 PHÂN TÍCH VÙNG PHỦ ĐA CAMPUS (DEBUG MODE)")
    print("="*80)
    print(f"📅 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Debug mode: {'✅ ON' if DEBUG_MODE else '❌ OFF'}")
    print(f"⏸️  Step-by-step: {'✅ ON' if STEP_BY_STEP else '❌ OFF'}")
    
    # Hiển thị steps sẽ chạy
    print(f"\n📋 Steps to run:")
    for step_name, enabled in STEPS_TO_RUN.items():
        status = "✅" if enabled else "❌"
        print(f"   {status} {step_name}")
    
    # Hiển thị debug options
    if DEBUG_MODE:
        print(f"\n🔍 Debug options:")
        for debug_name, enabled in DEBUG_STEPS.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {debug_name}")
    
    wait_for_user()
    
    # Tạo namespace global
    global_vars = globals()
    
    # Export cấu hình
    for key, value in {
        'PENETRATION_RATE': PENETRATION_RATE,
        'COVERAGE_RADIUS_KM': COVERAGE_RADIUS_KM,
        'OVERLAP_SHARE': OVERLAP_SHARE,
        'STUDENTS_PER_ROOM': STUDENTS_PER_ROOM,
        'SELECTED_CAMPUSES': SELECTED_CAMPUSES,
        'NEW_CAMPUSES': NEW_CAMPUSES,
        'USE_CAMPUS_SELECTION': USE_CAMPUS_SELECTION,
        'DEBUG_MODE': DEBUG_MODE
    }.items():
        global_vars[key] = value
    
    try:
        # Import pandas for debug functions
        import pandas as pd
        global_vars['pd'] = pd
        
        # Chạy từng bước
        steps = [
            ('step1_load_data', '01_load_data_selection.py', 1),
            ('step2_compute_coverage', '02_compute_coverage.py', 2),
            ('step3_overlap_matrix', '03_overlap_matrix.py', 3),
            ('step4_tam_analysis', '04_tam_analysis.py', 4),
            ('step5_generate_map', '05_generate_map.py', 5),
            ('step6_export_excel', '06_export_excel.py', 6)
        ]
        
        for step_name, file_name, step_num in steps:
            success = run_step_with_debug(step_name, file_name, step_num, global_vars)
            if not success:
                print(f"❌ Dừng tại {step_name} do lỗi")
                return False
        
        # Tổng kết
        print("\n" + "="*80)
        print("🎉 PHÂN TÍCH HOÀN TẤT THÀNH CÔNG!")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI KHÔNG MONG MUỐN: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        input("\n✅ Nhấn Enter để thoát...")
    else:
        input("\n❌ Có lỗi xảy ra. Nhấn Enter để thoát...")