# visualize_solution.py
import time
from tkinter import Tk
from game_logic import Game
from game_ui import GameUI
from solvers.dfs_solver import DFSSolver

def main():
    root = Tk()
    game = Game()
    game_ui = GameUI(root, game, visual=True)
    game_ui.init_ui()
    solver = DFSSolver(game)

    while not game.game_over and not game.is_win:
        best_move = solver.solve()
        if best_move is not None:
            game.play(best_move)
            game_ui.update_grid_cells()
            time.sleep(0)  # You can adjust the sleep time as needed
        else:
            print("No moves left, game over")
            break

    print("Game Over!" if game.game_over else "You Win!")
    root.mainloop()

if __name__ == "__main__":
    main()