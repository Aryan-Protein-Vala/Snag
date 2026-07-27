import sys
import os
import json
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame,
                             QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt6.QtCore import Qt, QPoint, QSize, QUrl, QTimer, pyqtSignal, QObject, QMimeData
from PyQt6.QtGui import QColor, QFont, QDrag, QCursor

# --- Configurations ---
APP_DIR = os.path.expanduser("~/.config/snag")
LICENSE_FILE = os.path.join(APP_DIR, "license.json")
SNIPPETS_FILE = os.path.join(APP_DIR, "snippets.json")
WINDOW_WIDTH = 340
WINDOW_HEIGHT = 480

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: #E0E0E0;
                padding: 10px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:hover {
                background-color: #2A2A2A;
                border-radius: 6px;
            }
        """)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item: return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        
        data = item.data(Qt.ItemDataRole.UserRole)
        
        if data and data.get("type") == "file":
            url = QUrl.fromLocalFile(data["path"])
            mimeData.setUrls([url])
        else:
            mimeData.setText(item.text())
            
        drag.setMimeData(mimeData)
        drag.exec(Qt.DropAction.CopyAction)


class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    def on_any_event(self, event):
        self.callback()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clipboard_history = []
        self.snippets = []
        self.load_snippets()
        
        self.initUI()
        
        # Setup Watchdog for Downloads and Screenshots
        self.setup_watchers()
        
        # Setup Clipboard Timer
        self.clip_timer = QTimer(self)
        self.clip_timer.timeout.connect(self.check_clipboard)
        self.clip_timer.start(1000)
        
    def setup_watchers(self):
        self.observer = Observer()
        self.watchdog_handler = WatchdogHandler(self.refresh_files)
        
        paths_to_watch = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures/Screenshots")
        ]
        
        for p in paths_to_watch:
            if os.path.exists(p):
                self.observer.schedule(self.watchdog_handler, p, recursive=False)
        
        self.observer.start()

    def refresh_files(self):
        # We must use QTimer.singleShot to ensure UI updates run on main thread
        QTimer.singleShot(0, self.update_file_lists)

    def load_snippets(self):
        os.makedirs(APP_DIR, exist_ok=True)
        if os.path.exists(SNIPPETS_FILE):
            try:
                with open(SNIPPETS_FILE, 'r') as f:
                    self.snippets = json.load(f)
            except:
                self.snippets = []

    def save_snippets(self):
        with open(SNIPPETS_FILE, 'w') as f:
            json.dump(self.snippets, f)

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - WINDOW_WIDTH - 20
        y = screen.height() - WINDOW_HEIGHT - 20
        self.move(x, y)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.bg_container = QFrame()
        self.bg_container.setObjectName("bgContainer")
        self.bg_container.setStyleSheet("""
            #bgContainer {
                background-color: #1A1A1A;
                border-radius: 12px;
                border: 1px solid #333333;
                background-image: url('noise.png'); /* Fallback grain if we had one */
            }
        """)
        
        self.bg_layout = QVBoxLayout(self.bg_container)
        self.bg_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.addWidget(self.bg_container)
        
        # --- GLOBAL HEADER (CLOSE BUTTON) ---
        self.header_top = QHBoxLayout()
        self.header_top.setContentsMargins(0,0,0,0)
        self.header_top.addStretch()
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(24, 24)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #808080;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 12px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #FF5555;
            }
        """)
        self.btn_close.clicked.connect(self.close_app)
        self.header_top.addWidget(self.btn_close)
        self.bg_layout.addLayout(self.header_top)
        
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

    def close_app(self):
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        QApplication.quit()

    def show_licensing_gate(self):
        gate_widget = QWidget()
        layout = QVBoxLayout(gate_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Activate Snag")
        title.setStyleSheet("color: #E0E0E0; font-size: 24px; font-weight: bold; font-family: 'SF Pro', sans-serif;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("SNAG-XXXX-XXXX-XXXX")
        self.key_input.setStyleSheet("""
            QLineEdit { background-color: #0A0A0A; color: #E0E0E0; border: 1px solid #333333; border-radius: 6px; padding: 10px; font-size: 14px;}
            QLineEdit:focus { border: 1px solid #555555; }
        """)
        
        btn_activate = QPushButton("Activate")
        btn_activate.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; color: #1A1A1A; border-radius: 6px; padding: 10px; font-weight: bold; margin-top: 10px; }
            QPushButton:hover { background-color: #FFFFFF; }
        """)
        btn_activate.clicked.connect(self.activate_license)
        
        layout.addWidget(title)
        layout.addWidget(self.key_input)
        layout.addWidget(btn_activate)
        
        self.bg_layout.addWidget(gate_widget)
        self.current_view = gate_widget

    def activate_license(self):
        key = self.key_input.text().strip()
        if len(key) >= 16:
            with open(LICENSE_FILE, 'w') as f:
                json.dump({"is_active": True, "key": key}, f)
            self.current_view.setParent(None)
            self.show_main_interface()

    def show_main_interface(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header Tabs
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        tabs = ["Scrn", "Down", "Clip", "Snip"]
        self.tab_buttons = []
        for i, tab in enumerate(tabs):
            btn = QPushButton(tab)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background-color: transparent; color: #808080; border: none; font-size: 13px; font-weight: bold; padding: 8px;}
                QPushButton:hover { color: #E0E0E0; }
                QPushButton:checked { color: #FFFFFF; border-bottom: 2px solid #FFFFFF; }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            self.tab_buttons.append(btn)
            header_layout.addWidget(btn)
        
        layout.addLayout(header_layout)
        
        # Content Area
        self.stacked_widget = QStackedWidget()
        
        # 0. Screenshots Tab
        self.list_screenshots = DraggableListWidget()
        self.stacked_widget.addWidget(self.list_screenshots)
        
        # 1. Downloads Tab
        self.list_downloads = DraggableListWidget()
        self.stacked_widget.addWidget(self.list_downloads)
        
        # 2. Clipboard Tab
        self.list_clipboard = DraggableListWidget()
        self.stacked_widget.addWidget(self.list_clipboard)
        
        # 3. Snippets Tab
        snippet_widget = QWidget()
        s_layout = QVBoxLayout(snippet_widget)
        s_layout.setContentsMargins(0,0,0,0)
        
        self.snippet_input = QLineEdit()
        self.snippet_input.setPlaceholderText("Add a snippet...")
        self.snippet_input.setStyleSheet("QLineEdit { background-color: #0A0A0A; color: #E0E0E0; border: 1px solid #333333; border-radius: 6px; padding: 8px; }")
        self.snippet_input.returnPressed.connect(self.add_snippet)
        s_layout.addWidget(self.snippet_input)
        
        self.list_snippets = DraggableListWidget()
        s_layout.addWidget(self.list_snippets)
        self.stacked_widget.addWidget(snippet_widget)
        
        layout.addWidget(self.stacked_widget)
        
        self.bg_layout.addWidget(main_widget)
        self.current_view = main_widget
        
        self.switch_tab(0)
        self.update_file_lists()
        self.update_snippets_list()

    def switch_tab(self, index):
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        self.stacked_widget.setCurrentIndex(index)

    def get_latest_files(self, directory, count=10):
        if not os.path.exists(directory): return []
        files = [os.path.join(directory, f) for f in os.listdir(directory)]
        files = [f for f in files if os.path.isfile(f)]
        files.sort(key=os.path.getmtime, reverse=True)
        return files[:count]

    def update_file_lists(self):
        if not hasattr(self, 'list_downloads'): return
        
        # Downloads
        dl_dir = os.path.expanduser("~/Downloads")
        self.list_downloads.clear()
        for f in self.get_latest_files(dl_dir):
            item = QListWidgetItem(os.path.basename(f))
            item.setData(Qt.ItemDataRole.UserRole, {"type": "file", "path": f})
            self.list_downloads.addItem(item)
            
        # Screenshots
        sc_dirs = [os.path.expanduser("~/Desktop"), os.path.expanduser("~/Pictures/Screenshots")]
        all_sc = []
        for d in sc_dirs:
            if os.path.exists(d):
                all_sc.extend([os.path.join(d, f) for f in os.listdir(d) if "screenshot" in f.lower() or f.endswith(('.png', '.jpg'))])
        all_sc.sort(key=os.path.getmtime, reverse=True)
        self.list_screenshots.clear()
        for f in all_sc[:10]:
            item = QListWidgetItem(os.path.basename(f))
            item.setData(Qt.ItemDataRole.UserRole, {"type": "file", "path": f})
            self.list_screenshots.addItem(item)

    def check_clipboard(self):
        try:
            text = pyperclip.paste()
            if text and (not self.clipboard_history or self.clipboard_history[0] != text):
                self.clipboard_history.insert(0, text)
                if len(self.clipboard_history) > 15:
                    self.clipboard_history.pop()
                self.update_clipboard_list()
        except:
            pass

    def update_clipboard_list(self):
        if not hasattr(self, 'list_clipboard'): return
        self.list_clipboard.clear()
        for t in self.clipboard_history:
            item = QListWidgetItem(t.replace('\\n', ' ')[:50] + "...")
            item.setData(Qt.ItemDataRole.UserRole, {"type": "text"})
            self.list_clipboard.addItem(item)

    def add_snippet(self):
        text = self.snippet_input.text().strip()
        if text:
            self.snippets.insert(0, text)
            self.save_snippets()
            self.update_snippets_list()
            self.snippet_input.clear()

    def update_snippets_list(self):
        self.list_snippets.clear()
        for s in self.snippets:
            item = QListWidgetItem(s)
            item.setData(Qt.ItemDataRole.UserRole, {"type": "text"})
            self.list_snippets.addItem(item)

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
    font = QFont("SF Pro", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
