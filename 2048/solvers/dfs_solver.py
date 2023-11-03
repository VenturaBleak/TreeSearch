# dfs_solver.py
from solvers.solver import Solver
from game_logic import Game
import numpy as np


class DFSSolver(Solver):
    def __init__(self, game, max_depth=50):
        self.game = game
        self.max_depth = max_depth

    def solve(self):
        _, best_move = self.search(self.game, depth=0)
        return best_move

    def search(self, game, depth):
        if depth >= self.max_depth or game.is_game_over():
            return self.evaluate_heuristic(game), None

        best_heuristic_value = -float('inf')
        best_move = None

        for move in game.get_legal_moves():
            new_game = Game(size=game.size, win_tile=game.win_tile)
            new_game.grid = np.copy(game.grid)
            new_game.score = game.score

            new_game.play(move)

            heuristic_value, _ = self.search(new_game, depth + 1)
            if heuristic_value > best_heuristic_value:
                best_heuristic_value = heuristic_value
                best_move = move

        return best_heuristic_value, best_move

    def evaluate_heuristic(self, game):
        # Implement your heuristic here. As a simple example, counting the empty tiles:
        empty_tiles = np.count_nonzero(game.grid == 0)
        return empty_tiles
