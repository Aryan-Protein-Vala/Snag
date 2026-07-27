import sys
import os
import json
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame,
                             QLineEdit, QListWidget, QListWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt, QPoint, QSize, QUrl, QTimer, pyqtSignal, QMimeData
from PyQt6.QtGui import QFont, QDrag, QGuiApplication, QPalette, QColor

# ─── Config ───────────────────────────────────────────────────────────────────
APP_DIR        = os.path.expanduser("~/.config/snag")
LICENSE_FILE   = os.path.join(APP_DIR, "license.json")
SNIPPETS_FILE  = os.path.join(APP_DIR, "snippets.json")
CLIPBOARD_FILE = os.path.join(APP_DIR, "clipboard_history.json")
WINDOW_WIDTH   = 340
WINDOW_HEIGHT  = 480

# ─── Cross-platform file helpers ─────────────────────────────────────────────
def reveal_in_explorer(file_path: str):
    if not os.path.exists(file_path):
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", "-R", file_path])
    elif sys.platform == "win32":
        subprocess.Popen(["explorer", "/select,", os.path.normpath(file_path)])
    else:  # Linux: open parent dir
        subprocess.Popen(["xdg-open", os.path.dirname(file_path)])

def open_file(file_path: str):
    if not os.path.exists(file_path):
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", file_path])
    elif sys.platform == "win32":
        os.startfile(os.path.normpath(file_path))
    else:
        subprocess.Popen(["xdg-open", file_path])


# ─── File Row Widget (hover → reveal button appears) ─────────────────────────
class FileRowWidget(QWidget):
    revealed = pyqtSignal()

    def __init__(self, filename: str, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 6, 8)
        layout.setSpacing(6)

        # Icon label based on extension
        ext = os.path.splitext(filename)[1].lower()
        icon = "🖼" if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp") else "📄"
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size:14px; background: transparent;")
        icon_lbl.setFixedWidth(20)

        self.name_lbl = QLabel(filename)
        self.name_lbl.setStyleSheet(
            "color: #E0E0E0; font-size: 12px; background: transparent;"
        )
        self.name_lbl.setWordWrap(False)

        self.btn_reveal = QPushButton("⇱")
        self.btn_reveal.setToolTip("Reveal in Explorer / Finder")
        self.btn_reveal.setFixedSize(26, 26)
        self.btn_reveal.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reveal.setStyleSheet("""
            QPushButton {
                background: #2A2A2A;
                color: #AAAAAA;
                border: 1px solid #444;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover { background: #3A3A3A; color: #FFFFFF; }
        """)
        self.btn_reveal.hide()
        self.btn_reveal.clicked.connect(lambda: reveal_in_explorer(self.file_path))

        self.main_layout = layout
        layout.addWidget(icon_lbl)
        layout.addWidget(self.name_lbl, 1)
        layout.addWidget(self.btn_reveal)

    def enterEvent(self, event):
        self.btn_reveal.show()
        self.setStyleSheet("background: #262626; border-radius: 6px;")
        self.main_layout.setContentsMargins(16, 8, 12, 8) # Bounce right effect
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.btn_reveal.hide()
        self.setStyleSheet("background: transparent;")
        self.main_layout.setContentsMargins(10, 8, 6, 8) # Revert bounce
        super().leaveEvent(event)


