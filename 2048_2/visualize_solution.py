import pygame
from game_logic import Board, Action
from agents import RandomAgent, MCTSAgent
from game_visualizer import Visualizer
import cProfile, pstats, io
from pstats import SortKey

def main():
    pr = cProfile.Profile()
    pr.enable()
    game = Board()
    agent = RandomAgent()  # or MCTS() once you have implemented it
    agent = MCTSAgent(10)
    visualizer = Visualizer()

    running = True

    while running and not game.is_game_over():
        visualizer.draw_board(game)

        move = agent.select_move(game)
        game.move(move)

        visualizer.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.wait(10)

    visualizer.close()

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == "__main__":
    main()
