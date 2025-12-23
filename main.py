# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from tabs.tab_numeric import NumericTab
from tabs.tab_linear import LinearAlgebraTab
from tabs.tab_graph import GraphTab
from tabs.tab_calculus import CalculusTab
import styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Math Suite 2025")
        self.resize(1200, 800)
        self.setStyleSheet(styles.STYLESHEET)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        tabs = QTabWidget()
        tabs.addTab(NumericTab(), "Calculator")
        tabs.addTab(LinearAlgebraTab(), "Linear Algebra")
        tabs.addTab(GraphTab(), "Graph Algorithms")
        tabs.addTab(CalculusTab(), "Calculus")
        
        layout.addWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow()
    win.show()
    sys.exit(app.exec())