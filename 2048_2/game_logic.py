# game_logic.py
import numpy as np
from numpy.random import choice

# Enumeration for actions that can be performed in the game.
class Action:
    UP = 3
    RIGHT = 2
    DOWN = 1
    LEFT = 0

# The Board class encapsulates the game state.
class Board:
    def __init__(self, size=4):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        self.add_tile()
        self.add_tile()

    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        self.add_tile()
        self.add_tile()

    def rotate_board(self, action):
        return np.rot90(self.board, -action)

    def stack(self, board):
        new_board = np.zeros_like(board)
        for i in range(self.size):
            fill_position = 0
            for j in range(self.size):
                if board[i][j] != 0:
                    new_board[i][fill_position] = board[i][j]
                    fill_position += 1
        return new_board

    def merge(self, board):
        for i in range(self.size):
            for j in range(self.size-1):
                if board[i][j] == board[i][j+1] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i][j+1] = 0
                    self.score += board[i][j]
        return board

    def move(self, action):
        original_board = self.board.copy()
        self.board = self.rotate_board(action)
        self.board = self.stack(self.board)
        self.board = self.merge(self.board)
        self.board = self.stack(self.board)
        self.board = self.rotate_board(-action)
        if not all((self.board == original_board).flatten()):
            self.add_tile()

    def add_tile(self):
        if self.is_board_full():
            return
        empty_cells = [(x, y) for x, y in zip(*np.where(self.board == 0))]
        if not empty_cells:  # Just in case there are no empty cells.
            return
        index = np.random.choice(len(empty_cells))
        cell = empty_cells[index]
        self.board[cell] = 4 if np.random.rand() < 0.1 else 2

    def is_board_full(self):
        return not np.any(self.board == 0)

    def get_available_moves(self):
        available_moves = []
        for action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
            board_copy = self.board.copy()
            self.move(action)
            if not all((self.board == board_copy).flatten()):
                available_moves.append(action)
            self.board = board_copy  # revert the move
        return available_moves

    def is_game_over(self):
        return self.is_board_full() and not self.get_available_moves()

    def __str__(self):
        return np.array_str(self.board)