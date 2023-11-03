# solver.py (Superclass)
import numpy as np

class Solver:
    def __init__(self, env, max_depth=50):
        self.env = env
        self.max_depth = max_depth

    def solve(self, obs):
        raise NotImplementedError("This method should be overridden by subclasses")

    def evaluate_heuristic(self, state):
        # Count the number of empty tiles (assuming empty tiles are represented by 0)
        return np.count_nonzero(state == 0)