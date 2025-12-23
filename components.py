# components.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, is_3d=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#ffffff')
        self.axes = self.fig.add_subplot(111, projection='3d' if is_3d else None)
        self.axes.set_facecolor('#ffffff')
        super().__init__(self.fig)

class PlotWidget(QWidget):
    def __init__(self, parent=None, is_3d=False):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.canvas = MplCanvas(self, is_3d=is_3d)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def get_axes(self):
        return self.canvas.axes
    
    def draw(self):
        self.canvas.draw()