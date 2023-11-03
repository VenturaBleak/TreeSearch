# solvers/solver.py
class Solver:
    def __init__(self, env):
        self.env = env
        self.tree = nx.DiGraph()

    def expand_node(self, node):
        raise NotImplementedError("Expand method should be implemented by subclasses.")

    def solve(self):
        raise NotImplementedError("Solve method should be implemented by subclasses.")