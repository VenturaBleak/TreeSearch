# visualizer.py
import tkinter as tk
import time

class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, bg="white", height=600, width=800)
        self.canvas.pack()

    def draw_node(self, node, x, y, parent_coords=None, color="white"):
        circle_radius = 20
        self.canvas.create_oval(x - circle_radius, y - circle_radius,
                                x + circle_radius, y + circle_radius,
                                fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(node.state.value))
        if parent_coords:
            self.canvas.create_line(x, y - circle_radius, parent_coords[0], parent_coords[1] + circle_radius)

    def draw_tree(self, node, x, y, x_offset=200, y_offset=100, parent_coords=None):
        self.draw_node(node, x, y, parent_coords)
        if node.children:
            next_y = y + y_offset
            start_x = x - x_offset * (len(node.children) - 1) / 2
            for child in node.children:
                self.draw_tree(child, start_x, next_y, x_offset / 2, y_offset, (x, y))
                start_x += x_offset

    def animate_solver(self, solver):
        for node in solver.visited_sequence:
            x, y = self.get_node_coords(node)
            self.draw_node(node, x, y, color="lightgray")
            self.canvas.update()
            time.sleep(0.1)  # 100 ms delay

    def highlight_best_path(self, path):
        for node in path:
            x, y = self.get_node_coords(node)
            self.draw_node(node, x, y, color="lightblue")
            self.canvas.update()
            time.sleep(0.1)  # 100 ms delay

    def get_node_coords(self, node):
        # This function should be implemented to return the coordinates of the given node.
        # For simplicity, here's a placeholder implementation, but in practice, you'd
        # want to determine these coordinates based on the node's position in the tree.
        return (400, 50)

    def run(self, solver):
        self.draw_tree(self.root, 400, 50)
        self.animate_solver(solver)
        self.highlight_best_path(solver.best_path())
        self.window.mainloop()