import pygame
from game_logic import Board, Action

class Visualizer:
    BACKGROUND_COLOR_GAME = "#92877d"
    BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
    BACKGROUND_COLOR_DICT = {
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e",
        4096: "#eee4da",
        8192: "#edc22e",
        16384: "#f2b179",
        32768: "#f59563",
        65536: "#f67c5f",
    }

    CELL_COLOR_DICT = {
        2: "#776e65",
        4: "#776e65",
        8: "#f9f6f2",
        16: "#f9f6f2",
        32: "#f9f6f2",
        64: "#f9f6f2",
        128: "#f9f6f2",
        256: "#f9f6f2",
        512: "#f9f6f2",
        1024: "#f9f6f2",
        2048: "#f9f6f2",
        4096: "#776e65",
        8192: "#f9f6f2",
        16384: "#776e65",
        32768: "#776e65",
        65536: "#f9f6f2",
    }
    TILE_FONT = ("Verdana", 40, "bold")
    TEXT_FONT = ("Verdana", 20)

    # You might want to increase the window height to make room for the info text
    def __init__(self, board_size=4, tile_size=100, tile_margin=15, info_height=100, stats_width=400):
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.board_size = board_size
        self.window_width = (self.board_size * (self.tile_size + self.tile_margin)) + self.tile_margin + stats_width
        self.window_height = (self.board_size * (self.tile_size + self.tile_margin)) + self.tile_margin + info_height
        self.info_height = info_height
        self.stats_width = stats_width
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('2048')

    def draw_tile(self, value, x, y):
        bg_color = pygame.Color(self.BACKGROUND_COLOR_DICT.get(value, self.BACKGROUND_COLOR_CELL_EMPTY))
        fg_color = pygame.Color(self.CELL_COLOR_DICT.get(value, "#776e65"))
        rect = (x * (self.tile_size + self.tile_margin) + self.tile_margin,
                y * (self.tile_size + self.tile_margin) + self.tile_margin,
                self.tile_size, self.tile_size)
        pygame.draw.rect(self.window, bg_color, rect)
        if value:
            font = pygame.font.SysFont(*self.TILE_FONT)
            text = font.render(f"{value}", True, fg_color)
            text_rect = text.get_rect(center=(rect[0] + self.tile_size / 2, rect[1] + self.tile_size / 2))
            self.window.blit(text, text_rect)

    def draw_bottom_info(self, board, reached_2048, elapsed_time):
        font = pygame.font.SysFont(*self.TEXT_FONT)
        bottom_info_text = f"Score: {board.score} | Highest Value {board.highest_value} | 2048: {'SUCCESS!!!' if reached_2048 else 'not reached'} | Time: {elapsed_time:.2f} s"
        text_surface = font.render(bottom_info_text, True, pygame.Color("black"))
        y_position = (self.board_size * (self.tile_size + self.tile_margin)) + self.tile_margin // 2
        self.window.blit(text_surface, (self.tile_margin, y_position))

    def draw_right_stats(self, last_move_stats):
        font = pygame.font.SysFont(*self.TEXT_FONT)
        x_position = (self.board_size * (self.tile_size + self.tile_margin)) + self.tile_margin
        y_offset = self.tile_margin
        for key, value in last_move_stats.items():
            stats_text = f"{key}: {value}"
            text_surface = font.render(stats_text, True, pygame.Color("black"))
            self.window.blit(text_surface, (x_position, y_offset))
            y_offset += text_surface.get_height() + 5

    def draw_board(self, board):
        self.window.fill(pygame.Color(self.BACKGROUND_COLOR_GAME))
        for y in range(board.size):
            for x in range(board.size):
                value = board.board[y][x]
                self.draw_tile(value, x, y)

    def update_display(self, board, last_move_stats, reached_2048, elapsed_time):
        self.draw_board(board)  # Draw the board first
        self.draw_bottom_info(board, reached_2048, elapsed_time)
        self.draw_right_stats(last_move_stats)
        pygame.display.flip()

    def close(self):
        pygame.quit()