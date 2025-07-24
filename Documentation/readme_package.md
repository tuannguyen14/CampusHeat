# Campus Analysis Pro v1.0

## 🎯 Tổng quan

**Campus Analysis Pro** là hệ thống phân tích vùng phủ đa campus với giao diện đồ họa hiện đại, giúp bạn:

- ✅ Phân tích vùng phủ của các campus
- ✅ Tính toán TAM (Total Addressable Market)  
- ✅ Xác định overlap giữa các campus
- ✅ Tạo bản đồ interactive
- ✅ Xuất báo cáo Excel chi tiết

## 📦 Nội dung Package

```
CampusAnalysisPro_v1.0/
├── 📁 Core Files/
│   ├── campus_gui.py                   # Ứng dụng GUI chính
│   ├── main_select_campus.py           # Console version
│   ├── 01_load_data_selection.py       # Module load data
│   ├── 02_compute_coverage.py          # Module tính coverage
│   ├── 03_overlap_matrix.py            # Module overlap
│   ├── 04_tam_analysis.py              # Module TAM
│   ├── 05_generate_map.py              # Module tạo map
│   └── 06_export_excel.py              # Module export Excel
├── 📁 Build Tools/
│   ├── requirements.txt                # Dependencies
│   ├── build_exe.py                    # Build EXE script
│   └── install.bat                     # One-click installer
├── 📁 Sample Data/
│   └── Input/
│       ├── Campuses_with_latlon.xlsx   # Dữ liệu campus mẫu
│       ├── Students_with_latlon.xlsx   # Dữ liệu học viên mẫu
│       └── Public_Schools_with_latlon.xlsx  # Dữ liệu trường công mẫu
├── 📁 Config/
│   ├── campus_config.json              # Cấu hình mẫu
│   └── demo_config.json                # Demo config
├── 📁 Documentation/
│   ├── README.txt                      # Hướng dẫn cơ bản
│   ├── USER_GUIDE.pdf                  # Hướng dẫn chi tiết
│   └── TECHNICAL_DOCS.md               # Tài liệu kỹ thuật
└── 📁 Output/                          # Thư mục kết quả (trống)
```

## 🚀 Cài đặt Nhanh

### Option 1: One-Click Install (Khuyến nghị)
```bash
# Chạy installer tự động
install.bat
```

### Option 2: Manual Install
```bash
# 1. Tạo virtual environment
python -m venv campus_env
campus_env\Scripts\activate

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Test installation
python campus_gui.py
```

## 🎮 Cách sử dụng

### Mode 1: GUI Application (Dễ nhất)
```bash
python campus_gui.py
```

**Workflow:**
1. ✅ Mở ứng dụng GUI
2. ✅ Cấu hình tham số bên trái
3. ✅ Chọn campus từ Excel hoặc thêm mới
4. ✅ Nhấn "Bắt đầu phân tích"
5. ✅ Xem kết quả và mở Map/Excel

### Mode 2: Console Version
```bash
python main_select_campus.py
```

### Mode 3: Build EXE
```bash
python build_exe.py
# Kết quả: dist/CampusAnalysisPro.exe
```

## ⚙️ Cấu hình

### Tham số hệ thống
```python
PENETRATION_RATE = 0.0162      # 1.62% - Tỷ lệ chuyển đổi
COVERAGE_RADIUS_KM = 3         # 3km - Bán kính phủ
OVERLAP_SHARE = 0.5            # 50% - Chia sẻ overlap
STUDENTS_PER_ROOM = 100        # 100 học viên/phòng
```

### Campus Selection
```python
# Chọn từ Excel
SELECTED_CAMPUSES = ["HCM_GR", "HCM_TQB", "DN_MAIN"]

# Thêm campus mới
NEW_CAMPUSES = [
    {
        "Campus Code": "HCM_New_1",
        "Campus Name": "Ho Chi Minh New Campus",
        "lat": 10.7769,
        "lon": 106.7009,
        "Số phòng học": 8
    }
]
```

## 📊 Kết quả Output

### 1. Bản đồ Interactive
- **File**: `Output/Map_Campus_Multi.html`
- **Tính năng**: 
  - Click campus/trường để xem thông tin
  - Layer control để bật/tắt hiển thị
  - Polygon coverage (không phải circles)
  - Legend với thống kê chi tiết

