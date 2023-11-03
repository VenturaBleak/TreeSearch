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
        def dfs_max_score(node):
            if not node.children:
                return node.state.value, [node]
            max_score = float('-inf')
            best_child_path = []
            for child in node.children:
                score, path = dfs_max_score(child)
                if score > max_score:
                    max_score = score
                    best_child_path = path
            return max_score, [node] + best_child_path

        _, path = dfs_max_score(self.root)
        return path