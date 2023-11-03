# solvers/node.py

import copy
import networkx as nx

class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.children = []
