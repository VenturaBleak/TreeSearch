# game_logic.py

class GameState:
    def __init__(self, value=0):
        self.value = value  # -1, 0, or 1
        self.is_terminal = False

    def evaluate(self):
        return self.value

    def possible_moves(self):
        if not self.is_terminal:
            return [GameState() for _ in range(3)]
        return []
