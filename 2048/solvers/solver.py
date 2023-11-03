# solvers.solver.py
class Solver:
    def __init__(self, game_state):
        self.game_state = game_state

    def find_best_move(self):
        raise NotImplementedError("This method should be overridden.")