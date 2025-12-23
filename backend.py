# backend.py
import copy
import numpy as np

# ==========================================
# CUSTOM MATRIX CLASS (From User Provided graph.py)
# ==========================================
class Matrix:
    def __init__(self, data=None, dim=None, init_value=0):
        if data is None and dim is None:
            # Fallback for empty init to avoid crash, though user logic raises error
            self.data = []
            self.dim = (0, 0)
            return

        if data is not None:
            if not isinstance(data, list):
                raise TypeError("1-2: The data should be a nested list")
            else:
                for i in range(len(data)):
                    if i == 0:
                        if not isinstance(data[i], list):
                            raise TypeError("1-3: All the elements in 'data' should be a list")
                    else:
                        if (not isinstance(data[i], list)) or (len(data[i]) != len(data[i-1])):
                            raise TypeError("1-4: All elements must be lists of the same length")
                    
            if len(data) == 0:
                self.data = []
                self.dim = (0, 0)
            else:
                row_num = len(data)
                col_num = len(data[0])
                self.dim = (row_num, col_num)
                self.data = [row[:] for row in data] # Deep copy
        else:
            if not isinstance(dim, tuple) or len(dim) != 2:
                raise ValueError("1-6: dim should be a tuple of two integers")
            m, n = dim
            self.data = [[init_value for _ in range(n)] for _ in range(m)]
            self.dim = dim
        
        self.init_value = init_value

    @property
    def rows(self): return self.dim[0]
    @property
    def cols(self): return self.dim[1]

    def to_float(self):
        """Helper for UI display"""
        return [[float(x) for x in row] for row in self.data]

    def T(self):
        """Transpose"""
        if not isinstance(self, Matrix):
            raise TypeError("5-1: Only Matrix objects can be transposed")
        res = []
        if self.rows == 0: return Matrix(data=[])
        for i in range(len(self.data[0])):
            new_row = []
            for j in range(len(self.data)):
                new_row.append(self.data[j][i])
            res.append(new_row)
        return Matrix(res)

    def __pow__(self, n):
        """Matrix Power"""
        if not isinstance(n, int): raise TypeError("11-1: Exponent must be integer")
        if self.rows != self.cols: raise ValueError("11-4: Only square matrix can be exponentiated")
        
        res = Matrix(data=self.data)
        for _ in range(n-1):
            res = res * self
            res = Matrix(data=res.data)
        return res

    def __add__(self, other):
        """Matrix Addition"""
        if not isinstance(other, Matrix): raise TypeError("12-1: Only Matrix objects can be added")
        if self.dim != other.dim: raise ValueError("12-3: Dimensions do not match")
        
        res = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            res.append(row)
        return Matrix(data=res)

    def __mul__(self, other):
        """Matrix Multiplication"""
        if not isinstance(other, Matrix): raise TypeError("4-1: Both must be Matrix objects")
        if self.cols != other.rows: raise TypeError("4-3: Matrix dimensions incompatible for multiplication")
        
        new_self = self.data
        new_other = (other.T()).data
        width = len(new_self[0])
        
        res = []
        for i in range(len(new_self)):
            new_row = []
            for j in range(len(new_other)):
                new_ele = 0
                for k in range(width):
                    new_ele += new_self[i][k] * new_other[j][k]
                new_row.append(new_ele)
            res.append(new_row)
        return Matrix(data=res)
    
    # --- Added Helper methods for Linear Algebra Tab ---
    def det(self):
        import numpy as np
        if self.rows != self.cols: return "Undefined (Not Square)"
        try: return float(np.linalg.det(np.array(self.data, dtype=float)))
        except: return "Error"

    def rank(self):
        import numpy as np
        try: return np.linalg.matrix_rank(np.array(self.data, dtype=float))
        except: return 0

    def inverse(self):
        import numpy as np
        try:
            inv = np.linalg.inv(np.array(self.data, dtype=float))
            return Matrix(data=inv.tolist())
        except: return None
        
    def rref(self):
        import sympy
        try:
            m = sympy.Matrix(self.data)
            rref_mat, pivots = m.rref()
            return Matrix(data=np.array(rref_mat).astype(float).tolist())
        except: return self


