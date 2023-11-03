# game_visualize.py
import time
from tkinter import Tk
from game_logic import Game
from game_ui import GameUI
import random

def main():
    root = Tk()
    game = Game()
    game_ui = GameUI(root, game, visual=True)
    game_ui.init_ui()
    game_over = False
    is_won = False

    while not game_over and not is_won:
        legal_moves = game.get_legal_moves()
        print(f"Legal moves: {legal_moves}")
        if legal_moves:  # Check if there are any legal moves left
            action = random.choice(legal_moves)
            grid, score, game_over, is_won = game.play(action)
            game_ui.update_grid_cells()  # Update UI after move
            time.sleep(0.1)
        else:
            print("No moves left, game over")
            break

    print("Game Over!" if game_over else "You Win!")
    root.mainloop()

if __name__ == "__main__":
    main()