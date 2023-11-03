# game_state.py
from game_logic import Game

class GameState:
    def __init__(self):
        self.game = Game()  # Create an instance of the Game class
        self.reset()

    def reset(self):
        self.matrix = self.game.reset_game()  # Use methods from the Game instance
        self.score = 0
        self.terminated = False

    def update_state(self, command):
        try:
            done = command()  # Execute the move command
            if done:
                self.game.add_random_tile()  # Add a random tile after a successful move
                current_state = self.game.game_state()  # Check the game state
                if current_state == 'win':
                    self.terminated = True
                    return self.matrix, 'You win!'
                elif current_state == 'lose':
                    self.terminated = True
                    return self.matrix, 'You lose!'
                # If game is not over, just return the updated matrix and terminated status
                return self.matrix, self.terminated
        except Exception as e:
            print(f"An error occurred: {e}")
        return self.matrix, self.terminated