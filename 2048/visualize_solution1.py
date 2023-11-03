# visualize_solution.py
import time
from tkinter import Tk
from game_logic import Game
from game_ui import GameUI
from solvers.mcts_solver import MCTS, MCTSNode  # Import the correct solver

def main():
    root = Tk()
    game = Game()
    game_ui = GameUI(root, game, visual=True)
    game_ui.init_ui()
    mcts = MCTS(exploration_weight=1.4)

    root_node = MCTSNode(game)
    mcts.children[root_node] = root_node.find_children()  # Initialize the root's children

    # Adjust the game loop
    while not game.game_over:
        mcts.do_rollouts(root_node, n_rollouts=32, max_depth=7)  # Perform 100 rollouts to depth 5-10
        root_node = mcts.choose(root_node)  # Choose the best move based on the rollouts
        game.play(root_node.move)
        game_ui.update_grid_cells()
        time.sleep(0)  # Sleep time for visualization

        if not root_node.untried_actions:
            print("No moves left, game over")
            break

    print("Game Over!" if game.game_over else "Maximized empty tiles!")
    root.mainloop()

if __name__ == "__main__":
    main()
