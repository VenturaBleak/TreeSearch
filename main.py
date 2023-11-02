# main.py
from graph import Graph
from visualizer import Visualizer

if __name__ == "__main__":
    g = Graph()
    v = Visualizer(g.root)
    v.visualize()