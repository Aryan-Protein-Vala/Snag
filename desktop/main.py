import sys
import os
import json
import subprocess
import threading
from pynput import keyboard

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame,
                             QLineEdit, QListWidget, QListWidgetItem, QSystemTrayIcon, QMenu, QDialog)
from PyQt6.QtCore import (Qt, QPoint, QSize, QUrl, QTimer, pyqtSignal, QMimeData,
                          QPropertyAnimation, QVariantAnimation, QEasingCurve, pyqtProperty, QRectF)
from PyQt6.QtGui import QFont, QDrag, QGuiApplication, QColor, QIcon, QPixmap, QAction, QPainter, QBrush, QPen, QCursor

# ─── Config ───────────────────────────────────────────────────────────────────
APP_DIR        = os.path.expanduser("~/.config/snag")
LICENSE_FILE   = os.path.join(APP_DIR, "license.json")
SNIPPETS_FILE  = os.path.join(APP_DIR, "snippets.json")
CLIPBOARD_FILE = os.path.join(APP_DIR, "clipboard_history.json")
ASSETS_FILE    = os.path.join(APP_DIR, "assets.json")
HIDDEN_FILE    = os.path.join(APP_DIR, "hidden.json")
SVG_DIR        = os.path.join(APP_DIR, "svgs")
WINDOW_WIDTH   = 340
WINDOW_HEIGHT  = 480

