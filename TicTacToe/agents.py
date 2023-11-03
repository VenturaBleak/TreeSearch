# agents.py
import random
import numpy as np

class Agent:
    # Every agent should be able to select a move given a game state
    def select_move(self, game_state):
        raise NotImplementedError()

class RandomAgent(Agent):
    # Selects a random legal move from the game state
    def select_move(self, game_state):
        return random.choice(game_state.legal_actions())

class MinimaxAgent(Agent):
    # Initializer sets the depth limit for the minimax search
    def __init__(self, depth_limit=3):
        self.depth_limit = depth_limit

    # Selects a move using the minimax algorithm with alpha-beta pruning
    def select_move(self, game_state):
        # Determine if we are maximizing or minimizing
        is_maximizing = game_state.current_player == game_state.PLAYER1
        best_move = None
        # Set the initial best score to the worst possible
        best_score = float('-inf') if is_maximizing else float('inf')

        # Evaluate all possible legal moves
        for move in game_state.legal_actions():
            game_state.set_move(*move)  # Apply a move
            # Start the minimax search
            score = self.minimax(game_state, self.depth_limit - 1, -float('inf'), float('inf'), not is_maximizing)
            game_state.undo_move(*move)  # Undo the move

            # Update the best score and move
            if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
                best_score = score
                best_move = move

        return best_move

    # Minimax search with alpha-beta pruning
    def minimax(self, game_state, depth, alpha, beta, is_maximizing):
        status = game_state.check_game_status()  # Check the current game status
        if depth == 0 or status != game_state.NOT_FINISHED:  # If reached depth limit or end game
            return self.evaluate(game_state, status)  # Evaluate the board

        # Maximizing player logic
        if is_maximizing:
            max_eval = float('-inf')
            for move in game_state.legal_actions():
                game_state.set_move(*move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, False)
                game_state.undo_move(*move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)  # Update alpha
                if beta <= alpha:  # Beta cut-off
                    break
            return max_eval
        # Minimizing player logic
        else:
            min_eval = float('inf')
            for move in game_state.legal_actions():
                game_state.set_move(*move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, True)
                game_state.undo_move(*move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # Update beta
                if beta <= alpha:  # Alpha cut-off
                    break
            return min_eval

    # Evaluates the game state
    def evaluate(self, game_state, status):
        # Check the game status and return the appropriate score
        if status == game_state.P1_WIN:
            return float('inf')  # Maximizing player wins
        elif status == game_state.P2_WIN:
            return float('-inf')  # Minimizing player wins
        elif status == game_state.DRAW:
            return 0  # Draw
        # Can add heuristic evaluation for non-terminal states if necessary
        return 0