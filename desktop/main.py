import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame,
                             QLineEdit)
from PyQt6.QtCore import Qt, QPoint, QSize, QUrl
from PyQt6.QtGui import QColor, QPalette, QIcon, QFont, QPainter, QPainterPath, QBrush, QPixmap

# --- Configurations ---
APP_DIR = os.path.expanduser("~/.config/snag")
LICENSE_FILE = os.path.join(APP_DIR, "license.json")
WINDOW_WIDTH = 340
WINDOW_HEIGHT = 480

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Window properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Position at bottom right
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - WINDOW_WIDTH - 20
        y = screen.height() - WINDOW_HEIGHT - 20
        self.move(x, y)

        # Main Central Widget (rounded corners)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background Container
        self.bg_container = QFrame()
        self.bg_container.setObjectName("bgContainer")
        self.bg_container.setStyleSheet("""
            #bgContainer {
                background-color: #1A1A1A;
                border-radius: 12px;
                border: 1px solid #333333;
            }
        """)
        
        self.bg_layout = QVBoxLayout(self.bg_container)
        self.bg_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.addWidget(self.bg_container)
        
        # Check License
        if not self.check_license():
            self.show_licensing_gate()
        else:
            self.show_main_interface()

    def check_license(self):
        if not os.path.exists(APP_DIR):
            os.makedirs(APP_DIR, exist_ok=True)
        if os.path.exists(LICENSE_FILE):
            try:
                with open(LICENSE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get("is_active", False)
            except:
                return False
        return False

    def show_licensing_gate(self):
        gate_widget = QWidget()
        layout = QVBoxLayout(gate_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Activate Snag")
        title.setStyleSheet("color: #E0E0E0; font-size: 24px; font-weight: bold; font-family: 'SF Pro', sans-serif;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Enter your 16-character license key")
        subtitle.setStyleSheet("color: #808080; font-size: 13px; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("SNAG-XXXX-XXXX-XXXX")
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: #0A0A0A;
                color: #E0E0E0;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                letter-spacing: 1px;
            }
            QLineEdit:focus {
                border: 1px solid #555555;
            }
        """)
        
        btn_activate = QPushButton("Activate")
        btn_activate.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_activate.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                color: #1A1A1A;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #FFFFFF;
            }
        """)
        btn_activate.clicked.connect(self.activate_license)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.key_input)
        layout.addWidget(btn_activate)
        
        self.bg_layout.addWidget(gate_widget)
        self.current_view = gate_widget

    def show_main_interface(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Header Tabs
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        # Mocking tabs with buttons
        tabs = ["Screenshots", "Downloads", "Clipboard", "Snippets"]
        for tab in tabs:
            btn = QPushButton(tab[:4]) # Just short names for now
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #808080;
                    border: none;
                    font-size: 12px;
                    padding: 5px;
                }
                QPushButton:hover {
                    color: #E0E0E0;
                }
            """)
            header_layout.addWidget(btn)
        
        layout.addLayout(header_layout)
        
        # Content Area
        self.stacked_widget = QStackedWidget()
        # Mock empty content
        content = QLabel("Content Area")
        content.setStyleSheet("color: #E0E0E0; font-size: 14px;")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(content)
        
        layout.addWidget(self.stacked_widget)
        
        self.bg_layout.addWidget(main_widget)
        self.current_view = main_widget

    def activate_license(self):
        key = self.key_input.text().strip()
        if len(key) >= 16: # basic validation
            # Here we would normally make API call to activate
            with open(LICENSE_FILE, 'w') as f:
                json.dump({"is_active": True, "key": key}, f)
            
            # Switch to main interface
            self.current_view.setParent(None)
            self.show_main_interface()

    # Allow dragging window if clicking on empty space
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Global Font
    font = QFont("SF Pro", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
