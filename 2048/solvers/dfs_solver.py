# dfs_solver.py
from solvers.solver import Solver
import numpy as np
from game_logic import Game

class DFSSolver(Solver):
    def __init__(self, game, max_depth=5, rollouts=140):
        super().__init__(game, max_depth)
        self.rollouts = rollouts

    def solve(self):
        best_heuristic_value = -float('inf')
        best_move = None
        for _ in range(self.rollouts):
            # Randomly select a move to simulate
            move = np.random.choice(self.env.get_legal_moves())
            new_game = self.clone_game(self.env)
            new_game.play(move)
            heuristic_value = self.evaluate_rollout(new_game, depth=1)
            if heuristic_value > best_heuristic_value:
                best_heuristic_value = heuristic_value
                best_move = move
        return best_move

    def evaluate_rollout(self, game, depth):
        if depth >= self.max_depth or game.game_over:
            return self.evaluate_heuristic(game)

        # Randomly select a move for the rollout
        move = np.random.choice(game.get_legal_moves())
        new_game = self.clone_game(game)
        new_game.play(move)
        return self.evaluate_rollout(new_game, depth + 1)

    def clone_game(self, game):
        # Deep copy the game state
        new_game = Game(size=game.size, win_tile=game.win_tile)
        new_game.grid = np.copy(game.grid)
        new_game.score = game.score
        new_game.is_win = game.is_win
        new_game.game_over = game.game_over
        return new_game

    def evaluate_heuristic(self, game):
        # Example heuristic: number of empty tiles
        return np.count_nonzero(game.grid == 0)