# agents.py
import numpy as np
import random
import time
from itertools import groupby
from operator import itemgetter
from collections import namedtuple
# deepcopy is used to create a copy of the board
from copy import deepcopy

# import custom modules
from game_logic import Board, Action


class Agent:
    """Base class for agents that can play the 2048 game."""

    def select_move(self, game_state: Board):
        """Selects the next move based on the game state.

        Args:
            game_state (Board): The current state of the game.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()


class RandomAgent(Agent):
    """An agent that selects moves at random."""

    def select_move(self, game_state: Board):
        """Selects a random move from available game moves.

        Args:
            game_state (Board): The current state of the game.

        Returns:
            An action representing the move (up, down, left, right).
        """
        return random.choice(game_state.get_available_moves())

MoveEvaluation = namedtuple('MoveEvaluation', 'move empty_tiles high_value_tiles')

class MCTSAgent:
    def __init__(self, time_limit: float, max_depth: int = np.inf):
        self.time_limit = time_limit / 1000  # Convert milliseconds to seconds
        self.temporary_time_limit = self.time_limit
        self.previous_max_empty_tiles = np.inf
        self.max_depth = max_depth
        self.last_move_stats = {}

    def select_move(self, game_state: Board):
        start_time = time.time()
        moves = game_state.get_available_moves()
        rollouts_data = []


        max = self.time_limit

        while time.time() - start_time < self.temporary_time_limit:
            move = random.choice(moves)
            empty_tiles, high_value_tiles = self.random_playout(game_state, move)
            if empty_tiles != -np.inf:
                rollouts_data.append(MoveEvaluation(move, empty_tiles, high_value_tiles))

        best_move = self.evaluate(rollouts_data) if rollouts_data else None
        self.calculate_last_move_stats(rollouts_data, start_time)

        return best_move

    def random_playout(self, game_state: Board, move):
        board_copy = deepcopy(game_state)
        board_copy.move(move)
        if np.array_equal(board_copy.board, game_state.board):
            return -np.inf, np.inf

        for _ in range(self.max_depth):
            if board_copy.is_game_over():
                break
            random_move = random.choice(board_copy.get_available_moves())
            board_copy.move(random_move)

        empty_tiles = np.count_nonzero(board_copy.board == 0)
        high_value_tiles = np.count_nonzero(~np.isin(board_copy.board, [0, 2, 4]))
        return empty_tiles, high_value_tiles

    def evaluate(self, rollouts_data):
        max_empty_tiles = max(rollouts_data, key=lambda x: x.empty_tiles).empty_tiles
        candidates = [data for data in rollouts_data if data.empty_tiles == max_empty_tiles]
        best_move_data = min(candidates, key=lambda x: x.high_value_tiles)
        return best_move_data.move

    def calculate_last_move_stats(self, rollouts_data, start_time):
        num_rollouts = len(rollouts_data)
        total_empty_tiles = sum(data.empty_tiles for data in rollouts_data)
        average_empty_tiles = total_empty_tiles / num_rollouts if num_rollouts else 0
        max_empty_tiles = max(rollouts_data, key=lambda x: x.empty_tiles).empty_tiles if rollouts_data else 0

        self.last_move_stats = {
            'time_taken': time.time() - start_time,
            'num_rollouts': num_rollouts,
            'average_empty_tiles': average_empty_tiles,
            'max_empty_tiles': max_empty_tiles,
        }