# ─── Draggable List ────────────────────────────────────────────────────────────
class SnagList(QListWidget):
    copy_requested = pyqtSignal(str)

    def __init__(self, is_file_list: bool = False):
        super().__init__()
        self.is_file_list = is_file_list
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: #E0E0E0;
                background: transparent;
                border-bottom: 1px solid #2A2A2A;
                padding: 0px;
                min-height: 38px;
            }
            QListWidget::item:selected {
                background: #2C2C2C;
                border-radius: 6px;
            }
            QScrollBar:vertical {
                background: #1A1A1A;
                width: 4px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #444;
                border-radius: 2px;
            }
        """)
        self.itemClicked.connect(self._on_click)
        if is_file_list:
            self.itemDoubleClicked.connect(self._on_double_click)

    def _on_click(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        if data["type"] == "file":
            self.copy_requested.emit(data["path"])
        else:
            self.copy_requested.emit(data["text"])

    def _on_double_click(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if data and data["type"] == "file":
            open_file(data["path"])

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        mime = QMimeData()
        if data["type"] == "file":
            mime.setUrls([QUrl.fromLocalFile(data["path"])])
        else:
            mime.setText(data["text"])
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.DropAction.CopyAction)


# ─── Watchdog ─────────────────────────────────────────────────────────────────
class DirWatcher(FileSystemEventHandler):
    def __init__(self, cb):
        self.cb = cb
    def on_any_event(self, event):
        self.cb()


# ─── Main Window ──────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.internal_copy_text = None
        self.snippets: list[str] = []
        self.clipboard_history: list[str] = []

        os.makedirs(APP_DIR, exist_ok=True)
        self._load_snippets()
        self._load_clipboard_history()   # ← persists across restarts

        # Native Qt clipboard watcher
        self._qt_clipboard = QGuiApplication.clipboard()
        self._qt_clipboard.dataChanged.connect(self._on_clipboard_change)

        self._build_ui()
        self._start_watchers()

    # ── Persistence ───────────────────────────────────────────────────────────
    def _load_snippets(self):
        try:
            with open(SNIPPETS_FILE, "r", encoding="utf-8") as f:
                self.snippets = json.load(f)
        except Exception:
            self.snippets = []

    def _save_snippets(self):
        with open(SNIPPETS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.snippets, f, ensure_ascii=False)

    def _load_clipboard_history(self):
        """Load saved clipboard history so it survives restarts."""
        try:
            with open(CLIPBOARD_FILE, "r", encoding="utf-8") as f:
                self.clipboard_history = json.load(f)
        except Exception:
            self.clipboard_history = []

    def _save_clipboard_history(self):
        with open(CLIPBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(self.clipboard_history, f, ensure_ascii=False)

    # ── Clipboard logic ───────────────────────────────────────────────────────
    def copy_to_clipboard(self, text: str):
        """Copies text and flags it as internal so we don't re-add it."""
        self.internal_copy_text = text
        self._qt_clipboard.setText(text)
        self._show_toast("✓ Copied")

    def _on_clipboard_change(self):
        new_text = self._qt_clipboard.text().strip()
        if not new_text:
            return
        # Ignore copies triggered by Snag itself
        if new_text == self.internal_copy_text:
            self.internal_copy_text = None
            return
        # Ignore duplicate at top
        if self.clipboard_history and self.clipboard_history[0] == new_text:
            return
        self.clipboard_history.insert(0, new_text)
        if len(self.clipboard_history) > 15:
            self.clipboard_history.pop()
        self._save_clipboard_history()
        self._refresh_clipboard_ui()

    # ── Watchers ──────────────────────────────────────────────────────────────
    def _start_watchers(self):
        self.observer = Observer()
        handler = DirWatcher(lambda: QTimer.singleShot(0, self._refresh_file_lists))
        for p in [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures/Screenshots"),
        ]:
            if os.path.exists(p):
                self.observer.schedule(handler, p, recursive=False)
        self.observer.start()

    # ── Toast ─────────────────────────────────────────────────────────────────
    def _show_toast(self, msg: str):
        self._toast.setText(msg)
        self._toast.show()
        QTimer.singleShot(1500, self._toast.hide)

    # ══════════════════════════════════════════════════════════════════════════
    #  UI BUILD
    # ══════════════════════════════════════════════════════════════════════════
    def _build_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - WINDOW_WIDTH - 20, screen.height() - WINDOW_HEIGHT - 20)

        root = QWidget(self)
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Card background
        self._card = QFrame()
        self._card.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border-radius: 14px;
                border: 1px solid #2E2E2E;
            }
        """)
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(14, 10, 14, 12)
        card_layout.setSpacing(8)
        root_layout.addWidget(self._card)

        # ── Top bar: logo + close ────────────────────────────────────────────
        top_bar = QHBoxLayout()
        logo = QLabel("snag.")
        logo.setStyleSheet("color:#C8C8C8; font-size:13px; font-weight:700; letter-spacing:1px;")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(22, 22)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton { background:transparent; color:#666; border:none; font-size:13px; border-radius:11px; }
            QPushButton:hover { color:#fff; background:#E05050; }
        """)
        btn_close.clicked.connect(self._quit)
        top_bar.addWidget(logo)
        top_bar.addStretch()
        top_bar.addWidget(btn_close)
        card_layout.addLayout(top_bar)

        # ── License gate OR main content ─────────────────────────────────────
        if not self._is_licensed():
            self._build_license_gate(card_layout)
        else:
            self._build_main(card_layout)

        # ── Toast overlay ─────────────────────────────────────────────────────
        self._toast = QLabel(self)
        self._toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._toast.setStyleSheet("""
            QLabel {
                background: #2E2E2E;
                color: #DDDDDD;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 4px 14px;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        self._toast.resize(110, 26)
        self._toast.move((WINDOW_WIDTH - 110) // 2, WINDOW_HEIGHT - 44)
        self._toast.hide()

    # ── License ───────────────────────────────────────────────────────────────
    def _is_licensed(self) -> bool:
        try:
            with open(LICENSE_FILE, "r") as f:
                return json.load(f).get("is_active", False)
        except Exception:
            return False

    def _build_license_gate(self, parent_layout):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("Activate Snag")
        title.setStyleSheet("color:#E0E0E0; font-size:22px; font-weight:700;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Enter your license key to unlock")
        sub.setStyleSheet("color:#666; font-size:12px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._key_input = QLineEdit()
        self._key_input.setPlaceholderText("SNAG-XXXX-XXXX-XXXX")
        self._key_input.setStyleSheet("""
            QLineEdit { background:#0D0D0D; color:#E0E0E0; border:1px solid #333;
                        border-radius:7px; padding:10px 12px; font-size:13px; letter-spacing:1px; }
            QLineEdit:focus { border:1px solid #555; }
        """)

        btn = QPushButton("Activate")
        btn.setStyleSheet("""
            QPushButton { background:#E0E0E0; color:#111; border-radius:7px;
                          padding:10px; font-weight:700; font-size:13px; }
            QPushButton:hover { background:#fff; }
        """)
        btn.clicked.connect(self._activate)
        self._key_input.returnPressed.connect(self._activate)

        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(self._key_input)
        layout.addWidget(btn)
        parent_layout.addWidget(container)
        self._gate_widget = container

    def _activate(self):
        key = self._key_input.text().strip()
        if len(key) >= 16:
            with open(LICENSE_FILE, "w") as f:
                json.dump({"is_active": True, "key": key}, f)
            self._gate_widget.setParent(None)
            self._build_main(self._card.layout())

    # ── Main Interface ────────────────────────────────────────────────────────
    def _build_main(self, parent_layout):
        # ── Tab header ───────────────────────────────────────────────────────
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(0)
        self._tab_btns: list[QPushButton] = []
        tab_labels = ["Screenshots", "Downloads", "Clipboard", "Snippets"]
        tab_icons  = ["🖼️", "📥", "📋", "📌"]

        for i, (lbl, icon_char) in enumerate(zip(tab_labels, tab_icons)):
            btn = QPushButton(icon_char)
            btn.setToolTip(lbl)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #777; border: none;
                    font-size: 16px; padding: 6px 12px;
                    border-bottom: 2px solid transparent;
                }
                QPushButton:hover  { color: #AAA; }
                QPushButton:checked { color: #E0E0E0; border-bottom: 2px solid #888; }
            """)
            btn.clicked.connect(lambda _, idx=i: self._switch_tab(idx))
            self._tab_btns.append(btn)
            tab_bar.addWidget(btn)
        tab_bar.addStretch()
        parent_layout.addLayout(tab_bar)

        # ── Stacked pages ────────────────────────────────────────────────────
        self._pages = QStackedWidget()

        # Page 0: Screenshots
        self._list_screenshots = SnagList(is_file_list=True)
        self._list_screenshots.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_screenshots)

        # Page 1: Downloads
        self._list_downloads = SnagList(is_file_list=True)
        self._list_downloads.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_downloads)

        # Page 2: Clipboard
        self._list_clipboard = SnagList()
        self._list_clipboard.copy_requested.connect(self.copy_to_clipboard)
        self._pages.addWidget(self._list_clipboard)

        # Page 3: Snippets
        snip_page = QWidget()
        snip_layout = QVBoxLayout(snip_page)
        snip_layout.setContentsMargins(0, 0, 0, 0)
        snip_layout.setSpacing(6)

        self._snip_input = QLineEdit()
        self._snip_input.setPlaceholderText("Type a snippet and press Enter…")
        self._snip_input.setStyleSheet("""
            QLineEdit { background:#0D0D0D; color:#E0E0E0; border:1px solid #333;
                        border-radius:7px; padding:8px 10px; font-size:12px; }
            QLineEdit:focus { border:1px solid #555; }
        """)
        self._snip_input.returnPressed.connect(self._add_snippet)

        self._list_snippets = SnagList()
        self._list_snippets.copy_requested.connect(self.copy_to_clipboard)

        snip_layout.addWidget(self._snip_input)
        snip_layout.addWidget(self._list_snippets)
        self._pages.addWidget(snip_page)

        parent_layout.addWidget(self._pages)

        self._switch_tab(0)
        self._refresh_file_lists()
        self._refresh_clipboard_ui()
        self._refresh_snippets_ui()

    def _switch_tab(self, index: int):
        for i, btn in enumerate(self._tab_btns):
            btn.setChecked(i == index)
        self._pages.setCurrentIndex(index)

    # ── File helpers ──────────────────────────────────────────────────────────
    def _get_recent_files(self, directory: str, count: int = 10) -> list[str]:
        if not os.path.exists(directory):
            return []
        files = [
            os.path.join(directory, n)
            for n in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, n))
        ]
        files.sort(key=os.path.getmtime, reverse=True)
        return files[:count]

    def _add_file_row(self, list_widget: SnagList, file_path: str):
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, {"type": "file", "path": file_path})

        row = FileRowWidget(os.path.basename(file_path), file_path)
        # Make sure the item height matches the widget
        item.setSizeHint(QSize(WINDOW_WIDTH - 30, 42))
        list_widget.addItem(item)
        list_widget.setItemWidget(item, row)

    def _refresh_file_lists(self):
        if not hasattr(self, "_list_downloads"):
            return

        # Downloads
        self._list_downloads.clear()
        for f in self._get_recent_files(os.path.expanduser("~/Downloads")):
            self._add_file_row(self._list_downloads, f)

        # Screenshots (Desktop + Pictures/Screenshots, image files only)
        sc_dirs = [
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures/Screenshots"),
        ]
        images = []
        for d in sc_dirs:
            if os.path.exists(d):
                images.extend([
                    os.path.join(d, n) for n in os.listdir(d)
                    if n.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
                ])
        images.sort(key=os.path.getmtime, reverse=True)
        self._list_screenshots.clear()
        for f in images[:10]:
            self._add_file_row(self._list_screenshots, f)

    # ── Clipboard UI ──────────────────────────────────────────────────────────
    def _refresh_clipboard_ui(self):
        if not hasattr(self, "_list_clipboard"):
            return
        self._list_clipboard.clear()
        for text in self.clipboard_history:
            preview = text.replace("\n", " ").strip()
            if len(preview) > 52:
                preview = preview[:52] + "…"
            item = QListWidgetItem(preview)
            item.setData(Qt.ItemDataRole.UserRole, {"type": "text", "text": text})
            item.setForeground(QColor("#C8C8C8"))
            self._list_clipboard.addItem(item)

    # ── Snippets ──────────────────────────────────────────────────────────────
    def _add_snippet(self):
        text = self._snip_input.text().strip()
        if text:
            self.snippets.insert(0, text)
            self._save_snippets()
            self._refresh_snippets_ui()
            self._snip_input.clear()

    def _refresh_snippets_ui(self):
        if not hasattr(self, "_list_snippets"):
            return
        self._list_snippets.clear()
        for s in self.snippets:
            item = QListWidgetItem(s[:54] + "…" if len(s) > 54 else s)
            item.setData(Qt.ItemDataRole.UserRole, {"type": "text", "text": s})
            item.setForeground(QColor("#C8C8C8"))
            self._list_snippets.addItem(item)

    # ── Cleanup ───────────────────────────────────────────────────────────────
    def _quit(self):
        if hasattr(self, "observer"):
            self.observer.stop()
            self.observer.join()
        QApplication.quit()

    # ── Window drag ───────────────────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_drag_pos"):
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._drag_pos = event.globalPosition().toPoint()


# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))  # cross-platform font (SF Pro on macOS, Segoe UI on Windows)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