# ==========================================
# CUSTOM GRAPH LOGIC (From User Provided graph.py)
# ==========================================
class GraphAlgo:
    def __init__(self, data):
        """
        data: adjacency matrix (nested list)
        """
        self.data = data
        self.validate()
        
    def validate(self):
        if not isinstance(self.data, list): raise TypeError("Graph data must be list")
        if len(self.data) == 0: return # Allow empty graph for UI init
        lenth = len(self.data[0])
        if len(self.data) != lenth: raise ValueError("Adjacency matrix must be square")

    def connectness(self):
        """Check if graph is connected using Matrix powers"""
        try:
            mat = Matrix(self.data)
            vertices_count = len(mat.data)
            if vertices_count == 0: return False
            res = Matrix(dim=mat.dim, init_value=0)
            # Sum of powers A^1 + ... + A^n
            for i in range(1, vertices_count + 1):
                res += mat**i # This uses the custom __pow__ and __add__
            
            for j in range(vertices_count):
                for k in range(vertices_count):
                    if j != k and res.data[j][k] == 0:
                        return False
            return True
        except Exception as e:
            return False

    def connect_components(self):
        """Return list of components [ [0,1], [2] ]"""
        mat = self.data
        vertices_count = len(mat)
        check = [False] * vertices_count
        res = []
        
        for index in range(vertices_count):
            if not check[index]:
                component = []
                queue = [index]
                check[index] = True
                while queue:
                    curr = queue.pop(0)
                    component.append(curr)
                    for neighbor in range(vertices_count):
                        # Treat non-zero as connected
                        if mat[curr][neighbor] != 0 and not check[neighbor]:
                            check[neighbor] = True
                            queue.append(neighbor)
                res.append(component)
        return res

    def is_bipartite_BFS(self):
        mat = self.data
        vertices_count = len(mat)
        color = {}
        for start in range(vertices_count):
            if start not in color:
                color[start] = 0
                queue = [start]
                while queue:
                    u = queue.pop(0)
                    for v in range(vertices_count):
                        if mat[u][v] != 0:
                            if v not in color:
                                color[v] = 1 - color[u]
                                queue.append(v)
                            elif color[v] == color[u]:
                                return False
        return True

    def find_shortest_path_weight(self, start, end):
        """Dijkstra's Algorithm"""
        vertices_count = len(self.data)
        distances = {i: float('inf') for i in range(vertices_count)}
        distances[start] = 0
        visited = [False] * vertices_count
        parent = {start: None}

        for _ in range(vertices_count):
            min_dist = float('inf')
            curr = -1
            for i in range(vertices_count):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    curr = i
            
            if curr == -1 or distances[curr] == float('inf'): break
            if curr == end: break

            visited[curr] = True
            for i in range(vertices_count):
                weight = self.data[curr][i]
                if weight > 0 and not visited[i]:
                    new_dist = distances[curr] + weight
                    if new_dist < distances[i]:
                        distances[i] = new_dist
                        parent[i] = curr
        
        if end not in parent: return None
        path = []
        curr_node = end
        while curr_node is not None:
            path.append(curr_node)
            curr_node = parent[curr_node]
        return path[::-1]

    def mst_prim(self):
        """Prim's Algo -> Returns Adjacency Matrix of MST"""
        weights = self.data
        n = len(weights)
        if n == 0: return []
        INF = float('inf')
        key = [INF] * n
        parent = [None] * n
        mst_set = [False] * n
        key[0] = 0
        parent[0] = -1

        for _ in range(n):
            min_val = INF
            u = -1
            for v in range(n):
                if not mst_set[v] and key[v] < min_val:
                    min_val = key[v]
                    u = v
            if u == -1: break
            mst_set[u] = True
            
            for v in range(n):
                w = weights[u][v]
                if w > 0 and not mst_set[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u
        
        mst_edges = []
        for i in range(1, n):
            if parent[i] is not None:
                # Store as tuple (u, v)
                mst_edges.append((parent[i], i))
        return mst_edges

    def mst_kruskal(self):
        """Kruskal's Algo -> Returns list of edges"""
        weights = self.data
        n = len(weights)
        edges = []
        for i in range(n):
            for j in range(i + 1, n): # Upper triangle
                if weights[i][j] > 0:
                    edges.append((weights[i][j], i, j))
        edges.sort()
        
        parent = list(range(n))
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
        
        mst_edges = []
        for w, u, v in edges:
            if union(u, v):
                mst_edges.append((u, v))
        return mst_edges