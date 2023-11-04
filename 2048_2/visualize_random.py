import pygame
import random
from game_visualizer import Visualizer
from game_logic import Board, Action

def main():
    EPISODES = 10
    visualizer = Visualizer()

    for episode in range(EPISODES):
        game = Board()
        running = True

        while running and not game.is_game_over():
            visualizer.draw_board(game)

            # Make a random move from the legal actions
            action = random.choice(game.get_available_moves())
            game.move(action)

            visualizer.update_display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Instead of limiting the frame rate, wait for a second
            pygame.time.wait(100)  # waits for 1000 milliseconds or 1 second

    visualizer.close()

if __name__ == "__main__":
    main()