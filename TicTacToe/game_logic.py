# game_logic.py
import numpy as np
import random

class TicTacToe:
    PLAYER1, PLAYER2 = 1, 2
    NOT_FINISHED, DRAW, P1_WIN, P2_WIN = -1, 0, 1, 2

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = self.PLAYER1

    def check_game_status(self):
        # Check for wins in rows, columns, and diagonals
        for player in [self.PLAYER1, self.PLAYER2]:
            if any(np.all(self.board == player, axis=0)) or \
                    any(np.all(self.board == player, axis=1)) or \
                    np.all(np.diag(self.board) == player) or \
                    np.all(np.diag(np.fliplr(self.board)) == player):
                return self.P1_WIN if player == self.PLAYER1 else self.P2_WIN

        # Check for a draw
        if not self.empty_cells():
            return self.DRAW

        # Game is not finished
        return self.NOT_FINISHED

    def empty_cells(self):
        return list(zip(*np.where(self.board == 0)))

    def valid_move(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3 and self.board[x, y] == 0

    def set_move(self, x, y):
        assert self.valid_move(x, y), "The move is not valid!"
        self.board[x, y] = self.current_player
        self.current_player = self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
        return self.empty_cells()

    def legal_actions(self):
        return self.empty_cells()

    def undo_move(self, x, y):
        self.board[x, y] = 0
        self.current_player = self.PLAYER1 if self.current_player == self.PLAYER2 else self.PLAYER2

# Usage
game = TicTacToe()
print(game.board)
game.set_move(0, 0)  # Player 1 moves
print(game.board)
# Random sample from legal actions
x, y = random.choice(game.legal_actions())
print(f"Player 2 moves to ({x}, {y})")
game.set_move(x, y)  # Player 2 moves
game.legal_actions()  # Get legal actions for Player 1
print(game.board)