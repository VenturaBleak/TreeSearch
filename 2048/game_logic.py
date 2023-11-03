# game_logic.py
import numpy as np
import random

class Game:
    def __init__(self, size=4, win_tile=2048):
        self.win_tile = win_tile
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.score = 0
        self.game_over = False
        self.direction_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}

    def new_game(self, size):
        grid = np.zeros((size, size), dtype=int)
        return self.place_random(grid, 2)  # Place two '2's in the grid to start

    def place_random(self, grid, count):
        empty_cells = np.argwhere(grid == 0)
        indices = np.random.choice(len(empty_cells), size=min(count, len(empty_cells)), replace=False)
        for index in indices:
            y, x = empty_cells[index]
            grid[y, x] = 2
        return grid

    def compress(self, grid):
        new_grid = np.zeros_like(grid)
        changed = False
        for row in range(self.size):
            non_zero_elements = grid[row][grid[row] != 0]
            non_zero_elements = non_zero_elements[:self.size]
            new_grid[row, :len(non_zero_elements)] = non_zero_elements
            if len(non_zero_elements) < self.size:
                changed = True
        return new_grid, changed

    def merge(self, grid):
        changed = False
        for row in range(self.size):
            for col in range(self.size - 1):
                if grid[row, col] == grid[row, col + 1] and grid[row, col] != 0:
                    grid[row, col] *= 2
                    grid[row, col + 1] = 0
                    self.score += grid[row, col]
                    changed = True
        return grid, changed

    def move(self, direction_num):
        string_direction = self.direction_map.get(direction_num, None)

        if string_direction is None:
            raise ValueError("Invalid numeric direction. Must be 0, 1, 2, or 3.")

        original_grid = self.grid.copy()
        if direction_num == 0:  # Up
            self.grid = np.rot90(self.grid)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.rot90(self.grid, -1)
        elif direction_num == 1:  # Down
            self.grid = np.rot90(self.grid, -1)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.rot90(self.grid)
        elif direction_num == 2:  # Left
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
        elif direction_num == 3:  # Right
            self.grid = np.fliplr(self.grid)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.fliplr(self.grid)

        change_made = compressed or merged
        if compressed or merged:
            self.grid = self.place_random(self.grid, 1)

        return change_made  # Return whether a change has been made to the grid

    def check_win(self):
        # Win condition should not set the game as over; it should only check for win
        return np.any(self.grid == self.win_tile)

    def check_no_moves(self):
        can_move = False  # Assume no moves are possible unless proven otherwise
        for direction_num in range(4):
            temp_grid = np.copy(self.grid)
            if self.move(direction_num):  # Attempt to make a move
                can_move = True
            self.grid = temp_grid  # Reset grid to original after checking
            if can_move:  # If a move is possible, break early
                break
        self.game_over = not can_move

    def play(self, direction_num):
        if not self.game_over:
            change_made = self.move(direction_num)
            if not change_made:
                return self.grid, self.score, self.game_over
            self.check_win()
            self.check_no_moves()
        return self.grid, self.score, self.game_over

    def get_max_tile(self):
        return np.max(self.grid)

    def get_legal_moves(self):
        legal_moves = []
        for direction_num in self.direction_map:
            grid_copy = self.grid.copy()
            self.move(direction_num)
            if not np.array_equal(grid_copy, self.grid):
                legal_moves.append(direction_num)
            self.grid = grid_copy  # Reset grid to original
        return legal_moves

    def make_random_move(self):
        legal_moves = self.get_legal_moves()
        if legal_moves:
            move_num = random.choice(legal_moves)
            self.play(move_num)
            return move_num
        return None

# Example of usage:
game = Game()
print(game.grid)
_, _, game_over = game.play(1)  # Make a move (down)
print(game.grid)
_, _, game_over = game.play(1)  # Make a move (down)
print(game.grid)
_, _, game_over = game.play(1)  # Make a move (down)
print(game.grid)
print(game_over)