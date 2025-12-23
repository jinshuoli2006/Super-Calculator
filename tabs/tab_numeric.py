# tabs/tab_numeric.py
import math
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt

class NumericTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)
        
        grid = QGridLayout()
        buttons = [
            ('C',0,0), ('(',0,1), (')',0,2), ('/',0,3),
            ('7',1,0), ('8',1,1), ('9',1,2), ('*',1,3),
            ('4',2,0), ('5',2,1), ('6',2,2), ('-',2,3),
            ('1',3,0), ('2',3,1), ('3',3,2), ('+',3,3),
            ('0',4,0), ('.',4,1), ('^',4,2), ('=',4,3)
        ]
        for txt, r, c in buttons:
            btn = QPushButton(txt)
            btn.setMinimumHeight(50)
            if txt == '=': btn.clicked.connect(self.calc)
            elif txt == 'C': btn.clicked.connect(self.display.clear)
            else: btn.clicked.connect(lambda _, t=txt: self.display.setText(self.display.text()+t))
            grid.addWidget(btn, r, c)
        layout.addLayout(grid)

    def calc(self):
        try:
            res = eval(self.display.text().replace('^', '**'))
            self.display.setText(str(res))
        except: self.display.setText("Error")

# tabs/tab_linear.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QTextEdit)
from backend import Matrix

class LinearAlgebraTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        left = QWidget(); l_lay = QVBoxLayout(left)
        
        self.rows = QSpinBox(); self.rows.setValue(3)
        self.cols = QSpinBox(); self.cols.setValue(3)
        btn_gen = QPushButton("Set Grid"); btn_gen.clicked.connect(self.gen_grid)
        l_lay.addWidget(self.rows); l_lay.addWidget(self.cols); l_lay.addWidget(btn_gen)
        
        self.table = QTableWidget()
        self.gen_grid()
        l_lay.addWidget(self.table)
        
        for name, method in [("Det", "det"), ("Inv", "inverse"), ("Rank", "rank"), ("RREF", "rref")]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, m=method: self.run_op(m))
            l_lay.addWidget(btn)
            
        self.log = QTextEdit()
        layout.addWidget(left); layout.addWidget(self.log)

    def gen_grid(self):
        self.table.setRowCount(self.rows.value())
        self.table.setColumnCount(self.cols.value())
        for i in range(self.rows.value()):
            for j in range(self.cols.value()):
                self.table.setItem(i, j, QTableWidgetItem("0"))

    def run_op(self, method):
        try:
            data = []
            for i in range(self.table.rowCount()):
                row = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    row.append(float(item.text()) if item and item.text() else 0.0)
                data.append(row)
            m = Matrix(data)
            res = getattr(m, method)()
            self.log.append(f"{method}: {res}")
        except Exception as e:
            self.log.append(f"Error: {e}")

# tabs/tab_calculus.py
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QScrollArea)
from components import PlotWidget

class CalculusTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        left = QWidget(); l_lay = QVBoxLayout(left)
        
        self.funcs = []
        self.func_area = QWidget(); self.f_lay = QVBoxLayout(self.func_area)
        l_lay.addWidget(QScrollArea(widget=self.func_area))
        
        btn_add = QPushButton("Add Func"); btn_add.clicked.connect(self.add_f)
        btn_plot = QPushButton("Plot"); btn_plot.clicked.connect(self.plot)
        l_lay.addWidget(btn_add); l_lay.addWidget(btn_plot)
        
        self.plotter = PlotWidget()
        layout.addWidget(left, 1); layout.addWidget(self.plotter, 3)
        self.add_f()

    def add_f(self):
        inp = QLineEdit("x**2")
        self.funcs.append(inp)
        self.f_lay.addWidget(inp)

    def plot(self):
        ax = self.plotter.get_axes(); ax.clear(); ax.grid(True)
        x = np.linspace(-10, 10, 400)
        for inp in self.funcs:
            try:
                y = eval(inp.text(), {"x": x, "np": np})
                ax.plot(x, y, label=inp.text())
            except: pass
        ax.legend()
        self.plotter.draw()