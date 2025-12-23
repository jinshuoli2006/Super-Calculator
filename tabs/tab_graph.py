# tabs/tab_graph.py
import math
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QGraphicsScene, QGraphicsView, QGraphicsItem, 
                             QGraphicsEllipseItem, QGraphicsLineItem, 
                             QInputDialog, QButtonGroup, QRadioButton,
                             QTextEdit, QSplitter, QLabel, QCheckBox, 
                             QMessageBox, QSpinBox, QGroupBox)
from PyQt6.QtCore import Qt, QPointF, QLineF, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QFont
from backend import GraphAlgo

# --- Visual Components ---

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, id, radius=20):
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.setPos(x, y)
        self.id = id
        self.radius = radius
        
        self.default_brush = QBrush(QColor("#3b82f6")) # Blue
        self.highlight_brush = QBrush(QColor("#ef4444")) # Red (Path)
        self.select_brush = QBrush(QColor("#f59e0b")) # Orange (Selection)
        
        self.setBrush(self.default_brush)
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.edges = []

    def reset_color(self):
        self.setBrush(self.default_brush)

    def highlight(self, color_type="path"):
        if color_type == "path": self.setBrush(self.highlight_brush)
        elif color_type == "select": self.setBrush(self.select_brush)
        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for edge in self.edges: edge.adjust()
        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, str(self.id))

class EdgeItem(QGraphicsLineItem):
    def __init__(self, start_node, end_node, weight=1, is_directed=False):
        super().__init__()
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.is_directed = is_directed
        
        self.default_pen = QPen(QColor("#9ca3af"), 2)
        self.highlight_pen = QPen(QColor("#ef4444"), 4) # Red for path
        self.mst_pen = QPen(QColor("#10b981"), 4)       # Green for MST
        
        self.setPen(self.default_pen)
        self.setZValue(-1)
        self.adjust()

    def reset_color(self):
        self.setPen(self.default_pen)

    def highlight(self, type="path"):
        if type == "path": self.setPen(self.highlight_pen)
        elif type == "mst": self.setPen(self.mst_pen)

    def adjust(self):
        line = QLineF(self.start_node.scenePos(), self.end_node.scenePos())
        self.setLine(line)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        # Weight Label
        mid = self.line().center()
        painter.setPen(QColor("#1f2937"))
        painter.setBrush(QColor("#ffffff"))
        painter.drawRect(QRectF(mid.x()-10, mid.y()-10, 20, 20))
        painter.drawText(QRectF(mid.x()-10, mid.y()-10, 20, 20), 
                         Qt.AlignmentFlag.AlignCenter, str(self.weight))
        
        if self.is_directed:
            line = self.line()
            angle = math.atan2(-line.dy(), line.dx())
            node_radius = 20
            dest_p = line.p2()
            arrow_tip_x = dest_p.x() - node_radius * math.cos(angle)
            arrow_tip_y = dest_p.y() + node_radius * math.sin(angle)
            arrow_size = 10
            p1 = QPointF(arrow_tip_x + arrow_size * math.sin(angle + math.pi / 3),
                         arrow_tip_y + arrow_size * math.cos(angle + math.pi / 3))
            p2 = QPointF(arrow_tip_x + arrow_size * math.sin(angle + math.pi - math.pi / 3),
                         arrow_tip_y + arrow_size * math.cos(angle + math.pi - math.pi / 3))
            painter.setBrush(self.pen().color()) # Match edge color
            painter.drawPolygon([QPointF(arrow_tip_x, arrow_tip_y), p1, p2])

# --- Logic & Layout ---

class GraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "move"
        self.node_counter = 0
        self.is_directed = False
        self.temp_source_node = None

    def mousePressEvent(self, event):
        pos = event.scenePos()
        if self.mode == "node":
            node = NodeItem(pos.x(), pos.y(), self.node_counter)
            self.addItem(node)
            self.node_counter += 1
        elif self.mode == "edge":
            item = self.itemAt(pos, QGraphicsView().transform())
            if isinstance(item, NodeItem):
                if self.temp_source_node is None:
                    self.temp_source_node = item
                    self.temp_source_node.highlight("select")
                else:
                    if item != self.temp_source_node:
                        self.create_edge(self.temp_source_node, item)
                    self.temp_source_node.reset_color()
                    self.temp_source_node = None
            else:
                if self.temp_source_node:
                    self.temp_source_node.reset_color()
                    self.temp_source_node = None
        super().mousePressEvent(event)

    def create_edge(self, u, v):
        weight, ok = QInputDialog.getInt(None, "Edge Weight", "Enter weight:", 1)
        if ok:
            edge = EdgeItem(u, v, weight, self.is_directed)
            self.addItem(edge)
            u.edges.append(edge)
            v.edges.append(edge)

class GraphTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        # === Left Panel: Controls ===
        ctrl_widget = QWidget()
        ctrl_layout = QVBoxLayout(ctrl_widget)
        
        # 1. Tools Group
        gb_tools = QGroupBox("Drawing Tools")
        vbox_tools = QVBoxLayout()
        self.scene = GraphScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.rb_move = QRadioButton("Move / Select"); self.rb_move.setChecked(True)
        self.rb_node = QRadioButton("Add Node")
        self.rb_edge = QRadioButton("Add Edge")
        bg = QButtonGroup(self)
        bg.addButton(self.rb_move); bg.addButton(self.rb_node); bg.addButton(self.rb_edge)
        bg.buttonClicked.connect(self.change_mode)
        
        self.chk_directed = QCheckBox("Directed Graph")
        self.chk_directed.stateChanged.connect(self.toggle_directed)
        
        btn_clear = QPushButton("Clear Canvas")
        btn_clear.clicked.connect(self.clear_all)
        
        vbox_tools.addWidget(self.rb_move)
        vbox_tools.addWidget(self.rb_node)
        vbox_tools.addWidget(self.rb_edge)
        vbox_tools.addWidget(self.chk_directed)
        vbox_tools.addWidget(btn_clear)
        gb_tools.setLayout(vbox_tools)
        
        # 2. Algorithms Group
        gb_algo = QGroupBox("Algorithms")
        vbox_algo = QVBoxLayout()
        
        # Pathfinding Inputs
        hbox_path = QHBoxLayout()
        self.sp_start = QSpinBox(); self.sp_start.setPrefix("Start: ")
        self.sp_end = QSpinBox(); self.sp_end.setPrefix("End: ")
        hbox_path.addWidget(self.sp_start)
        hbox_path.addWidget(self.sp_end)
        
        btn_path = QPushButton("Shortest Path (Dijkstra)")
        btn_path.clicked.connect(self.run_dijkstra)
        
        btn_conn = QPushButton("Check Connectivity")
        btn_conn.clicked.connect(self.check_connectivity)
        
        btn_bip = QPushButton("Check Bipartite")
        btn_bip.clicked.connect(self.check_bipartite)
        
        btn_mst = QPushButton("Show MST (Prim)")
        btn_mst.clicked.connect(self.run_mst)
        
        btn_mat = QPushButton("Show Adj Matrix")
        btn_mat.clicked.connect(self.show_matrix)
        
        vbox_algo.addLayout(hbox_path)
        vbox_algo.addWidget(btn_path)
        vbox_algo.addWidget(btn_mst)
        vbox_algo.addWidget(btn_conn)
        vbox_algo.addWidget(btn_bip)
        vbox_algo.addWidget(btn_mat)
        gb_algo.setLayout(vbox_algo)
        
        ctrl_layout.addWidget(gb_tools)
        ctrl_layout.addWidget(gb_algo)
        ctrl_layout.addStretch()
        
        # === Right Panel: Canvas & Log ===
        self.log = QTextEdit()
        self.log.setMaximumHeight(150)
        self.log.setReadOnly(True)
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.view)
        splitter.addWidget(self.log)
        
        layout.addWidget(ctrl_widget, 1)
        layout.addWidget(splitter, 4)

    def change_mode(self):
        if self.scene.temp_source_node:
            self.scene.temp_source_node.reset_color()
            self.scene.temp_source_node = None
        if self.rb_move.isChecked(): self.scene.mode = "move"
        elif self.rb_node.isChecked(): self.scene.mode = "node"
        elif self.rb_edge.isChecked(): self.scene.mode = "edge"

    def toggle_directed(self):
        self.scene.is_directed = self.chk_directed.isChecked()

    def clear_all(self):
        self.scene.clear()
        self.scene.node_counter = 0
        self.log.clear()

    # --- Matrix Extraction ---
    def get_graph_data(self):
        nodes = [item for item in self.scene.items() if isinstance(item, NodeItem)]
        nodes.sort(key=lambda x: x.id)
        if not nodes: return None, None
        
        id_map = {node.id: i for i, node in enumerate(nodes)}
        n = len(nodes)
        adj = [[0]*n for _ in range(n)]
        
        edges = [item for item in self.scene.items() if isinstance(item, EdgeItem)]
        for edge in edges:
            if edge.start_node.id in id_map and edge.end_node.id in id_map:
                u, v = id_map[edge.start_node.id], id_map[edge.end_node.id]
                adj[u][v] = edge.weight
                if not self.scene.is_directed:
                    adj[v][u] = edge.weight
        return adj, id_map

    # --- Algorithm Wrappers ---

    def show_matrix(self):
        adj, _ = self.get_graph_data()
        if adj:
            self.log.append("Adjacency Matrix:")
            self.log.append(str(adj))

    def reset_visuals(self):
        for item in self.scene.items():
            if isinstance(item, NodeItem): item.reset_color()
            if isinstance(item, EdgeItem): item.reset_color()

    def check_connectivity(self):
        adj, _ = self.get_graph_data()
        if not adj: return
        algo = GraphAlgo(adj)
        is_conn = algo.connectness()
        comps = algo.connect_components()
        msg = f"Connected: {is_conn}\nComponents: {comps}"
        QMessageBox.information(self, "Connectivity", msg)
        self.log.append(msg)

    def check_bipartite(self):
        adj, _ = self.get_graph_data()
        if not adj: return
        algo = GraphAlgo(adj)
        is_bip = algo.is_bipartite_BFS()
        msg = f"Is Bipartite: {is_bip}"
        QMessageBox.information(self, "Bipartite Check", msg)
        self.log.append(msg)

    def run_dijkstra(self):
        self.reset_visuals()
        adj, id_map = self.get_graph_data()
        if not adj: return
        
        algo = GraphAlgo(adj)
        start_id = self.sp_start.value()
        end_id = self.sp_end.value()
        
        if start_id not in id_map or end_id not in id_map:
            self.log.append("Error: Start or End ID does not exist.")
            return

        u, v = id_map[start_id], id_map[end_id]
        path_indices = algo.find_shortest_path_weight(u, v)
        
        if path_indices:
            self.log.append(f"Shortest Path: {path_indices}")
            # Highlight Path
            nodes = [item for item in self.scene.items() if isinstance(item, NodeItem)]
            nodes_by_idx = sorted(nodes, key=lambda x: x.id) # Assuming consecutive for now
            
            # Map back matrix index to NodeItem
            # Since we re-indexed based on sort, nodes_by_idx[i] corresponds to matrix index i
            path_nodes = [nodes_by_idx[i] for i in path_indices]
            
            for i in range(len(path_nodes) - 1):
                n1 = path_nodes[i]
                n2 = path_nodes[i+1]
                n1.highlight("path")
                n2.highlight("path")
                # Find edge between them
                for edge in n1.edges:
                    if (edge.start_node == n1 and edge.end_node == n2) or \
                       (edge.start_node == n2 and edge.end_node == n1):
                        edge.highlight("path")
        else:
            self.log.append("No path found.")

    def run_mst(self):
        self.reset_visuals()
        adj, _ = self.get_graph_data()
        if not adj: return
        if self.scene.is_directed:
            QMessageBox.warning(self, "Error", "MST is for Undirected graphs only.")
            return

        algo = GraphAlgo(adj)
        mst_edges_idx = algo.mst_prim() # List of tuples (u, v) indices
        
        nodes = [item for item in self.scene.items() if isinstance(item, NodeItem)]
        nodes_by_idx = sorted(nodes, key=lambda x: x.id)
        
        self.log.append(f"MST Edges: {mst_edges_idx}")
        
        for u_idx, v_idx in mst_edges_idx:
            n1 = nodes_by_idx[u_idx]
            n2 = nodes_by_idx[v_idx]
            for edge in n1.edges:
                if (edge.start_node == n1 and edge.end_node == n2) or \
                   (edge.start_node == n2 and edge.end_node == n1):
                    edge.highlight("mst")