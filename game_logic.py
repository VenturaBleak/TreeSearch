# game_logic.py
import random

class GameState:
    def __init__(self, value=None):
        self.value = value  # -1, 0, or 1 only for terminal nodes
        self.is_terminal = value is not None

    def possible_moves(self):
        if not self.is_terminal:
            # Each non-terminal node has 2-3 child nodes.
            return [GameState() for _ in range(random.randint(2, 3))]
        return []
