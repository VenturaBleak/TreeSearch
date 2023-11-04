# agents.py
# agents.py
import numpy as np
import random
import time
from multiprocessing import Pool
from collections import namedtuple, defaultdict
from copy import deepcopy
from functools import partial

# Assuming game_logic.py and other necessary modules are in the same directory
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
    def __init__(self, time_limit: int, max_depth: int = np.inf, num_processes: int = None):
        self.base_time_limit = time_limit / 1000  # Convert milliseconds to seconds
        self.temporary_time_limit = self.base_time_limit  # Initialize temporary time limit
        self.previous_max_empty_tiles = np.inf
        self.max_depth = max_depth
        self.temporary_depth_limit = max_depth
        self.last_move_stats = {}
        self.num_processes = num_processes

    def adjust_temporary_time_limit(self):
        """Adjust the temporary time limit based on the number of previous max empty tiles."""
        if self.previous_max_empty_tiles >= 4:
            self.temporary_time_limit = self.base_time_limit * 0.05
            self.temporary_depth_limit = self.max_depth
        else:
            # Increase time limit by a more-than-linear function of empty tiles
            # The following is an example, you can define this function as needed
            empty_tiles_factor = max(1, 5 - self.previous_max_empty_tiles)  # Values from 1 to 6
            self.temporary_time_limit = self.base_time_limit * (empty_tiles_factor ** 2.5) / 36
            self.temporary_depth_limit = int(self.max_depth + (empty_tiles_factor) * 1.8)
            print(f"Adjusted time limit: {self.temporary_time_limit:.2f} s | Adjusted depth limit: {self.temporary_depth_limit}")

    def select_move(self, game_state: Board):
        start_time = time.time()
        self.adjust_temporary_time_limit()
        moves = game_state.get_available_moves()

        # Using multiprocessing Pool
        with Pool(self.num_processes) as pool:
            # We pass the entire game state and all available moves to each worker
            # Each worker will then perform random playouts for different moves until the time limit is reached
            rollouts_data = pool.starmap_async(self.random_playout_worker,
                                               [(deepcopy(game_state), moves, self.temporary_time_limit) for _ in
                                                moves]).get()

        # Flattening the list of lists into a single list
        rollouts_data = [item for sublist in rollouts_data for item in sublist]

        # Filter out invalid moves
        rollouts_data = [data for data in rollouts_data if data.empty_tiles != -np.inf]

        best_move = self.evaluate(rollouts_data) if rollouts_data else None
        self.calculate_last_move_stats(rollouts_data, start_time)

        # Update previous_max_empty_tiles for the next move
        self.previous_max_empty_tiles = np.count_nonzero(game_state.board == 0)

        return best_move

    def random_playout_worker(self, game_state, moves, time_limit):
        end_time = time.time() + time_limit
        rollouts_data = []

        while time.time() < end_time:
            move = random.choice(moves)
            _, empty_tiles, high_value_tiles = self.random_playout(game_state, move)
            if empty_tiles != -np.inf:
                rollouts_data.append(MoveEvaluation(move, empty_tiles, high_value_tiles))

        return rollouts_data

    def random_playout(self, game_state: Board, move):
        board_copy = deepcopy(game_state)
        board_copy.move(move)
        if np.array_equal(board_copy.board, game_state.board):
            return move, -np.inf, np.inf

        # Correctly checking the copied board's state for the game-over condition
        for _ in range(self.temporary_depth_limit):
            if board_copy.is_game_over():
                break
            random_move = random.choice(board_copy.get_available_moves())
            board_copy.move(random_move)

        empty_tiles = np.count_nonzero(board_copy.board == 0)
        high_value_tiles = np.count_nonzero(~np.isin(board_copy.board, [0, 2, 4]))
        return move, empty_tiles, high_value_tiles

    def evaluate(self, rollouts_data):
        aggregated_rollouts = defaultdict(list)
        for move, empty_tiles, high_value_tiles in rollouts_data:
            if empty_tiles != -np.inf:
                aggregated_rollouts[move].append(empty_tiles)

        print(aggregated_rollouts)
        best_move = None
        best_score = -np.inf
        for move, scores in aggregated_rollouts.items():
            if scores:
                percentile_value = np.percentile(scores, 75)
                if percentile_value > best_score:
                    best_score = percentile_value
                    best_move = move

        return best_move

    def calculate_last_move_stats(self, rollouts_data, start_time):
        move_count = defaultdict(int)
        total_empty_tiles = defaultdict(int)

        for move, empty_tiles, _ in rollouts_data:
            if empty_tiles != -np.inf:
                move_count[move] += 1
                total_empty_tiles[move] += empty_tiles

        self.last_move_stats = {
            'time_taken': time.time() - start_time,
            'num_rollouts': sum(move_count.values()),
            'average_empty_tiles': {
                move: (total_empty_tiles[move] / count if count else 0)
                for move, count in move_count.items()
            },
        }