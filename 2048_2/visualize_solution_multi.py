# visualize_solution.py
from game_logic import Board
import cProfile, pstats, io
from pstats import SortKey
import time
from copy import copy
import pandas as pd

from agents import RandomAgent
from agents_multi import MCTSAgent


def main():
    pr = cProfile.Profile()
    pr.enable()
    game_start_time = time.time()
    board = Board()
    agent = MCTSAgent(time_limit=1500, max_depth=7, num_processes=4)

    running = True
    reached_2048 = False
    while running and not board.is_game_over():

        move = agent.select_move(copy(board))
        board.move(move)

        # Check for reaching 2048 tile
        if board.has_reached_2048():
            reached_2048 = True
            break

        # save info in pandas dataframe, then print it
        # Use a multi-line f-string for a clean, formatted print output
        print((
            f"----------------------------------------\n"
            f"Time: {time.time() - game_start_time:.2f} seconds\n"
            f"Score: {board.score} | Highest Tile: {board.highest_value}\n"
            f"Move stats: {agent.last_move_stats}\n"
            f"{board}\n"
        ))

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
