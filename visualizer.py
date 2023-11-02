# visualizer.py
import networkx as nx
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, root_node):
        self.graph = nx.DiGraph()
        self.add_nodes(root_node)

    def add_nodes(self, node):
        self.graph.add_node(node)
        for child in node.children:
            self.graph.add_edge(node, child)
            self.add_nodes(child)

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold', node_color="skyblue")
        plt.show()