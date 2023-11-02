# graph.py
from game_logic import GameState
import random
from anytree import NodeMixin

class TreeNode(NodeMixin):
    def __init__(self, state, parent=None):
        super(TreeNode, self).__init__()
        self.state = state
        self.parent = parent
        self.name = str(state.value) if state.value else str(id(self))

class Graph:
    def __init__(self, depth=3):
        root_state = GameState()
        self.root = TreeNode(root_state)
        self.generate_tree(self.root, depth)

    def generate_tree(self, current_node, depth):
        if depth == 0:
            current_node.state.is_terminal = True
            current_node.state.value = random.randint(0,99)
            return
        for move in current_node.state.possible_moves():
            child_node = TreeNode(move, current_node)
            self.generate_tree(child_node, depth - 1)