# visualize_solution.py
import pygame
from game_logic import TicTacToe
from agents import RandomAgent, MinimaxAgent
from visualizer import Visualizer

def main():
    game = TicTacToe()
    player1 = MinimaxAgent(depth_limit=50000)
    player2 = MinimaxAgent(depth_limit=5)
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
            # Determine move based on current player
            if game.current_player == game.PLAYER1:
                move = player1.select_move(game)
            else:
                move = player2.select_move(game)
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