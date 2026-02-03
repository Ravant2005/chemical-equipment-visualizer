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
                              QFormLayout, QStackedWidget, QInputDialog, QLineEdit)
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
            # Default to a production placeholder — replace with your actual backend URL.
            self.base_url = os.environ.get('CHEMVIZ_API_URL', 'https://your-backend.railway.app/api')
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = f"Token {token}"
    
    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.set_token(data['token'])
            return data
        raise Exception(response.json().get('error', 'Login failed'))
    
    def register(self, username, email, password):
        response = requests.post(
            f"{self.base_url}/auth/register/",
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
                f"{self.base_url}/datasets/upload/",
                files=files,
                headers={"Authorization": f"Token {self.token}"}
            )
        if response.status_code == 201:
            return response.json()
        raise Exception(response.json().get('error', 'Upload failed'))
    
    def get_history(self):
        response = requests.get(
            f"{self.base_url}/datasets/history/",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to fetch history")
    
    def get_dataset(self, dataset_id):
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to fetch dataset")


class LoginWindow(QWidget):
    """Login/Register window with API URL configuration"""
    login_success = pyqtSignal(dict)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ChemViz Pro - Login")
        self.setGeometry(100, 100, 400, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
            QPushButton {
                padding: 14px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            #loginBtn {
                background-color: #3b82f6;
                color: white;
            }
            #loginBtn:hover {
                background-color: #2563eb;
            }
            #registerBtn {
                background-color: #8b5cf6;
                color: white;
            }
            #registerBtn:hover {
                background-color: #7c3aed;
            }
            #settingsBtn {
                background-color: #475569;
                color: white;
                font-size: 12px;
                padding: 8px;
            }
            #settingsBtn:hover {
                background-color: #64748b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Title
        title = QLabel("ChemViz Pro")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #60a5fa; margin-bottom: 10px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Equipment Analytics Platform")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #94a3b8; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Settings button for API URL
        settings_btn = QPushButton("⚙️ Configure API URL")
        settings_btn.setObjectName("settingsBtn")
        settings_btn.setToolTip("Click to set your backend API URL")
        settings_btn.clicked.connect(self.configure_api_url)
        layout.addWidget(settings_btn)
        
        # API URL display
        self.api_url_label = QLabel(f"API: {self.api_client.base_url}")
        self.api_url_label.setAlignment(Qt.AlignCenter)
        self.api_url_label.setStyleSheet("color: #64748b; font-size: 11px; margin-bottom: 10px;")
        self.api_url_label.setWordWrap(True)
        layout.addWidget(self.api_url_label)
        
        # Form
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (for registration)")
        layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Buttons
        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginBtn")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        register_btn = QPushButton("Register")
        register_btn.setObjectName("registerBtn")
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def configure_api_url(self):
        """Allow user to configure API URL"""
        api_url, ok = QInputDialog.getText(
            self,
            "Configure API URL",
            "Enter your backend API URL:",
            QLineEdit.Normal,
            self.api_client.base_url
        )
        
        if ok and api_url:
            # Remove trailing slash if present
            api_url = api_url.rstrip('/')
            # Add /api if not present
            if not api_url.endswith('/api'):
                api_url = f"{api_url}/api"
            
            self.api_client.base_url = api_url
            self.api_url_label.setText(f"API: {api_url}")
            QMessageBox.information(self, "API URL Updated", f"API URL set to:\n{api_url}")
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        try:
            data = self.api_client.login(username, password)
            self.login_success.emit(data)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", str(e))
    
    def handle_register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        try:
            data = self.api_client.register(username, email, password)
            self.login_success.emit(data)
            self.close()
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
    
    def plot_distribution(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        labels = list(distribution.keys())
        values = list(distribution.values())
        colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
        
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors,
               textprops={'color': 'white', 'fontsize': 12})
        ax.set_title('Equipment Type Distribution', color='white', fontsize=14, pad=20)
        self.canvas.draw()
    
    def plot_parameters(self, equipment_data):
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
        tabs = QTabWidget()
        tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        tabs.addTab(self.create_history_tab(), "History")
        main_layout.addWidget(tabs)
    
    def create_header(self):
        header = QWidget()
        header.setStyleSheet("background-color: #1e293b; border-radius: 12px; padding: 16px;")
        layout = QHBoxLayout(header)
        
        title = QLabel("ChemViz Pro")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #60a5fa;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"User: {self.user_data['user']['username']}")
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
        
        # Charts
        charts_layout = QHBoxLayout()
        self.chart1 = ChartWidget()
        self.chart2 = ChartWidget()
        charts_layout.addWidget(self.chart1)
        charts_layout.addWidget(self.chart2)
        layout.addLayout(charts_layout)
        
        # Data table
        table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        table_layout.addWidget(self.data_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
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
        # Clear previous stats
        while self.stats_layout.count():
            child = self.stats_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Display statistics
        self.stats_layout.addRow("Total Equipment:", QLabel(str(dataset['total_count'])))
        self.stats_layout.addRow("Avg Flowrate:", QLabel(f"{dataset['avg_flowrate']:.2f}"))
        self.stats_layout.addRow("Avg Pressure:", QLabel(f"{dataset['avg_pressure']:.2f}"))
        self.stats_layout.addRow("Avg Temperature:", QLabel(f"{dataset['avg_temperature']:.2f}"))
        
        # Plot charts
        if dataset['equipment_distribution']:
            self.chart1.plot_distribution(dataset['equipment_distribution'])
        
        if dataset.get('equipment'):
            self.chart2.plot_parameters(dataset['equipment'])
            
            # Display table
            equipment = dataset['equipment']
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
    
    def load_history(self):
        try:
            datasets = self.api_client.get_history()
            self.history_table.setRowCount(len(datasets))
            
            for i, ds in enumerate(datasets):
                self.history_table.setItem(i, 0, QTableWidgetItem(ds['filename']))
                self.history_table.setItem(i, 1, QTableWidgetItem(ds['uploaded_at'][:19]))
                self.history_table.setItem(i, 2, QTableWidgetItem(str(ds['total_count'])))
                self.history_table.setItem(i, 3, QTableWidgetItem(f"{ds['avg_flowrate']:.2f}"))
                self.history_table.setItem(i, 4, QTableWidgetItem(f"{ds['avg_pressure']:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load history: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    api_client = APIClient()
    
    # Show login window
    login_window = LoginWindow(api_client)
    
    def on_login_success(user_data):
        main_window = MainWindow(api_client, user_data)
        main_window.show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()