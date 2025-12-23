# styles.py

COLORS = {
    "bg_main": "#f3f4f6",
    "bg_card": "#ffffff",
    "text_main": "#1f2937",
    "primary": "#3b82f6",
    "border": "#e5e7eb"
}

STYLESHEET = f"""
QMainWindow {{ background-color: {COLORS["bg_main"]}; }}
QWidget {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; color: {COLORS["text_main"]}; }}
QTabWidget::pane {{ border: 1px solid {COLORS["border"]}; background: {COLORS["bg_card"]}; border-radius: 8px; }}
QTabBar::tab {{ background: {COLORS["bg_main"]}; padding: 10px 20px; border-top-left-radius: 6px; border-top-right-radius: 6px; }}
QTabBar::tab:selected {{ background: {COLORS["bg_card"]}; border-top: 2px solid {COLORS["primary"]}; }}
QPushButton {{ background-color: {COLORS["bg_card"]}; border: 1px solid {COLORS["border"]}; padding: 8px 16px; border-radius: 6px; }}
QPushButton:hover {{ border-color: {COLORS["primary"]}; color: {COLORS["primary"]}; }}
QLineEdit, QTextEdit, QSpinBox {{ background: white; border: 1px solid {COLORS["border"]}; padding: 6px; border-radius: 4px; }}
QTableWidget {{ background-color: white; gridline-color: {COLORS["border"]}; border: 1px solid {COLORS["border"]}; }}
"""