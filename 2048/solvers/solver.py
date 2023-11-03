class Solver:
    def __init__(self, game):
        self.game = game

    def solve(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def is_solution(self, state):
        return state.terminated and not state.truncated

    def get_next_states(self, state):
        legal_moves = state.get_legal_moves()
        next_states = []
        for move in legal_moves:
            new_state = deepcopy(state)
            new_state.play(move)
            next_states.append((new_state, move))
        return next_states

    def reset(self):
        self.game.grid = self.game.new_game(self.game.size)
        self.game.score = 0
        self.game.truncated = False
        self.game.terminated = False