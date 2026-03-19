# styles.py
import winreg
import sys


def get_windows_theme():
    """返回值 1 为浅色；2为深色"""
    if sys.platform != "win32":
        return "light"

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 1
    except:
        return 1  # 读取失败，默认浅色

LIGHT_COLORS = {
    "bg_main": "#f3f4f6",
    "bg_card": "#ffffff",
    "text_main": "#1f2937",
    "text_secondary": "#6b7280",
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "border": "#e5e7eb",
    "border_focus": "#3b82f6",
    "table_alternate": "#f9fafb",
    "scrollbar": "#d1d5db",
    "scrollbar_hover": "#9ca3af"
}


DARK_COLORS = {
    "bg_main": "#1a1a1a",
    "bg_card": "#2d2d2d",
    "text_main": "#e5e7eb",
    "text_secondary": "#9ca3af",
    "primary": "#60a5fa",
    "primary_hover": "#3b82f6",
    "success": "#34d399",
    "warning": "#fbbf24",
    "error": "#f87171",
    "border": "#404040",
    "border_focus": "#60a5fa",
    "table_alternate": "#373737",
    "scrollbar": "#4b4b4b",
    "scrollbar_hover": "#5f5f5f"
}


def get_stylesheet(Light= True):
    colors = LIGHT_COLORS if Light else DARK_COLORS

    return f"""
    QMainWindow {{ 
        background-color: {colors["bg_main"]}; 
    }}

    QWidget {{ 
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; 
        font-size: 14px; 
        color: {colors["text_main"]}; 
    }}

    QTabWidget::pane {{ 
        border: 1px solid {colors["border"]}; 
        background: {colors["bg_card"]}; 
        border-radius: 8px; 
    }}

    QTabBar::tab {{ 
        background: {colors["bg_main"]}; 
        color: {colors["text_secondary"]};
        padding: 10px 20px; 
        border-top-left-radius: 6px; 
        border-top-right-radius: 6px; 
    }}

    QTabBar::tab:hover {{ 
        color: {colors["text_main"]};
    }}

    QTabBar::tab:selected {{ 
        background: {colors["bg_card"]}; 
        color: {colors["primary"]};
        border-top: 2px solid {colors["primary"]}; 
    }}

    QPushButton {{ 
        background-color: {colors["bg_card"]}; 
        border: 1px solid {colors["border"]}; 
        padding: 8px 16px; 
        border-radius: 6px; 
        color: {colors["text_main"]};
    }}

    QPushButton:hover {{ 
        border-color: {colors["primary"]}; 
        color: {colors["primary"]}; 
    }}

    QPushButton:pressed {{ 
        background-color: {colors["bg_main"]}; 
    }}

    QLineEdit, QTextEdit, QSpinBox, QComboBox, QDateEdit {{ 
        background: {colors["bg_card"]}; 
        border: 1px solid {colors["border"]}; 
        padding: 6px; 
        border-radius: 4px; 
        color: {colors["text_main"]};
        selection-background-color: {colors["primary"]};
    }}

    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus {{ 
        border-color: {colors["border_focus"]}; 
    }}

    QTableWidget {{ 
        background-color: {colors["bg_card"]}; 
        gridline-color: {colors["border"]}; 
        border: 1px solid {colors["border"]}; 
        color: {colors["text_main"]};
    }}

    QTableWidget::item {{ 
        padding: 5px; 
    }}

    QTableWidget::item:selected {{ 
        background-color: {colors["primary"]}; 
        color: white;
    }}

    QTableWidget::item:hover {{ 
        background-color: {colors["primary"]}20; 
    }}

    QHeaderView::section {{ 
        background-color: {colors["bg_main"]}; 
        color: {colors["text_main"]}; 
        border: 1px solid {colors["border"]}; 
        padding: 5px; 
    }}

    QScrollBar:vertical, QScrollBar:horizontal {{ 
        background: {colors["bg_main"]}; 
        border: none; 
        border-radius: 4px; 
    }}

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{ 
        background: {colors["scrollbar"]}; 
        border-radius: 4px; 
        min-height: 20px; 
    }}

    QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{ 
        background: {colors["scrollbar_hover"]}; 
    }}

    QScrollBar::add-line, QScrollBar::sub-line {{ 
        border: none; 
        background: none; 
    }}

    QGroupBox {{ 
        border: 1px solid {colors["border"]}; 
        border-radius: 6px; 
        margin-top: 10px; 
        color: {colors["text_main"]};
    }}

    QGroupBox::title {{ 
        subcontrol-origin: margin; 
        left: 10px; 
        padding: 0 5px 0 5px; 
    }}

    QMenuBar {{ 
        background-color: {colors["bg_main"]}; 
        color: {colors["text_main"]}; 
        border-bottom: 1px solid {colors["border"]};
    }}

    QMenuBar::item:selected {{ 
        background-color: {colors["primary"]}20; 
    }}

    QMenu {{ 
        background-color: {colors["bg_card"]}; 
        color: {colors["text_main"]}; 
        border: 1px solid {colors["border"]}; 
    }}

    QMenu::item:selected {{ 
        background-color: {colors["primary"]}; 
        color: white; 
    }}

    QProgressBar {{ 
        border: 1px solid {colors["border"]}; 
        border-radius: 4px; 
        text-align: center; 
        color: {colors["text_main"]};
    }}

    QProgressBar::chunk {{ 
        background-color: {colors["primary"]}; 
        border-radius: 3px; 
    }}

    QCheckBox {{ 
        color: {colors["text_main"]}; 
    }}

    QCheckBox::indicator {{ 
        width: 18px; 
        height: 18px; 
        border: 1px solid {colors["border"]}; 
        border-radius: 3px; 
        background: {colors["bg_card"]};
    }}

    QCheckBox::indicator:checked {{ 
        background-color: {colors["primary"]}; 
        border-color: {colors["primary"]}; 
        image: url(checkmark.png);
    }}

    QRadioButton {{ 
        color: {colors["text_main"]}; 
    }}

    QRadioButton::indicator {{ 
        width: 18px; 
        height: 18px; 
        border: 1px solid {colors["border"]}; 
        border-radius: 9px; 
        background: {colors["bg_card"]};
    }}

    QRadioButton::indicator:checked {{ 
        background-color: {colors["primary"]}; 
        border-color: {colors["primary"]}; 
    }}

    QStatusBar {{ 
        background-color: {colors["bg_main"]}; 
        color: {colors["text_secondary"]}; 
        border-top: 1px solid {colors["border"]};
    }}
    """

sys_style = get_windows_theme()

STYLESHEET = get_stylesheet(sys_style)

COLORS = LIGHT_COLORS if sys_style else DARK_COLORS
