# visualizer.py

import tkinter as tk
from tkinter import font
from anytree import PreOrderIter
import time

class TreeVisualizer:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.master = tk.Tk()
        self.master.title('Tree Visualization')
        self.canvas_width = 1400
        self.canvas_height = 1000
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.node_positions = {}

        # Aesthetic settings
        self.font = font.Font(size=10, weight='bold')
        self.node_fill_color = '#D3D3D3'
        self.node_visited_color = '#4CAF50'
        self.path_color = '#FFD700'
        self.edge_default_color = '#A9A9A9'
        self.edge_visited_color = self.node_visited_color
        self.edge_path_color = self.path_color

    def hierarchical_layout(self):
        levels = {}
        for node in PreOrderIter(self.root):
            depth = node.depth
            if depth in levels:
                levels[depth].append(node)
            else:
                levels[depth] = [node]

        pos = {}
        max_depth = max(levels.keys())
        for depth, nodes in levels.items():
            width_offset = self.canvas_width / (len(nodes) + 1)
            for idx, node in enumerate(nodes, start=1):
                pos[node] = (idx * width_offset, depth * (self.canvas_height / (max_depth + 2)) + 50)  # +50 to ensure the root node is visible

        return pos

    def draw_node(self, x, y, color=None, text=None):
        depth = len(self.node_positions) // 10 + 1
        radius = 100 / depth
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.node_fill_color if not color else color, outline='')
        if text:
            self.canvas.create_text(x, y, text=text, font=self.font)

    def draw_edge(self, x1, y1, x2, y2, color=None):
        self.canvas.create_line(x1, y1, x2, y2, fill=self.edge_default_color if not color else color, width=1.5)

    def animate_solver_process(self):
        self.node_positions = self.hierarchical_layout()

        # Draw all edges first
        for node in PreOrderIter(self.root):
            if node.parent:
                px, py = self.node_positions[node.parent]
                x, y = self.node_positions[node]
                self.draw_edge(px, py, x, y)

        # Draw all nodes
        for node in PreOrderIter(self.root):
            x, y = self.node_positions[node]
            self.draw_node(x, y, text=str(node.state.value))

        # Animate the solving process
        for node in self.solver.visited_sequence:
            x, y = self.node_positions[node]
            if node.parent:
                px, py = self.node_positions[node.parent]
                self.draw_edge(px, py, x, y, color=self.edge_visited_color)
            self.draw_node(x, y, color=self.node_visited_color, text=str(node.state.value))  # Re-draw the node to keep it in the foreground
            self.master.update()
            time.sleep(0.05)

    def highlight_best_path(self):
        best_path_nodes = self.solver.best_path()
        for i, node in enumerate(best_path_nodes):
            x, y = self.node_positions[node]
            if i < len(best_path_nodes) - 1:  # not the last node
                next_node = best_path_nodes[i+1]
                nx, ny = self.node_positions[next_node]
                self.draw_edge(x, y, nx, ny, color=self.edge_path_color)
            self.draw_node(x, y, color=self.path_color, text=str(node.state.value))  # Re-draw the node to keep it in the foreground
            self.master.update()
            time.sleep(0.2)

        time.sleep(2)  # Let user see the final result for a bit
        self.master.destroy()  # Close the canvas

    def visualize(self):
        self.animate_solver_process()
        self.highlight_best_path()