# agents.py
import random
import time
import numpy as np
import itertools

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


class MCTSAgent:
    """Monte Carlo Tree Search agent for the game of 2048."""

    def __init__(self, time_limit: float, max_depth: int = np.inf):
        """
        Initializes the MCTS agent with a time limit and maximum depth for playouts.
        """
        self.time_limit = time_limit / 1000  # Convert to seconds
        self.max_depth = max_depth
        self.last_move_stats = {}

    def select_move(self, game_state: Board):
        rollouts_data = []
        start_time = time.time()

        while time.time() - start_time < self.time_limit:
            move = random.choice(game_state.get_available_moves())
            score, steps, empty_tiles, highest_value = self.random_playout(game_state, move)
            if score != -np.inf:
                rollouts_data.append((move, steps, empty_tiles, highest_value))

        if rollouts_data:
            best_move = self.select_best_move(rollouts_data)
        else:
            best_move = None

        # Update last move statistics
        self.last_move_stats = self.calculate_move_stats(rollouts_data, best_move)

        return best_move

    def random_playout(self, game_state: Board, move):
        """Simulates a random playout from the current state after a given move."""
        board_copy = Board()
        board_copy.board = np.copy(game_state.board)
        board_copy.score = game_state.score

        steps = 0
        board_copy.move(move)

        # Check if the move resulted in a change
        if np.array_equal(board_copy.board, game_state.board):
            return -np.inf, 0, 0, 0

        # Perform random moves until the game is over or max depth is reached
        while not board_copy.is_game_over() and steps < self.max_depth:
            random_move = random.choice(board_copy.get_available_moves())
            board_copy.move(random_move)
            steps += 1

        empty_tiles = np.count_nonzero(board_copy.board == 0)
        highest_value = np.max(board_copy.board)
        return board_copy.score, steps, empty_tiles, highest_value

    def select_best_move(self, rollouts_data):
        # Sort rollouts data based on the heuristic
        rollouts_data.sort(key=lambda x: (-x[1], -x[2], -x[3]))

        # Filter moves with the longest rollout length
        max_length = max(rollouts_data, key=lambda x: x[1])[1]
        longest_rollouts = [data for data in rollouts_data if data[1] == max_length]

        # If there's more than one longest rollout, proceed with the next criteria
        if len(longest_rollouts) > 1:
            # Further sort by number of empty tiles and highest value
            longest_rollouts.sort(key=lambda x: (-x[2], -x[3]))
            # Choose move with max empty tiles if there is still a tie
            max_empty_tiles = max(longest_rollouts, key=lambda x: x[2])[2]
            top_moves = [data for data in longest_rollouts if data[2] == max_empty_tiles]

            # If there's still a tie, pick randomly
            if len(top_moves) > 1:
                return random.choice(top_moves)[0]
            else:
                return top_moves[0][0]
        else:
            return longest_rollouts[0][0]

    def calculate_move_stats(self, rollouts_data, best_move):
        """Calculates and returns the statistics for the last move."""
        num_rollouts = len(rollouts_data)
        total_move_length = sum(data[1] for data in rollouts_data)
        average_move_length = total_move_length / num_rollouts if num_rollouts else 0
        best_move_length = next((data[1] for data in rollouts_data if data[0] == best_move), 0)

        return {
            'time_taken': self.time_limit,
            'num_rollouts': num_rollouts,
            'average_move_length': average_move_length,
            'best_move_length': best_move_length
        }