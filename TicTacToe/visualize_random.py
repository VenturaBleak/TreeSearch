# visualize_random.py
import random
import pygame

# import custom modules
from game_logic import TicTacToe
from visualizer import Visualizer

def main():
    EPISODES = 10

    for episode in range(EPISODES):
        game = TicTacToe()
        visualizer = Visualizer()
        running = True
        clock = pygame.time.Clock()
        while running:
            # Draw the current state of the game
            visualizer.draw_board(game.board)

            # Check if the game is over
            status = game.check_game_status()
            if status != game.NOT_FINISHED:
                running = False
            else:
                # Make a random move from the legal actions
                move = random.choice(game.legal_actions())
                game.set_move(*move)

            # Update the display
            visualizer.update_display()

            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Limit the frame rate
            clock.tick(10)

    visualizer.close()

if __name__ == "__main__":
    main()