# agents.py
import random
import numpy as np
from game_logic import Board, Action

class Agent:
    def select_move(self, game_state: Board):
        raise NotImplementedError()

class RandomAgent(Agent):
    def select_move(self, game_state: Board):
        return random.choice(game_state.get_available_moves())

class MCTSAgent:
    def __init__(self, num_rollouts):
        self.num_rollouts = num_rollouts

    def select_move(self, game_state: Board):
        best_move = None
        best_value = -np.inf

        for move in game_state.get_available_moves():
            move_sum_value = 0
            for _ in range(self.num_rollouts):
                move_sum_value += self.random_playout(game_state, move)

            if move_sum_value > best_value:
                best_value = move_sum_value
                best_move = move

        return best_move

    def random_playout(self, game_state: Board, move):
        board_copy = Board()
        board_copy.board = np.copy(game_state.board)
        board_copy.score = game_state.score

        board_copy.move(move)
        if np.array_equal(board_copy.board, game_state.board):
            return -np.inf  # Penalize non-changing moves

        while not board_copy.is_game_over():
            move = random.choice(board_copy.get_available_moves())
            board_copy.move(move)

        return board_copy.score