# game_logic.py
import numpy as np
import random
class Game:
    def __init__(self, size=4, win_tile=2048):
        self.size = size
        self.win_tile = win_tile
        self.grid = self.new_game(size)
        self.truncated = False
        self.terminated = False
        self.score = 0

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
        done = False
        for row in range(self.size):
            non_zero_elements = grid[row][grid[row] != 0]
            non_zero_elements = non_zero_elements[:self.size]
            new_grid[row, :len(non_zero_elements)] = non_zero_elements
            if len(non_zero_elements) < self.size:
                done = True
        return new_grid, done

    def merge(self, grid):
        done = False
        for row in range(self.size):
            for col in range(self.size - 1):
                if grid[row, col] == grid[row, col + 1] != 0:
                    grid[row, col] *= 2
                    grid[row, col + 1] = 0
                    self.score += grid[row, col]
                    done = True
        return grid, done

    def move(self, direction):
        original_grid = self.grid.copy()
        if direction == 'up':
            self.grid = np.rot90(self.grid)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.rot90(self.grid, -1)
        elif direction == 'down':
            self.grid = np.rot90(self.grid, -1)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.rot90(self.grid)
        elif direction == 'left':
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
        elif direction == 'right':
            self.grid = np.fliplr(self.grid)
            compressed_grid, compressed = self.compress(self.grid)
            merged_grid, merged = self.merge(compressed_grid)
            self.grid = self.compress(merged_grid)[0]
            self.grid = np.fliplr(self.grid)

        if compressed or merged:
            self.grid = self.place_random(self.grid, 1)

        if not np.array_equal(self.grid, original_grid):
            self.truncated = True
        else:
            self.truncated = False

    def check_win(self):
        self.terminated = np.any(self.grid == self.win_tile)

    def check_no_moves(self):
        temp_grid = np.copy(self.grid)
        can_merge = any(
            np.array_equal(self.compress(self.grid)[0], temp_grid) == False
            or np.array_equal(self.merge(self.grid)[0], temp_grid) == False
            for _ in range(4)
        )
        self.grid = temp_grid
        self.terminated = not can_merge

    def play(self, direction):
        if not self.terminated:
            self.move(direction)
            self.check_win()
            if not self.truncated:
                self.check_no_moves()
        return self.truncated, self.terminated

    # Add this function to Game class to determine legal moves
    def get_legal_moves(self):
        legal_moves = []
        for direction in ['up', 'down', 'left', 'right']:
            grid_copy = self.grid.copy()
            self.move(direction)
            if not np.array_equal(grid_copy, self.grid):
                legal_moves.append(direction)
            self.grid = grid_copy  # Reset grid to original
        return legal_moves

    # Add this function to Game class to make a random legal move
    def make_random_move(self):
        legal_moves = self.get_legal_moves()
        if legal_moves:  # Check if there are any legal moves left
            move = random.choice(legal_moves)
            self.play(move)
            return move
        return None

# Example of usage:
game = Game()
print(game.grid)
truncated, terminated = game.play('down')  # Make a move
print(game.grid)
truncated, terminated = game.play('down')  # Make a move
print(game.grid)
truncated, terminated = game.play('down')  # Make a move
print(game.grid)
print("Truncated:", truncated)
print("Terminated:", terminated)