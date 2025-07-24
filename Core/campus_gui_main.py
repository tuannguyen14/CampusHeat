#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Campus Analysis Pro - Main GUI File
File: campus_gui.py
"""

import sys
import os
import json
import threading
import traceback
from datetime import datetime
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox,
        QCheckBox, QSpinBox, QDoubleSpinBox, QProgressBar, QTabWidget,
        QScrollArea, QFrame, QGroupBox, QTableWidget, QTableWidgetItem,
        QFileDialog, QMessageBox, QSplitter, QStatusBar
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor
except ImportError:
    print("❌ Lỗi: Chưa cài đặt PyQt5")
    print("Chạy: pip install PyQt5")
    sys.exit(1)

class AnalysisWorker(QThread):
    """Worker thread để chạy analysis không block GUI"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    log_updated = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        """Chạy analysis pipeline"""
        try:
            # Change to script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            
            self.log_updated.emit("🚀 Bắt đầu phân tích...")
            self.log_updated.emit(f"📁 Working directory: {os.getcwd()}")
            
            # Setup global variables
            globals().update(self.config)
            
            # Step 1: Load data
            self.progress_updated.emit(10, "Đang load dữ liệu...")
            self.log_updated.emit("📂 BƯỚC 1: Load dữ liệu từ Excel...")
            
            # Check if analysis files exist
            required_files = [
                "01_load_data_selection.py",
                "02_compute_coverage.py", 
                "03_overlap_matrix.py",
                "04_tam_analysis.py",
                "05_generate_map.py",
                "06_export_excel.py"
            ]
            
            for file in required_files:
                if not os.path.exists(file):
                    raise FileNotFoundError(f"Không tìm thấy file: {file}")
            
            # Execute analysis steps
            with open("01_load_data_selection.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            # Step 2: Coverage
            self.progress_updated.emit(25, "Tính vùng phủ...")
            self.log_updated.emit("🗺️ BƯỚC 2: Tính vùng phủ từng campus...")
            with open("02_compute_coverage.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            # Step 3: Overlap
            self.progress_updated.emit(45, "Tính ma trận overlap...")
            self.log_updated.emit("🔄 BƯỚC 3: Tính ma trận overlap...")
            with open("03_overlap_matrix.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            # Step 4: TAM
            self.progress_updated.emit(65, "Phân tích TAM...")
            self.log_updated.emit("📈 BƯỚC 4: Phân tích TAM...")
            with open("04_tam_analysis.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            # Step 5: Map
            self.progress_updated.emit(80, "Tạo bản đồ...")
            self.log_updated.emit("🎨 BƯỚC 5: Tạo bản đồ interactive...")
            with open("05_generate_map.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            # Step 6: Excel
            self.progress_updated.emit(95, "Xuất báo cáo Excel...")
            self.log_updated.emit("📊 BƯỚC 6: Xuất báo cáo Excel...")
            with open("06_export_excel.py", "r", encoding="utf-8") as f:
                exec(f.read(), globals())
            
            self.progress_updated.emit(100, "Hoàn thành!")
            self.log_updated.emit("✅ Phân tích hoàn tất thành công!")
            self.finished.emit(True, "Phân tích hoàn tất thành công!")
            
        except FileNotFoundError as e:
            error_msg = f"❌ Không tìm thấy file: {str(e)}"
            self.log_updated.emit(error_msg)
            self.finished.emit(False, error_msg)
        except Exception as e:
            error_msg = f"❌ Lỗi: {str(e)}"
            self.log_updated.emit(error_msg)
            self.log_updated.emit(traceback.format_exc())
            self.finished.emit(False, error_msg)

class CampusAnalysisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analysis_worker = None
        self.init_ui()
        self.setup_default_config()

    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("Campus Analysis Pro v1.0 - Phân tích vùng phủ đa campus")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Configuration
        config_widget = self.create_config_panel()
        splitter.addWidget(config_widget)
        
        # Right panel - Output & Control
        output_widget = self.create_output_panel()
        splitter.addWidget(output_widget)
        
        # Set splitter proportions - MỞ RỘNG CONFIG PANEL
        splitter.setStretchFactor(0, 3)  # Config panel (tăng từ 1 lên 3)
        splitter.setStretchFactor(1, 2)  # Output panel (giữ nguyên 2)
        
        # Set minimum widths
        config_widget.setMinimumWidth(450)  # Đảm bảo config panel đủ rộng
        output_widget.setMinimumWidth(350)  # Output panel không quá nhỏ
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng phân tích - Campus Analysis Pro v1.0")
        
        # Apply modern styling
        self.apply_modern_style()

    def create_config_panel(self):
        """Tạo panel cấu hình"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("🎯 CAMPUS ANALYSIS CONFIGURATION")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 10px; background: #ecf0f1; border-radius: 5px;")
        layout.addWidget(title)
        
        # Scroll area for config
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # System Parameters Group - TĂNG KÍCH THƯỚC INPUT
        sys_group = QGroupBox("⚙️ Tham số hệ thống")
        sys_layout = QGridLayout(sys_group)
        
        # Penetration Rate
        sys_layout.addWidget(QLabel("Penetration Rate (%):"), 0, 0)
        self.penetration_rate = QDoubleSpinBox()
        self.penetration_rate.setRange(0.1, 10.0)
        self.penetration_rate.setValue(1.62)
        self.penetration_rate.setSuffix("%")
        self.penetration_rate.setDecimals(2)
        self.penetration_rate.setMinimumHeight(35)  # Tăng chiều cao
        sys_layout.addWidget(self.penetration_rate, 0, 1)
        
        # Coverage Radius
        sys_layout.addWidget(QLabel("Bán kính phủ (km):"), 1, 0)
        self.coverage_radius = QDoubleSpinBox()
        self.coverage_radius.setRange(1.0, 10.0)
        self.coverage_radius.setValue(3.0)
        self.coverage_radius.setSuffix(" km")
        self.coverage_radius.setMinimumHeight(35)  # Tăng chiều cao
        sys_layout.addWidget(self.coverage_radius, 1, 1)
        
        # Overlap Share
        sys_layout.addWidget(QLabel("Overlap Share (%):"), 2, 0)
        self.overlap_share = QDoubleSpinBox()
        self.overlap_share.setRange(10.0, 90.0)
        self.overlap_share.setValue(50.0)
        self.overlap_share.setSuffix("%")
        self.overlap_share.setMinimumHeight(35)  # Tăng chiều cao
        sys_layout.addWidget(self.overlap_share, 2, 1)
        
        # Students per Room
        sys_layout.addWidget(QLabel("Học viên/phòng:"), 3, 0)
        self.students_per_room = QSpinBox()
        self.students_per_room.setRange(50, 200)
        self.students_per_room.setValue(100)
        self.students_per_room.setMinimumHeight(35)  # Tăng chiều cao
        sys_layout.addWidget(self.students_per_room, 3, 1)
        
        scroll_layout.addWidget(sys_group)
        
        # Campus Selection Group
        campus_group = QGroupBox("🏢 Lựa chọn Campus")
        campus_layout = QVBoxLayout(campus_group)
        
        # Enable campus selection
        self.use_campus_selection = QCheckBox("Sử dụng Campus Selection")
        self.use_campus_selection.setChecked(True)
        self.use_campus_selection.toggled.connect(self.on_campus_selection_toggled)
        campus_layout.addWidget(self.use_campus_selection)
        
        # Selected campuses - TĂNG CHIỀU CAO INPUT
        campus_layout.addWidget(QLabel("Campus từ Excel (cách nhau bằng dấu phẩy):"))
        self.selected_campuses = QLineEdit()
        self.selected_campuses.setPlaceholderText("HCM_GR, HCM_TQB, DN_MAIN")
        self.selected_campuses.setMinimumHeight(35)  # Tăng chiều cao
        campus_layout.addWidget(self.selected_campuses)
        
        # New campuses table - TĂNG CHIỀU CAO
        campus_layout.addWidget(QLabel("Campus mới:"))
        self.new_campuses_table = QTableWidget(0, 5)
        self.new_campuses_table.setHorizontalHeaderLabels([
            "Campus Code", "Campus Name", "Latitude", "Longitude", "Số phòng"
        ])
        self.new_campuses_table.setMinimumHeight(180)  # Tăng từ 150 lên 180
        self.new_campuses_table.setMaximumHeight(220)  # Thêm max height
        
        # Tự động điều chỉnh độ rộng cột
        header = self.new_campuses_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(4):  # 4 cột đầu
            header.setSectionResizeMode(i, header.ResizeToContents)
        
        campus_layout.addWidget(self.new_campuses_table)
        
        # Buttons for campus table
        campus_btn_layout = QHBoxLayout()
        add_campus_btn = QPushButton("➕ Thêm Campus")
        add_campus_btn.clicked.connect(self.add_new_campus)
        remove_campus_btn = QPushButton("➖ Xóa Campus")
        remove_campus_btn.clicked.connect(self.remove_campus)
        campus_btn_layout.addWidget(add_campus_btn)
        campus_btn_layout.addWidget(remove_campus_btn)
        campus_layout.addLayout(campus_btn_layout)
        
        scroll_layout.addWidget(campus_group)
        
        # File Paths Group
        file_group = QGroupBox("📁 Đường dẫn File")
        file_layout = QVBoxLayout(file_group)
        
        # Input directory
        file_layout.addWidget(QLabel("Thư mục Input:"))
        input_layout = QHBoxLayout()
        self.input_dir = QLineEdit("./Input")
        self.input_dir.setMinimumHeight(30)  # Tăng chiều cao
        browse_input_btn = QPushButton("📂Browse")
        browse_input_btn.setMaximumWidth(120)  # Giới hạn độ rộng nút
        browse_input_btn.clicked.connect(self.browse_input_dir)
        input_layout.addWidget(self.input_dir)
        input_layout.addWidget(browse_input_btn)
        file_layout.addLayout(input_layout)
        
       
        # Output directory
        file_layout.addWidget(QLabel("Thư mục Output:"))
        output_layout = QHBoxLayout()
        self.output_dir = QLineEdit("./Output")
        self.output_dir.setMinimumHeight(30)  # Tăng chiều cao
        browse_output_btn = QPushButton("📂Browse")
        browse_output_btn.setMaximumWidth(120)  # Giới hạn độ rộng nút
        browse_output_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.output_dir)
        output_layout.addWidget(browse_output_btn)
        file_layout.addLayout(output_layout)
        
        scroll_layout.addWidget(file_group)
        
        # Config buttons - TĂNG KÍCH THƯỚC NÚT
        config_btn_layout = QHBoxLayout()
        save_config_btn = QPushButton("💾 Lưu Config")
        save_config_btn.setMinimumHeight(40)  # Tăng chiều cao nút
        save_config_btn.clicked.connect(self.save_config)
        load_config_btn = QPushButton("📂 Load Config")
        load_config_btn.setMinimumHeight(40)  # Tăng chiều cao nút
        load_config_btn.clicked.connect(self.load_config)
        reset_config_btn = QPushButton("🔄 Reset")
        reset_config_btn.setMinimumHeight(40)  # Tăng chiều cao nút
        reset_config_btn.clicked.connect(self.reset_config)
        
        config_btn_layout.addWidget(save_config_btn)
        config_btn_layout.addWidget(load_config_btn)
        config_btn_layout.addWidget(reset_config_btn)
        scroll_layout.addLayout(config_btn_layout)
        
        # Stretch
        scroll_layout.addStretch()
        
        return widget

    def create_output_panel(self):
        """Tạo panel output và control"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Control section
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.StyledPanel)
        control_layout = QVBoxLayout(control_frame)
        
        # Start button
        self.start_btn = QPushButton("🚀 BẮT ĐẦU PHÂN TÍCH")
        self.start_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.start_btn.clicked.connect(self.start_analysis)
        control_layout.addWidget(self.start_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(True)
        control_layout.addWidget(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("Sẵn sàng để phân tích")
        self.progress_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.progress_label)
        
        layout.addWidget(control_frame)
        
        # Output tabs
        self.output_tabs = QTabWidget()
        
        # Log tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        self.output_tabs.addTab(self.log_text, "📋 Log")
        
        # Results tab
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        
        # Results buttons
        results_btn_layout = QHBoxLayout()
        self.open_map_btn = QPushButton("🗺️ Mở Map")
        self.open_map_btn.clicked.connect(self.open_map)
        self.open_map_btn.setEnabled(False)
        
        self.open_excel_btn = QPushButton("📊 Mở Excel")
        self.open_excel_btn.clicked.connect(self.open_excel)
        self.open_excel_btn.setEnabled(False)
        
        self.open_output_btn = QPushButton("📁 Mở thư mục Output")
        self.open_output_btn.clicked.connect(self.open_output_folder)
        
        results_btn_layout.addWidget(self.open_map_btn)
        results_btn_layout.addWidget(self.open_excel_btn)
        results_btn_layout.addWidget(self.open_output_btn)
        results_layout.addLayout(results_btn_layout)
        
        # Results summary
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlainText("Kết quả phân tích sẽ hiển thị ở đây sau khi hoàn thành.")
        results_layout.addWidget(self.results_text)
        
        self.output_tabs.addTab(results_widget, "📈 Kết quả")
        
        layout.addWidget(self.output_tabs)
        
        return widget

    def apply_modern_style(self):
        """Áp dụng style hiện đại"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f8f9fa;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                font-size: 11px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

    def setup_default_config(self):
        """Thiết lập cấu hình mặc định"""
        # Add some default campuses
        self.selected_campuses.setText("HCM_GR, HCM_TQB")
        
        # Add a default new campus
        self.add_new_campus()
        if self.new_campuses_table.rowCount() > 0:
            self.new_campuses_table.setItem(0, 0, QTableWidgetItem("HCM_New_1"))
            self.new_campuses_table.setItem(0, 1, QTableWidgetItem("Ho Chi Minh New Campus"))
            self.new_campuses_table.setItem(0, 2, QTableWidgetItem("10.7769"))
            self.new_campuses_table.setItem(0, 3, QTableWidgetItem("106.7009"))
            self.new_campuses_table.setItem(0, 4, QTableWidgetItem("8"))

    def on_campus_selection_toggled(self, checked):
        """Xử lý khi toggle campus selection"""
        self.selected_campuses.setEnabled(checked)
        self.new_campuses_table.setEnabled(checked)

    def add_new_campus(self):
        """Thêm campus mới vào bảng"""
        row = self.new_campuses_table.rowCount()
        self.new_campuses_table.insertRow(row)
        
        # Set default values
        self.new_campuses_table.setItem(row, 0, QTableWidgetItem(f"NEW_{row+1}"))
        self.new_campuses_table.setItem(row, 1, QTableWidgetItem("New Campus"))
        self.new_campuses_table.setItem(row, 2, QTableWidgetItem("10.7769"))
        self.new_campuses_table.setItem(row, 3, QTableWidgetItem("106.7009"))
        self.new_campuses_table.setItem(row, 4, QTableWidgetItem("8"))

    def remove_campus(self):
        """Xóa campus được chọn"""
        current_row = self.new_campuses_table.currentRow()
        if current_row >= 0:
            self.new_campuses_table.removeRow(current_row)

    def browse_input_dir(self):
        """Browse input directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục Input")
        if dir_path:
            self.input_dir.setText(dir_path)

    def browse_output_dir(self):
        """Browse output directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục Output")
        if dir_path:
            self.output_dir.setText(dir_path)

    def get_config(self):
        """Lấy cấu hình hiện tại"""
        # Parse selected campuses
        selected_campuses = []
        if self.selected_campuses.text().strip():
            selected_campuses = [c.strip() for c in self.selected_campuses.text().split(",")]
        
        # Parse new campuses
        new_campuses = []
        for row in range(self.new_campuses_table.rowCount()):
            campus_code = self.new_campuses_table.item(row, 0)
            campus_name = self.new_campuses_table.item(row, 1)
            lat = self.new_campuses_table.item(row, 2)
            lon = self.new_campuses_table.item(row, 3)
            rooms = self.new_campuses_table.item(row, 4)
            
            if all([campus_code, campus_name, lat, lon, rooms]):
                try:
                    new_campuses.append({
                        "Campus Code": campus_code.text(),
                        "Campus Name": campus_name.text(),
                        "lat": float(lat.text()),
                        "lon": float(lon.text()),
                        "Số phòng học": int(rooms.text())
                    })
                except ValueError:
                    continue
        
        return {
            "PENETRATION_RATE": self.penetration_rate.value() / 100,
            "COVERAGE_RADIUS_KM": self.coverage_radius.value(),
            "OVERLAP_SHARE": self.overlap_share.value() / 100,
            "STUDENTS_PER_ROOM": self.students_per_room.value(),
            "USE_CAMPUS_SELECTION": self.use_campus_selection.isChecked(),
            "SELECTED_CAMPUSES": selected_campuses,
            "NEW_CAMPUSES": new_campuses,
            "INPUT_DIR": self.input_dir.text(),
            "OUTPUT_DIR": self.output_dir.text()
        }

    def save_config(self):
        """Lưu cấu hình ra file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu Config", "campus_config.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                config = self.get_config()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Thành công", "Đã lưu cấu hình!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể lưu config: {e}")

    def load_config(self):
        """Load cấu hình từ file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Config", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Apply config to UI
                self.penetration_rate.setValue(config.get("PENETRATION_RATE", 0.0162) * 100)
                self.coverage_radius.setValue(config.get("COVERAGE_RADIUS_KM", 3.0))
                self.overlap_share.setValue(config.get("OVERLAP_SHARE", 0.5) * 100)
                self.students_per_room.setValue(config.get("STUDENTS_PER_ROOM", 100))
                self.use_campus_selection.setChecked(config.get("USE_CAMPUS_SELECTION", True))
                
                selected_campuses = config.get("SELECTED_CAMPUSES", [])
                self.selected_campuses.setText(", ".join(selected_campuses))
                
                # Load new campuses
                self.new_campuses_table.setRowCount(0)
                new_campuses = config.get("NEW_CAMPUSES", [])
                for campus in new_campuses:
                    self.add_new_campus()
                    row = self.new_campuses_table.rowCount() - 1
                    self.new_campuses_table.setItem(row, 0, QTableWidgetItem(campus.get("Campus Code", "")))
                    self.new_campuses_table.setItem(row, 1, QTableWidgetItem(campus.get("Campus Name", "")))
                    self.new_campuses_table.setItem(row, 2, QTableWidgetItem(str(campus.get("lat", 0))))
                    self.new_campuses_table.setItem(row, 3, QTableWidgetItem(str(campus.get("lon", 0))))
                    self.new_campuses_table.setItem(row, 4, QTableWidgetItem(str(campus.get("Số phòng học", 8))))
                
                self.input_dir.setText(config.get("INPUT_DIR", "./Input"))
                self.output_dir.setText(config.get("OUTPUT_DIR", "./Output"))
                
                QMessageBox.information(self, "Thành công", "Đã load cấu hình!")
                
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể load config: {e}")

    def reset_config(self):
        """Reset về cấu hình mặc định"""
        self.penetration_rate.setValue(1.62)
        self.coverage_radius.setValue(3.0)
        self.overlap_share.setValue(50.0)
        self.students_per_room.setValue(100)
        self.use_campus_selection.setChecked(True)
        self.selected_campuses.setText("HCM_GR, HCM_TQB")
        self.new_campuses_table.setRowCount(0)
        self.input_dir.setText("./Input")
        self.output_dir.setText("./Output")
        self.setup_default_config()

    def start_analysis(self):
        """Bắt đầu phân tích"""
        # Validate config
        config = self.get_config()
        
        if not config["USE_CAMPUS_SELECTION"] or not (config["SELECTED_CAMPUSES"] or config["NEW_CAMPUSES"]):
            if config["USE_CAMPUS_SELECTION"]:
                QMessageBox.warning(self, "Cảnh báo", 
                    "Vui lòng chọn ít nhất một campus hoặc thêm campus mới!")
                return
        
        # Check input files
        input_dir = Path(config["INPUT_DIR"])
        required_files = [
            "Campuses_with_latlon.xlsx",
            "Students_with_latlon.xlsx", 
            "Public_Schools_with_latlon.xlsx"
        ]
        
        missing_files = []
        for file in required_files:
            if not (input_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            QMessageBox.critical(self, "Lỗi", 
                f"Không tìm thấy các file cần thiết trong {input_dir}:\n" + "\n".join(missing_files))
            return
        
        # Create output directory
        os.makedirs(config["OUTPUT_DIR"], exist_ok=True)
        
        # Start analysis
        self.start_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.log_text.append(f"🚀 Bắt đầu phân tích lúc {datetime.now().strftime('%H:%M:%S')}")
        
        # Start worker thread
        self.analysis_worker = AnalysisWorker(config)
        self.analysis_worker.progress_updated.connect(self.update_progress)
        self.analysis_worker.log_updated.connect(self.update_log)
        self.analysis_worker.finished.connect(self.analysis_finished)
        self.analysis_worker.start()

    def update_progress(self, value, message):
        """Cập nhật progress bar"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(message)
        self.status_bar.showMessage(message)

    def update_log(self, message):
        """Cập nhật log"""
        self.log_text.append(message)
        self.log_text.ensureCursorVisible()

    def analysis_finished(self, success, message):
        """Xử lý khi phân tích hoàn thành"""
        self.start_btn.setEnabled(True)
        
        if success:
            self.progress_bar.setValue(100)
            self.progress_label.setText("✅ Hoàn thành!")
            self.status_bar.showMessage("Phân tích hoàn thành thành công!")
            
            # Enable result buttons
            self.open_map_btn.setEnabled(True)
            self.open_excel_btn.setEnabled(True)
            
            # Update results tab
            self.update_results_summary()
            
            # Switch to results tab
            self.output_tabs.setCurrentIndex(1)
            
            # Show success message
            QMessageBox.information(self, "Thành công", 
                "Phân tích hoàn thành!\n\n"
                "Các file kết quả:\n"
                "• Map_Campus_Multi.html\n"
                "• Report_Campus_Multi.xlsx")
        else:
            self.progress_bar.setValue(0)
            self.progress_label.setText("❌ Có lỗi xảy ra")
            self.status_bar.showMessage("Phân tích thất bại!")
            QMessageBox.critical(self, "Lỗi", f"Phân tích thất bại:\n{message}")

    def update_results_summary(self):
        """Cập nhật tóm tắt kết quả"""
        try:
            output_dir = Path(self.output_dir.text())
            
            summary = []
            summary.append("🎉 PHÂN TÍCH HOÀN TẤT THÀNH CÔNG!")
            summary.append("=" * 50)
            summary.append("")
            
            # Check output files
            map_file = output_dir / "Map_Campus_Multi.html"
            excel_file = output_dir / "Report_Campus_Multi.xlsx"
            
            summary.append("📁 FILES ĐÃ TẠO:")
            if map_file.exists():
                summary.append(f"  ✅ {map_file.name} ({map_file.stat().st_size // 1024} KB)")
            else:
                summary.append(f"  ❌ {map_file.name} - Không tìm thấy")
                
            if excel_file.exists():
                summary.append(f"  ✅ {excel_file.name} ({excel_file.stat().st_size // 1024} KB)")
            else:
                summary.append(f"  ❌ {excel_file.name} - Không tìm thấy")
            
            summary.append("")
            summary.append("💡 HƯỚNG DẪN SỬ DỤNG:")
            summary.append("  • Click 'Mở Map' để xem bản đồ interactive")
            summary.append("  • Click 'Mở Excel' để xem báo cáo chi tiết")
            summary.append("  • Click vào campus/trường trên map để xem thông tin")
            summary.append("  • Sử dụng Layer Control để bật/tắt hiển thị")
            summary.append("")
            
            # Add config summary
            config = self.get_config()
            summary.append("⚙️ CẤU HÌNH ĐÃ SỬ DỤNG:")
            summary.append(f"  • Penetration Rate: {config['PENETRATION_RATE']:.2%}")
            summary.append(f"  • Bán kính phủ: {config['COVERAGE_RADIUS_KM']} km")
            summary.append(f"  • Overlap Share: {config['OVERLAP_SHARE']:.0%}")
            summary.append(f"  • Campus Selection: {'Bật' if config['USE_CAMPUS_SELECTION'] else 'Tắt'}")
            
            if config['USE_CAMPUS_SELECTION']:
                if config['SELECTED_CAMPUSES']:
                    summary.append(f"  • Campus từ Excel: {', '.join(config['SELECTED_CAMPUSES'])}")
                if config['NEW_CAMPUSES']:
                    new_codes = [c['Campus Code'] for c in config['NEW_CAMPUSES']]
                    summary.append(f"  • Campus mới: {', '.join(new_codes)}")
            
            self.results_text.setPlainText("\n".join(summary))
            
        except Exception as e:
            self.results_text.setPlainText(f"Lỗi khi tạo tóm tắt: {e}")

    def open_map(self):
        """Mở file map"""
        map_file = Path(self.output_dir.text()) / "Map_Campus_Multi.html"
        if map_file.exists():
            import webbrowser
            webbrowser.open(f"file://{map_file.absolute()}")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy file map!")

    def open_excel(self):
        """Mở file Excel"""
        excel_file = Path(self.output_dir.text()) / "Report_Campus_Multi.xlsx"
        if excel_file.exists():
            if sys.platform.startswith('win'):
                os.startfile(str(excel_file))
            elif sys.platform.startswith('darwin'):
                os.system(f"open '{excel_file}'")
            else:
                os.system(f"xdg-open '{excel_file}'")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy file Excel!")

    def open_output_folder(self):
        """Mở thư mục output"""
        output_path = Path(self.output_dir.text())
        if output_path.exists():
            if sys.platform.startswith('win'):
                os.startfile(str(output_path))
            elif sys.platform.startswith('darwin'):
                os.system(f"open '{output_path}'")
            else:
                os.system(f"xdg-open '{output_path}'")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Thư mục output không tồn tại!")

    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        if self.analysis_worker and self.analysis_worker.isRunning():
            reply = QMessageBox.question(self, "Xác nhận", 
                "Phân tích đang chạy. Bạn có muốn đóng ứng dụng?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.analysis_worker.terminate()
                self.analysis_worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Hàm main để chạy ứng dụng"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Campus Analysis Pro")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Campus Analytics")
    
    # Create and show main window
    window = CampusAnalysisGUI()
    window.show()
    
    # Center window on screen
    screen = app.primaryScreen().geometry()
    size = window.geometry()
    window.move((screen.width() - size.width()) // 2, 
                (screen.height() - size.height()) // 2)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()