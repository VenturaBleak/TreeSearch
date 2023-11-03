# solvers/solver.py

class Solver:
    def __init__(self, root):
        self.root = root
        self.visited = set()

    def solve(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def best_path(self):
        raise NotImplementedError("Subclasses should implement this method.")