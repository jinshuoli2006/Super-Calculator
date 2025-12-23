# tabs/tab_calculus.py
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QScrollArea, QFrame)
from components import PlotWidget

class FunctionItem(QFrame):
    """Represents a single function input row."""
    def __init__(self, parent_tab, index):
        super().__init__()
        self.parent_tab = parent_tab
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(f"e.g., np.sin(x) or x**2")
        self.input.setText("x**2") if index == 1 else None
        
        btn_del = QPushButton("×")
        btn_del.setFixedSize(30, 30)
        btn_del.setStyleSheet("color: red; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.parent_tab.remove_func(self))
        
        self.layout.addWidget(QLabel(f"f{index}(x) ="))
        self.layout.addWidget(self.input)
        self.layout.addWidget(btn_del)

class CalculusTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        # --- Left: Controls ---
        ctrl_panel = QWidget()
        ctrl_layout = QVBoxLayout(ctrl_panel)
        
        # Function List Area
        self.func_area = QWidget()
        self.func_layout = QVBoxLayout(self.func_area)
        self.func_layout.addStretch()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.func_area)
        
        # Range Inputs
        range_layout = QHBoxLayout()
        self.xmin = QLineEdit("-10"); self.xmin.setPlaceholderText("Min X")
        self.xmax = QLineEdit("10"); self.xmax.setPlaceholderText("Max X")
        range_layout.addWidget(QLabel("X Range:"))
        range_layout.addWidget(self.xmin)
        range_layout.addWidget(self.xmax)
        
        btn_add = QPushButton("+ Add Function")
        btn_add.clicked.connect(self.add_func)
        btn_plot = QPushButton("Plot All")
        btn_plot.setObjectName("PrimaryBtn")
        btn_plot.clicked.connect(self.plot)
        
        ctrl_layout.addWidget(QLabel("<b>Functions:</b>"))
        ctrl_layout.addWidget(scroll)
        ctrl_layout.addWidget(btn_add)
        ctrl_layout.addLayout(range_layout)
        ctrl_layout.addWidget(btn_plot)
        
        # --- Right: Plot ---
        self.plotter = PlotWidget()
        
        layout.addWidget(ctrl_panel, 1)
        layout.addWidget(self.plotter, 3)
        
        self.funcs = []
        self.add_func() # Add initial input

    def add_func(self):
        item = FunctionItem(self, len(self.funcs)+1)
        self.func_layout.insertWidget(len(self.funcs), item)
        self.funcs.append(item)

    def remove_func(self, item):
        self.func_layout.removeWidget(item)
        item.deleteLater()
        self.funcs.remove(item)

    def plot(self):
        ax = self.plotter.get_axes()
        ax.clear()
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.axhline(0, color='black', alpha=0.3)
        ax.axvline(0, color='black', alpha=0.3)
        
        try:
            x_min = float(self.xmin.text())
            x_max = float(self.xmax.text())
            x = np.linspace(x_min, x_max, 500)
            
            for i, item in enumerate(self.funcs):
                txt = item.input.text()
                if not txt.strip(): continue
                try:
                    # Allow math/numpy functions
                    y = eval(txt, {"x": x, "np": np, "abs": abs})
                    ax.plot(x, y, label=f"f{i+1}: {txt}")
                except Exception as e:
                    print(f"Plot error: {e}")
            
            ax.legend()
            self.plotter.draw()
        except ValueError:
            pass