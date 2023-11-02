# graph.py
from game_logic import GameState
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.children = []
        self.parent = parent

    def add_child(self, child_node):
        self.children.append(child_node)

class Graph:
    def __init__(self, depth=3):
        root_state = GameState()
        self.root = Node(root_state)
        self.generate_tree(self.root, depth)

    def generate_tree(self, current_node, depth):
        if depth == 0:
            current_node.state.is_terminal = True
            current_node.state.value = random.choice([-1, 0, 1])
            return
        for move in current_node.state.possible_moves():
            child_node = Node(move, current_node)
            current_node.add_child(child_node)
            self.generate_tree(child_node, depth-1)