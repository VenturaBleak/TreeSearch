# visualizer.py
import pygame


class Visualizer:
    # Style parameters
    GRID_SIZE = 100
    PADDING = 5
    LINE_WIDTH = 5
    LIGHT_SQUARE_COLOR = (238, 238, 210)  # Light color for the checkered board
    DARK_SQUARE_COLOR = (118, 150, 86)  # Dark color for the checkered board
    X_COLOR = (0, 0, 0)  # Black color for 'X'
    O_COLOR = (0, 0, 0)  # Black color for the outline of 'O'

    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.width = self.height = self.GRID_SIZE * 3 + self.PADDING * (3 - 1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tic Tac Toe Visualizer')

    def draw_board(self, board):
        for y in range(3):
            for x in range(3):
                # Determine square color based on position
                color = self.DARK_SQUARE_COLOR if (x + y) % 2 else self.LIGHT_SQUARE_COLOR

                # Calculate square position and size
                rect = pygame.Rect(
                    x * self.GRID_SIZE + x * self.PADDING,
                    y * self.GRID_SIZE + y * self.PADDING,
                    self.GRID_SIZE,
                    self.GRID_SIZE
                )

                # Draw the square
                pygame.draw.rect(self.screen, color, rect)

                # Draw the game pieces
                if board[y, x] == 1:  # PLAYER1 has an 'X'
                    self.draw_x(rect)
                elif board[y, x] == 2:  # PLAYER2 has an 'O'
                    self.draw_o(rect)

    def draw_x(self, rect):
        # Draw 'X' as two lines with a black color
        pygame.draw.line(self.screen, self.X_COLOR, rect.topleft, rect.bottomright, self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.X_COLOR, rect.bottomleft, rect.topright, self.LINE_WIDTH)

    def draw_o(self, rect):
        # Draw 'O' as a ring with a black color
        radius = self.GRID_SIZE // 2 - self.PADDING
        center = rect.center
        pygame.draw.circle(self.screen, self.O_COLOR, center, radius, self.LINE_WIDTH)  # Draw the outline

    def update_display(self):
        pygame.display.flip()

    def close(self):
        # Optionally display the outcome for a few seconds
        pygame.time.wait(1000)
        pygame.quit()