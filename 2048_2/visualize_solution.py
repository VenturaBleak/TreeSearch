import pygame
from game_logic import Board
from agents import RandomAgent, MCTSAgent
from game_visualizer import Visualizer
import cProfile, pstats, io
from pstats import SortKey
import time


def main():
    pr = cProfile.Profile()
    pr.enable()
    game_start_time = time.time()
    board = Board()
    agent = MCTSAgent(time_limit=50, max_depth=10)
    visualizer = Visualizer()

    running = True
    reached_2048 = False
    while running and not board.is_game_over():

        move = agent.select_move(board)
        board.move(move)

        # Check for reaching 2048 tile
        if board.has_reached_2048():
            reached_2048 = True
            break

        visualizer.update_display(board, agent.last_move_stats, reached_2048, time.time() - game_start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.wait(0)

    visualizer.close()
    game_end_time = time.time()

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    total_time = game_end_time - game_start_time
    print(f"Time to reach 2048: {total_time:.2f} seconds" if reached_2048 else "Did not reach 2048.")


if __name__ == "__main__":
    main()
