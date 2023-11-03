# game_ui.py
from tkinter import Frame, Label, CENTER, Tk
import game_constants as c
import random

from game_logic import Game

class GameUI(Frame):
    def __init__(self, master, game, visual=True):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.game = game
        self.visual = visual

        self.commands = {
            c.KEY_UP: 'up',
            c.KEY_DOWN: 'down',
            c.KEY_LEFT: 'left',
            c.KEY_RIGHT: 'right'
        }

        self.grid_cells = []
        if self.visual:
            self.init_grid()
            self.update_grid_cells()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(self.game.size):
            grid_row = []
            for j in range(self.game.size):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / self.game.size,
                    height=c.SIZE / self.game.size
                )
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)
                t = Label(master=cell, text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        if not self.visual:
            return
        for i in range(self.game.size):
            for j in range(self.game.size):
                new_number = self.game.grid[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT.get(new_number, c.BACKGROUND_COLOR_CELL_EMPTY),
                        # Provide a default color if CELL_TEXT_COLOR is not defined
                        fg=c.CELL_COLOR_DICT.get(new_number, getattr(c, 'CELL_TEXT_COLOR', "#000000"))
                    )
        self.update_idletasks()
    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.make_move(self.commands[key])

    def random_move(self):
        if not self.game.terminated:
            move = random.choice(list(self.commands.values()))
            self.make_move(move)
            # Set the delay for the next move to 100ms (0.1 seconds)
            self.after(100, self.random_move)
        else:
            message = 'You win!' if self.game.win_tile in self.game.grid else 'You lose!'
            print(f"Game Over: {message} Score: {self.game.score}")

    def run(self):
        if self.visual:
            self.update_grid_cells()  # Initial update to show the starting grid
            # Start the automatic random moves after the mainloop starts
            self.after(100, self.random_move)
            self.mainloop()

    def make_move(self, direction):
        truncated, terminated = self.game.play(direction)
        self.update_grid_cells()
        if terminated:
            message = 'You win!' if self.game.win_tile in self.game.grid else 'You lose!'
            print(f"Game Over: {message} Score: {self.game.score}")

# When initializing the game UI, simply pass the game instance
root = Tk()
game = Game()
game_app = GameUI(root, game)  # Pass the game instance directly
game_app.run()