# ─── SVGs ─────────────────────────────────────────────────────────────────────
# Same vector line art as the website!
SVGS = {
    "tab_scrn": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#777" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>''',
    "tab_scrn_active": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#E0E0E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>''',
    "tab_down": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#777" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>''',
    "tab_down_active": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#E0E0E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>''',
    "tab_clip": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#777" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>''',
    "tab_clip_active": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#E0E0E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>''',
    "tab_snip": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#777" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>''',
    "tab_snip_active": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#E0E0E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>''',
    "tab_asset": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#777" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>''',
    "tab_asset_active": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#E0E0E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>''',
    "item_img": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>''',
    "item_file": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>''',
    "item_text": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>''',
    "drag": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>''',
    "drag_hover": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#AAA" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>''',
    "close": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>''',
}

def ensure_svgs():
    os.makedirs(SVG_DIR, exist_ok=True)
    for name, content in SVGS.items():
        with open(os.path.join(SVG_DIR, f"{name}.svg"), "w") as f:
            f.write(content)

def get_icon(name: str) -> QIcon:
    return QIcon(os.path.join(SVG_DIR, f"{name}.svg"))

def get_pixmap(name: str, size: int = 14) -> QPixmap:
    icon = get_icon(name)
    return icon.pixmap(QSize(size, size))

def create_app_icon() -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    painter.setBrush(QBrush(QColor("#111111")))
    painter.setPen(QPen(QColor("#444444"), 3))
    painter.drawRoundedRect(QRectF(4, 4, 56, 56), 12, 12)
    
    painter.setPen(QColor("#EBEBEB"))
    font = QFont("Segoe UI", 26, QFont.Weight.Black)
    painter.setFont(font)
    painter.drawText(QRectF(4, 4, 56, 56), Qt.AlignmentFlag.AlignCenter, "S.")
    
    painter.end()
    return QIcon(pixmap)

# ─── Cross-platform file helpers ─────────────────────────────────────────────
def reveal_in_explorer(file_path: str):
    if not os.path.exists(file_path): return
    if sys.platform == "darwin": subprocess.Popen(["open", "-R", file_path])
    elif sys.platform == "win32": subprocess.Popen(["explorer", "/select,", os.path.normpath(file_path)])
    else: subprocess.Popen(["xdg-open", os.path.dirname(file_path)])

def open_file(file_path: str):
    if not os.path.exists(file_path): return
    if sys.platform == "darwin": subprocess.Popen(["open", file_path])
    elif sys.platform == "win32": os.startfile(os.path.normpath(file_path))
    else: subprocess.Popen(["xdg-open", file_path])


# ─── Universal Item Row (Smooth Bounce Animations + Icons) ───────────────────

class EditDialog(QDialog):
    def __init__(self, parent, title: str, allow_rename: bool = True):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.new_title = title
        self.action = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setStyleSheet("QWidget { background: #1A1A1A; border: 1px solid #333; border-radius: 8px; }")
        clayout = QVBoxLayout(container)
        clayout.setContentsMargins(12, 12, 12, 12)
        clayout.setSpacing(10)
        
        self.input_edit = QLineEdit(title)
        self.input_edit.setStyleSheet("QLineEdit { background: #0D0D0D; color: #E0E0E0; border: 1px solid #333; border-radius: 4px; padding: 6px; }")
        if not allow_rename:
            self.input_edit.setReadOnly(True)
            self.input_edit.setStyleSheet("QLineEdit { background: #111; color: #888; border: 1px solid #222; border-radius: 4px; padding: 6px; }")
        clayout.addWidget(self.input_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("QPushButton { background: #4A1A1A; color: #FF6B6B; border: none; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background: #5A1A1A; }")
        btn_delete.clicked.connect(self._on_delete)
        btn_layout.addWidget(btn_delete)
        
        if allow_rename:
            btn_save = QPushButton("Rename")
            btn_save.setStyleSheet("QPushButton { background: #2A2A2A; color: #E0E0E0; border: none; border-radius: 4px; padding: 6px 12px; font-weight: bold; } QPushButton:hover { background: #3A3A3A; }")
            btn_save.clicked.connect(self._on_save)
            self.input_edit.returnPressed.connect(self._on_save)
            btn_layout.addWidget(btn_save)
            
        clayout.addLayout(btn_layout)
        layout.addWidget(container)
        
    def _on_delete(self):
        self.action = "delete"
        self.accept()
        
    def _on_save(self):
        self.action = "rename"
        self.new_title = self.input_edit.text()
        self.accept()

class UniversalRowWidget(QWidget):
    def __init__(self, title: str, subtitle: str, icon_name: str, file_path: str = None, edit_cb=None, data_ref=None, list_type=None):
        super().__init__()
        self.file_path = file_path
        self.edit_cb = edit_cb
        self.data_ref = data_ref
        self.list_type = list_type
        self.title_val = title
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent; border-radius: 6px;")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        # Padding container for animation
        self.inner_widget = QWidget()
        self.inner_layout = QHBoxLayout(self.inner_widget)
        self.inner_layout.setContentsMargins(4, 10, 4, 10)
        self.inner_layout.setSpacing(8)

        # Icon
        self.icon_lbl = QLabel()
        self.icon_lbl.setPixmap(get_pixmap(icon_name, 16))
        self.inner_layout.addWidget(self.icon_lbl)

        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: #E0E0E0; font-size: 12px; font-weight: 500;")
        text_layout.addWidget(self.title_lbl)
        
        if subtitle:
            self.sub_lbl = QLabel(subtitle)
            self.sub_lbl.setStyleSheet("color: #555; font-size: 10px;")
            text_layout.addWidget(self.sub_lbl)
        
        self.inner_layout.addLayout(text_layout)
        self.inner_layout.addStretch()

        # Hover Actions
        
        self.btn_edit = QPushButton("⋮")
        self.btn_edit.setFixedSize(26, 26)
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.setStyleSheet("QPushButton { background: #2A2A2A; color: #AAA; border: 1px solid #444; border-radius: 5px; font-weight: bold; } QPushButton:hover { background: #3A3A3A; color: #FFF; }")
        self.btn_edit.hide()
        if self.edit_cb:
            self.btn_edit.clicked.connect(lambda: self.edit_cb(self.list_type, self.data_ref, self.title_val))
        self.inner_layout.addWidget(self.btn_edit)

        if self.file_path:
            self.btn_reveal = QPushButton("⇱")
            self.btn_reveal.setFixedSize(26, 26)
            self.btn_reveal.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_reveal.setStyleSheet("""
                QPushButton { background: #2A2A2A; color: #AAA; border: 1px solid #444; border-radius: 5px; font-size: 14px; }
                QPushButton:hover { background: #3A3A3A; color: #FFF; }
            """)
            self.btn_reveal.hide()
            self.btn_reveal.clicked.connect(lambda: reveal_in_explorer(self.file_path))
            self.inner_layout.addWidget(self.btn_reveal)
        else:
            self.drag_hint = QLabel()
            self.drag_hint.setPixmap(get_pixmap("drag", 14))
            self.drag_hint.hide()
            self.inner_layout.addWidget(self.drag_hint)

        self.layout.addWidget(self.inner_widget)

        # Smooth Padding Animation
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.valueChanged.connect(self._update_padding)

    def _update_padding(self, val):
        self.inner_layout.setContentsMargins(val, 10, 4, 10)

    def enterEvent(self, event):
        self.setStyleSheet("background: #262626; border-radius: 6px;")
        if hasattr(self, 'btn_edit') and self.edit_cb: self.btn_edit.show()
        if hasattr(self, 'btn_reveal'):
            self.btn_reveal.show()
        elif hasattr(self, 'drag_hint'):
            self.drag_hint.setPixmap(get_pixmap("drag_hover", 14))
            self.drag_hint.show()
        self.anim.stop()
        self.anim.setStartValue(self.inner_layout.contentsMargins().left())
        self.anim.setEndValue(12)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background: transparent; border-radius: 6px;")
        if hasattr(self, 'btn_edit') and self.edit_cb: self.btn_edit.hide()
        if hasattr(self, 'btn_reveal'):
            self.btn_reveal.hide()
        elif hasattr(self, 'drag_hint'):
            self.drag_hint.hide()
        self.anim.stop()
        self.anim.setStartValue(self.inner_layout.contentsMargins().left())
        self.anim.setEndValue(4)
        self.anim.start()
        super().leaveEvent(event)


class SnagList(QListWidget):
    copy_requested = pyqtSignal(str)

    def __init__(self, is_file_list: bool = False):
        super().__init__()
        self.is_file_list = is_file_list
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(15)
        self.setStyleSheet("""
            QListWidget { background: transparent; border: none; outline: none; }
            QListWidget::item { border-bottom: 1px solid #2A2A2A; padding: 0px; min-height: 48px; }
            QListWidget::item:selected { background: transparent; }
            QScrollBar:vertical { background: #1A1A1A; width: 4px; border-radius: 2px; }
            QScrollBar::handle:vertical { background: #444; border-radius: 2px; }
        """)
        self.itemClicked.connect(self._on_click)
        if is_file_list:
            self.itemDoubleClicked.connect(self._on_double_click)

    def _on_click(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data: return
        self.copy_requested.emit(data["path"] if data["type"] == "file" else data["text"])

    def _on_double_click(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if data and data["type"] == "file":
            open_file(data["path"])

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if not item: return
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data: return
        mime = QMimeData()
        if data["type"] == "file": mime.setUrls([QUrl.fromLocalFile(data["path"])])
        else: mime.setText(data["text"])
        drag = QDrag(self)
        drag.setMimeData(mime)
        
        pixmap = self.itemWidget(item).grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        
        drag.exec(Qt.DropAction.CopyAction)

class AssetList(SnagList):
    def __init__(self, add_cb):
        super().__init__(is_file_list=True)
        self.add_cb = add_cb
        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()
        else: super().dragEnterEvent(event)
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()
        else: super().dragMoveEvent(event)
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            for url in urls:
                if url.isLocalFile(): self.add_cb(url.toLocalFile())
            event.acceptProposedAction()

class DirWatcher(FileSystemEventHandler):
    def __init__(self, cb): self.cb = cb
    def on_any_event(self, event): self.cb()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ensure_svgs()
        
        self.internal_copy_text = None
        self.snippets: list[str] = []
        self.clipboard_history: list[str] = []
        self.assets: list[str] = []
        self.hidden_files: list[str] = []

        self._load_snippets()
        self._load_assets()
        self._load_hidden()
        self._load_clipboard_history()

        self._qt_clipboard = QGuiApplication.clipboard()
        self._qt_clipboard.dataChanged.connect(self._on_clipboard_change)

        self._build_ui()
        self._setup_tray()
        self._start_watchers()
        self._start_hotkey_listener()

    def _setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(create_app_icon()) 
        
        tray_menu = QMenu()
        
        # Tray styling
        tray_menu.setStyleSheet("""
            QMenu { background: #1A1A1A; border: 1px solid #333; color: #E0E0E0; border-radius: 6px; padding: 4px; }
            QMenu::item { padding: 6px 20px; border-radius: 4px; }
            QMenu::item:selected { background: #5ECC7B; color: #111; }
        """)

        show_action = QAction("Open Snag", self)
        show_action.triggered.connect(self.toggle_visibility)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _start_hotkey_listener(self):
        def on_activate():
            try:
                # Force release Alt and X to prevent keys from getting "stuck" when focus is stolen
                ctrl = keyboard.Controller()
                ctrl.release(keyboard.Key.alt)
                ctrl.release(keyboard.Key.alt_l)
                ctrl.release(keyboard.Key.alt_r)
                ctrl.release('x')
            except Exception:
                pass
            QTimer.singleShot(0, self.toggle_visibility)

        def listen():
            # New shortcut: Alt+X (fast, 2 keys, minimal conflicts)
            with keyboard.GlobalHotKeys({'<alt>+x': on_activate}) as h:
                h.join()
        
        self.hotkey_thread = threading.Thread(target=listen, daemon=True)
        self.hotkey_thread.start()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def _upload_asset(self):
        # pyrefly: ignore [missing-import]
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Asset")
        if file_path:
            self._add_asset(file_path)

    def _load_assets(self):
        try:
            with open(ASSETS_FILE, "r") as f:
                self.assets = json.load(f)
        except:
            self.assets = []

    def _save_assets(self):
        with open(ASSETS_FILE, "w") as f:
            json.dump(self.assets, f)

    def _add_asset(self, file_path):
        if file_path not in self.assets:
            self.assets.insert(0, file_path)
            self._save_assets()
            self._refresh_file_lists()

    def _load_snippets(self):
        try:
            with open(SNIPPETS_FILE, "r", encoding="utf-8") as f: self.snippets = json.load(f)
        except: self.snippets = []

    def _save_snippets(self):
        with open(SNIPPETS_FILE, "w", encoding="utf-8") as f: json.dump(self.snippets, f, ensure_ascii=False)

    def _load_clipboard_history(self):
        try:
            with open(CLIPBOARD_FILE, "r", encoding="utf-8") as f: self.clipboard_history = json.load(f)
        except: self.clipboard_history = []

    def _save_clipboard_history(self):
        with open(CLIPBOARD_FILE, "w", encoding="utf-8") as f: json.dump(self.clipboard_history, f, ensure_ascii=False)

    def copy_to_clipboard(self, text: str):
        self.internal_copy_text = text
        self._qt_clipboard.setText(text)
        self._show_toast("✓ Copied")

    def _on_clipboard_change(self):
        new_text = self._qt_clipboard.text().strip()
        if not new_text or new_text == self.internal_copy_text:
            self.internal_copy_text = None
            return
        if self.clipboard_history and self.clipboard_history[0] == new_text: return
        
        self.clipboard_history.insert(0, new_text)
        if len(self.clipboard_history) > 15: self.clipboard_history.pop()
        self._save_clipboard_history()
        self._refresh_clipboard_ui()

    def _start_watchers(self):
        self.observer = Observer()
        handler = DirWatcher(lambda: QTimer.singleShot(0, self._refresh_file_lists))
        for p in [os.path.expanduser("~/Downloads"), os.path.expanduser("~/Desktop"), os.path.expanduser("~/Pictures/Screenshots")]:
            if os.path.exists(p): self.observer.schedule(handler, p, recursive=False)
        self.observer.start()

    def _show_toast(self, msg: str):
        self._toast.setText(msg)
        self._toast.show()
        QTimer.singleShot(1500, self._toast.hide)

    def _build_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - WINDOW_WIDTH - 20, screen.height() - WINDOW_HEIGHT - 20)

        self.setStyleSheet("QMainWindow { background: transparent; border: none; }")

        root = QWidget(self)
        root.setStyleSheet("QWidget { background: transparent; border: none; }")
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(1, 1, 1, 1) # Tiny margin to avoid clipping bounds

        self._card = QFrame()
        self._card.setStyleSheet("QFrame { background-color: #1A1A1A; border-radius: 14px; border: none; }")
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(14, 10, 14, 12)
        card_layout.setSpacing(8)
        root_layout.addWidget(self._card)

        # Top bar
        top_bar = QHBoxLayout()
        logo = QLabel("snag.")
        logo.setStyleSheet("color:#C8C8C8; font-size:13px; font-weight:700; letter-spacing:1px;")
        
        btn_close = QPushButton()
        btn_close.setIcon(get_icon("close"))
        btn_close.setFixedSize(22, 22)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background:transparent; border:none; border-radius:11px; } QPushButton:hover { background:#E05050; }")
        btn_close.clicked.connect(self.hide)
        
        top_bar.addWidget(logo)
        top_bar.addStretch()
        top_bar.addWidget(btn_close)
        card_layout.addLayout(top_bar)

        if not self._is_licensed(): self._build_license_gate(card_layout)
        else: self._build_main(card_layout)

        # Toast
        self._toast = QLabel(self)
        self._toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._toast.setStyleSheet("QLabel { background: #2E2E2E; color: #DDDDDD; border: 1px solid #444; border-radius: 8px; padding: 4px 14px; font-size: 11px; font-weight: 600; }")
        self._toast.resize(110, 26)
        self._toast.move((WINDOW_WIDTH - 110) // 2, WINDOW_HEIGHT - 44)
        self._toast.hide()

    def _is_licensed(self) -> bool:
        try:
            with open(LICENSE_FILE, "r") as f: return json.load(f).get("is_active", False)
        except: return False

    def _build_license_gate(self, parent_layout):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Activate Snag")
        title.setStyleSheet("color:#E0E0E0; font-size:22px; font-weight:700;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._key_input = QLineEdit()
        self._key_input.setPlaceholderText("SNAG-XXXX-XXXX-XXXX")
        self._key_input.setStyleSheet("QLineEdit { background:#0D0D0D; color:#E0E0E0; border:1px solid #333; border-radius:7px; padding:10px 12px; font-size:13px; } QLineEdit:focus { border:1px solid #555; }")
        btn = QPushButton("Activate")
        btn.setStyleSheet("QPushButton { background:#E0E0E0; color:#111; border-radius:7px; padding:10px; font-weight:700; font-size:13px; } QPushButton:hover { background:#fff; }")
        btn.clicked.connect(self._activate)
        self._key_input.returnPressed.connect(self._activate)
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self._key_input)
        layout.addWidget(btn)
        parent_layout.addWidget(container)
        self._gate_widget = container

    def _activate(self):
        key = self._key_input.text().strip()
        if len(key) >= 16:
            with open(LICENSE_FILE, "w") as f: json.dump({"is_active": True, "key": key}, f)
            self._gate_widget.setParent(None)
            self._build_main(self._card.layout())

    def _build_main(self, parent_layout):
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(8)
        self._tab_btns: list[QPushButton] = []
        tab_ids = ["scrn", "down", "clip", "snip", "asset"]

        for i, tid in enumerate(tab_ids):
            btn = QPushButton()
            btn.setIcon(get_icon(f"tab_{tid}"))
            btn.setIconSize(QSize(16, 16))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: none; padding: 6px 4px; border-bottom: 2px solid transparent; }
                QPushButton:checked { border-bottom: 2px solid #888; }
            """)
            btn.clicked.connect(lambda _, idx=i: self._switch_tab(idx))
            self._tab_btns.append(btn)
            tab_bar.addWidget(btn)
        tab_bar.addStretch()
        parent_layout.addLayout(tab_bar)

        self._pages = QStackedWidget()

        self._list_screenshots = SnagList(is_file_list=True)
        self._list_screenshots.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_screenshots)

        self._list_downloads = SnagList(is_file_list=True)
        self._list_downloads.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_downloads)

        self._list_clipboard = SnagList()
        self._list_clipboard.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_clipboard)

        snip_page = QWidget()
        snip_layout = QVBoxLayout(snip_page)
        snip_layout.setContentsMargins(0, 0, 0, 0)
        snip_layout.setSpacing(6)
        self._snip_input = QLineEdit()
        self._snip_input.setPlaceholderText("Type a snippet and press Enter…")
        self._snip_input.setStyleSheet("QLineEdit { background:#0D0D0D; color:#E0E0E0; border:1px solid #333; border-radius:7px; padding:8px 10px; font-size:12px; } QLineEdit:focus { border:1px solid #555; }")
        self._snip_input.returnPressed.connect(self._add_snippet)
        self._list_snippets = SnagList()
        self._list_snippets.copy_requested.connect(self.copy_to_clipboard)
        snip_layout.addWidget(self._snip_input)
        snip_layout.addWidget(self._list_snippets)
        self._pages.addWidget(snip_page)

        # Assets page
        asset_page = QWidget()
        asset_layout = QVBoxLayout(asset_page)
        asset_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_add_asset = QPushButton("  Upload / Pin File")
        btn_add_asset.setIcon(get_icon("item_file"))
        btn_add_asset.setStyleSheet("QPushButton { background: #2A2A2A; color: #E0E0E0; border: none; border-radius: 6px; padding: 10px; margin: 4px; font-weight: bold; font-size: 11px; } QPushButton:hover { background: #383838; }")
        btn_add_asset.clicked.connect(self._upload_asset)
        asset_layout.addWidget(btn_add_asset)
        
        self._list_assets = AssetList(self._add_asset)
        asset_layout.addWidget(self._list_assets)
        self._pages.addWidget(asset_page)

        parent_layout.addWidget(self._pages)
        
        bottom_hint = QLabel("(Alt+X to toggle)")
        bottom_hint.setStyleSheet("color:#555555; font-size:10px;")
        bottom_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(bottom_hint)

        self._switch_tab(0, animate=False)
        self._refresh_file_lists()
        self._refresh_clipboard_ui()
        self._refresh_snippets_ui()

    def _switch_tab(self, index: int, animate=True):
        for i, btn in enumerate(self._tab_btns):
            tid = ["scrn", "down", "clip", "snip", "asset"][i]
            btn.setChecked(i == index)
            btn.setIcon(get_icon(f"tab_{tid}_active" if i == index else f"tab_{tid}"))
            
        self._pages.setCurrentIndex(index)

    def _get_recent_files(self, directory: str, count: int = 10) -> list[str]:
        if not os.path.exists(directory): return []
        files = [os.path.join(directory, n) for n in os.listdir(directory) if os.path.isfile(os.path.join(directory, n))]
        files.sort(key=os.path.getmtime, reverse=True)
        return files[:count]

    def _add_item_row(self, list_widget: SnagList, title: str, subtitle: str, icon_name: str, file_path: str = None, data_val: str = None, list_type: str = None):
        item = QListWidgetItem()
        if file_path:
            item.setData(Qt.ItemDataRole.UserRole, {"type": "file", "path": file_path})
        else:
            item.setData(Qt.ItemDataRole.UserRole, {"type": "text", "text": data_val})

        row = UniversalRowWidget(title, subtitle, icon_name, file_path, edit_cb=self._on_edit_item, data_ref=(file_path if file_path else data_val), list_type=list_type)
        item.setSizeHint(QSize(WINDOW_WIDTH - 30, 48))
        list_widget.addItem(item)
        list_widget.setItemWidget(item, row)

    
    def _load_hidden(self):
        try:
            with open(HIDDEN_FILE, "r") as f: self.hidden_files = json.load(f)
        except: self.hidden_files = []
        
    def _save_hidden(self):
        with open(HIDDEN_FILE, "w") as f: json.dump(self.hidden_files, f)
        
    def _on_edit_item(self, list_type, data_ref, title):
        allow_rename = list_type in ["downloads", "screenshots"]
        dlg = EditDialog(self, title, allow_rename)
        dlg.move(QCursor.pos())
        if dlg.exec():
            if dlg.action == "delete":
                if list_type in ["downloads", "screenshots"]:
                    if data_ref not in self.hidden_files:
                        self.hidden_files.append(data_ref)
                        self._save_hidden()
                elif list_type == "assets":
                    if data_ref in self.assets:
                        self.assets.remove(data_ref)
                        self._save_assets()
                elif list_type == "snippets":
                    if data_ref in self.snippets:
                        self.snippets.remove(data_ref)
                        with open(SNIPPETS_FILE, "w", encoding="utf-8") as f: json.dump(self.snippets, f)
                elif list_type == "clipboard":
                    if data_ref in self.clipboard_history:
                        self.clipboard_history.remove(data_ref)
                        with open(CLIPBOARD_FILE, "w", encoding="utf-8") as f: json.dump(self.clipboard_history, f)
            elif dlg.action == "rename" and allow_rename:
                new_path = os.path.join(os.path.dirname(data_ref), dlg.new_title)
                if new_path != data_ref:
                    try:
                        os.rename(data_ref, new_path)
                    except:
                        pass
            
            self._refresh_file_lists()
            self._refresh_clipboard_ui()
            self._refresh_snippets_ui()

    def _refresh_file_lists(self):
        if not hasattr(self, "_list_downloads"): return
        
        self._list_assets.clear()
        for f in self.assets:
            if os.path.exists(f):
                self._add_item_row(self._list_assets, os.path.basename(f), "Pinned Asset", "item_file", file_path=f, list_type="assets")
                
        self._list_downloads.clear()
        for f in self._get_recent_files(os.path.expanduser("~/Downloads")):
            if f not in self.hidden_files: self._add_item_row(self._list_downloads, os.path.basename(f), "Recently Added", "item_file", file_path=f, list_type="downloads")

        sc_dirs = [
            os.path.expanduser("~/Desktop"), 
            os.path.expanduser("~/Pictures/Screenshots"),
            os.path.expanduser("~/OneDrive/Desktop"),
            os.path.expanduser("~/OneDrive/Pictures/Screenshots")
        ]
        images = []
        for d in sc_dirs:
            if os.path.exists(d): images.extend([os.path.join(d, n) for n in os.listdir(d) if n.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))])
        images.sort(key=os.path.getmtime, reverse=True)
        self._list_screenshots.clear()
        for f in images[:10]:
            if f not in self.hidden_files: self._add_item_row(self._list_screenshots, os.path.basename(f), "Recently Saved", "item_img", file_path=f, list_type="screenshots")

    def _refresh_clipboard_ui(self):
        if not hasattr(self, "_list_clipboard"): return
        self._list_clipboard.clear()
        for text in self.clipboard_history:
            preview = text.replace("\n", " ").strip()
            if len(preview) > 42: preview = preview[:42] + "…"
            self._add_item_row(self._list_clipboard, preview, "Copied text", "item_text", data_val=text, list_type="clipboard")

    def _add_snippet(self):
        text = self._snip_input.text().strip()
        if text:
            self.snippets.insert(0, text)
            self._save_snippets()
            self._refresh_snippets_ui()
            self._snip_input.clear()

    def _refresh_snippets_ui(self):
        if not hasattr(self, "_list_snippets"): return
        self._list_snippets.clear()
        for s in self.snippets:
            preview = s.replace("\n", " ").strip()
            if len(preview) > 42: preview = preview[:42] + "…"
            self._add_item_row(self._list_snippets, preview, "Pinned snippet", "item_text", data_val=s)

    def _quit(self):
        if hasattr(self, "observer"):
            self.observer.stop()
            self.observer.join()
        QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_drag_pos"):
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._drag_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QFont("Segoe UI", 10))
    app.setWindowIcon(create_app_icon())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
