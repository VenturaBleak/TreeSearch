# game_ui.py
from tkinter import Frame, Label, CENTER, Tk
import game_constants as c

class GameUI(Frame):
    def __init__(self, master, game, visual=True):
        Frame.__init__(self, master)
        self.grid()
        self.master.title('2048')
        self.game = game
        self.visual = visual

        self.grid_cells = []
        if self.visual:
            self.init_grid()
            self.update_grid_cells()

    def init_grid(self):
        print(f"Initializing grid with game size: {self.game.size}")
        print(f"Game grid shape (should be {self.game.size}x{self.game.size}): {self.game.grid.shape}")
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        # Use self.game.size to determine the grid size
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

        print(f"grid_cells row count (should be {self.game.size}): {len(self.grid_cells)}")
        print(
            f"grid_cells column count per row (should all be {self.game.size}): {[len(row) for row in self.grid_cells]}")

    def update_grid_cells(self):
        if not self.visual:
            return

        for i in range(self.game.size):  # Assuming game.size is the length of one dimension of the square grid
            for j in range(self.game.size):
                new_number = self.game.grid[i, j]  # Accessing NumPy array element

                # The rest of the logic remains the same
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT.get(new_number, c.BACKGROUND_COLOR_CELL_EMPTY),
                        fg=c.CELL_COLOR_DICT.get(new_number, getattr(c, 'CELL_TEXT_COLOR', "#000000"))
                    )
        self.update_idletasks()

    # Rename start to init_ui and remove the call to mainloop()
    def init_ui(self):
        self.init_grid()
        self.update_grid_cells()
        # Do not call mainloop here as it is a blocking call.

