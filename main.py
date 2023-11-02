# main.py
from graph import Graph
from visualizer import TreeVisualizer
from solvers.dfs_solver import DFSSolver

def main():
    game_tree = Graph(depth=4)
    dfs_solver = DFSSolver(game_tree.root)
    dfs_solver.solve()

    visualizer = TreeVisualizer(game_tree.root, dfs_solver)
    visualizer.animate_solver_process()
    visualizer.highlight_best_path()

if __name__ == "__main__":
    main()