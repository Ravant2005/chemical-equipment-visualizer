# Set Qt environment variables BEFORE any Qt imports to suppress warnings
import os
os.environ['QT_DEBUG_PLUGINS'] = '0'
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.xcb=false;qt.qpa.wayland=false'
os.environ['QT_ASSUME_STDERR_HAS_CONSOLE'] = '0'

import sys
import json
import warnings
import logging
import requests

# Suppress Python warnings
warnings.filterwarnings('ignore')
logging.getLogger('matplotlib').setLevel(logging.WARNING)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
                              QTableWidgetItem, QTabWidget, QMessageBox, QTextEdit, QGroupBox,
                              QFormLayout, QStackedWidget, QFrame, QButtonGroup, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


# Monkey patch FigureCanvas to suppress propagateSizeHints warning
_original_init = FigureCanvas.__init__

def _patched_init(self, figure):
    _original_init(self, figure)
    self.setSizePolicy(3, 3)  # QSizePolicy.Fixed, QSizePolicy.Fixed to prevent resize issues

FigureCanvas.__init__ = _patched_init


class APIClient:
    """Handle API communication"""
    def __init__(self, base_url=None):
        # Use environment variable or default to localhost
        if base_url:
            self.base_url = base_url
        else:
            # Use environment variable `CHEMVIZ_API_URL` in production.
            # Default to the Render backend URL; override as needed.
            self.base_url = os.environ.get('CHEMVIZ_API_URL', 'https://chemical-equipment-visualizer-t6zk.onrender.com/api')
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/accounts/auth/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.set_token(data['token'])
            return data
        raise Exception(response.json().get('error', 'Login failed'))
    
    def register(self, username, email, password):
        response = requests.post(
            f"{self.base_url}/accounts/auth/register/",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 201:
            data = response.json()
            self.set_token(data['token'])
            return data
        raise Exception(response.json().get('error', 'Registration failed'))
    
    def upload_csv(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/equipments/datasets/upload/",
                files=files,
                headers={"Authorization": f"Bearer {self.token}"}
            )
        if response.status_code == 201:
            return response.json()
        raise Exception(response.json().get('error', 'Upload failed'))
    
    def get_history(self):
        response = requests.get(
            f"{self.base_url}/equipments/datasets/history/",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to fetch history")
    
    def get_dataset(self, dataset_id):
        response = requests.get(
            f"{self.base_url}/equipments/datasets/{dataset_id}/",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to fetch dataset")

    def generate_report(self, dataset_id):
        response = requests.get(
            f"{self.base_url}/equipments/datasets/{dataset_id}/generate_report/",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.content
        raise Exception("Failed to generate report")


class LoginWindow(QWidget):
    """Login/Register window"""
    login_success = pyqtSignal(dict)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ChemViz Pro")
        self.setObjectName("LoginWindow")
        self.setMinimumSize(440, 640)
        self.setStyleSheet("""
            #LoginWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #0b1230, stop:1 #1f2b5f);
            }
            QFrame#loginCard {
                background-color: rgba(15, 23, 42, 0.96);
                border: 1px solid #1e293b;
                border-radius: 18px;
            }
            QLabel {
                color: #e2e8f0;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 10px;
                background-color: #0f172a;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
            QPushButton {
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#primaryBtn {
                background-color: #3b82f6;
                color: white;
            }
            QPushButton#primaryBtn:hover {
                background-color: #2563eb;
            }
            QPushButton#secondaryBtn {
                background-color: #8b5cf6;
                color: white;
            }
            QPushButton#secondaryBtn:hover {
                background-color: #7c3aed;
            }
            QPushButton#toggleBtn {
                background-color: transparent;
                border: 1px solid #334155;
                color: #94a3b8;
            }
            QPushButton#toggleBtn:checked {
                background-color: #3b82f6;
                color: white;
                border-color: #3b82f6;
            }
            QPushButton#settingsBtn {
                background-color: #1e293b;
                color: #cbd5f5;
                font-size: 12px;
                padding: 8px 12px;
            }
            QPushButton#settingsBtn:hover {
                background-color: #334155;
            }
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 30, 40, 30)
        outer.addStretch()

        card = QFrame()
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(28, 28, 28, 28)

        title = QLabel("ChemViz Pro")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #7dd3fc;")
        card_layout.addWidget(title)

        subtitle = QLabel("Equipment Analytics Platform")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #94a3b8; margin-bottom: 8px;")
        card_layout.addWidget(subtitle)

        toggle_layout = QHBoxLayout()
        toggle_group = QButtonGroup(self)
        toggle_group.setExclusive(True)

        self.login_toggle = QPushButton("Login")
        self.login_toggle.setObjectName("toggleBtn")
        self.login_toggle.setCheckable(True)
        self.login_toggle.setChecked(True)
        self.login_toggle.clicked.connect(lambda: self.auth_stack.setCurrentIndex(0))
        toggle_group.addButton(self.login_toggle)
        toggle_layout.addWidget(self.login_toggle)

        self.register_toggle = QPushButton("Register")
        self.register_toggle.setObjectName("toggleBtn")
        self.register_toggle.setCheckable(True)
        self.register_toggle.clicked.connect(lambda: self.auth_stack.setCurrentIndex(1))
        toggle_group.addButton(self.register_toggle)
        toggle_layout.addWidget(self.register_toggle)

        card_layout.addLayout(toggle_layout)

        self.auth_stack = QStackedWidget()
        self.auth_stack.addWidget(self._build_login_page())
        self.auth_stack.addWidget(self._build_register_page())
        card_layout.addWidget(self.auth_stack)

        outer.addWidget(card)
        outer.addStretch()

    def _build_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        heading = QLabel("Welcome Back")
        heading.setFont(QFont("Arial", 18, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("color: #e2e8f0; margin-top: 6px;")
        layout.addWidget(heading)

        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Username")
        layout.addWidget(self.login_username_input)

        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Password")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password_input)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("primaryBtn")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        layout.addStretch()
        return page

    def _build_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        heading = QLabel("Create Account")
        heading.setFont(QFont("Arial", 18, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("color: #e2e8f0; margin-top: 6px;")
        layout.addWidget(heading)

        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Username")
        layout.addWidget(self.reg_username_input)

        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Email")
        layout.addWidget(self.reg_email_input)

        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Password")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_input)

        self.reg_confirm_input = QLineEdit()
        self.reg_confirm_input.setPlaceholderText("Confirm Password")
        self.reg_confirm_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_confirm_input)

        register_btn = QPushButton("Create Account")
        register_btn.setObjectName("secondaryBtn")
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)

        layout.addStretch()
        return page
    
    def handle_login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        try:
            data = self.api_client.login(username, password)
            self.login_success.emit(data)
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", str(e))
    
    def handle_register(self):
        username = self.reg_username_input.text()
        email = self.reg_email_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_input.text()
        
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        try:
            data = self.api_client.register(username, email, password)
            self.login_success.emit(data)
        except Exception as e:
            QMessageBox.critical(self, "Registration Failed", str(e))


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6), facecolor='#0f172a')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def _show_empty(self, message):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        ax.text(0.5, 0.5, message, ha='center', va='center', color='white', fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
    
    def plot_distribution(self, distribution):
        if not distribution:
            self._show_empty("No distribution data available")
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        labels = list(distribution.keys())
        values = list(distribution.values())
        if not values or sum(values) <= 0:
            self._show_empty("No distribution data available")
            return
        colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
        
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors,
               textprops={'color': 'white', 'fontsize': 12})
        ax.set_title('Equipment Type Distribution', color='white', fontsize=14, pad=20)
        self.canvas.draw()
    
    def plot_parameters(self, equipment_data):
        if not equipment_data:
            self._show_empty("No equipment data available")
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        names = [e['equipment_name'] for e in equipment_data]
        flowrates = [e['flowrate'] for e in equipment_data]
        pressures = [e['pressure'] for e in equipment_data]
        temps = [e['temperature'] for e in equipment_data]
        
        x = range(len(names))
        width = 0.25
        
        ax.bar([i - width for i in x], flowrates, width, label='Flowrate', color='#3b82f6')
        ax.bar(x, pressures, width, label='Pressure', color='#8b5cf6')
        ax.bar([i + width for i in x], temps, width, label='Temperature', color='#ec4899')
        
        ax.set_xlabel('Equipment', color='white')
        ax.set_ylabel('Values', color='white')
        ax.set_title('Equipment Parameters Comparison', color='white', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', color='white')
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1e293b', edgecolor='white', labelcolor='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self, api_client, user_data):
        super().__init__()
        self.api_client = api_client
        self.user_data = user_data
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ChemViz Pro - Desktop Application")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0f172a;
                color: white;
            }
            QPushButton {
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                background-color: #3b82f6;
                color: white;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QTableWidget {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 8px;
                color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid #334155;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: white;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
            }
            QGroupBox {
                border: 2px solid #334155;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #60a5fa;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        self.tabs.addTab(self.create_history_tab(), "History")
        main_layout.addWidget(self.tabs)
    
    def create_header(self):
        header = QWidget()
        header.setStyleSheet("background-color: #1e293b; border-radius: 12px; padding: 16px;")
        layout = QHBoxLayout(header)
        
        title = QLabel("ChemViz Pro")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #60a5fa;")
        layout.addWidget(title)
        
        layout.addStretch()

        username = None
        if isinstance(self.user_data, dict):
            username = self.user_data.get('user', {}).get('username') or self.user_data.get('username')
        if not username:
            username = "User"
        user_label = QLabel(f"User: {username}")
        user_label.setStyleSheet("color: #94a3b8; font-size: 14px;")
        layout.addWidget(user_label)
        
        return header
    
    def create_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Upload section
        upload_group = QGroupBox("Upload CSV File")
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #94a3b8;")
        upload_layout.addWidget(self.file_label)
        
        upload_btn = QPushButton("Select File")
        upload_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(upload_btn)
        
        process_btn = QPushButton("Upload & Process")
        process_btn.setStyleSheet("background-color: #10b981;")
        process_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(process_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Statistics
        stats_group = QGroupBox("Summary Statistics")
        self.stats_layout = QFormLayout()
        stats_group.setLayout(self.stats_layout)
        layout.addWidget(stats_group)

        # Report download
        report_layout = QHBoxLayout()
        report_layout.addStretch()
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.setStyleSheet("background-color: #10b981;")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_current_report)
        report_layout.addWidget(self.download_btn)
        layout.addLayout(report_layout)
        
        # Analysis area (charts + table) with resizable splitter
        analysis_splitter = QSplitter(Qt.Vertical)
        analysis_splitter.setStyleSheet("QSplitter::handle { background-color: #1e293b; }")

        charts_container = QWidget()
        charts_layout = QHBoxLayout(charts_container)
        charts_layout.setContentsMargins(0, 0, 0, 0)
        charts_layout.setSpacing(16)
        self.chart1 = ChartWidget()
        self.chart2 = ChartWidget()
        charts_layout.addWidget(self.chart1, 1)
        charts_layout.addWidget(self.chart2, 1)
        analysis_splitter.addWidget(charts_container)

        table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        self.data_table.setMinimumHeight(220)
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.verticalHeader().setDefaultSectionSize(28)
        table_layout.addWidget(self.data_table)
        table_group.setLayout(table_layout)
        analysis_splitter.addWidget(table_group)

        analysis_splitter.setStretchFactor(0, 2)
        analysis_splitter.setStretchFactor(1, 1)

        layout.addWidget(analysis_splitter, 1)
        
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        controls = QHBoxLayout()
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        controls.addWidget(refresh_btn)

        view_btn = QPushButton("View Selected")
        view_btn.setStyleSheet("background-color: #8b5cf6;")
        view_btn.clicked.connect(self.view_selected_history)
        controls.addWidget(view_btn)

        download_btn = QPushButton("Download Report")
        download_btn.setStyleSheet("background-color: #10b981;")
        download_btn.clicked.connect(self.download_selected_report)
        controls.addWidget(download_btn)

        controls.addStretch()
        layout.addLayout(controls)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Filename", "Upload Date", "Total Count", "Avg Flowrate", "Avg Pressure"
        ])
        layout.addWidget(self.history_table)
        
        self.load_history()
        return widget
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, "Error", "Please select a file first")
            return
        
        try:
            dataset = self.api_client.upload_csv(self.selected_file)
            self.current_dataset = dataset
            self.display_dataset(dataset)
            QMessageBox.information(self, "Success", "File uploaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def display_dataset(self, dataset):
        if not isinstance(dataset, dict):
            QMessageBox.critical(self, "Error", "Invalid dataset format received from API.")
            return
        # Clear previous stats
        while self.stats_layout.count():
            child = self.stats_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Display statistics
        self.stats_layout.addRow("Total Equipment:", QLabel(str(dataset.get('total_count', 0))))
        self.stats_layout.addRow("Avg Flowrate:", QLabel(f"{dataset.get('avg_flowrate', 0):.2f}"))
        self.stats_layout.addRow("Avg Pressure:", QLabel(f"{dataset.get('avg_pressure', 0):.2f}"))
        self.stats_layout.addRow("Avg Temperature:", QLabel(f"{dataset.get('avg_temperature', 0):.2f}"))
        
        # Plot charts
        self.chart1.plot_distribution(dataset.get('equipment_distribution') or {})
        
        equipment = dataset.get('equipment') or []
        if equipment:
            self.chart2.plot_parameters(equipment)
            
            # Display table
            self.data_table.setRowCount(len(equipment))
            self.data_table.setColumnCount(5)
            self.data_table.setHorizontalHeaderLabels([
                "Name", "Type", "Flowrate", "Pressure", "Temperature"
            ])
            
            for i, eq in enumerate(equipment):
                self.data_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
                self.data_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
                self.data_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.1f}"))
                self.data_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.1f}"))
                self.data_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.1f}"))
        else:
            self.chart2.plot_parameters([])
            self.data_table.setRowCount(0)
            self.data_table.setColumnCount(0)

        self.download_btn.setEnabled(bool(dataset.get('id')))
    
    def load_history(self):
        try:
            datasets = self.api_client.get_history()
            self.history_table.setRowCount(len(datasets))
            
            for i, ds in enumerate(datasets):
                filename_item = QTableWidgetItem(ds['filename'])
                filename_item.setData(Qt.UserRole, ds['id'])
                self.history_table.setItem(i, 0, filename_item)
                self.history_table.setItem(i, 1, QTableWidgetItem(ds['uploaded_at'][:19]))
                self.history_table.setItem(i, 2, QTableWidgetItem(str(ds['total_count'])))
                self.history_table.setItem(i, 3, QTableWidgetItem(f"{ds['avg_flowrate']:.2f}"))
                self.history_table.setItem(i, 4, QTableWidgetItem(f"{ds['avg_pressure']:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load history: {str(e)}")

    def get_selected_history_id(self):
        row = self.history_table.currentRow()
        if row < 0:
            return None
        item = self.history_table.item(row, 0)
        if not item:
            return None
        return item.data(Qt.UserRole)

    def view_selected_history(self):
        dataset_id = self.get_selected_history_id()
        if not dataset_id:
            QMessageBox.warning(self, "Select Dataset", "Please select a dataset from history.")
            return
        try:
            dataset = self.api_client.get_dataset(dataset_id)
            self.current_dataset = dataset
            self.display_dataset(dataset)
            self.tabs.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {str(e)}")

    def download_current_report(self):
        if not self.current_dataset:
            QMessageBox.warning(self, "No Dataset", "Please upload or select a dataset first.")
            return
        self.download_report(self.current_dataset['id'])

    def download_selected_report(self):
        dataset_id = self.get_selected_history_id()
        if not dataset_id:
            QMessageBox.warning(self, "Select Dataset", "Please select a dataset from history.")
            return
        self.download_report(dataset_id)

    def download_report(self, dataset_id):
        try:
            pdf_bytes = self.api_client.generate_report(dataset_id)
            default_name = f"equipment-report-{dataset_id}.pdf"
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report",
                default_name,
                "PDF Files (*.pdf)"
            )
            if not save_path:
                return
            with open(save_path, 'wb') as f:
                f.write(pdf_bytes)
            QMessageBox.information(self, "Report Saved", f"Report saved to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download report: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    api_client = APIClient()
    
    # Show login window
    login_window = LoginWindow(api_client)
    app_state = {"main_window": None}
    
    def on_login_success(user_data):
        try:
            app_state["main_window"] = MainWindow(api_client, user_data)
            app_state["main_window"].show()
            login_window.hide()
        except Exception as exc:
            QMessageBox.critical(login_window, "Startup Error", f"Failed to open app:\n{exc}")
            login_window.show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
