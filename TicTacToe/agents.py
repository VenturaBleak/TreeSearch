# agents.py
import random

# Constants to represent the score for winning and losing.
WIN_SCORE = 10000  # A high positive score for winning.
LOSE_SCORE = -WIN_SCORE  # A high negative score for losing.


class Agent:
    """
    Base class for an agent that can play a game by selecting moves.
    Each agent subclass should implement the `select_move` method.
    """

    def select_move(self, game_state):
        """
        Selects the next move given the current game state.

        :param game_state: The current state of the game.
        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError()


class RandomAgent(Agent):
    """
    Agent that selects a move randomly from the available legal moves.
    Inherits from the Agent class.
    """

    def select_move(self, game_state):
        """
        Selects a random move from the game state's legal actions.

        :param game_state: The current state of the game.
        :return: A move selected at random from the legal moves.
        """
        return random.choice(game_state.legal_actions())


class MinimaxAgent(Agent):
    """
    Agent that uses the Minimax algorithm to select the best move based on
    game state evaluation. It employs alpha-beta pruning to optimize the search.

    The Minimax algorithm is a recursive algorithm for choosing the next move in
    an n-player game. A value is associated with each position or state of the game.
    This value is computed by means of a position evaluation function and it indicates
    how good it would be for a player to reach that position.
    """

    def __init__(self, depth_limit=3):
        """
        Initializes the Minimax agent with a depth limit for the search.

        :param depth_limit: The maximum depth the search algorithm will explore.
        """
        self.depth_limit = depth_limit

    def select_move(self, game_state):
        """
        Selects the best move using the Minimax algorithm with alpha-beta pruning.

        :param game_state: The current state of the game.
        :return: The best move determined by the minimax algorithm.
        """
        # Determine if the current agent is maximizing or minimizing.
        is_maximizing = game_state.current_player == game_state.PLAYER1
        best_move = None
        # Initialize best_score to the worst possible score.
        best_score = -WIN_SCORE if is_maximizing else WIN_SCORE

        # Iterate over all legal moves in the current game state.
        for move in game_state.legal_actions():
            game_state.set_move(*move)  # Apply a move
            # Start the minimax search.
            score = self.minimax(game_state, self.depth_limit - 1, -WIN_SCORE, WIN_SCORE, not is_maximizing)
            game_state.undo_move(*move)  # Undo the move

            # Update the best score and move, considering if we want to maximize or minimize the score.
            if best_move is None or (is_maximizing and score > best_score) or (
                    not is_maximizing and score < best_score):
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game_state, depth, alpha, beta, is_maximizing):
        """
        The Minimax function with alpha-beta pruning. It searches the game tree
        to determine the best move by evaluating the game states to a certain depth.

        Alpha-beta pruning is an optimization technique for the minimax algorithm
        that stops evaluating a move when at least one possibility has been found
        that proves the move to be worse than a previously examined move.

        :param game_state: The current state of the game.
        :param depth: The current depth in the game tree.
        :param alpha: The best already explored option along the path for the maximizer.
        :param beta: The best already explored option along the path for the minimizer.
        :param is_maximizing: A boolean flag that is True if the current player is maximizing.
        :return: The best evaluated score for the current move.
        """
        # Check the current status of the game or if we've reached the depth limit.
        status = game_state.check_game_status()
        if depth == 0 or status != game_state.NOT_FINISHED:
            # Return the evaluated score of the game state.
            return self.evaluate(game_state, status, self.depth_limit - depth)

        # Logic for the maximizing player.
        if is_maximizing:
            max_eval = -WIN_SCORE
            for move in game_state.legal_actions():
                game_state.set_move(*move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, False)
                game_state.undo_move(*move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                # Alpha-beta pruning check.
                if beta <= alpha:
                    break
            return max_eval
        # Logic for the minimizing player.
        else:
            min_eval = WIN_SCORE
            for move in game_state.legal_actions():
                game_state.set_move(*move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, True)
                game_state.undo_move(*move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                # Alpha-beta pruning check.
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, game_state, status, depth):
        """
        Evaluates the game state and returns a score indicating how favorable the state is.
        Adjusts scores to prioritize quicker wins and slower losses.

        :param game_state: The current state of the game.
        :param status: The status of the game (win, lose, draw, ongoing).
        :param depth: The depth of the game state in the search tree.
        :return: The score representing the favorability of the state.
        """
        if status == game_state.P1_WIN:
            # Subtract depth to prioritize quicker wins.
            return WIN_SCORE - depth
        elif status == game_state.P2_WIN:
            # Add depth to prioritize slower losses.
            return LOSE_SCORE + depth
        elif status == game_state.DRAW:
            return 0
        else:
            # Implement your heuristic evaluation here for non-terminal states.
            # This heuristic needs to be designed based on game-specific factors.
            return heuristic_evaluation(game_state)

    def heuristic_evaluation(self, game_state):
        """
        Evaluates the game state and returns a score indicating how favorable the state is.
        Adjusts scores to prioritize quicker wins and slower losses.

        :param game_state: The current state of the game.
        :return: The score representing the favorability of the state.
        """
        return 0