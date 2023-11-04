# visualize_solution.py
import numpy as np
import pygame

# import custom modules
from game_logic import TicTacToe
from agents import RandomAgent, MinimaxAgent
from visualizer import Visualizer


import cProfile, pstats, io
from pstats import SortKey


def main():
    pr = cProfile.Profile()
    pr.enable()
    game = TicTacToe()
    player1 = RandomAgent()
    player2 = RandomAgent()
    visualizer = Visualizer()

    running = True
    count = 0

    while running:
        count += 1
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
        print(count)

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Instead of limiting the frame rate, wait for a second
        pygame.time.wait(1000)  # waits for 1000 milliseconds or 1 second

    visualizer.close()

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == "__main__":
    main()