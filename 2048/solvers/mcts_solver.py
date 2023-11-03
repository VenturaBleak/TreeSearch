import math
import random
from collections import defaultdict
import numpy as np

# mcts.py
from game_logic import Game

class MCTSNode:
    def __init__(self, game, move=None, parent=None):
        self.game = game  # The game state at this node
        self.move = move  # The move that led to this game state
        self.parent = parent  # The parent node of this node
        self.children = []  # Child nodes of this node
        self.wins = 0  # Number of wins when simulating from this node
        self.visits = 0  # Number of visits to this node during the search
        self.untried_actions = self.untried_moves()  # Legal moves from this node that haven't been tried
        self.is_terminal_state = game.game_over  # Boolean flag indicating if the game is over at this node

    def untried_moves(self):
        # Get legal moves from the current game state
        return self.game.get_legal_moves()

    def expand(self):
        # Expand the tree by one of the untried moves and return the new child node
        move = self.untried_actions.pop()  # Remove a move from untried actions
        new_game_state = clone_game(self.game)  # Clone the current game state to apply the move
        new_game_state.play(move)  # Apply the move
        child_node = MCTSNode(new_game_state, move=move, parent=self)  # Create a new child node with the new game state
        self.children.append(child_node)  # Add the new child node to the children list
        return child_node

    def update(self, result):
        # Update this node's data with the result of a simulation
        self.visits += 1  # Increment the visit count
        self.wins += result  # Add the result to the win count

    def is_terminal(self):
        # Check if the game is over at this node
        return self.game.game_over

    def reward(self):
        # Define the reward for simulations
        # For 2048, a possible reward could be based on the number of empty tiles
        # This reward function could be more complex to better reflect good game states
        empty_tiles = np.count_nonzero(self.game.grid == 0)
        return empty_tiles

    def __hash__(self):
        # Define a hash for the node based on its game state
        return hash(self.game.grid.tostring())

    def __eq__(self, other):
        # Nodes are equal if their game states are equal
        return np.array_equal(self.game.grid, other.game.grid)

    def find_children(self):
        # Find all possible children of this node (all possible moves)
        if self.is_terminal_state:
            return set()  # If the game is over, there are no children
        children = set()
        for move in self.untried_actions:
            new_game_state = clone_game(self.game)
            new_game_state.play(move)
            children.add(MCTSNode(new_game_state, move=move, parent=self))
        return children

    def find_random_child(self):
        # Find a random child node
        if self.is_terminal_state:
            return None  # If the game is over, there is no random child
        move = random.choice(self.untried_actions)  # Choose a random move
        new_game_state = clone_game(self.game)
        new_game_state.play(move)
        return MCTSNode(new_game_state, move=move, parent=self)

class MCTS:
    # Constructor for the MCTS class.
    def __init__(self, exploration_weight=1):
        # Total accumulated reward for each node, used in calculating UCT values.
        self.Q = defaultdict(int)
        # The number of times each node has been visited, used in calculating UCT values.
        self.N = defaultdict(int)
        # Dictionary mapping a node to its children nodes.
        self.children = defaultdict(list)
        # Parameter to balance exploration & exploitation, higher values favor exploring less visited nodes.
        self.exploration_weight = exploration_weight

    # Chooses the best child node to visit based on UCT scores.
    def choose(self, node):
        # If the node passed is a terminal node (end of game), raise an error as there's no child to choose.
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        # If the node has no children, a random child node is selected.
        if not self.children[node]:
            return node.find_random_child()

        # score is a local function used to calculate the UCT score for a node.
        # It's a nested function as it's only used within the scope of 'choose'.
        def score(n):
            # If the node has not been visited yet, it gets a score of negative infinity to encourage exploration.
            if self.N[n] == 0:
                return float("-inf")
            # Otherwise, the score is the average reward per visit for the node.
            return self.Q[n] / self.N[n]

        # Selects the child with the highest UCT score.
        return max(self.children[node], key=score)

    # Performs multiple rollouts (simulations) to estimate the value of the current node.
    def do_rollouts(self, node, n_rollouts, max_depth=7):
        # Loop to perform n_rollouts simulations.
        for _ in range(n_rollouts):
            # Select a path through the tree to a leaf node.
            path = self._select(node)
            leaf = path[-1]  # The last node in the path is the leaf node.
            # Expand the tree from the leaf node, adding one layer of children nodes.
            self._expand(leaf)
            # Simulate a game from the leaf node and obtain a reward.
            reward = self._simulate(leaf, max_depth)
            # Propagate the results of the simulation back up the tree.
            self._backpropagate(path, reward)

    # Simulates a game from the given node to a specified depth.
    def _simulate(self, node, max_depth):
        # Flag to track whose "turn" it is; invert on each level to simulate the opponent's turn.
        invert_reward = True
        # Counter to track the depth of the simulation.
        depth = 0
        # Continue simulation until terminal state or max depth reached.
        while not node.is_terminal() and depth < max_depth:
            # Select a random child of the node to explore.
            node = node.find_random_child()
            # Invert the flag as we go one level deeper in the simulation.
            invert_reward = not invert_reward
            depth += 1
        # Get the reward from the node where the simulation ended.
        reward = node.reward()
        # If the simulation ended on the opponent's turn, invert the reward.
        return 1 - reward if invert_reward else reward

    # Selects a path through the tree to a leaf node that has not been fully expanded.
    def _select(self, node):
        # List to keep track of the path taken to reach the leaf.
        path = []
        # Loop until a leaf node is reached.
        while True:
            path.append(node)
            # If a node has no children or is terminal, we've reached a leaf.
            if not self.children[node] or node.is_terminal():
                return path
            # Filter out the children that have not been explored.
            unexplored = self.children[node] - set(self.children)
            # If there's any unexplored node, select it and return the path.
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            # If all children are explored, use the UCT selection method to choose a node.
            node = self._uct_select(node)

    # Expands the tree from the given node by adding all possible children to the node.
    def _expand(self, node):
        # If the node is not in children or has no children, find all children and add them.
        if node not in self.children or not self.children[node]:
            self.children[node] = node.find_children()

    # Updates the statistics for the nodes in the path after a simulation.
    def _backpropagate(self, path, reward):
        # Go through the path in reverse (from leaf to root).
        for node in reversed(path):
            # Increment the visit count for the node.
            self.N[node] += 1
            # Update the total reward for the node.
            self.Q[node] += reward
            # Invert the reward as we go back up the tree.
            reward = 1 - reward

    # Uses the UCT formula to select the best node to explore next.
    def _uct_select(self, node):
        # Ensure that each child has been added to the tree.
        assert all(n in self.children for n in self.children[node])

        # Calculate the logarithm of the visit count for the current node.
        log_N_vertex = math.log(self.N[node])

        # UCT calculation for a node, balancing exploration and exploitation.
        def uct(n):
            # Calculate the UCT score for the node.
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        # Select the child with the maximum UCT score.
        return max(self.children[node], key=uct)

# Function to clone a game state.
def clone_game(game):
    # Create a new game instance with the same size and win conditions.
    new_game = Game(size=game.size, win_tile=game.win_tile)
    # Deep copy the grid to ensure no references to the original game grid remain.
    new_game.grid = np.copy(game.grid)
    # Copy the current score from the original game.
    new_game.score = game.score
    # Copy the win status from the original game.
    new_game.is_win = game.is_win
    # Copy the game over status from the original game.
    new_game.game_over = game.game_over
    # Return the new cloned game.
    return new_game
