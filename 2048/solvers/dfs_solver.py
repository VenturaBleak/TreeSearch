from solvers.solver import Solver
from copy import deepcopy


class DFSLimitedSolver(Solver):
    def __init__(self, game, depth_limit=10):
        super().__init__(game)
        self.depth_limit = depth_limit

    def solve(self):
        stack = [(deepcopy(self.game), [], 0)]  # state, path, depth

        while stack:
            current_state, path, depth = stack.pop()
            if self.is_solution(current_state):
                yield path
                break  # Stop after finding the first solution

            if depth < self.depth_limit:
                for next_state, move in self.get_next_states(current_state):
                    stack.append((next_state, path + [move], depth + 1))

            yield path, current_state  # For visualization purposes

    def is_solution(self, state):
        # Override if necessary, for example to check for specific score
        return super().is_solution(state)