### 2. Báo cáo Excel
- **File**: `Output/Report_Campus_Multi.xlsx`
- **Sheets**:
  - Overview - Tổng quan hệ thống
  - Overlap_Matrix - Ma trận overlap
  - TAM_Analysis - Chi tiết TAM
  - Competition_Zones - Vùng cạnh tranh
  - [Campus]_Schools - Chi tiết từng campus
  - Market_Opportunity - Cơ hội thị trường
  - Recommendations - Khuyến nghị

## 🎨 Giao diện GUI

### Panel Trái - Configuration
- **System Parameters**: Penetration rate, coverage radius, etc.
- **Campus Selection**: Chọn/thêm campus
- **File Paths**: Input/Output directories
- **Config Management**: Save/Load JSON config

### Panel Phải - Control & Output
- **Start Button**: Bắt đầu phân tích
- **Progress Bar**: Tiến độ real-time
- **Log Tab**: Chi tiết quá trình
- **Results Tab**: Tóm tắt + nút mở file

## 🔧 Tùy chỉnh nâng cao

### Thay đổi giao diện
```python
# Trong campus_gui.py - apply_modern_style()
def apply_dark_theme(self):
    self.setStyleSheet("""
        QMainWindow { background-color: #2b2b2b; color: white; }
        QGroupBox { border: 2px solid #555; color: white; }
    """)
```

### Thêm campus analysis
```python
# Trong 04_tam_analysis.py
def custom_tam_calculation(exclusive, competition, custom_rate):
    return (exclusive + competition * 0.3) * custom_rate
```

### Export formats khác
```python
# Thêm vào 06_export_excel.py
def export_to_powerpoint():
    # Create PowerPoint slides
    pass

def export_to_pdf():
    # Create PDF report
    pass
```

## 🐛 Troubleshooting

### Lỗi cài đặt
```bash
# Lỗi: "pip not found"
python -m ensurepip --upgrade

# Lỗi: "PyQt5 install failed"
pip install --upgrade pip
pip install PyQt5 --no-cache-dir

# Lỗi: "Permission denied" 
# Chạy Command Prompt as Administrator
```

### Lỗi runtime
```bash
# Lỗi: "Module not found"
# Activate virtual environment:
campus_env\Scripts\activate

# Lỗi: "Excel file not found"
# Check file paths trong Input/
```

### Lỗi build EXE
```bash
# EXE quá lớn (>200MB)
# Edit campus_analysis.spec, thêm excludes

# Lỗi: "Failed to execute script"
# Test trước: python campus_gui.py
```

## 📈 Performance Tips

### Tối ưu tốc độ
- ✅ Giảm số campus phân tích
- ✅ Giảm coverage radius
- ✅ Sử dụng SSD thay vì HDD
- ✅ Đóng các ứng dụng khác

### Tối ưu memory
- ✅ Xử lý từng campus một
- ✅ Clear cache sau mỗi step
- ✅ Sử dụng chunking cho big data

## 🚀 Roadmap

### v1.1 - Advanced Analytics
- [ ] Real-time data integration
- [ ] Machine learning predictions
- [ ] Advanced visualizations
- [ ] REST API support

### v1.2 - Enterprise Features  
- [ ] Multi-user support
- [ ] Role-based access control
- [ ] Database integration
- [ ] Cloud deployment

### v1.3 - Mobile Support
- [ ] Web application
- [ ] Mobile app (React Native)
- [ ] Progressive Web App

## 💬 Support

### Community
- **GitHub**: https://github.com/campus-analysis/pro
- **Forum**: https://forum.campusanalysis.com
- **Discord**: https://discord.gg/campusanalysis

### Commercial Support
- **Email**: support@campusanalysis.com
- **Phone**: +84-xxx-xxx-xxx
- **Training**: Available on request

## 📝 License

**Campus Analysis Pro v1.0**
- ✅ Free for educational use
- ✅ Commercial license available
- ✅ Source code included
- ✅ No usage restrictions for analysis

## 🙏 Acknowledgments

Developed with ❤️ using:
- **PyQt5** - GUI framework
- **Pandas** - Data processing
- **Folium** - Interactive maps
- **Shapely** - Geospatial analysis
- **Openpyxl** - Excel export

---

**Made in Vietnam 🇻🇳 | Campus Analysis Pro v1.0 | 2024**

**Ready to analyze your campus coverage! 🚀**