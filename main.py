# main.py
from graph import Graph
from visualizer import TreeVisualizer
from solvers.dfs_solver import DFSSolver

def main():
    game_tree = Graph(depth=3)
    dfs_solver = DFSSolver(game_tree.root)
    dfs_solver.solve()

    visualizer = TreeVisualizer(game_tree.root)
    visualizer.run(dfs_solver)

if __name__ == "__main__":
    main()