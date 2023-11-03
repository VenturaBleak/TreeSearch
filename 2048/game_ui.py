# game_ui.py
from tkinter import Frame, Label, CENTER, Tk
import constants as c
import random

# import custom modules
from game_state import GameState
from game_logic import Game

class GameUI(Frame):
    def __init__(self, master, game_state, visual=True):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.game_state = game_state
        self.visual = visual

        self.commands = {
            c.KEY_UP: self.game_state.game.move_up,
            c.KEY_DOWN: self.game_state.game.move_down,
            c.KEY_LEFT: self.game_state.game.move_left,
            c.KEY_RIGHT: self.game_state.game.move_right
        }

        self.grid_cells = []
        if self.visual:
            self.init_grid()
            self.update_grid_cells()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
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
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.game_state.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.make_move(self.commands[key])

    def random_move(self):
        if not self.game_state.terminated:
            move = random.choice(list(self.commands.values()))
            print(f"Making random move: {move}")
            self.make_move(move)
            self.after(100, self.random_move)

    def make_move(self, move):
        matrix, terminated = self.game_state.update_state(move)
        self.update_grid_cells()
        if terminated:
            # Update the termination message handling based on new return value of update_state
            message = terminated  # This will be 'You win!' or 'You lose!'
            print(f"Game Over: {message} Score: {self.game_state.score}")

    def run(self):
        if self.visual:
            self.random_move()
            self.mainloop()