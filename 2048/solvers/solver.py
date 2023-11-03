# solver.py (Superclass)
import numpy as np

class Solver:
    def __init__(self, env, max_depth=50):
        self.env = env
        self.max_depth = max_depth

    def solve(self, obs):
        raise NotImplementedError("This method should be overridden by subclasses")

    def evaluate_heuristic(self, state):
        raise NotImplementedError("This method should be overridden by subclasses")

def clone_game(self, game):
    # Deep copy the game state
    new_game = Game(size=game.size, win_tile=game.win_tile)
    new_game.grid = np.copy(game.grid)
    new_game.score = game.score
    new_game.is_win = game.is_win
    new_game.game_over = game.game_over
    return new_game