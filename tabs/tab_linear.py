# tabs/tab_linear.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QSpinBox, 
                             QLabel, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt
from backend import Matrix

class LinearAlgebraTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        # --- Left Panel: Input ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Grid Controls
        ctrl_layout = QHBoxLayout()
        self.rows = QSpinBox(); self.rows.setRange(1, 10); self.rows.setValue(3)
        self.cols = QSpinBox(); self.cols.setRange(1, 10); self.cols.setValue(3)
        btn_gen = QPushButton("Reset Grid"); btn_gen.clicked.connect(self.create_grid)
        
        ctrl_layout.addWidget(QLabel("Rows:"))
        ctrl_layout.addWidget(self.rows)
        ctrl_layout.addWidget(QLabel("Cols:"))
        ctrl_layout.addWidget(self.cols)
        ctrl_layout.addWidget(btn_gen)
        ctrl_layout.addStretch()
        
        self.table = QTableWidget()
        self.create_grid()
        
        # Operation Buttons
        ops_layout = QHBoxLayout()
        for label, func in [("Determinant", self.do_det), ("Inverse", self.do_inv), 
                            ("Rank", self.do_rank), ("RREF", self.do_rref), ("Transpose", self.do_T)]:
            btn = QPushButton(label)
            btn.clicked.connect(func)
            ops_layout.addWidget(btn)
            
        left_layout.addLayout(ctrl_layout)
        left_layout.addWidget(self.table)
        left_layout.addLayout(ops_layout)
        
        # --- Right Panel: Output ---
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Calculation results will appear here...")
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.log)
        splitter.setSizes([600, 300])
        
        layout.addWidget(splitter)

    def create_grid(self):
        r, c = self.rows.value(), self.cols.value()
        self.table.setRowCount(r)
        self.table.setColumnCount(c)
        for i in range(r):
            for j in range(c):
                self.table.setItem(i, j, QTableWidgetItem("0"))

    def get_matrix(self):
        """Parses the QTableWidget into a Matrix object."""
        try:
            data = []
            for i in range(self.table.rowCount()):
                row = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    val = float(item.text()) if item and item.text() else 0.0
                    row.append(val)
                data.append(row)
            return Matrix(data)
        except ValueError:
            self.log.append("Error: Invalid numeric input in grid.")
            return None

    def print_res(self, title, res):
        self.log.append(f"<b>{title}:</b>")
        if isinstance(res, Matrix):
            for row in res.to_float():
                self.log.append(str([round(x, 4) for x in row]))
        else:
            self.log.append(str(res))
        self.log.append("-" * 30)

    # Operations
    def do_det(self): 
        m = self.get_matrix()
        if m: self.print_res("Determinant", m.det())
    def do_inv(self):
        m = self.get_matrix()
        if m: self.print_res("Inverse", m.inverse() or "Singular Matrix (No Inverse)")
    def do_rank(self):
        m = self.get_matrix()
        if m: self.print_res("Rank", m.rank())
    def do_rref(self):
        m = self.get_matrix()
        if m: self.print_res("RREF", m.rref())
    def do_T(self):
        m = self.get_matrix()
        if m: self.print_res("Transpose", m.T())