from game_logic import Board
import numpy as np

# set seed and np.random.seed
np.random.seed(42)

# Instantiate the board with the given state
initial_state = [
    [128, 4, 0, 2],
    [4, 32, 8, 4],
    [16, 64, 16, 8],
    [32, 8, 4, 16]
]

# Create a new Board instance
board = Board()
board.board = np.array(initial_state)
print("Initial Board State:")
print(board.board)

# Apply the move (assuming 3 corresponds to 'up')
board.move(3)

# Check if the game is over
is_game_over = board.is_game_over()
print("Board State After Move:")
print(board.board)
print(f"Board is full: {board.is_board_full()}")
print(f"available moves: {board.get_available_moves()}")
print("Is Game Over:", is_game_over)