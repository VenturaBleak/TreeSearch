# solvers/dfs_solver.py
from solvers.solver import Solver

class DFSSolver(Solver):
    def __init__(self, root):
        super().__init__(root)
        self.stack = []
        self.visited_sequence = []

    def solve(self):
        self.stack.append(self.root)
        while self.stack:
            node = self.stack.pop()
            if node not in self.visited:
                self.visited.add(node)
                self.visited_sequence.append(node)
                for child in node.children:
                    self.stack.append(child)

    def best_path(self):
        # For DFS, return the path to the deepest node
        path = []
        node = self.visited_sequence[-1]
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]