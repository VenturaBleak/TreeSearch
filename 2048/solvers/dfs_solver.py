# solvers/dfs_solver.py

class DFSSolver(Solver):
    def solve(self):
        root = Node(copy.deepcopy(self.env))  # We make a deep copy of the environment for the root node
        self.tree.add_node(root)
        return self.dfs(root)

    def dfs(self, node):
        # Check if the current state is a goal state
        is_goal = self.is_goal(node.state)
        if is_goal:
            return self.reconstruct_path(node)

        legal_moves = node.state.get_legal_moves()
        for action in legal_moves:
            # Perform the action and get the new state
            new_state = copy.deepcopy(node.state)
            new_state.step(action)
            child_node = Node(new_state, parent=node, action=action, depth=node.depth+1)
            self.tree.add_node(child_node)
            self.tree.add_edge(node, child_node)

            result = self.dfs(child_node)
            if result:
                return result
        return None

    def is_goal(self, state):
        # Define goal condition
        return state.is_goal()

    def reconstruct_path(self, node):
        # Reconstruct the path from node to root
        path = []
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1]  # Return reversed path